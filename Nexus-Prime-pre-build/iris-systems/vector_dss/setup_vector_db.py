from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
import time
import os

def wait_for_connection(max_retries=30, delay=5):
    milvus_host = os.getenv('MILVUS_HOST', 'milvus-standalone')
    milvus_port = os.getenv('MILVUS_PORT', '19530')
    
    print(f"Attempting to connect to Milvus at {milvus_host}:{milvus_port}")
    
    for i in range(max_retries):
        try:
            connections.connect(
                alias="default",
                host=milvus_host,
                port=milvus_port
            )
            print(f"Successfully connected to Milvus on attempt {i+1}")
            return True
        except Exception as e:
            print(f"Connection attempt {i+1} failed: {str(e)}")
            if i < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Max retries reached. Could not connect to Milvus.")
                return False

def create_collections():
    try:
        # List existing collections
        existing = utility.list_collections()
        print(f"Existing collections: {existing}")

        # Drop existing collections if they exist
        for collection_name in ['quantum_pattern_store', 'pattern_coherence', 'pattern_evolution']:
            if collection_name in existing:
                Collection(collection_name).drop()
                print(f"Dropped existing collection: {collection_name}")

        # Create quantum pattern collection
        pattern_fields = [
            FieldSchema(name="pattern_id", dtype=DataType.VARCHAR, is_primary=True, max_length=100),
            FieldSchema(name="pattern_vector", dtype=DataType.FLOAT_VECTOR, dim=512),
            FieldSchema(name="coherence_level", dtype=DataType.FLOAT),
            FieldSchema(name="evolution_state", dtype=DataType.VARCHAR, max_length=100),
            FieldSchema(name="creation_timestamp", dtype=DataType.INT64),
            FieldSchema(name="metadata", dtype=DataType.JSON)
        ]

        pattern_schema = CollectionSchema(
            fields=pattern_fields,
            description="Quantum pattern storage with coherence tracking"
        )

        pattern_collection = Collection(
            name="quantum_pattern_store",
            schema=pattern_schema,
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

        pattern_collection.create_index(
            field_name="pattern_vector",
            index_params=index_params
        )

        print("Successfully created quantum pattern collection with HNSW index")

        # Create coherence tracking collection
        coherence_fields = [
            FieldSchema(name="coherence_id", dtype=DataType.VARCHAR, is_primary=True, max_length=100),
            FieldSchema(name="pattern_ids", dtype=DataType.ARRAY, element_type=DataType.VARCHAR),
            FieldSchema(name="group_coherence", dtype=DataType.FLOAT),
            FieldSchema(name="last_update", dtype=DataType.INT64)
        ]

        coherence_schema = CollectionSchema(
            fields=coherence_fields,
            description="Pattern coherence group tracking"
        )

        coherence_collection = Collection(
            name="pattern_coherence",
            schema=coherence_schema,
            using='default'
        )

        print("Successfully created coherence tracking collection")

        # Create evolution tracking collection
        evolution_fields = [
            FieldSchema(name="evolution_id", dtype=DataType.VARCHAR, is_primary=True, max_length=100),
            FieldSchema(name="pattern_id", dtype=DataType.VARCHAR, max_length=100),
            FieldSchema(name="state_vector", dtype=DataType.FLOAT_VECTOR, dim=512),
            FieldSchema(name="transition_metadata", dtype=DataType.JSON),
            FieldSchema(name="timestamp", dtype=DataType.INT64)
        ]

        evolution_schema = CollectionSchema(
            fields=evolution_fields,
            description="Pattern evolution state tracking"
        )

        evolution_collection = Collection(
            name="pattern_evolution",
            schema=evolution_schema,
            using='default',
            shards_num=2
        )

        evolution_collection.create_index(
            field_name="state_vector",
            index_params=index_params
        )

        print("Successfully created evolution tracking collection with HNSW index")

        # Load collections
        pattern_collection.load()
        coherence_collection.load()
        evolution_collection.load()

        print("All collections loaded successfully")

    except Exception as e:
        print(f"Error creating collections: {str(e)}")
        raise

def main():
    print("Starting vector database initialization...")
    if wait_for_connection():
        try:
            create_collections()
            print("Vector database initialization completed successfully!")
        except Exception as e:
            print(f"Setup failed: {str(e)}")
        finally:
            try:
                connections.disconnect("default")
                print("Disconnected from Milvus")
            except:
                pass
    else:
        print("Failed to establish connection to Milvus")

if __name__ == "__main__":
    main()