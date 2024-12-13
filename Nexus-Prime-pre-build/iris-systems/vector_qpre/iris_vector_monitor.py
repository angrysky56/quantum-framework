from pymilvus import connections, Collection
import numpy as np
from typing import Dict, Any
import json
import time

class IRISVectorMonitor:
    def __init__(self):
        self.batch_optimizer = BatchSizeOptimizer()
        self.anomaly_detector = AnomalyDetector()
        self.coherence_controller = CoherenceController()
        
    def monitor_metrics(self, collection_name: str) -> Dict[str, Any]:
        collection = Collection(collection_name)
        
        # Get collection statistics
        stats = {
            "entity_count": collection.num_entities,
            "index_type": collection.index().params,
            "timestamp": time.time()
        }
        
        return stats

class BatchSizeOptimizer:
    def __init__(self, initial_size: int = 64):
        self.current_size = initial_size
        self.min_size = 16
        self.max_size = 1024
        
    def adjust_batch_size(self, performance: Dict[str, float]) -> int:
        if performance["avg_processing_time"] < 80 and performance["failure_rate"] < 0.005:
            self.current_size = min(self.current_size + 16, self.max_size)
        elif performance["failure_rate"] > 0.01 or performance["avg_processing_time"] > 150:
            self.current_size = max(self.current_size - 16, self.min_size)
            
        return self.current_size

class AnomalyDetector:
    def __init__(self, num_clusters: int = 10, threshold: float = 2.5):
        self.num_clusters = num_clusters
        self.threshold = threshold
        
    def detect_anomalies(self, vectors: np.ndarray) -> Dict[str, Any]:
        # Simplified anomaly detection using mean distance
        mean_vector = np.mean(vectors, axis=0)
        distances = np.linalg.norm(vectors - mean_vector, axis=1)
        anomalies = distances > self.threshold
        
        return {
            "anomaly_count": np.sum(anomalies),
            "mean_distance": np.mean(distances),
            "max_distance": np.max(distances)
        }

class CoherenceController:
    def __init__(self, window_size: int = 100, initial_threshold: float = 0.95):
        self.window_size = window_size
        self.current_threshold = initial_threshold
        self.history = []
        
    def update_threshold(self, coherence_score: float) -> float:
        self.history.append(coherence_score)
        if len(self.history) > self.window_size:
            self.history.pop(0)
            
        mean = np.mean(self.history)
        std = np.std(self.history)
        
        # Adjust threshold based on recent statistics
        if mean > self.current_threshold and std < 0.1:
            self.current_threshold = min(mean, 0.98)  # Cap at 0.98
        elif mean < self.current_threshold - 2*std:
            self.current_threshold = max(mean + std, 0.9)  # Floor at 0.9
            
        return self.current_threshold

def monitor_iris_collections():
    # Connect to Milvus
    connections.connect(
        alias="default",
        host="milvus-standalone",
        port="19530"
    )
    
    monitor = IRISVectorMonitor()
    collections = ["iris_qpre", "iris_dss", "iris_tcw"]
    
    monitoring_data = {}
    for collection_name in collections:
        try:
            metrics = monitor.monitor_metrics(collection_name)
            monitoring_data[collection_name] = metrics
        except Exception as e:
            print(f"Error monitoring {collection_name}: {str(e)}")
    
    return monitoring_data

if __name__ == "__main__":
    monitoring_data = monitor_iris_collections()
    print(json.dumps(monitoring_data, indent=2))