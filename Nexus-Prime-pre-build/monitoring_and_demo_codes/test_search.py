from pymilvus import connections, Collection
import numpy as np
import json

def test_vector_search():
    try:
        # Connect to Milvus
        connections.connect(
            alias="default",
            host="milvus-standalone",
            port="19530"
        )
        print("Connected to Milvus successfully")

        # Access the existing collection
        collection = Collection("correlation_patterns")
        collection.load()
        print("Collection loaded")

        # Create a test search vector
        search_vector = np.random.rand(512)

        # Search parameters optimized for GPU-based similarity
        search_params = {
            "metric_type": "L2",
            "params": {"ef": 64}
        }

        # Perform the vector search
        results = collection.search(
            data=[search_vector.tolist()],
            anns_field="vector",
            param=search_params,
            limit=5,
            output_fields=["pattern_type", "coherence_metrics", "temporal_context"]
        )

        print("\nSearch Results:")
        for hits in results:
            for hit in hits:
                print("\nMatch Details:")
                print(f"Pattern ID: {hit.id}")
                print(f"Distance: {hit.distance}")
                print(f"Pattern Type: {hit.entity.get('pattern_type')}")

                coherence = json.loads(hit.entity.get('coherence_metrics'))
                print("\nCoherence Metrics:")
                print(f"- Quantum Coherence: {coherence.get('coherence', 'N/A')}")
                print(f"- Quantum Stability: {coherence.get('quantum_stability', 'N/A')}")
                print(f"- Pattern Coherence: {coherence.get('pattern_coherence', 'N/A')}")

        # Retrieve and print the total number of entities in the collection
        total_entities = collection.num_entities
        print("\nCollection Statistics:")
        print(f"Total Entities: {total_entities}")

        return True

    except Exception as e:
        print(f"Error during search test: {e}")
        return False

if __name__ == "__main__":
    test_vector_search()
