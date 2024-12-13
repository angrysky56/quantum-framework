import os
import sys
import time
import logging
from pymilvus import connections, utility

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("TCW_System")

def initialize_milvus():
    """Initialize connection to Milvus with detailed error reporting"""
    host = os.getenv('MILVUS_HOST', 'milvus-standalone')
    port = int(os.getenv('MILVUS_PORT', 19530))
    
    logger.info(f"Attempting to connect to Milvus at {host}:{port}")
    
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            connections.connect(
                alias="default",
                host=host,
                port=port,
                timeout=10  # 10 second timeout
            )
            logger.info("Successfully connected to Milvus")
            return True
        except Exception as e:
            logger.error(f"Connection attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                logger.error("Failed to connect after all retries")
                return False

def main():
    """Main function with enhanced error handling"""
    try:
        logger.info("Starting Temporal Coherence Weaver (TCW)...")
        logger.info(f"Environment variables: MILVUS_HOST={os.getenv('MILVUS_HOST')}, MILVUS_PORT={os.getenv('MILVUS_PORT')}")
        
        if not initialize_milvus():
            logger.error("Failed to initialize Milvus connection")
            sys.exit(1)
            
        # Keep the container running
        logger.info("TCW system initialized, entering main loop")
        while True:
            try:
                # Verify Milvus connection is still alive
                version = utility.get_server_version()
                logger.info(f"System healthy - Milvus version: {version}")
            except Exception as e:
                logger.error(f"Health check failed: {str(e)}")
                if not initialize_milvus():
                    logger.error("Failed to re-establish connection")
                    sys.exit(1)
            
            time.sleep(30)
    except Exception as e:
        logger.error(f"Critical error in main loop: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()