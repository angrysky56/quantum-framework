-- Nexus Prime PORTAL Integration Schema
-- Version: 1.0.0

-- Core PORTAL Registry
CREATE TABLE nexus_portal_registry (
    portal_id TEXT PRIMARY KEY,
    portal_type TEXT NOT NULL,
    portal_config JSON NOT NULL,
    quantum_signature JSON NOT NULL,
    neural_mappings JSON NOT NULL,
    temporal_context JSON NOT NULL,
    activation_state TEXT DEFAULT 'inactive',
    coherence_metrics JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP
);

-- Integration State Registry
CREATE TABLE portal_integration_state (
    state_id TEXT PRIMARY KEY,
    portal_id TEXT NOT NULL,
    integration_phase TEXT NOT NULL,
    quantum_state JSON,
    neural_state JSON,
    temporal_state JSON,
    coherence_metrics JSON,
    state_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (portal_id) REFERENCES nexus_portal_registry(portal_id)
);

-- System Capability Matrix
CREATE TABLE portal_capability_matrix (
    capability_id TEXT PRIMARY KEY,
    portal_id TEXT NOT NULL,
    capability_type TEXT NOT NULL,
    capability_config JSON NOT NULL,
    activation_rules JSON,
    coherence_requirements JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (portal_id) REFERENCES nexus_portal_registry(portal_id)
);

-- Quantum Bridge Configuration
CREATE TABLE portal_quantum_bridge (
    bridge_id TEXT PRIMARY KEY,
    portal_id TEXT NOT NULL,
    bridge_type TEXT NOT NULL,
    quantum_config JSON NOT NULL,
    entanglement_patterns JSON,
    coherence_field JSON,
    stability_metrics JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (portal_id) REFERENCES nexus_portal_registry(portal_id)
);

-- Neural Weave Configuration
CREATE TABLE portal_neural_weave (
    weave_id TEXT PRIMARY KEY,
    portal_id TEXT NOT NULL,
    neural_architecture JSON NOT NULL,
    pattern_mappings JSON NOT NULL,
    learning_configuration JSON,
    adaptation_history JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (portal_id) REFERENCES nexus_portal_registry(portal_id)
);

-- Integration Views
CREATE VIEW v_portal_integration_status AS
SELECT 
    pr.portal_id,
    pr.portal_type,
    pr.activation_state,
    pis.integration_phase,
    pis.coherence_metrics,
    pqb.stability_metrics
FROM nexus_portal_registry pr
LEFT JOIN portal_integration_state pis ON pr.portal_id = pis.portal_id
LEFT JOIN portal_quantum_bridge pqb ON pr.portal_id = pqb.portal_id
WHERE pis.state_timestamp = (
    SELECT MAX(state_timestamp)
    FROM portal_integration_state
    WHERE portal_id = pr.portal_id
);

-- Integration Functions
CREATE FUNCTION initialize_portal_integration(
    p_portal_id TEXT,
    p_portal_type TEXT,
    p_config JSON
) RETURNS TEXT AS $$
DECLARE
    v_integration_id TEXT;
BEGIN
    -- Generate unique integration ID
    v_integration_id := 'INT-' || substr(md5(random()::text), 1, 12);
    
    -- Initialize portal registry entry
    INSERT INTO nexus_portal_registry (
        portal_id,
        portal_type,
        portal_config,
        quantum_signature,
        neural_mappings,
        temporal_context
    ) VALUES (
        p_portal_id,
        p_portal_type,
        p_config->>'base_config',
        p_config->>'quantum_signature',
        p_config->>'neural_mappings',
        p_config->>'temporal_context'
    );
    
    -- Initialize integration state
    INSERT INTO portal_integration_state (
        state_id,
        portal_id,
        integration_phase,
        quantum_state,
        neural_state,
        temporal_state
    ) VALUES (
        v_integration_id,
        p_portal_id,
        'initialization',
        '{}'::json,
        '{}'::json,
        '{}'::json
    );
    
    RETURN v_integration_id;
END;
$$ LANGUAGE plpgsql;

-- Indexes for Performance Optimization
CREATE INDEX idx_portal_integration_portal ON portal_integration_state(portal_id);
CREATE INDEX idx_portal_capability_portal ON portal_capability_matrix(portal_id);
CREATE INDEX idx_quantum_bridge_portal ON portal_quantum_bridge(portal_id);
CREATE INDEX idx_neural_weave_portal ON portal_neural_weave(portal_id);