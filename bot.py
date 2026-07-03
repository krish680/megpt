import asyncio
import os
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import BOT_TOKEN, BASE_URL
from database import create_page

# -------- Conversation States --------
(
    RECEIVER,
    THEME,
    PHOTO,
    TITLE,
    MESSAGE,
    MUSIC,
    SENDER,
) = range(7)


# -------- Start --------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name

    text = f"""
?? Welcome, {user}!

I'm QR Vault ??

I can create a beautiful memory page containing:

?? Photo
?? Music
?? Personalized Message
?? Theme
?? Shareable Link

Let's begin.

Who is going to receive this memory?
(Type their name)
"""

    await update.message.reply_text(
        text,
        reply_markup=ReplyKeyboardRemove(),
    )
    return RECEIVER


# -------- Receiver --------
async def receiver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["receiver"] = update.message.text.strip()

    keyboard = [
        ["?? Love", "?? Birthday"],
        ["?? Anime", "?? Cute"],
        ["??? Memory", "? Elegant"],
    ]

    await update.message.reply_text(
        "Choose a theme:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )
    return THEME


# -------- Theme --------
async def theme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["theme"] = update.message.text.strip()
    receiver_name = context.user_data["receiver"]

    await update.message.reply_text(
        f"Great! ??\n\nNow send me the photo you'd like {receiver_name} to see.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return PHOTO


# -------- Photo --------
async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        await update.message.reply_text("Please send a photo, not text.")
        return PHOTO

    photo_file = await update.message.photo[-1].get_file()

    os.makedirs("static/uploads", exist_ok=True)
    filename = f"{update.effective_user.id}_{update.message.photo[-1].file_unique_id}.jpg"
    filepath = os.path.join("static", "uploads", filename)

    await photo_file.download_to_drive(filepath)

    context.user_data["image_url"] = f"/static/uploads/{filename}"

    await update.message.reply_text("Nice ??\n\nNow send the page title.")
    return TITLE


# -------- Title --------
async def title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["title"] = update.message.text.strip()

    await update.message.reply_text("Now send the message you want on the page ??")
    return MESSAGE


# -------- Message --------
async def message_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["message"] = update.message.text.strip()

    await update.message.reply_text(
        "Now send a music link for the page ??\n\nOr type: skip"
    )
    return MUSIC


# -------- Music --------
async def music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text.lower() == "skip":
        context.user_data["music"] = None
    else:
        context.user_data["music"] = text

    await update.message.reply_text("Finally, send your name (the sender name).")
    return SENDER


# -------- Sender --------
async def sender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["sender"] = update.message.text.strip()

    receiver_name = context.user_data["receiver"]
    sender_name = context.user_data["sender"]
    title_text = context.user_data["title"]
    message_body = context.user_data["message"]
    image_url = context.user_data["image_url"]
    music_url = context.user_data.get("music")
    theme_name = context.user_data["theme"]

    try:
        page_id = create_page(
            receiver=receiver_name,
            sender=sender_name,
            title=title_text,
            message=message_body,
            image_url=image_url,
            music_url=music_url,
            theme=theme_name,
        )

        base = (BASE_URL or "http://127.0.0.1:10000").rstrip("/")
        page_link = f"{base}/page/{page_id}"

        await update.message.reply_text(
            "?? Your QR Vault page is ready!\n\n"
            f"?? {page_link}\n\n"
            "Open the link in your browser to view it."
        )

    except Exception as e:
        print("CREATE PAGE ERROR:", e)
        await update.message.reply_text(
            "Something went wrong while creating the page. Please try again."
        )

    context.user_data.clear()
    return ConversationHandler.END


# -------- Cancel --------
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


application = Application.builder().token(BOT_TOKEN).build()

conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        RECEIVER: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, receiver)
        ],
        THEME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, theme)
        ],
        PHOTO: [
            MessageHandler(filters.PHOTO, photo),
            MessageHandler(filters.TEXT & ~filters.COMMAND, photo),
        ],
        TITLE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, title)
        ],
        MESSAGE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, message_text)
        ],
        MUSIC: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, music)
        ],
        SENDER: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, sender)
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

application.add_handler(conv)


def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    application.run_polling()
