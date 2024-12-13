import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType
import signal
import sys
import logging
import os
import time
import backoff

# Configure detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] QPRE: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Environment variables with defaults
MILVUS_HOST = os.getenv('MILVUS_HOST', 'milvus-standalone')
MILVUS_PORT = os.getenv('MILVUS_PORT', '19530')

app = FastAPI()
logger.info(f"Initializing QPRE service - Milvus host: {MILVUS_HOST}, port: {MILVUS_PORT}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def signal_handler(sig, frame):
    logger.info("Received shutdown signal - cleaning up connections")
    try:
        connections.disconnect("default")
        logger.info("Gracefully disconnected from Milvus")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def connect_with_retry():
    """Attempt to connect to Milvus with exponential backoff"""
    retry_count = 0
    max_retries = 10
    initial_delay = 1  # seconds
    max_delay = 30     # seconds

    while retry_count < max_retries:
        try:
            logger.info(f"Attempting to connect to Milvus ({retry_count + 1}/{max_retries})")
            connections.connect("default", host=MILVUS_HOST, port=MILVUS_PORT)
            logger.info("Successfully connected to Milvus")
            return True
        except Exception as e:
            retry_count += 1
            if retry_count == max_retries:
                logger.error(f"Failed to connect after {max_retries} attempts")
                return False
            
            delay = min(initial_delay * (2 ** retry_count), max_delay)
            logger.warning(f"Failed to connect: {str(e)}. Retrying in {delay} seconds...")
            time.sleep(delay)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting QPRE vector service initialization")
    while not connect_with_retry():
        logger.warning("Initial connection attempt failed, waiting 30 seconds before trying again")
        time.sleep(30)

@app.get("/health")
def health_check():
    try:
        is_connected = connections.has_connection("default")
        if not is_connected:
            is_connected = connect_with_retry()
        
        logger.info(f"Health check - Milvus connection status: {is_connected}")
        if is_connected:
            return {"status": "healthy", "milvus_connection": "active"}
        return {"status": "unhealthy", "milvus_connection": "inactive"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/init")
async def initialize_vector_space(collection_name: str = "iris_quantum_patterns", dimension: int = 512):
    logger.info(f"Starting vector space initialization - collection: {collection_name}, dimension: {dimension}")
    start_time = time.time()
    
    # Ensure connection is active
    if not connections.has_connection("default"):
        if not connect_with_retry():
            raise HTTPException(status_code=503, detail="Could not establish Milvus connection")

    try:
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=dimension),
            FieldSchema(name="metadata", dtype=DataType.JSON)
        ]
        
        schema = CollectionSchema(
            fields=fields,
            description="QPRE Vector Space"
        )

        logger.info("Creating collection with schema")
        collection = Collection(name=collection_name, schema=schema)
        
        logger.info("Creating HNSW index")
        index_params = {
            "metric_type": "L2",
            "index_type": "HNSW",
            "params": {
                "M": 48,
                "efConstruction": 500
            }
        }
        collection.create_index(field_name="vector", index_params=index_params)
        
        logger.info("Loading collection into memory")
        collection.load()
        
        elapsed_time = time.time() - start_time
        logger.info(f"Vector space initialization completed in {elapsed_time:.2f} seconds")
        
        return {
            "status": "success",
            "message": f"Initialized {collection_name} with dimension {dimension}",
            "index_type": "HNSW",
            "initialization_time": f"{elapsed_time:.2f}s"
        }
    except Exception as e:
        logger.error(f"Vector space initialization failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logger.info("QPRE service starting up")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")