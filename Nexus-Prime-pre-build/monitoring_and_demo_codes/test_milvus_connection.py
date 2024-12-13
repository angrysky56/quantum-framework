from pymilvus import connections, utility

def test_milvus_connection():
    """Test connection to Milvus server"""
    print("Testing Milvus connection...")
    
    # Try different possible host configurations
    configs = [
        {"host": "localhost", "port": "19530"},
        {"host": "127.0.0.1", "port": "19530"},
        {"host": "milvus-standalone", "port": "19530"}
    ]
    
    for config in configs:
        try:
            print(f"\nTrying connection with: {config}")
            connections.connect(
                alias="default",
                host=config["host"],
                port=config["port"]
            )
            print("✓ Connection successful!")
            
            # Try to list collections
            collections = utility.list_collections()
            print(f"Available collections: {collections}")
            
            # Disconnect before trying next config
            connections.disconnect("default")
            
        except Exception as e:
            print(f"✗ Connection failed: {str(e)}")
            continue

if __name__ == "__main__":
    test_milvus_connection()