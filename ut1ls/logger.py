import logging
import os

def setup_logging():
    """Sets up the basic configuration for structured logging."""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Configure the root logger
    logging.basicConfig(
        level=os.environ.get("LOG_LEVEL", "INFO").upper(),
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Return a logger instance that modules can use
    return logging.getLogger("CryptoRAG")

# Initialize logger for use in other modules
logger = setup_logging()

if __name__ == "__main__":
    logger.info("Logger setup complete. Testing levels...")
    logger.warning("This is a warning during initialization.")
    logger.error("A critical error happened!")