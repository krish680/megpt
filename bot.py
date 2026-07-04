from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
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

# ---------------- STATES ----------------
(
    RECEIVER,
    THEME,
    PHOTO,
    TITLE,
    MESSAGE,
    MUSIC,
    SENDER,
) = range(7)


# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name or "there"

    text = f"""
🌟 Welcome, {user}!

I'm QR Vault 💌

I can create a beautiful memory page containing:
📸 Photos
🎵 Music
💌 Messages
🎨 Themes
🔗 Shareable Link
📱 QR Code

Who is this memory for?
"""

    await update.message.reply_text(
        text.strip(),
        reply_markup=ReplyKeyboardRemove()
    )
    return RECEIVER


# ---------------- RECEIVER ----------------
async def receiver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["receiver"] = update.message.text.strip()

    keyboard = [
        ["❤️ Love", "🎂 Birthday"],
        ["🌌 Anime", "🌸 Cute"],
        ["✨ Elegant", "🖤 Memory"],
    ]

    await update.message.reply_text(
        "Choose a theme:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
    )
    return THEME


# ---------------- THEME ----------------
async def theme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["theme"] = update.message.text.strip()

    await update.message.reply_text(
        "Now send me a photo 📸",
        reply_markup=ReplyKeyboardRemove(),
    )
    return PHOTO


# ---------------- PHOTO ----------------
async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        await update.message.reply_text("Please send a valid photo.")
        return PHOTO

    photo = update.message.photo[-1]
    file = await photo.get_file()

    image_bytes = await file.download_as_bytearray()
    context.user_data["image_bytes"] = bytes(image_bytes)

    await update.message.reply_text("Nice 👍\nNow send a title for this memory:")
    return TITLE


# ---------------- TITLE ----------------
async def title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["title"] = update.message.text.strip()
    await update.message.reply_text("Write a message 💌")
    return MESSAGE


# ---------------- MESSAGE ----------------
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["message"] = update.message.text.strip()
    await update.message.reply_text("Optional: send music link 🎵 or type 'skip'")
    return MUSIC


# ---------------- MUSIC ----------------
async def music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text.lower() != "skip":
        context.user_data["music"] = text
    else:
        context.user_data["music"] = None

    await update.message.reply_text("Finally, send sender name 👤")
    return SENDER


# ---------------- SENDER ----------------
async def sender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["sender"] = update.message.text.strip()

    try:
        page_id = create_page(
            receiver=context.user_data["receiver"],
            sender=context.user_data["sender"],
            title=context.user_data["title"],
            message=context.user_data["message"],
            image_bytes=context.user_data.get("image_bytes"),
            music_url=context.user_data.get("music"),
            theme=context.user_data.get("theme", "default"),
        )

        link = f"{BASE_URL}/page/{page_id}"

        await update.message.reply_text(
            f"✅ Memory created successfully!\n\n🔗 Your page:\n{link}",
            reply_markup=ReplyKeyboardRemove(),
        )

    except Exception as e:
        print("BOT ERROR:", e)
        await update.message.reply_text(f"❌ Error while creating page:\n{e}")

    return ConversationHandler.END


# ---------------- CANCEL ----------------
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


# ---------------- RUN BOT ----------------
def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            RECEIVER: [MessageHandler(filters.TEXT & ~filters.COMMAND, receiver)],
            THEME: [MessageHandler(filters.TEXT & ~filters.COMMAND, theme)],
            PHOTO: [MessageHandler(filters.PHOTO, photo_handler)],
            TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, title)],
            MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, message)],
            MUSIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, music)],
            SENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, sender)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv)

    print("Bot is running...")
    application.run_polling(stop_signals=None)