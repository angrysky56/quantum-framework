from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
import numpy as np

# Connect to Milvus
def setup_milvus_connection():
    connections.connect(
        alias="default",
        host="milvus-standalone",
        port="19530"
    )

# Create IRIS Collections based on the vector_native_001 pattern
def create_iris_collections():
    # Common dimension from vector_native_001 pattern
    dim = 512
    
    # Collection definitions for each IRIS component
    collections = {
        "iris_qpre": {
            "fields": [
                FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=100),
                FieldSchema(name="pattern_vector", dtype=DataType.FLOAT_VECTOR, dim=dim),
                FieldSchema(name="quantum_state", dtype=DataType.JSON),
                FieldSchema(name="coherence_level", dtype=DataType.FLOAT)
            ]
        },
        "iris_dss": {
            "fields": [
                FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=100),
                FieldSchema(name="dream_vector", dtype=DataType.FLOAT_VECTOR, dim=dim),
                FieldSchema(name="consciousness_state", dtype=DataType.JSON),
                FieldSchema(name="coherence_level", dtype=DataType.FLOAT)
            ]
        },
        "iris_tcw": {
            "fields": [
                FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=100),
                FieldSchema(name="temporal_vector", dtype=DataType.FLOAT_VECTOR, dim=dim),
                FieldSchema(name="temporal_state", dtype=DataType.JSON),
                FieldSchema(name="coherence_level", dtype=DataType.FLOAT)
            ]
        }
    }

    # Create collections with optimized index
    for name, schema_def in collections.items():
        if utility.exists_collection(name):
            utility.drop_collection(name)
            
        schema = CollectionSchema(fields=schema_def["fields"], description=f"IRIS {name} vectors")
        collection = Collection(name=name, schema=schema)
        
        # Create HNSW index based on vector_native_001 pattern
        index_params = {
            "metric_type": "L2",
            "index_type": "HNSW",
            "params": {
                "M": 16,
                "efConstruction": 200
            }
        }
        
        vec_field = "pattern_vector" if "pattern_vector" in schema_def["fields"] else \
                   "dream_vector" if "dream_vector" in schema_def["fields"] else \
                   "temporal_vector"
        
        collection.create_index(
            field_name=vec_field,
            index_params=index_params
        )
        
        # Load collection for searching
        collection.load()

# Set up monitoring based on optimization algorithms
def setup_monitoring():
    # Initialize monitoring tables for each optimization algorithm
    monitoring_configs = {
        "batch_optimization": {
            "algorithm_id": "OPT-BATCH-001",
            "initial_size": 64,
            "min_size": 16,
            "max_size": 1024
        },
        "anomaly_detection": {
            "algorithm_id": "OPT-ANOM-001",
            "num_clusters": 10,
            "distance_threshold": 2.5,
            "sample_size": 1000
        },
        "coherence_control": {
            "algorithm_id": "OPT-SPC-001",
            "window_size": 100,
            "sigma_levels": 3,
            "threshold": 0.95
        }
    }
    
    return monitoring_configs

if __name__ == "__main__":
    # Set up Milvus connection
    setup_milvus_connection()
    
    # Create IRIS collections
    create_iris_collections()
    
    # Initialize monitoring
    monitoring_configs = setup_monitoring()
    
    print("IRIS vector integration setup complete")