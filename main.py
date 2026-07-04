from threading import Thread
import asyncio

from keep_alive import app
from bot import run_bot
from config import PORT

if __name__ == "__main__":
    # tiny health server for Render/UptimeRobot
    Thread(
        target=lambda: app.run(
            host="0.0.0.0",
            port=PORT,
            debug=False,
            use_reloader=False
        ),
        daemon=True
    ).start()

    # Python 3.14 fix: create event loop manually
    asyncio.set_event_loop(asyncio.new_event_loop())

    # start telegram bot
    run_bot()