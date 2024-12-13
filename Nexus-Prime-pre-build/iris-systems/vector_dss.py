import uvicorn
from fastapi import FastAPI, HTTPException
from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/init")
async def initialize_vector_space(collection_name: str = "iris_dream_states", dimension: int = 256):
    try:
        connections.connect("default", host="milvus-standalone", port="19530")
        
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=dimension),
            FieldSchema(name="metadata", dtype=DataType.JSON)
        ]
        
        schema = CollectionSchema(fields=fields, description="Dream State Synthesis Vector Space")
        collection = Collection(name=collection_name, schema=schema)
        
        index_params = {
            "metric_type": "L2",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 1024}
        }
        collection.create_index(field_name="vector", index_params=index_params)
        collection.load()
        
        return {"status": "success", "message": f"Initialized {collection_name} with dimension {dimension}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)