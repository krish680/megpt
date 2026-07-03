<<<<<<< HEAD
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

from config import BOT_TOKEN

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
🌟 Welcome, {user}!

I'm QR Vault ❤️

I can create a beautiful memory page containing

📷 Photos
🎵 Music
💌 Personalized Messages
🎨 Themes
🔗 QR Code

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

    context.user_data["receiver"] = update.message.text

    keyboard = [
        ["❤️ Love", "🎂 Birthday"],
        ["🌌 Anime", "🌸 Cute"],
        ["🕊️ Memory", "✨ Elegant"],
    ]

    await update.message.reply_text(
        "Choose a theme:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
        ),
    )

    return THEME


# -------- Theme --------

async def theme(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["theme"] = update.message.text

    receiver = context.user_data["receiver"]

    await update.message.reply_text(
        f"Great! 🎉\n\nNow send me the photo you'd like {receiver} to see.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return PHOTO


# -------- Cancel --------

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END
application = Application.builder().token(BOT_TOKEN).build()

conv = ConversationHandler(

    entry_points=[
        CommandHandler("start", start)
    ],

    states={

        RECEIVER: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, receiver)
        ],

        THEME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, theme)
        ],

    },

    fallbacks=[
        CommandHandler("cancel", cancel)
    ],

)

application.add_handler(conv)
def run_bot():
=======
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

from config import BOT_TOKEN

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
🌟 Welcome, {user}!

I'm QR Vault ❤️

I can create a beautiful memory page containing

📷 Photos
🎵 Music
💌 Personalized Messages
🎨 Themes
🔗 QR Code

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

    context.user_data["receiver"] = update.message.text

    keyboard = [
        ["❤️ Love", "🎂 Birthday"],
        ["🌌 Anime", "🌸 Cute"],
        ["🕊️ Memory", "✨ Elegant"],
    ]

    await update.message.reply_text(
        "Choose a theme:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
        ),
    )

    return THEME


# -------- Theme --------

async def theme(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["theme"] = update.message.text

    receiver = context.user_data["receiver"]

    await update.message.reply_text(
        f"Great! 🎉\n\nNow send me the photo you'd like {receiver} to see.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return PHOTO


# -------- Cancel --------

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END
application = Application.builder().token(BOT_TOKEN).build()

conv = ConversationHandler(

    entry_points=[
        CommandHandler("start", start)
    ],

    states={

        RECEIVER: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, receiver)
        ],

        THEME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, theme)
        ],

    },

    fallbacks=[
        CommandHandler("cancel", cancel)
    ],

)

application.add_handler(conv)
def run_bot():
>>>>>>> e25fd19efe1b9ce37d47aa9f9c0c7ef17e8eb413
    application.run_polling()