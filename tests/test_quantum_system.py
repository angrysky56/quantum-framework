"""
Quantum System Test Framework
---------------------------
Tests quantum state evolution and visualization components
using property-based testing with hypothesis.

Mathematical Framework:
H|ψ⟩ = E|ψ⟩ - Schrödinger Equation
P(x) = |⟨x|ψ⟩|² - Measurement Probability
"""

import numpy as np
import pytest
from hypothesis import given, strategies as st
from hypothesis.extra.numpy import arrays

from quantum_system import QuantumState, Hamiltonian, Measurement

class TestQuantumSystem:
    @given(
        arrays(np.complex128, shape=(10,), elements=st.complex_numbers())
    )
    def test_wavefunction_normalization(self, psi):
        """Test that wavefunctions are properly normalized"""
        state = QuantumState(psi)
        norm = np.abs(np.vdot(state.wavefunction, state.wavefunction))
        assert np.abs(norm - 1.0) < 1e-10

    @given(
        st.integers(min_value=1, max_value=5),
        st.integers(min_value=0, max_value=4),
        st.integers(min_value=-2, max_value=2)
    )
    def test_quantum_numbers(self, n, l, m):
        """Test quantum number constraints"""
        assert abs(m) <= l < n
        
    def test_measurement_probability(self):
        """Test that measurement probabilities sum to 1"""
        wf = np.random.randn(100) + 1j*np.random.randn(100)
        wf = wf / np.sqrt(np.sum(np.abs(wf)**2))
        
        measurement = Measurement(wf)
        probs = measurement.get_probabilities()
        
        assert np.abs(np.sum(probs) - 1.0) < 1e-10