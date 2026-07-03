<<<<<<< HEAD
import threading
from config import PORT
from web import app
from bot import run_bot


def start_web():
    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=False,
        use_reloader=False,
    )


if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()

=======
import threading
from config import PORT
from web import app
from bot import run_bot


def start_web():
    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=False,
        use_reloader=False,
    )


if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()

>>>>>>> e25fd19efe1b9ce37d47aa9f9c0c7ef17e8eb413
    start_web()