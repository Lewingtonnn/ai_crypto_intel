import uvicorn
from app.config_loader import load_config

# We load the config to get host and port
# This ensures our launcher is also configurable
cfg = load_config()
API_HOST = cfg.api["host"]
API_PORT = cfg.api["port"]

if __name__ == "__main__":
    print(f"🚀 Starting API server on http://{API_HOST}:{API_PORT}...")

    # This command tells uvicorn where to find the FastAPI 'app' object.
    # 'app.api.main:app' means "in the 'app/api/main.py' file, find the variable named 'app'".
    # 'reload=True' is for development. It automatically restarts the server
    # when you save a file. Do not use in production.
    uvicorn.run(
        "app.api.main:app",
        host=API_HOST,
        port=API_PORT,
        reload=True
    )