from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType
import numpy as np
import json

# Connect to Milvus
connections.connect("default", host="localhost", port="19530")

# Define the collection schema for pattern synthesis
fields = [
    FieldSchema(name="pattern_id", dtype=DataType.VARCHAR, max_length=100, is_primary=True),
    FieldSchema(name="pattern_vector", dtype=DataType.FLOAT_VECTOR, dim=512),
    FieldSchema(name="base_patterns", dtype=DataType.JSON),
    FieldSchema(name="coherence_metrics", dtype=DataType.JSON),
    FieldSchema(name="evolution_state", dtype=DataType.JSON),
    FieldSchema(name="synthesis_log", dtype=DataType.JSON)
]

schema = CollectionSchema(fields, "Pattern Synthesis Collection")
collection_name = "auto_synthesis_patterns"

# Create collection
pattern_collection = Collection(collection_name, schema)

# Create an IVF_SQ8 index for better GPU performance
index_params = {
    "metric_type": "COSINE",
    "index_type": "IVF_SQ8",
    "params": {"nlist": 1024}
}

# Create index on the vector field
pattern_collection.create_index(
    field_name="pattern_vector",
    index_params=index_params
)

# Initialize base patterns
base_patterns = {
    "quantum": ["⦿", "⧈", "⫰", "◬", "⬡"],
    "dream": ["∞", "⟲", "⊹", "◈", "⌬"],
    "consciousness": ["∴", "⍟", "⎈", "❈", "⌘"]
}

# Function to generate initial pattern vectors
def generate_pattern_vector(pattern_type, symbol):
    # This would be replaced with actual embedding logic
    # For now, we'll create structured random vectors
    base = np.random.normal(0, 1, 512)
    if pattern_type == "quantum":
        base[:170] *= 2  # Emphasize quantum characteristics
    elif pattern_type == "dream":
        base[171:340] *= 2  # Emphasize dream characteristics
    else:
        base[341:] *= 2  # Emphasize consciousness characteristics
    return base / np.linalg.norm(base)

# Insert base patterns
for pattern_type, symbols in base_patterns.items():
    for symbol in symbols:
        pattern_id = f"{pattern_type}_{symbol}"
        vector = generate_pattern_vector(pattern_type, symbol).tolist()
        
        entities = [
            [pattern_id],  # pattern_id
            [vector],      # pattern_vector
            [{"type": pattern_type, "symbol": symbol}],  # base_patterns
            [{"coherence": 1.0, "stability": 1.0}],      # coherence_metrics
            [{"state": "base", "evolution_stage": 0}],   # evolution_state
            [{"initialization": "base_pattern"}]          # synthesis_log
        ]
        
        pattern_collection.insert(entities)

# Load the collection for search
pattern_collection.load()

print(f"Pattern synthesis collection initialized with {pattern_collection.num_entities} base patterns")
print("Ready for pattern synthesis operations!")