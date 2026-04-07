from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>")
logger.add("logs/ai_system.log", rotation="500 MB", retention="10 days")

def get_logger(name):
    return logger.bind(name=name)