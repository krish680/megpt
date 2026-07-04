from threading import Thread
import asyncio

from keep_alive import app
from bot import run_bot
from config import PORT

if __name__ == "__main__":
    # Start tiny Flask health server in background
    Thread(
        target=lambda: app.run(
            host="0.0.0.0",
            port=PORT,
            debug=False,
            use_reloader=False
        ),
        daemon=True
    ).start()

    # Create event loop explicitly for Python 3.14 / Render
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Start telegram bot in main thread
    run_bot()