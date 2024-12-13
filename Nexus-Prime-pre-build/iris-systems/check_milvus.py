from pymilvus import connections, utility
import time

def check_milvus():
    max_retries = 5
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            # Attempt to connect
            connections.connect(
                alias="default",
                host="milvus-standalone",
                port="19530"
            )
            print(f"Successfully connected to Milvus on attempt {attempt + 1}")
            
            # Check server version
            print(f"Server version: {utility.get_server_version()}")
            
            # List collections
            print("Existing collections:", utility.list_collections())
            
            return True

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Could not connect to Milvus.")
                return False

if __name__ == "__main__":
    check_milvus()