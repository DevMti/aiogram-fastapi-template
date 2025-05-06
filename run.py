import uvicorn
from config import WEB_SERVER_HOST, WEB_SERVER_PORT, WORKERS_COUNT

if __name__ == "__main__":
    uvicorn.run(
        "bot.main:app",
        host=WEB_SERVER_HOST,
        port=WEB_SERVER_PORT,
        workers=WORKERS_COUNT
    )