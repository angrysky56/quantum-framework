"""
Quantum Core System Test Suite
---------------------------
Implements systematic validation of quantum operations and state evolution.

Test Architecture:
-----------------
Γ_test = {T_quantum, T_evolution, T_coherence}
"""

import numpy as np
import pytest
from numpy import linalg as LA
import sys
from pathlib import Path

# Add source directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.append(str(src_path))

from quantum_core import (
    QuantumState,
    Hamiltonian,
    Measurement
)

class TestQuantumCore:
    """
    Quantum core functionality test suite
    
    Test Categories:
    ---------------
    1. State Operations
       - Normalization
       - Evolution
       - Measurement
       
    2. Hamiltonian Properties
       - Hermiticity
       - Energy conservation
    """
    
    @pytest.fixture
    def quantum_state(self) -> QuantumState:
        """Initialize test quantum state"""
        return QuantumState.hydrogen_state(n=2, l=1, m=0)
    
    @pytest.fixture
    def hamiltonian(self) -> Hamiltonian:
        """Initialize test Hamiltonian"""
        def potential(r):
            return -1.0/r  # Coulomb potential
        return Hamiltonian(potential)
    
    def test_state_normalization(self, quantum_state):
        """Verify quantum state normalization"""
        wf = quantum_state.wavefunction
        norm = np.sqrt(np.vdot(wf, wf).real)
        assert np.isclose(norm, 1.0, atol=1e-6), \
            f"State not normalized: {norm}"
    
    def test_hamiltonian_hermiticity(self, hamiltonian, quantum_state):
        """Verify Hamiltonian hermiticity"""
        wf = quantum_state.wavefunction
        # Test ⟨ψ|H|ψ⟩ is real
        energy = np.vdot(wf, hamiltonian.apply(quantum_state).wavefunction)
        assert np.isclose(energy.imag, 0.0, atol=1e-6), \
            f"Energy not real: {energy}"
    
    def test_measurement_probability(self, quantum_state):
        """Verify measurement probability normalization"""
        measurement = Measurement(quantum_state.wavefunction)
        prob = measurement.get_probabilities()
        total_prob = np.sum(prob)
        assert np.isclose(total_prob, 1.0, atol=1e-6), \
            f"Probability not normalized: {total_prob}"
    
    @pytest.mark.parametrize("n,l,m", [
        (1, 0, 0),
        (2, 0, 0),
        (2, 1, 0),
        (2, 1, 1)
    ])
    def test_hydrogen_states(self, n, l, m):
        """Test various hydrogen atom eigenstates"""
        state = QuantumState.hydrogen_state(n, l, m)
        assert state.n == n and state.l == l and state.m == m, \
            "Quantum numbers not properly set"
        
        # Verify normalization
        norm = np.sqrt(np.vdot(state.wavefunction, 
                              state.wavefunction).real)
        assert np.isclose(norm, 1.0, atol=1e-6), \
            f"State (n={n},l={l},m={m}) not normalized"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])