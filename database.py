import uuid
import io
import json
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
    Handles errors like:

    Error 200:
    Message: JSON could not be generated
    Hint: Refer to full message for details
    Details: b'{"id":6,"receiver":"..."}'
    """
    try:
        err_str = str(err)

        # Case 1: "Details: b'...json...'"
        if "Details: b'" in err_str:
            start = err_str.find("Details: b'")
            if start != -1:
                start += len("Details: b'")
                end = err_str.find("'", start)
                if end != -1:
                    raw = err_str[start:end]
                    raw = raw.encode("latin1").decode("unicode_escape")
                    return json.loads(raw)

        # Case 2: dict-style string with 'details': 'b\'...\''
        if "'details':" in err_str:
            start = err_str.find("b'{")
            end = err_str.rfind("}'")
            if start != -1 and end != -1:
                raw = err_str[start + 2:end + 2]   # strip leading b'
                raw = raw.encode("latin1").decode("unicode_escape")
                return json.loads(raw)

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
        print("GET_PAGE RAW ERROR:", e)

        fallback_data = parse_supabase_json_error(e)
        if fallback_data:
            return fallback_data

        raise