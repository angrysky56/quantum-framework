"""
Quantum Core System Implementation
--------------------------------
Implements foundational quantum mechanics with rigorous mathematical formalism.

Framework Architecture:
---------------------
Γ_system = {H, Ψ, M}
where:
H: Hamiltonian operator
Ψ: State space
M: Measurement operators

Core Mathematical Framework:
-------------------------
Ψ_{nlm}(r,θ,φ) = R_{nl}(r)Y_{lm}(θ,φ)
"""

import numpy as np
from scipy.special import sph_harm, factorial
from numba import jit, float64, int64
from typing import Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QuantumState:
    """
    Quantum state representation with dimensional analysis
    
    Mathematical Framework:
    ---------------------
    |ψ⟩ = Σ_{nlm} c_{nlm}|nlm⟩
    """
    
    def __init__(self,
                 wavefunction: np.ndarray,
                 n: Optional[int] = None,
                 l: Optional[int] = None,
                 m: Optional[int] = None):
        """Initialize quantum state"""
        self.wavefunction = wavefunction
        self.n = n
        self.l = l
        self.m = m
        self._normalize()
    
    def _normalize(self):
        """
        Normalize wavefunction
        ∫|ψ|² dτ = 1
        """
        norm = np.sqrt(np.vdot(self.wavefunction, self.wavefunction).real)
        if norm > 1e-10:
            self.wavefunction = self.wavefunction / norm
    
    @classmethod
    def hydrogen_state(cls, n: int, l: int, m: int) -> 'QuantumState':
        """
        Create hydrogen atom eigenstate
        
        Parameters:
        -----------
        n: Principal quantum number
        l: Angular momentum quantum number
        m: Magnetic quantum number
        
        Returns:
        --------
        QuantumState: Initialized hydrogen eigenstate
        """
        if not (0 <= l < n and abs(m) <= l):
            raise ValueError("Invalid quantum numbers")
        
        # Create coordinate grid
        r = np.linspace(0, 20, 100)
        theta = np.linspace(0, np.pi, 50)
        phi = np.linspace(0, 2*np.pi, 50)
        
        # Create meshgrid with explicit dimension preservation
        R, Theta, Phi = np.meshgrid(r, theta, phi, indexing='ij')
        
        # Compute radial part with dimension preservation
        radial = radial_wavefunction(n, l, R)
        
        # Compute angular part
        angular = sph_harm(m, l, Phi, Theta)
        
        # Combine components
        wf = radial * angular
        
        return cls(wf, n, l, m)

class Measurement:
    """
    Quantum measurement operations with dimensional analysis
    
    Framework:
    ---------
    - Probability: |⟨ψ|ϕ⟩|²
    - Expectation: ⟨ψ|A|ψ⟩
    """
    
    def __init__(self, wavefunction: np.ndarray):
        self.wf = wavefunction
    
    def get_probabilities(self) -> np.ndarray:
        """
        Compute probability density |ψ|²
        """
        return np.abs(self.wf)**2
    
    def expectation_value(self, operator: np.ndarray) -> complex:
        """
        Compute expectation value ⟨ψ|A|ψ⟩
        """
        return np.vdot(self.wf, operator @ self.wf)

class Hamiltonian:
    """
    Quantum Hamiltonian operator with spherical coordinate implementation
    
    Mathematical Framework:
    ---------------------
    H = -½∇² + V(r)
    
    where ∇² in spherical coordinates is:
    ∇² = ∂²/∂r² + (2/r)∂/∂r + (1/r²)L²
    """
    
    def __init__(self, potential_function):
        self.V = potential_function
    
    def apply(self, state: QuantumState) -> QuantumState:
        """
        Apply Hamiltonian to quantum state
        
        H|ψ⟩ = (-½∇² + V)|ψ⟩
        """
        kinetic = self._laplacian_spherical(state.wavefunction)
        potential = self.V(state.wavefunction)
        return QuantumState(-0.5 * kinetic + potential)
    
    @staticmethod
    @jit(nopython=True)
    def _finite_diff_2nd(f: np.ndarray, dx: float, axis: int) -> np.ndarray:
        """
        Second derivative using central finite differences
        f''(x) ≈ (f(x+h) - 2f(x) + f(x-h))/h²
        """
        result = np.zeros_like(f)
        if axis == 0:  # r
            result[1:-1, :, :] = (f[2:, :, :] - 2*f[1:-1, :, :] + f[:-2, :, :]) / (dx * dx)
            result[0, :, :] = result[1, :, :]
            result[-1, :, :] = result[-2, :, :]
        elif axis == 1:  # θ
            result[:, 1:-1, :] = (f[:, 2:, :] - 2*f[:, 1:-1, :] + f[:, :-2, :]) / (dx * dx)
            result[:, 0, :] = result[:, 1, :]
            result[:, -1, :] = result[:, -2, :]
        else:  # φ
            result[:, :, 1:-1] = (f[:, :, 2:] - 2*f[:, :, 1:-1] + f[:, :, :-2]) / (dx * dx)
            result[:, :, 0] = result[:, :, 1]
            result[:, :, -1] = result[:, :, -2]
        return result
    
    @staticmethod
    @jit(nopython=True)
    def _finite_diff_1st(f: np.ndarray, dx: float, axis: int) -> np.ndarray:
        """
        First derivative using central finite differences
        f'(x) ≈ (f(x+h) - f(x-h))/(2h)
        """
        result = np.zeros_like(f)
        if axis == 0:  # r
            result[1:-1, :, :] = (f[2:, :, :] - f[:-2, :, :]) / (2 * dx)
            result[0, :, :] = result[1, :, :]
            result[-1, :, :] = result[-2, :, :]
        elif axis == 1:  # θ
            result[:, 1:-1, :] = (f[:, 2:, :] - f[:, :-2, :]) / (2 * dx)
            result[:, 0, :] = result[:, 1, :]
            result[:, -1, :] = result[:, -2, :]
        else:  # φ
            result[:, :, 1:-1] = (f[:, :, 2:] - f[:, :, :-2]) / (2 * dx)
            result[:, :, 0] = result[:, :, 1]
            result[:, :, -1] = result[:, :, -2]
        return result
    
    @staticmethod
    @jit(nopython=True)
    def _laplacian_spherical(wf: np.ndarray) -> np.ndarray:
        """
        Compute Laplacian in spherical coordinates
        ∇² = ∂²/∂r² + (2/r)∂/∂r + (1/r²)L²
        """
        # Grid parameters
        nr, ntheta, nphi = wf.shape
        r = np.linspace(1e-10, 20, nr)
        theta = np.linspace(0, np.pi, ntheta)
        phi = np.linspace(0, 2*np.pi, nphi)
        
        dr = r[1] - r[0]
        dtheta = theta[1] - theta[0]
        dphi = phi[1] - phi[0]
        
        result = np.zeros_like(wf)
        
        # Compute derivatives
        d2r = Hamiltonian._finite_diff_2nd(wf, dr, 0)
        dr_wf = Hamiltonian._finite_diff_1st(wf, dr, 0)
        d2theta = Hamiltonian._finite_diff_2nd(wf, dtheta, 1)
        dtheta_wf = Hamiltonian._finite_diff_1st(wf, dtheta, 1)
        d2phi = Hamiltonian._finite_diff_2nd(wf, dphi, 2)
        
        # Combine components
        for i in range(nr):
            r_val = r[i]
            for j in range(ntheta):
                theta_val = theta[j]
                sin_theta = np.sin(theta_val)
                
                result[i, j, :] = d2r[i, j, :] + (2.0/r_val) * dr_wf[i, j, :]
                
                if r_val > 1e-8:
                    result[i, j, :] += (1.0/(r_val*r_val)) * (
                        (1.0/sin_theta) * dtheta_wf[i, j, :] +
                        d2theta[i, j, :] +
                        (1.0/(sin_theta*sin_theta)) * d2phi[i, j, :]
                    )
        
        return result

@jit(float64[:](int64, int64, float64[:]), nopython=True)
def _laguerre_array(n: int, alpha: int, x: np.ndarray) -> np.ndarray:
    """
    Compute associated Laguerre polynomial L_n^α(x)
    """
    result = np.zeros_like(x)
    
    for i in range(len(x)):
        if n == 0:
            result[i] = 1.0
        elif n == 1:
            result[i] = 1.0 + alpha - x[i]
        else:
            L_prev = 1.0
            L_curr = 1.0 + alpha - x[i]
            
            for k in range(2, n + 1):
                L_next = ((2*k - 1 + alpha - x[i]) * L_curr -
                         (k - 1 + alpha) * L_prev) / k
                L_prev = L_curr
                L_curr = L_next
            
            result[i] = L_curr
    
    return result

@jit(float64(int64, int64), nopython=True)
def _factorial_ratio(n: int, l: int) -> float:
    """
    Compute factorial ratio (n-l-1)! / (n+l)!
    """
    if n <= l:
        return 0.0
    
    numerator = 1.0
    for i in range(1, n-l):
        numerator *= i
        
    denominator = 1.0
    for i in range(1, n+l+1):
        denominator *= i
        
    return numerator / denominator

@jit(float64[:, :, :](int64, int64, float64[:, :, :]), nopython=True)
def radial_wavefunction(n: int, l: int, r: np.ndarray) -> np.ndarray:
    """
    Compute hydrogen atom radial wavefunction R_{nl}(r)
    """
    if not (0 <= l < n):
        return np.zeros_like(r)
    
    # Compute normalization
    norm = np.sqrt((2.0/n)**3 * _factorial_ratio(n, l) / (2.0*n))
    
    # Initialize result array
    result = np.zeros_like(r)
    
    # Compute for each point
    for i in range(r.shape[0]):
        for j in range(r.shape[1]):
            for k in range(r.shape[2]):
                rho = 2.0 * r[i,j,k] / float(n)
                x = np.array([rho])
                L = _laguerre_array(n-l-1, 2*l+1, x)[0]
                result[i,j,k] = np.exp(-rho/2.0) * np.power(rho, l) * L
    
    return norm * result