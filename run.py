import uvicorn, logging, os
from config import WEB_SERVER_HOST, WEB_SERVER_PORT, WORKERS_COUNT

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    logging.basicConfig(level=logging.INFO, format='%(levelname)s:     %(message)s')
    logging.info(f"Starting server at {WEB_SERVER_HOST}:{WEB_SERVER_PORT} with {WORKERS_COUNT} workers")
    uvicorn.run(
        "bot.main:app",
        host=WEB_SERVER_HOST,
        port=WEB_SERVER_PORT,
        workers=WORKERS_COUNT
    )