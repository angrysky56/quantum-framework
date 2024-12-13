import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType
import signal
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def signal_handler(sig, frame):
    logger.info("Shutting down gracefully...")
    try:
        connections.disconnect("default")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting TCW service...")
    try:
        # Connect to Milvus
        connections.connect("default", host="milvus-standalone", port="19530")
        logger.info("Connected to Milvus successfully")
    except Exception as e:
        logger.error(f"Failed to connect to Milvus: {e}")
        raise

@app.get("/health")
def health_check():
    try:
        if connections.has_connection("default"):
            return {"status": "healthy", "milvus_connection": "active"}
        return {"status": "unhealthy", "milvus_connection": "inactive"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/init")
async def initialize_vector_space(collection_name: str = "iris_temporal_coherence", dimension: int = 128):
    try:
        logger.info(f"Initializing collection {collection_name} with dimension {dimension}")
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=dimension),
            FieldSchema(name="metadata", dtype=DataType.JSON)
        ]
        
        schema = CollectionSchema(
            fields=fields,
            description="Temporal Coherence Weaving Vector Space"
        )

        # Create collection
        collection = Collection(name=collection_name, schema=schema)
        
        # Create IVF_SQ8 index for efficient temporal matching
        index_params = {
            "metric_type": "L2",
            "index_type": "IVF_SQ8",
            "params": {"nlist": 1024}
        }
        collection.create_index(field_name="vector", index_params=index_params)
        collection.load()
        
        logger.info(f"Successfully initialized collection {collection_name}")
        return {
            "status": "success",
            "message": f"Initialized {collection_name} with dimension {dimension}",
            "index_type": "IVF_SQ8"
        }
    except Exception as e:
        logger.error(f"Failed to initialize vector space: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")