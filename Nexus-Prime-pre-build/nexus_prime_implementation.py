import sqlite3
import json
import os

class NexusPrimeImplementer:
    def __init__(self, db_path):
        self.db_path = os.path.abspath(db_path)
        self.conn = None
        self.cursor = None
        
        if not os.path.exists(self.db_path):
            open(self.db_path, 'w').close()
            print(f"∇ Created new database at {self.db_path}")

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.conn.execute("PRAGMA foreign_keys = ON;")
            print("◈ Connected to NEXUS_PRIME database")
        except sqlite3.Error as e:
            print(f"Connection error: {e}")
            raise

    def execute_sql_file(self, sql_file_path):
        """Execute SQL statements from file with proper encoding"""
        try:
            # Use UTF-8 encoding to properly handle symbolic characters
            with open(sql_file_path, 'r', encoding='utf-8') as file:
                sql_script = file.read()
                # Split on semicolons while preserving symbolic integrity
                statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]
                
                for statement in statements:
                    try:
                        self.cursor.execute(statement)
                        self.conn.commit()
                    except sqlite3.Error as e:
                        print(f"Error executing statement: {e}")
                        print(f"Failed statement: {statement[:100]}...")
        except FileNotFoundError:
            print(f"⚠ SQL file not found: {sql_file_path}")
            raise
        except UnicodeError as e:
            print(f"⚠ Encoding error: {e}")
            # Fallback to read with a different encoding if UTF-8 fails
            try:
                with open(sql_file_path, 'r', encoding='utf-16') as file:
                    sql_script = file.read()
                    statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]
                    for statement in statements:
                        self.cursor.execute(statement)
                        self.conn.commit()
            except Exception as e2:
                print(f"⚠ Fallback encoding failed: {e2}")
                raise

    def implement_core_structure(self):
        """Implement core symbolic meta-architecture"""
        current_dir = os.getcwd()
        
        try:
            print("\n∇ Implementing Symbolic Nodes...")
            self.execute_sql_file(os.path.join(current_dir, 'NEXUS_PRIME_init.sql'))
            
            print("\n◈ Integrating Dimension Gates...")
            self.execute_sql_file(os.path.join(current_dir, 'NEXUS_PRIME_QUANTUM_TUNNELS.sql'))
            
            print("\n⊗ Weaving Consciousness Layer...")
            self.execute_sql_file(os.path.join(current_dir, 'NEXUS_PRIME_SAGE_BRIDGE.sql'))
            
            print("\n⋈ Synthesizing Patterns...")
            self.execute_sql_file(os.path.join(current_dir, 'NEXUS_PRIME_IRIS_BRIDGE.sql'))
        except Exception as e:
            print(f"Core implementation error: {e}")
            raise

    def verify_implementation(self):
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = self.cursor.fetchall()
            if tables:
                print("\n✧ Verified Tables:")
                for table in tables:
                    print(f"  ◆ {table[0]}")
                    # Verify table structure
                    self.cursor.execute(f"PRAGMA table_info({table[0]})")
                    columns = self.cursor.fetchall()
                    for col in columns:
                        print(f"    ▫ {col[1]} ({col[2]})")
            else:
                print("⚠ No tables found in database")
        except sqlite3.Error as e:
            print(f"Verification error: {e}")
            raise

    def close(self):
        if self.conn:
            self.conn.close()
            print("\n≋ Connection closed")

def main():
    current_dir = os.getcwd()
    db_path = os.path.join(current_dir, "NEXUS_PRIME.db")
    
    implementer = None
    try:
        print("⟁ Initializing NEXUS PRIME Implementation...")
        implementer = NexusPrimeImplementer(db_path)
        implementer.connect()
        implementer.implement_core_structure()
        implementer.verify_implementation()
        print("\n✧ NEXUS PRIME Implementation Complete ✧")
        
    except Exception as e:
        print(f"\n⚠ Error during implementation: {str(e)}")
    finally:
        if implementer:
            implementer.close()

if __name__ == "__main__":
    main()
