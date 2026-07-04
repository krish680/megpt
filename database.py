import uuid
import io
import json
import qrcode
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY, BASE_URL

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ---------------- Upload Image ----------------
def upload_image(file_bytes, filename="photo.jpg"):
    file_name = f"{uuid.uuid4()}_{filename}"

    supabase.storage.from_("uploads").upload(
        file_name,
        file_bytes,
        {"content-type": "image/jpeg"}
    )

    return supabase.storage.from_("uploads").get_public_url(file_name)


# ---------------- Generate QR ----------------
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


# ---------------- Create Page ----------------
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


# ---------------- Get Page ----------------
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
        err_text = str(e)

        if "JSON could not be generated" in err_text and "details" in err_text:
            try:
                start = err_text.find("b'{")
                end = err_text.rfind("}'")

                if start != -1 and end != -1:
                    raw = err_text[start + 2:end + 2]
                    raw_bytes = raw.encode("latin1")
                    decoded = raw_bytes.decode("unicode_escape")
                    return json.loads(decoded)
            except Exception as inner_e:
                print("FALLBACK PARSE ERROR:", inner_e)

        raise e