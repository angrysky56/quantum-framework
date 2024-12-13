import os
import time
import logging
from pymilvus import connections, Collection, utility

# Configure logging for better visibility of system operations
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("QPRE_System")

def initialize_milvus_connection():
    """Establish connection to Milvus with retry logic"""
    max_retries = 5
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            connections.connect(
                alias="default",
                host=os.getenv('MILVUS_HOST', 'milvus-standalone'),
                port=os.getenv('MILVUS_PORT', 19530)
            )
            logger.info("Successfully connected to Milvus")
            return True
        except Exception as e:
            logger.warning(f"Connection attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                logger.error("Failed to connect to Milvus after all retries")
                return False

def verify_system_health():
    """Check system health and verify Milvus connection"""
    try:
        # Check if Milvus is healthy
        if utility.get_server_version():
            logger.info(f"Milvus server version: {utility.get_server_version()}")
            return True
        return False
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return False

def main():
    logger.info("Starting QPRE System...")
    
    if not initialize_milvus_connection():
        logger.error("Failed to initialize Milvus connection")
        return

    # Main system loop
    while True:
        if verify_system_health():
            logger.info("System healthy, standing by for vector operations")
        else:
            logger.warning("System health check failed, attempting recovery")
            initialize_milvus_connection()
        
        # Health check interval
        time.sleep(30)

if __name__ == "__main__":
    main()