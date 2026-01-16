import logging
import sys

LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(module)s:%(lineno)d] - %(message)s"

def setup_logging() :
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    file_handler = logging.FileHandler("logs/app.log", mode="a", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    logging.basicConfig(
        level=logging.INFO,
        handlers=[console_handler, file_handler]
    )
    
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    
    logger = logging.getLogger("wikismart")
    
    return logger

logger = setup_logging()