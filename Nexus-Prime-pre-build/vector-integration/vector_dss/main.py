import os
import time
import logging
from pymilvus import connections, Collection, utility

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DSS_System")

def initialize_storage_system():
    """Initialize the Dynamic Storage System with connection handling"""
    try:
        connections.connect(
            alias="default",
            host=os.getenv('MILVUS_HOST', 'milvus-standalone'),
            port=os.getenv('MILVUS_PORT', 19530)
        )
        logger.info("DSS: Storage system initialized successfully")
        return True
    except Exception as e:
        logger.error(f"DSS: Failed to initialize storage system: {str(e)}")
        return False

def monitor_storage_health():
    """Monitor storage system health and performance"""
    try:
        # Check Milvus connection and get metrics
        version = utility.get_server_version()
        logger.info(f"Storage system healthy - Milvus version: {version}")
        return True
    except Exception as e:
        logger.error(f"Storage system health check failed: {str(e)}")
        return False

def main():
    logger.info("Starting Dynamic Storage System (DSS)...")
    
    while True:
        if not initialize_storage_system():
            logger.error("Failed to initialize storage system, retrying in 10 seconds...")
            time.sleep(10)
            continue
            
        try:
            while True:
                if monitor_storage_health():
                    # System is healthy, perform regular operations
                    time.sleep(30)
                else:
                    # Attempt recovery
                    logger.warning("Storage system needs recovery, reinitializing...")
                    break
                    
        except Exception as e:
            logger.error(f"Unexpected error in storage system: {str(e)}")
            time.sleep(5)

if __name__ == "__main__":
    main()