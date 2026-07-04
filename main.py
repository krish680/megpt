from threading import Thread
from keep_alive import app
from bot import run_bot

if __name__ == "__main__":
    # Start small Flask health server in background
    Thread(target=lambda: app.run(host="0.0.0.0", port=10000, debug=False, use_reloader=False)).start()

    # Start telegram bot in main thread
    run_bot()