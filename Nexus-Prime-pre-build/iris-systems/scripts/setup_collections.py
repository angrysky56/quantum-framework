from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType
import time

def connect_to_milvus():
    try:
        connections.connect(
            alias="default",
            host="localhost",
            port="19530"
        )
        print("Successfully connected to Milvus")
    except Exception as e:
        print(f"Failed to connect to Milvus: {e}")
        raise

def create_quantum_pattern_collection():
    try:
        # Define fields for the collection
        fields = [
            FieldSchema(name="pattern_id", dtype=DataType.VARCHAR, is_primary=True, max_length=100),
            FieldSchema(name="pattern_vector", dtype=DataType.FLOAT_VECTOR, dim=512),
            FieldSchema(name="coherence_level", dtype=DataType.FLOAT),
            FieldSchema(name="evolution_state", dtype=DataType.VARCHAR, max_length=100),
            FieldSchema(name="creation_timestamp", dtype=DataType.INT64),
            FieldSchema(name="metadata", dtype=DataType.JSON)
        ]

        # Create collection schema
        schema = CollectionSchema(
            fields=fields,
            description="Quantum pattern storage with coherence tracking"
        )

        # Create collection
        collection = Collection(
            name="quantum_pattern_store",
            schema=schema,
            using='default',
            shards_num=2
        )

        # Create HNSW index
        index_params = {
            "metric_type": "L2",
            "index_type": "HNSW",
            "params": {
                "M": 16,
                "efConstruction": 200
            }
        }

        collection.create_index(
            field_name="pattern_vector",
            index_params=index_params
        )

        print("Successfully created quantum pattern collection with HNSW index")
        return collection
    except Exception as e:
        print(f"Failed to create collection: {e}")
        raise

def create_coherence_collection():
    try:
        fields = [
            FieldSchema(name="coherence_id", dtype=DataType.VARCHAR, is_primary=True, max_length=100),
            FieldSchema(name="pattern_ids", dtype=DataType.ARRAY, element_type=DataType.VARCHAR),
            FieldSchema(name="group_coherence", dtype=DataType.FLOAT),
            FieldSchema(name="last_update", dtype=DataType.INT64)
        ]

        schema = CollectionSchema(
            fields=fields,
            description="Pattern coherence group tracking"
        )

        collection = Collection(
            name="pattern_coherence",
            schema=schema,
            using='default'
        )

        print("Successfully created coherence tracking collection")
        return collection
    except Exception as e:
        print(f"Failed to create coherence collection: {e}")
        raise

def create_evolution_collection():
    try:
        fields = [
            FieldSchema(name="evolution_id", dtype=DataType.VARCHAR, is_primary=True, max_length=100),
            FieldSchema(name="pattern_id", dtype=DataType.VARCHAR, max_length=100),
            FieldSchema(name="state_vector", dtype=DataType.FLOAT_VECTOR, dim=512),
            FieldSchema(name="transition_metadata", dtype=DataType.JSON),
            FieldSchema(name="timestamp", dtype=DataType.INT64)
        ]

        schema = CollectionSchema(
            fields=fields,
            description="Pattern evolution state tracking"
        )

        collection = Collection(
            name="pattern_evolution",
            schema=schema,
            using='default',
            shards_num=2
        )

        # Create HNSW index for state vectors
        index_params = {
            "metric_type": "L2",
            "index_type": "HNSW",
            "params": {
                "M": 16,
                "efConstruction": 200
            }
        }

        collection.create_index(
            field_name="state_vector",
            index_params=index_params
        )

        print("Successfully created evolution tracking collection with HNSW index")
        return collection
    except Exception as e:
        print(f"Failed to create evolution collection: {e}")
        raise

def main():
    try:
        # Connect to Milvus
        connect_to_milvus()

        # Create collections
        pattern_collection = create_quantum_pattern_collection()
        coherence_collection = create_coherence_collection()
        evolution_collection = create_evolution_collection()

        # Load collections into memory
        pattern_collection.load()
        coherence_collection.load()
        evolution_collection.load()

        print("\nAll collections created and loaded successfully!")
        
    except Exception as e:
        print(f"Setup failed: {e}")
    finally:
        connections.disconnect("default")

if __name__ == "__main__":
    main()