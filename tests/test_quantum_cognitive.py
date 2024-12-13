"""
Quantum-Cognitive Framework Test Suite
-----------------------------------
Implements systematic validation of quantum-cognitive bridge operations
with rigorous mathematical verification.

Test Architecture:
Γ_test = {T_quantum ⊗ T_cognitive}
where:
- T_quantum: Quantum state validation
- T_cognitive: Cognitive processing verification
"""

import numpy as np
import pytest
from numpy import linalg as LA
from typing import Tuple, Optional
import logging
from pathlib import Path
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add source directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.append(str(src_path))

try:
    from quantum_cognitive_bridge import (
        QuantumCognitiveBridge,
        HybridState,
        CognitiveAdaptation
    )
except ImportError as e:
    logger.error(f"Import Error: {e}")
    logger.error("Ensure quantum_cognitive_bridge.py is in the src directory")
    raise

class TestQuantumCognitiveBridge:
    """
    Test suite for quantum-cognitive bridge implementation
    
    Test Framework:
    --------------
    1. Mathematical Properties
       - Hilbert space operations
       - Quantum coherence
       - Cognitive mappings
    
    2. State Evolution
       - Unitarity preservation
       - Coherence maintenance
       - Entanglement dynamics
    """
    
    @pytest.fixture
    def bridge(self) -> QuantumCognitiveBridge:
        """Initialize quantum-cognitive bridge instance"""
        return QuantumCognitiveBridge(
            quantum_dim=32,  # Reduced dimension for testing
            cognitive_dim=16
        )
    
    @pytest.fixture
    def hybrid_state(self, bridge) -> HybridState:
        """Generate test hybrid state"""
        # Initialize quantum component
        q_state = np.random.randn(bridge.quantum_dim) + \
                 1j * np.random.randn(bridge.quantum_dim)
        q_state = q_state / LA.norm(q_state)
        
        # Initialize cognitive component
        c_state = np.random.randn(bridge.cognitive_dim)
        c_state = c_state / LA.norm(c_state)
        
        return HybridState(
            quantum_component=q_state,
            cognitive_component=c_state,
            coherence=bridge.calculate_coherence(q_state),
            entanglement_measure=bridge.calculate_entanglement(q_state, c_state)
        )
    
    def test_hamiltonian_properties(self, bridge):
        """Validate mathematical properties of system Hamiltonians"""
        # Test quantum Hamiltonian hermiticity
        assert np.allclose(bridge.H_Q, bridge.H_Q.conj().T), \
            "Quantum Hamiltonian violates hermiticity"
        
        # Test cognitive operator symmetry
        assert np.allclose(bridge.H_C, bridge.H_C.T), \
            "Cognitive operator violates symmetry"
        
        # Test interaction Hamiltonian hermiticity
        assert np.allclose(bridge.H_int, bridge.H_int.conj().T), \
            "Interaction Hamiltonian violates hermiticity"
    
    def test_evolution_unitarity(self, bridge):
        """Verify unitarity of quantum evolution"""
        U = bridge.U
        U_dag = U.conj().T
        I = np.eye(U.shape[0])
        
        # Test U U† = I
        assert np.allclose(U @ U_dag, I, atol=1e-6), \
            "Evolution operator violates unitarity"
    
    def test_state_normalization(self, bridge, hybrid_state):
        """Verify quantum state normalization"""
        # Test quantum component normalization
        assert np.isclose(LA.norm(hybrid_state.quantum_component), 1.0, atol=1e-6), \
            "Quantum state normalization violation"
        
        # Test cognitive component normalization
        assert np.isclose(LA.norm(hybrid_state.cognitive_component), 1.0, atol=1e-6), \
            "Cognitive state normalization violation"
    
    def test_coherence_bounds(self, bridge, hybrid_state):
        """Validate coherence measure bounds"""
        coherence = bridge.calculate_coherence(hybrid_state.quantum_component)
        # Test coherence ∈ [0,1]
        assert 0 <= coherence <= 1, \
            f"Coherence {coherence} outside [0,1] bounds"
    
    def test_state_evolution(self, bridge, hybrid_state):
        """Test hybrid state evolution properties"""
        evolved_state = bridge.evolve_hybrid_state(hybrid_state)
        
        # Verify norm preservation
        assert np.isclose(LA.norm(evolved_state.quantum_component), 1.0, atol=1e-6), \
            "Evolution violates quantum norm conservation"
            
        assert np.isclose(LA.norm(evolved_state.cognitive_component), 1.0, atol=1e-6), \
            "Evolution violates cognitive norm conservation"
        
        # Verify coherence maintenance
        assert evolved_state.coherence >= bridge.coherence_threshold, \
            f"Evolution coherence {evolved_state.coherence} below threshold"

class TestCognitiveAdaptation:
    """
    Test suite for cognitive adaptation mechanisms
    
    Test Framework:
    --------------
    1. Learning Dynamics
       - State updates
       - Convergence properties
    
    2. Memory Management
       - Capacity constraints
       - Update mechanisms
    """
    
    @pytest.fixture
    def adaptation(self) -> CognitiveAdaptation:
        """Initialize cognitive adaptation module"""
        return CognitiveAdaptation(
            learning_rate=0.01,
            memory_capacity=100
        )
    
    def test_cognitive_update(self, adaptation):
        """Validate cognitive state update mechanism"""
        dim = 16
        # Initialize test states
        current = np.random.randn(dim)
        current = current / LA.norm(current)
        target = np.random.randn(dim)
        target = target / LA.norm(target)
        
        # Perform update
        updated = adaptation.update_cognitive_state(current, target)
        
        # Verify normalization
        assert np.isclose(LA.norm(updated), 1.0, atol=1e-6), \
            "Update violates state normalization"
        
        # Verify learning occurs
        assert not np.allclose(updated, current, atol=1e-6), \
            "No learning effect observed"
        
        # Verify convergence direction
        similarity = np.abs(updated @ target)
        original_similarity = np.abs(current @ target)
        assert similarity > original_similarity, \
            "Update did not improve target similarity"
    
    def test_memory_management(self, adaptation, hybrid_state):
        """Test experience memory system"""
        # Fill memory beyond capacity
        for _ in range(adaptation.memory_capacity + 10):
            adaptation.store_experience(hybrid_state, reward=1.0)
        
        # Verify capacity constraint
        assert len(adaptation.memory_buffer) == adaptation.memory_capacity, \
            "Memory capacity violation"
        
        # Test FIFO behavior
        adaptation.store_experience(hybrid_state, reward=2.0)
        assert len(adaptation.memory_buffer) == adaptation.memory_capacity, \
            "Memory overflow"
        assert adaptation.memory_buffer[-1][1] == 2.0, \
            "Incorrect memory update sequence"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])