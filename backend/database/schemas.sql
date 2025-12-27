-- ============================================
-- CLEANOUT PRO DATABASE SCHEMA
-- PostgreSQL 14+
-- Complete schema for cleanout/junk removal business management
-- ============================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- CUSTOMERS
-- ============================================
CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    address TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_phone ON customers(phone);

-- ============================================
-- JOBS
-- ============================================
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
    job_number VARCHAR(50) UNIQUE NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'draft',
        -- Status: draft, estimated, approved, in_progress, completed, invoiced, paid
    property_address TEXT NOT NULL,
    scheduled_date TIMESTAMP WITH TIME ZONE,
    completed_date TIMESTAMP WITH TIME ZONE,

    -- Pricing fields
    base_estimate DECIMAL(10, 2) DEFAULT 0.00,
    ai_estimate DECIMAL(10, 2) DEFAULT 0.00,
    human_adjusted_estimate DECIMAL(10, 2) DEFAULT 0.00,
    final_price DECIMAL(10, 2) DEFAULT 0.00,

    -- Adjustments tracking
    adjustments JSONB DEFAULT '[]',
    -- Format: [{"type": "stairs", "amount": 50.00, "reason": "3 flights"}]

    -- AI metadata
    ai_confidence FLOAT DEFAULT 0.0,
    ai_processing_time FLOAT DEFAULT 0.0,

    notes TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_jobs_customer ON jobs(customer_id);
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_scheduled ON jobs(scheduled_date);
CREATE INDEX idx_jobs_job_number ON jobs(job_number);

-- ============================================
-- ROOMS
-- ============================================
CREATE TABLE rooms (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    room_number INTEGER NOT NULL,

    -- Image data
    image_url TEXT,
    image_path TEXT,
    thumbnail_url TEXT,

    -- AI Classification
    ai_size_class VARCHAR(50),
        -- Size: small, medium, large, extra_large
    ai_workload_class VARCHAR(50),
        -- Workload: light, moderate, heavy, extreme
    ai_confidence FLOAT DEFAULT 0.0,
    ai_reasoning TEXT,
        -- Stores Ultrathink chain-of-thought

    -- AI Detected Features
    ai_features JSONB DEFAULT '{}',
    -- Format: {
    --   "clutter_density": 0.85,
    --   "accessibility": "difficult",
    --   "stairs_required": true,
    --   "hazmat_present": false,
    --   "salvage_potential": "low",
    --   "item_categories": ["furniture", "boxes", "appliances"]
    -- }

    -- Human Overrides
    human_size_class VARCHAR(50),
    human_workload_class VARCHAR(50),
    human_override_reason TEXT,

    -- Final Classification (AI or Human)
    final_size_class VARCHAR(50) NOT NULL,
    final_workload_class VARCHAR(50) NOT NULL,

    -- Pricing
    estimated_cost DECIMAL(10, 2) DEFAULT 0.00,

    captured_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processed_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_rooms_job ON rooms(job_id);
CREATE INDEX idx_rooms_size_class ON rooms(final_size_class);
CREATE INDEX idx_rooms_workload_class ON rooms(final_workload_class);

-- ============================================
-- INVOICES
-- ============================================
CREATE TABLE invoices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
    invoice_number VARCHAR(50) UNIQUE NOT NULL,

    -- Line items (denormalized for simplicity)
    line_items JSONB DEFAULT '[]',
    -- Format: [
    --   {"description": "Master Bedroom - Large/Heavy", "quantity": 1, "unit_price": 450.00, "total": 450.00},
    --   {"description": "Bin Rental (20 yard)", "quantity": 1, "unit_price": 200.00, "total": 200.00},
    --   {"description": "Stair Fee (3 flights)", "quantity": 1, "unit_price": 75.00, "total": 75.00}
    -- ]

    subtotal DECIMAL(10, 2) NOT NULL,
    tax_rate DECIMAL(5, 4) DEFAULT 0.0000,
    tax_amount DECIMAL(10, 2) DEFAULT 0.00,
    total DECIMAL(10, 2) NOT NULL,

    -- PayPal Integration
    paypal_payment_id VARCHAR(255),
    paypal_payment_status VARCHAR(50),
        -- Status: pending, completed, failed, refunded, cancelled
    paypal_payer_email VARCHAR(255),

    -- Invoice Status
    status VARCHAR(50) NOT NULL DEFAULT 'draft',
        -- Status: draft, sent, viewed, paid, overdue, cancelled

    issued_date TIMESTAMP WITH TIME ZONE,
    due_date TIMESTAMP WITH TIME ZONE,
    paid_date TIMESTAMP WITH TIME ZONE,

    notes TEXT,
    pdf_url TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_invoices_job ON invoices(job_id);
CREATE INDEX idx_invoices_number ON invoices(invoice_number);
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_invoices_paypal_payment ON invoices(paypal_payment_id);

-- ============================================
-- PAYMENT_TRANSACTIONS
-- ============================================
CREATE TABLE payment_transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    invoice_id UUID REFERENCES invoices(id) ON DELETE CASCADE,

    transaction_type VARCHAR(50) NOT NULL,
        -- Type: payment, refund, adjustment
    amount DECIMAL(10, 2) NOT NULL,

    -- PayPal details
    paypal_transaction_id VARCHAR(255) UNIQUE,
    paypal_status VARCHAR(50),
    paypal_response JSONB,

    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_transactions_invoice ON payment_transactions(invoice_id);
CREATE INDEX idx_transactions_paypal ON payment_transactions(paypal_transaction_id);

-- ============================================
-- PRICING_RULES
-- ============================================
CREATE TABLE pricing_rules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    rule_name VARCHAR(255) NOT NULL,
    rule_type VARCHAR(50) NOT NULL,
        -- Type: base_labor, size_multiplier, workload_multiplier, adjustment

    -- Size-based multipliers
    size_class VARCHAR(50),
    size_multiplier DECIMAL(5, 2),

    -- Workload-based multipliers
    workload_class VARCHAR(50),
    workload_multiplier DECIMAL(5, 2),

    -- Flat fees
    flat_fee DECIMAL(10, 2),

    -- Adjustment rules
    condition JSONB,
    -- Format: {"stairs": true, "flights": 3}

    active BOOLEAN DEFAULT TRUE,
    priority INTEGER DEFAULT 0,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_pricing_rules_type ON pricing_rules(rule_type);
CREATE INDEX idx_pricing_rules_active ON pricing_rules(active);

-- ============================================
-- SYNC_QUEUE (For offline mobile sync)
-- ============================================
CREATE TABLE sync_queue (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    device_id VARCHAR(255) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
        -- Type: job, room, image
    entity_id UUID NOT NULL,
    action VARCHAR(50) NOT NULL,
        -- Action: create, update, delete
    payload JSONB NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
        -- Status: pending, processing, completed, failed
    retry_count INTEGER DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_sync_queue_device ON sync_queue(device_id);
CREATE INDEX idx_sync_queue_status ON sync_queue(status);
CREATE INDEX idx_sync_queue_created ON sync_queue(created_at);

-- ============================================
-- AUDIT_LOG
-- ============================================
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(255),
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id UUID,
    changes JSONB,
    ip_address VARCHAR(50),
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_audit_user ON audit_log(user_id);
CREATE INDEX idx_audit_entity ON audit_log(entity_type, entity_id);
CREATE INDEX idx_audit_created ON audit_log(created_at);

-- ============================================
-- UPDATE TRIGGERS
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_customers_updated_at BEFORE UPDATE ON customers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_jobs_updated_at BEFORE UPDATE ON jobs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_rooms_updated_at BEFORE UPDATE ON rooms
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_invoices_updated_at BEFORE UPDATE ON invoices
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_pricing_rules_updated_at BEFORE UPDATE ON pricing_rules
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- SEED DATA: DEFAULT PRICING RULES
-- ============================================

-- Base labor rates
INSERT INTO pricing_rules (rule_name, rule_type, size_class, size_multiplier, workload_class, workload_multiplier) VALUES
('Small Room Base', 'size_multiplier', 'small', 1.0, NULL, NULL),
('Medium Room Base', 'size_multiplier', 'medium', 1.5, NULL, NULL),
('Large Room Base', 'size_multiplier', 'large', 2.0, NULL, NULL),
('Extra Large Room Base', 'size_multiplier', 'extra_large', 3.0, NULL, NULL),

('Light Workload', 'workload_multiplier', NULL, NULL, 'light', 1.0),
('Moderate Workload', 'workload_multiplier', NULL, NULL, 'moderate', 1.3),
('Heavy Workload', 'workload_multiplier', NULL, NULL, 'heavy', 1.6),
('Extreme Workload', 'workload_multiplier', NULL, NULL, 'extreme', 2.0);

-- Flat fees and adjustments
INSERT INTO pricing_rules (rule_name, rule_type, flat_fee, condition) VALUES
('Base Labor Rate', 'base_labor', 150.00, '{}'),
('Bin Rental - 20 yard', 'adjustment', 200.00, '{"type": "bin_rental", "size": "20_yard"}'),
('Bin Rental - 30 yard', 'adjustment', 300.00, '{"type": "bin_rental", "size": "30_yard"}'),
('Stair Fee (per flight)', 'adjustment', 25.00, '{"type": "stairs", "per": "flight"}'),
('Difficult Access', 'adjustment', 75.00, '{"type": "access", "difficulty": "high"}'),
('Hazmat Handling', 'adjustment', 150.00, '{"type": "hazmat"}');

-- ============================================
-- SCHEMA COMPLETE
-- ============================================
