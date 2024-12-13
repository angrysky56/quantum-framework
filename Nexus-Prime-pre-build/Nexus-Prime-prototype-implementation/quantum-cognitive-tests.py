"""
Test Suite for Quantum-Cognitive Bridge
-------------------------------------
Validates mathematical properties, state evolution,
and cognitive adaptation mechanisms.

Testing Framework:
----------------
1. Mathematical Properties
   - Unitarity
   - Hermiticity
   - Norm preservation
2. State Evolution
   - Coherence preservation
   - Entanglement dynamics
3. Cognitive Adaptation
   - Learning convergence
   - Memory management
"""

import numpy as np
import pytest
from numpy import linalg as LA
from typing import Tuple
import logging
from quantum_cognitive_bridge import (
    QuantumCognitiveBridge,
    HybridState,
    CognitiveAdaptation
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestQuantumCognitiveBridge:
    """Test suite for quantum-cognitive bridge implementation"""
    
    @pytest.fixture
    def bridge(self) -> QuantumCognitiveBridge:
        """Initialize bridge instance"""
        return QuantumCognitiveBridge(
            quantum_dim=32,  # Reduced dimension for testing
            cognitive_dim=16
        )
    
    @pytest.fixture
    def hybrid_state(self, bridge) -> HybridState:
        """Generate test hybrid state"""
        q_state = np.random.randn(bridge.quantum_dim) + \
                 1j * np.random.randn(bridge.quantum_dim)
        q_state = q_state / LA.norm(q_state)
        
        c_state = np.random.randn(bridge.cognitive_dim)
        c_state = c_state / LA.norm(c_state)
        
        return HybridState(
            quantum_component=q_state,
            cognitive_component=c_state,
            coherence=bridge.calculate_coherence(q_state),
            entanglement_measure=bridge.calculate_entanglement(q_state, c_state)
        )
    
    def test_hamiltonian_properties(self, bridge):
        """Test mathematical properties of Hamiltonians"""
        
        def is_hermitian(H: np.ndarray) -> bool:
            return np.allclose(H, H.conj().T)
        
        # Test quantum Hamiltonian
        assert is_hermitian(bridge.H_Q), "Quantum Hamiltonian not Hermitian"
        
        # Test cognitive operator
        assert np.allclose(bridge.H_C, bridge.H_C.T), \
            "Cognitive operator not symmetric"
        
        # Test interaction Hamiltonian
        assert is_hermitian(bridge.H_int), \
            "Interaction Hamiltonian not Hermitian"
    
    def test_evolution_unitarity(self, bridge):
        """Test unitarity of evolution operator"""
        U = bridge.U
        U_dag = U.conj().T
        I = np.eye(U.shape[0])
        
        assert np.allclose(U @ U_dag, I), \
            "Evolution operator not unitary"
    
    def test_state_normalization(self, bridge, hybrid_state):
        """Test norm preservation of state vectors"""
        # Test quantum component
        assert np.isclose(LA.norm(hybrid_state.quantum_component), 1.0), \
            "Quantum state not normalized"
        
        # Test cognitive component
        assert np.isclose(LA.norm(hybrid_state.cognitive_component), 1.0), \
            "Cognitive state not normalized"
    
    def test_coherence_bounds(self, bridge, hybrid_state):
        """Test coherence measure bounds"""
        coherence = bridge.calculate_coherence(hybrid_state.quantum_component)
        assert 0 <= coherence <= 1, \
            f"Coherence {coherence} outside [0,1] bounds"
    
    def test_entanglement_properties(self, bridge, hybrid_state):
        """Test entanglement measure properties"""
        entanglement = bridge.calculate_entanglement(
            hybrid_state.quantum_component,
            hybrid_state.cognitive_component
        )
        assert entanglement >= 0, \
            f"Negative entanglement measure: {entanglement}"
    
    def test_state_evolution(self, bridge, hybrid_state):
        """Test hybrid state evolution"""
        evolved_state = bridge.evolve_hybrid_state(hybrid_state)
        
        # Test norm preservation
        assert np.isclose(LA.norm(evolved_state.quantum_component), 1.0), \
            "Evolution violates quantum norm preservation"
        assert np.isclose(LA.norm(evolved_state.cognitive_component), 1.0), \
            "Evolution violates cognitive norm preservation"
        
        # Test coherence maintenance
        assert evolved_state.coherence >= bridge.coherence_threshold, \
            f"Coherence {evolved_state.coherence} below threshold"
    
    def test_bidirectional_mapping(self, bridge, hybrid_state):
        """Test quantum-cognitive mappings"""
        # Quantum to cognitive
        cognitive = bridge.quantum_to_cognitive(hybrid_state.quantum_component)
        assert cognitive.shape == (bridge.cognitive_dim,), \
            "Incorrect cognitive state dimension"
        assert np.isclose(LA.norm(cognitive), 1.0), \
            "Cognitive mapping violates normalization"
        
        # Cognitive to quantum
        quantum = bridge.cognitive_to_quantum(hybrid_state.cognitive_component)
        assert quantum.shape == (bridge.quantum_dim,), \
            "Incorrect quantum state dimension"
        assert np.isclose(LA.norm(quantum), 1.0), \
            "Quantum mapping violates normalization"
    
    @pytest.mark.parametrize("evolution_steps", [1, 5, 10])
    def test_long_evolution(self, bridge, hybrid_state, evolution_steps):
        """Test stability of long-term evolution"""
        state = hybrid_state
        coherence_history = []
        
        for _ in range(evolution_steps):
            state = bridge.evolve_hybrid_state(state)
            coherence_history.append(state.coherence)
            
            # Verify state properties
            assert np.isclose(LA.norm(state.quantum_component), 1.0), \
                "Long evolution violates quantum norm"
            assert np.isclose(LA.norm(state.cognitive_component), 1.0), \
                "Long evolution violates cognitive norm"
            assert state.coherence >= bridge.coherence_threshold, \
                f"Coherence degradation: {state.coherence}"
        
        # Test coherence stability
        coherence_std = np.std(coherence_history)
        assert coherence_std < 0.1, \
            f"Unstable coherence evolution: std={coherence_std}"

class TestCognitiveAdaptation:
    """Test suite for cognitive adaptation mechanisms"""
    
    @pytest.fixture
    def adaptation(self) -> CognitiveAdaptation:
        """Initialize adaptation module"""
        return CognitiveAdaptation(
            learning_rate=0.01,
            memory_capacity=100
        )
    
    def test_cognitive_update(self, adaptation):
        """Test cognitive state updates"""
        dim = 16
        current = np.random.randn(dim)
        current = current / LA.norm(current)
        target = np.random.randn(dim)
        target = target / LA.norm(target)
        
        updated = adaptation.update_cognitive_state(current, target)
        
        # Verify properties
        assert np.isclose(LA.norm(updated), 1.0), \
            "Update violates normalization"
        assert not np.allclose(updated, current), \
            "No learning occurred"
        
        # Verify convergence direction
        similarity = np.abs(updated @ target)
        original_similarity = np.abs(current @ target)
        assert similarity > original_similarity, \
            "Update did not improve target similarity"
    
    def test_memory_management(self, adaptation, hybrid_state):
        """Test experience memory management"""
        # Fill memory
        for _ in range(adaptation.memory_capacity + 10):
            adaptation.store_experience(hybrid_state, reward=1.0)
            
        assert len(adaptation.memory_buffer) == adaptation.memory_capacity, \
            "Memory capacity violation"
        
        # Verify FIFO behavior
        adaptation.store_experience(hybrid_state, reward=2.0)
        assert len(adaptation.memory_buffer) == adaptation.memory_capacity, \
            "Memory overflow"
        assert adaptation.memory_buffer[-1][1] == 2.0, \
            "Incorrect memory update"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])