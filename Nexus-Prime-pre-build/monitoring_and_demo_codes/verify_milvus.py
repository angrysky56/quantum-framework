from pymilvus import connections, utility

def verify_milvus():
    try:
        # Attempt to connect
        connections.connect(
            alias="default",
            host="localhost",
            port="19530"
        )
        print("Successfully connected to Milvus")
        
        # Check server version
        print(f"Server version: {utility.get_server_version()}")
        
        # List collections
        print("Existing collections:", utility.list_collections())
        
        return True
    except Exception as e:
        print(f"Error connecting to Milvus: {e}")
        return False

if __name__ == "__main__":
    verify_milvus()