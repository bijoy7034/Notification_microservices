import logging
from app.consumers.push_consumers import start_consumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting Push Notification Service...")
    start_consumer()
