-- Create a table to store FCC callsign data
CREATE TABLE IF NOT EXISTS fcc_callsigns (
    id SERIAL PRIMARY KEY,
    call_sign TEXT NOT NULL,
    unique_system_identifier BIGINT,
    license_status TEXT,
    operator_class TEXT,
    previous_call_sign TEXT,
    previous_operator_class TEXT,
    systematic_call_sign_change TEXT,
    vanity_call_sign_change TEXT,
    vanity_relationship TEXT,
    
    -- Entity (licensee) information
    entity_type TEXT,
    entity_name TEXT,
    first_name TEXT,
    mi TEXT,
    last_name TEXT,
    suffix TEXT,
    
    -- Contact information
    phone TEXT,
    email TEXT,
    street_address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    po_box TEXT,
    
    -- License dates
    grant_date DATE,
    expired_date DATE,
    cancellation_date DATE,
    effective_date DATE,
    last_action_date DATE,
    
    -- Timestamps for our records
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    import_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Create indexes for common search fields
    CONSTRAINT unique_call_sign UNIQUE (call_sign)
);

-- Create indexes for common search patterns
CREATE INDEX IF NOT EXISTS idx_callsigns_unique_system_identifier ON fcc_callsigns (unique_system_identifier);
CREATE INDEX IF NOT EXISTS idx_callsigns_license_status ON fcc_callsigns (license_status);
CREATE INDEX IF NOT EXISTS idx_callsigns_name ON fcc_callsigns (last_name, first_name);
CREATE INDEX IF NOT EXISTS idx_callsigns_entity_name ON fcc_callsigns (entity_name);
CREATE INDEX IF NOT EXISTS idx_callsigns_state ON fcc_callsigns (state);

-- Add a comment to the table
COMMENT ON TABLE fcc_callsigns IS 'Consolidated table of FCC amateur radio callsign data from ULS database'; 