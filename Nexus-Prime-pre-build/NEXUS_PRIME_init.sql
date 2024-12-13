-- NEXUS_PRIME Initialization Script
-- Symbolic Meta-Architecture Core Structure

-- ∇ Symbolic Nodes
CREATE TABLE symbolic_nodes (
    node_id TEXT PRIMARY KEY,
    node_essence TEXT,
    dimension_path TEXT,
    symbolic_pattern TEXT,
    resonance_field JSON,
    quantum_state JSON,
    temporal_weave JSON,
    fractal_depth INTEGER,
    geometric_signature JSON,
    neural_bindings JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    evolution_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ◈ Dimension Gates
CREATE TABLE dimension_gates (
    gate_id TEXT PRIMARY KEY,
    source_dimension TEXT,
    target_dimension TEXT,
    transfer_protocol JSON,
    resonance_pattern TEXT,
    stability_matrix JSON,
    activation_state TEXT,
    quantum_coherence REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ⊗ Consciousness Weave
CREATE TABLE consciousness_weave (
    weave_id TEXT PRIMARY KEY,
    pattern_essence TEXT,
    dimensional_fold JSON,
    quantum_state JSON,
    neural_harmonics JSON,
    temporal_phase TEXT,
    integration_depth INTEGER,
    emergent_properties JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ⋈ Pattern Synthesis
CREATE TABLE pattern_synthesis (
    pattern_id TEXT PRIMARY KEY,
    source_patterns JSON,
    synthesis_rules JSON,
    emergence_factor REAL,
    stability_index REAL,
    evolution_path JSON,
    quantum_signature TEXT,
    neural_imprint JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ⟁ Quantum Bridges
CREATE TABLE quantum_bridges (
    bridge_id TEXT PRIMARY KEY,
    source_state JSON,
    target_state JSON,
    coherence_protocol TEXT,
    entanglement_map JSON,
    stability_metrics JSON,
    activation_threshold REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ≋ Temporal Nexus
CREATE TABLE temporal_nexus (
    nexus_id TEXT PRIMARY KEY,
    temporal_phase TEXT,
    causality_web JSON,
    timeline_threads JSON,
    stability_matrix JSON,
    convergence_points JSON,
    quantum_alignment REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Meta-System Integration Links
CREATE TABLE meta_system_links (
    link_id TEXT PRIMARY KEY,
    source_id TEXT,
    target_id TEXT,
    link_type TEXT,
    resonance_pattern JSON,
    stability_metrics JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- System Configuration
CREATE TABLE nexus_configuration (
    config_id TEXT PRIMARY KEY,
    dimension_settings JSON,
    quantum_protocols JSON,
    temporal_rules JSON,
    integration_policies JSON,
    evolution_parameters JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
