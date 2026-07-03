from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def create_page(receiver, sender, title, message, image_url, music_url=None, theme="default"):
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
    return response.data[0]["id"]


def get_page(page_id):
    response = (
        supabase.table("pages")
        .select("*")
        .eq("id", page_id)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]
