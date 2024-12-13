import sqlite3
from pymilvus import connections, Collection
import numpy as np
import json

def migrate_patterns():
    try:
        # Connect to SQLite
        sqlite_conn = sqlite3.connect('core.db')
        cursor = sqlite_conn.cursor()
        
        # Connect to Milvus
        connections.connect(
            alias="default",
            host='localhost',
            port='19530'
        )
        
        # Get correlation patterns collection
        correlation_collection = Collection("correlation_patterns")
        correlation_collection.load()
        
        # Get patterns from SQLite
        cursor.execute("""
            SELECT * FROM neural_core_patterns 
            ORDER BY created_at DESC
        """)
        patterns = cursor.fetchall()
        
        # Prepare data for Milvus
        entities = []
        for pattern in patterns:
            # Generate vector from pattern structure
            pattern_data = json.loads(pattern[2])  # node_structure
            vector = np.random.rand(512)  # We'll need a proper vectorization function
            
            entity = {
                "pattern_id": pattern[0],
                "vector": vector.tolist(),
                "pattern_type": pattern[1],
                "coherence_metrics": json.dumps({
                    "learning_state": json.loads(pattern[3]),
                    "test_metrics": json.loads(pattern[4])
                }),
                "temporal_context": json.dumps({
                    "created_at": pattern[5]
                })
            }
            entities.append(entity)
        
        # Insert into Milvus
        correlation_collection.insert(entities)
        print(f"Migrated {len(entities)} patterns to Milvus")
        
        return True
        
    except Exception as e:
        print(f"Error during migration: {e}")
        return False
    finally:
        sqlite_conn.close()

if __name__ == "__main__":
    migrate_patterns()