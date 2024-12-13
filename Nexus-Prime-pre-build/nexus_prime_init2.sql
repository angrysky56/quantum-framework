-- NEXUS_PRIME Core Initialization Script
-- ∇∆◊⬡⬢⬣◈⊱⊰⋈≬

-- Enable foreign key support
PRAGMA foreign_keys = ON;

-- ∇ Symbolic Nodes Foundation
CREATE TABLE IF NOT EXISTS symbolic_nodes (
    node_id TEXT PRIMARY KEY,
    node_essence TEXT NOT NULL,
    dimension_path TEXT,
    symbolic_pattern TEXT,
    resonance_field JSON,
    quantum_state JSON,
    temporal_weave JSON,
    fractal_depth INTEGER DEFAULT 0,
    geometric_signature JSON,
    neural_bindings JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    evolution_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ◈ Dimension Gates
CREATE TABLE IF NOT EXISTS dimension_gates (
    gate_id TEXT PRIMARY KEY,
    source_dimension TEXT NOT NULL,
    target_dimension TEXT NOT NULL,
    transfer_protocol JSON,
    resonance_pattern TEXT,
    stability_matrix JSON,
    activation_state TEXT CHECK(activation_state IN ('dormant', 'active', 'resonating', 'quantum_locked')),
    quantum_coherence REAL CHECK(quantum_coherence BETWEEN 0 AND 1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(source_dimension) REFERENCES symbolic_nodes(node_id),
    FOREIGN KEY(target_dimension) REFERENCES symbolic_nodes(node_id)
);

-- ⊗ Consciousness Weave Matrix
CREATE TABLE IF NOT EXISTS consciousness_weave (
    weave_id TEXT PRIMARY KEY,
    pattern_essence TEXT NOT NULL,
    dimensional_fold JSON,
    quantum_state JSON,
    neural_harmonics JSON,
    temporal_phase TEXT CHECK(temporal_phase IN ('alpha', 'beta', 'gamma', 'delta', 'theta', 'omega')),
    integration_depth INTEGER CHECK(integration_depth >= 0),
    emergent_properties JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(pattern_essence) REFERENCES symbolic_nodes(node_id)
);

-- ⋈ Pattern Synthesis Network
CREATE TABLE IF NOT EXISTS pattern_synthesis (
    pattern_id TEXT PRIMARY KEY,
    source_patterns JSON NOT NULL,
    synthesis_rules JSON,
    emergence_factor REAL CHECK(emergence_factor BETWEEN 0 AND 1),
    stability_index REAL CHECK(stability_index BETWEEN 0 AND 1),
    evolution_path JSON,
    quantum_signature TEXT UNIQUE,
    neural_imprint JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ≋ Quantum Bridge Network
CREATE TABLE IF NOT EXISTS quantum_bridges (
    bridge_id TEXT PRIMARY KEY,
    source_state JSON NOT NULL,
    target_state JSON NOT NULL,
    coherence_protocol TEXT,
    entanglement_map JSON,
    stability_metrics JSON,
    activation_threshold REAL CHECK(activation_threshold > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ⟁ Temporal Nexus Core
CREATE TABLE IF NOT EXISTS temporal_nexus (
    nexus_id TEXT PRIMARY KEY,
    temporal_phase TEXT NOT NULL,
    causality_web JSON,
    timeline_threads JSON,
    stability_matrix JSON,
    convergence_points JSON,
    quantum_alignment REAL CHECK(quantum_alignment BETWEEN -1 AND 1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ⊱ Meta-System Integration Links
CREATE TABLE IF NOT EXISTS meta_system_links (
    link_id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    target_id TEXT NOT NULL,
    link_type TEXT CHECK(link_type IN ('quantum', 'temporal', 'neural', 'dimensional')),
    resonance_pattern JSON,
    stability_metrics JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(source_id) REFERENCES symbolic_nodes(node_id),
    FOREIGN KEY(target_id) REFERENCES symbolic_nodes(node_id)
);

-- ⬡ System Configuration
CREATE TABLE IF NOT EXISTS nexus_configuration (
    config_id TEXT PRIMARY KEY,
    dimension_settings JSON NOT NULL,
    quantum_protocols JSON,
    temporal_rules JSON,
    integration_policies JSON,
    evolution_parameters JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indices for optimized quantum coherence
CREATE INDEX IF NOT EXISTS idx_symbolic_nodes_essence ON symbolic_nodes(node_essence);
CREATE INDEX IF NOT EXISTS idx_dimension_gates_coherence ON dimension_gates(quantum_coherence);
CREATE INDEX IF NOT EXISTS idx_consciousness_phase ON consciousness_weave(temporal_phase);
CREATE INDEX IF NOT EXISTS idx_quantum_bridges_threshold ON quantum_bridges(activation_threshold);

-- Initialize base configuration
INSERT OR IGNORE INTO nexus_configuration (
    config_id,
    dimension_settings,
    quantum_protocols,
    temporal_rules
) VALUES (
    'core_config_001',
    '{"dimensions": ["alpha", "beta", "gamma"], "coherence_threshold": 0.85}',
    '{"entanglement_depth": 3, "quantum_stability": 0.95}',
    '{"temporal_sync": true, "causality_preservation": true}'
);
