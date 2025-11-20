import uvicorn
from app.config_loader import load_config
from ut1ls.logger import setup_logging
logger = setup_logging()
cfg = load_config()
API_HOST = cfg.api["host"]
API_PORT = cfg.api["port"]

if __name__ == "__main__":
    logger.info(f"🚀 Starting API server on http://{API_HOST}:{API_PORT}...")
    uvicorn.run(
        "app.api.main:app",
        host=API_HOST,
        port=API_PORT,
        reload=True
    )