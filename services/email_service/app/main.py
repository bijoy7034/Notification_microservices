from app.consumers.email_consumers import start_consumer
from app.core.logging import logger

if __name__ == "__main__":
    logger.info("Starting Email Service...")
    start_consumer()
