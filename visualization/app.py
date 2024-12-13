"""
Quantum Visualization Service
---------------------------
Interactive visualization of quantum mechanical systems
with real-time parameter adjustment and state evolution.

Mathematical Framework:
Ψ(r,θ,φ,t) = Σ c_n ψ_n(r,θ,φ)exp(-iE_nt/ℏ)
|Ψ(t)⟩ = exp(-iHt/ℏ)|Ψ(0)⟩
"""

import numpy as np
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from typing import Tuple, List, Optional

from quantum_system import QuantumState, Hamiltonian

class QuantumVisualizer:
    """
    Quantum state visualization engine with interactive dynamics
    
    Parameters:
    -----------
    resolution: int
        Grid resolution for numerical computations
    max_n: int
        Maximum principal quantum number
    """
    def __init__(self, resolution: int = 100, max_n: int = 5):
        self.resolution = resolution
        self.max_n = max_n
        self.setup_grid()
        
    def setup_grid(self):
        """Initialize computational grid"""
        self.r = np.linspace(0, 20, self.resolution)
        self.theta = np.linspace(0, np.pi, self.resolution)
        self.phi = np.linspace(0, 2*np.pi, self.resolution)
        self.R, self.Theta, self.Phi = np.meshgrid(self.r, self.theta, self.phi)
        
    def compute_wavefunction(self, n: int, l: int, m: int) -> np.ndarray:
        """Generate quantum wavefunction for given quantum numbers"""
        state = QuantumState.hydrogen_state(n, l, m)
        return state.wavefunction
        
    def plot_probability_density(self, wf: np.ndarray) -> go.Figure:
        """Create 3D visualization of probability density"""
        rho = np.abs(wf)**2
        
        return go.Figure(data=[
            go.Surface(
                x=self.R * np.sin(self.Theta) * np.cos(self.Phi),
                y=self.R * np.sin(self.Theta) * np.sin(self.Phi),
                z=self.R * np.cos(self.Theta),
                surfacecolor=rho,
                colorscale='Viridis',
                colorbar=dict(title='|Ψ|²')
            )
        ])

app = Dash(__name__)

# Initialize visualizer
viz = QuantumVisualizer()

# Layout
app.layout = html.Div([
    html.H1('Quantum State Visualization'),
    
    html.Div([
        html.Label('Principal Quantum Number (n)'),
        dcc.Slider(
            id='n-slider',
            min=1, max=5, value=1,
            marks={i: str(i) for i in range(1, 6)}
        ),
        
        html.Label('Angular Momentum (l)'),
        dcc.Slider(
            id='l-slider',
            min=0, max=4, value=0,
            marks={i: str(i) for i in range(5)}
        ),
        
        html.Label('Magnetic Quantum Number (m)'),
        dcc.Slider(
            id='m-slider',
            min=-2, max=2, value=0,
            marks={i: str(i) for i in range(-2, 3)}
        ),
    ], style={'width': '30%', 'float': 'left'}),
    
    dcc.Graph(
        id='orbital-plot',
        style={'width': '70%', 'float': 'right'}
    ),
])

@app.callback(
    Output('orbital-plot', 'figure'),
    [Input('n-slider', 'value'),
     Input('l-slider', 'value'),
     Input('m-slider', 'value')]
)
def update_plot(n: int, l: int, m: int) -> go.Figure:
    """Update visualization based on quantum numbers"""
    if abs(m) > l or l >= n:
        return go.Figure()  # Invalid quantum numbers
        
    wf = viz.compute_wavefunction(n, l, m)
    return viz.plot_probability_density(wf)

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
