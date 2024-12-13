from pymilvus import connections, Collection
import numpy as np
import json

def test_docker_integration():
    try:
        # Connect to Milvus
        connections.connect(
            alias="default",
            host="milvus-standalone",
            port="19530"
        )
        print("Successfully connected to Milvus")

        # Create a vector representing healthy Docker state
        # Using consistent values rather than random for stability
        base_vector = np.array([
            # Frontend health metrics (0.0-0.1 range)
            0.95,  # CPU usage normal
            0.93,  # Memory usage normal
            0.98,  # Response time good
            0.97,  # Error rate low
            
            # Backend health metrics (0.1-0.2 range)
            0.94,  # CPU usage normal
            0.92,  # Memory usage normal
            0.96,  # Response time good
            0.98,  # Error rate low
            
            # Postgres health metrics (0.2-0.3 range)
            0.97,  # CPU usage normal
            0.95,  # Memory usage normal
            0.99,  # Connection pool healthy
            0.96,  # Query performance good
            
            # Redis health metrics (0.3-0.4 range)
            0.98,  # CPU usage normal
            0.96,  # Memory usage normal
            0.99,  # Connection status good
            0.97   # Cache hit rate high
        ])
        
        # Extend to 512 dimensions with pattern repetition and variation
        docker_state_vector = np.tile(base_vector, 32)[:512]

        # Insert the Docker state pattern
        collection = Collection("correlation_patterns")
        
        docker_pattern = [
            ["docker_healthy_state_001"],  # pattern_id
            [docker_state_vector.tolist()],  # vector
            ["docker_environment"],  # pattern_type
            [json.dumps({
                "coherence": 0.96,
                "container_stability": 0.95,
                "network_health": 0.97,
                "volume_integrity": 0.98
            })],  # coherence_metrics
            [json.dumps({
                "timestamp": "2024-12-07",
                "state": "healthy_runtime",
                "containers": {
                    "dev-frontend": "healthy",
                    "dev-backend": "healthy",
                    "dev-postgres": "healthy",
                    "dev-redis": "healthy"
                }
            })]  # temporal_context
        ]

        collection.insert(docker_pattern)
        print("Inserted Docker healthy state pattern")

        # Perform a search to verify
        collection.load()
        search_params = {
            "metric_type": "L2",
            "params": {"ef": 64}
        }

        results = collection.search(
            data=[docker_state_vector.tolist()],
            anns_field="vector",
            param=search_params,
            limit=5,
            output_fields=["pattern_type", "coherence_metrics", "temporal_context"]
        )

        print("\nSearch Results:")
        for hits in results:
            for hit in hits:
                print(f"\nPattern Found:")
                print(f"Distance: {hit.distance}")
                print(f"Pattern Type: {hit.entity.get('pattern_type')}")
                print(f"Coherence Metrics: {hit.entity.get('coherence_metrics')}")
                print(f"Temporal Context: {hit.entity.get('temporal_context')}")

        return True

    except Exception as e:
        print(f"Error testing Docker integration: {e}")
        return False

if __name__ == "__main__":
    test_docker_integration()