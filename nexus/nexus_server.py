import os
import numpy as np
import torch
import jax
import jax.numpy as jnp
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType
import qutip as qt
import networkx as nx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from prometheus_client import start_http_server, Gauge, Counter
import logging
from pythonjsonlogger import jsonlogger
import time
from typing import Dict, List, Optional
from pydantic import BaseModel

# Configure logging
logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# Initialize metrics
QUANTUM_OPERATIONS = Counter('quantum_operations_total', 'Number of quantum operations performed')
PATTERN_SYNTHESES = Counter('pattern_syntheses_total', 'Number of pattern syntheses performed')
VECTOR_SEARCHES = Counter('vector_searches_total', 'Number of vector searches performed')
SYSTEM_MEMORY = Gauge('system_memory_usage_bytes', 'Current system memory usage')

class NexusPrime:
    def __init__(self):
        self.dimension = int(os.getenv('VECTOR_DIMENSION', '512'))
        self.clustering_enabled = os.getenv('CLUSTERING_ENABLED', 'true').lower() == 'true'
        
        # Initialize quantum layers
        self.quantum_layers = {
            'coherent': torch.nn.Parameter(torch.randn(self.dimension)),
            'entangled': torch.nn.Parameter(torch.randn(self.dimension, self.dimension))
        }
        
        # Collection parameters for new Faiss-based HNSW
        self.collection_params = {
            'dimension': self.dimension,
            'index_type': 'HNSW',
            'metric_type': 'L2',
            'params': {
                'M': 16,
                'efConstruction': 200,
                'quantization': {
                    'type': 'PRQ',
                    'nbits': 8
                }
            }
        }
        
        # Clustering configuration
        self.clustering_config = {
            'enable': self.clustering_enabled,
            'clustering_key': 'timestamp',
            'num_clusters': 128
        }
        
        # Setup Milvus connection
        self.setup_milvus()
        
        # Initialize quantum state
        self.psi = qt.basis([2, 2], [0, 0])
        
        # Setup pattern synthesis graph
        self.pattern_graph = nx.Graph()
        
        logger.info("NexusPrime initialized", extra={
            'dimension': self.dimension,
            'clustering_enabled': self.clustering_enabled
        })

    def setup_milvus(self):
        """Initialize Milvus connection and collections"""
        try:
            connections.connect(
                host=os.getenv('MILVUS_HOST', 'standalone'),
                port=os.getenv('MILVUS_PORT', '19530')
            )
            self.setup_collections()
            logger.info("Milvus connection established")
        except Exception as e:
            logger.error("Milvus connection failed", extra={'error': str(e)})
            raise

    def setup_collections(self):
        """Setup Milvus collections with new 2.5 features"""
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(
                name="timestamp",
                dtype=DataType.INT64,
                nullable=True,
                default_value=0
            ),
            FieldSchema(
                name="vector",
                dtype=DataType.FLOAT_VECTOR,
                dim=self.dimension
            ),
            FieldSchema(
                name="metadata",
                dtype=DataType.JSON,
                nullable=True
            )
        ]
        
        schema = CollectionSchema(
            fields=fields,
            description="Quantum state vectors with metadata"
        )
        
        try:
            collection = Collection(
                name="quantum_states",
                schema=schema,
                clustering=self.clustering_config if self.clustering_enabled else None
            )
            
            # Create HNSW index with new Faiss backend
            collection.create_index(
                field_name="vector",
                index_params=self.collection_params
            )
            logger.info("Collection and index created successfully")
        except Exception as e:
            logger.error("Collection setup failed", extra={'error': str(e)})
            raise

    def quantum_evolution(self, state, hamiltonian):
        """Quantum state evolution under given Hamiltonian"""
        QUANTUM_OPERATIONS.inc()
        U = (-1j * hamiltonian * 0.1).expm()
        return U * state
        
    def pattern_synthesis(self, input_pattern):
        """Synthesize patterns using quantum-classical hybrid approach"""
        PATTERN_SYNTHESES.inc()
        
        # Convert input to quantum state
        q_pattern = qt.Qobj(input_pattern)
        
        # Evolve quantum state
        H = qt.sigmax() + qt.sigmay() + qt.sigmaz()
        evolved = self.quantum_evolution(q_pattern, H)
        
        # Project back to classical domain
        classical = np.array(evolved.full())
        
        # Update pattern graph
        self.pattern_graph.add_edge(
            str(input_pattern),
            str(classical),
            weight=float(np.abs(evolved.norm()))
        )
        
        return classical

    def search_similar_states(self, query_state, collection_name="quantum_states", top_k=5):
        """Search for similar states in Milvus"""
        VECTOR_SEARCHES.inc()
        collection = Collection(collection_name)
        collection.load()
        try:
            results = collection.search(
                data=[query_state.flatten()],
                anns_field="vector",
                param={"metric_type": "L2", "params": {"nprobe": 16}},
                limit=top_k
            )
            return results
        except Exception as e:
            logger.error("Search failed", extra={'error': str(e)})
            raise
        finally:
            collection.release()

# FastAPI app initialization
app = FastAPI(title="NEXUS_PRIME API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize NexusPrime
nexus = NexusPrime()

class QuantumState(BaseModel):
    state_vector: List[float]
    metadata: Optional[Dict] = None

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/metrics")
async def get_metrics():
    """Expose metrics for Milvus WebUI"""
    collection = Collection("quantum_states")
    collection.load()
    try:
        return {
            "system_status": "healthy",
            "collections": {
                "quantum_states": {
                    "total_entities": collection.num_entities,
                    "index_status": "built",
                    "clustering_status": "optimized" if nexus.clustering_enabled else "disabled"
                }
            }
        }
    finally:
        collection.release()

@app.post("/quantum/evolve")
async def evolve_state(state: QuantumState):
    """Evolve quantum state endpoint"""
    try:
        # Convert input to quantum state
        q_state = qt.Qobj(np.array(state.state_vector))
        
        # Create Hamiltonian
        H = qt.sigmax() + qt.sigmay() + qt.sigmaz()
        
        # Evolve state
        evolved = nexus.quantum_evolution(q_state, H)
        
        return {
            "evolved_state": evolved.full().flatten().tolist(),
            "norm": float(evolved.norm())
        }
    except Exception as e:
        logger.error("Evolution failed", extra={'error': str(e)})
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/pattern/synthesize")
async def synthesize_pattern(state: QuantumState):
    """Pattern synthesis endpoint"""
    try:
        pattern = np.array(state.state_vector)
        synthesized = nexus.pattern_synthesis(pattern)
        return {
            "synthesized_pattern": synthesized.flatten().tolist()
        }
    except Exception as e:
        logger.error("Pattern synthesis failed", extra={'error': str(e)})
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Start Prometheus metrics server
    start_http_server(8000)
    
    # Start FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=5000)