"""
Quantum System Implementation
---------------------------
Implements core quantum mechanics functionality with
numerical precision and computational efficiency.

Mathematical Framework:
Ψ(r,θ,φ) = R(r)Y_{lm}(θ,φ) - Wavefunction
H = -ℏ²/2m ∇² + V(r) - Hamiltonian
⟨A⟩ = ⟨ψ|A|ψ⟩ - Expectation Value
"""

import numpy as np
from scipy.special import sph_harm, genlaguerre
from numba import jit
from dataclasses import dataclass
from typing import Tuple, Optional

@dataclass
class QuantumState:
    """Represents a quantum state with associated quantum numbers"""
    wavefunction: np.ndarray
    n: Optional[int] = None
    l: Optional[int] = None
    m: Optional[int] = None
    
    def __post_init__(self):
        """Normalize the wavefunction"""
        norm = np.sqrt(np.vdot(self.wavefunction, self.wavefunction))
        self.wavefunction = self.wavefunction / norm
    
    @classmethod
    def hydrogen_state(cls, n: int, l: int, m: int) -> 'QuantumState':
        """Create a hydrogen atom eigenstate"""
        if not (0 <= l < n and abs(m) <= l):
            raise ValueError("Invalid quantum numbers")
            
        r_points = np.linspace(0, 20, 100)
        theta_points = np.linspace(0, np.pi, 50)
        phi_points = np.linspace(0, 2*np.pi, 50)
        
        R, Theta, Phi = np.meshgrid(r_points, theta_points, phi_points)
        
        wf = radial_wavefunction(n, l, R) * sph_harm(m, l, Phi, Theta)
        return cls(wf, n, l, m)

@jit(nopython=True)
def radial_wavefunction(n: int, l: int, r: np.ndarray) -> np.ndarray:
    """Compute the radial part of the wavefunction"""
    rho = 2 * r / n
    L = genlaguerre(n-l-1, 2*l+1)
    norm = np.sqrt((2/n)**3 * factorial(n-l-1)/(2*n*factorial(n+l)))
    return norm * np.exp(-rho/2) * rho**l * L(rho)

class Hamiltonian:
    """Quantum Hamiltonian operator"""
    def __init__(self, potential_function):
        self.V = potential_function
        
    def apply(self, state: QuantumState) -> QuantumState:
        """Apply H to a quantum state"""
        kinetic = self._laplacian(state.wavefunction)
        potential = self.V(state.wavefunction)
        return QuantumState(-0.5 * kinetic + potential)
    
    @staticmethod
    @jit(nopython=True)
    def _laplacian(wf: np.ndarray) -> np.ndarray:
        """Compute ∇² of wavefunction"""
        return np.gradient(np.gradient(wf))[0]

class Measurement:
    """Quantum measurement operations"""
    def __init__(self, wavefunction: np.ndarray):
        self.wf = wavefunction
        
    def get_probabilities(self) -> np.ndarray:
        """Compute probability distribution |ψ|²"""
        return np.abs(self.wf)**2
        
    def expectation_value(self, operator: np.ndarray) -> complex:
        """Compute ⟨ψ|A|ψ⟩"""
        return np.vdot(self.wf, operator @ self.wf)