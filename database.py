import uuid
import io
import json
import ast
import qrcode
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY, BASE_URL

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# =========================
# Upload image to Supabase Storage
# =========================
def upload_image(file_bytes, filename="photo.jpg"):
    file_name = f"{uuid.uuid4()}_{filename}"

    supabase.storage.from_("uploads").upload(
        file_name,
        file_bytes,
        {"content-type": "image/jpeg"}
    )

    return supabase.storage.from_("uploads").get_public_url(file_name)


# =========================
# Generate QR and upload
# =========================
def generate_qr(url):
    qr = qrcode.make(url)

    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    file_name = f"{uuid.uuid4()}_qr.png"

    supabase.storage.from_("uploads").upload(
        file_name,
        buffer.getvalue(),
        {"content-type": "image/png"}
    )

    return supabase.storage.from_("uploads").get_public_url(file_name)


# =========================
# Create page
# =========================
def create_page(receiver, sender, title, message, image_bytes=None, music_url=None, theme="default"):
    image_url = None

    if image_bytes:
        image_url = upload_image(image_bytes, "photo.jpg")

    data = {
        "receiver": receiver,
        "sender": sender,
        "title": title,
        "message": message,
        "image": image_url,
        "music": music_url,
        "theme": theme,
    }

    response = supabase.table("pages").insert(data).execute()
    page_id = response.data[0]["id"]

    page_url = f"{BASE_URL}/page/{page_id}"
    qr_url = generate_qr(page_url)

    supabase.table("pages").update({"qr": qr_url}).eq("id", page_id).execute()

    return page_id


# =========================
# Parse weird Supabase JSON error
# =========================
def parse_supabase_json_error(err):
    """
    Supabase sometimes returns the actual row inside:
    error["details"] = 'b\'{"id":...}\''
    We extract and decode it safely.
    """
    try:
        err_str = str(err)

        # Find the details section
        if "'details':" not in err_str:
            return None

        start = err_str.find("'details': ")
        if start == -1:
            return None

        details_part = err_str[start + len("'details': "):]

        # ends before final }
        # example: 'b\'{"id":6,...}\''
        first_quote = details_part.find("'")
        last_quote = details_part.rfind("'")

        if first_quote == -1 or last_quote == -1 or last_quote <= first_quote:
            return None

        details_value = details_part[first_quote:last_quote + 1]

        # Convert the Python string literal to actual string
        parsed_literal = ast.literal_eval(details_value)

        # parsed_literal should now be something like:
        # b'{"id":6,"receiver":"..."}'
        if isinstance(parsed_literal, bytes):
            decoded = parsed_literal.decode("utf-8")
            return json.loads(decoded)

        if isinstance(parsed_literal, str):
            return json.loads(parsed_literal)

        return None

    except Exception as parse_error:
        print("PARSE_SUPABASE_JSON_ERROR FAILED:", repr(parse_error))
        return None


# =========================
# Get page
# =========================
def get_page(page_id):
    try:
        response = (
            supabase.table("pages")
            .select("*")
            .eq("id", page_id)
            .single()
            .execute()
        )
        return response.data

    except Exception as e:
        print("GET_PAGE RAW ERROR:", repr(e))

        fallback_data = parse_supabase_json_error(e)
        if fallback_data:
            return fallback_data

        raise