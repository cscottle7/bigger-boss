-- Bigger Boss Agent System - Database Schema
-- SQLite Database for Tracking Client Operations and API Usage
-- Created: 2025-10-01

-- ============================================================
-- CLIENTS TABLE
-- Track all clients and their engagement with the system
-- ============================================================
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain TEXT UNIQUE NOT NULL,  -- e.g., "drgraemebrown_com_au"
    business_name TEXT,
    industry TEXT,
    location TEXT,  -- e.g., "Sydney, NSW, Australia"
    first_audit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_audit_date TIMESTAMP,
    total_audits INTEGER DEFAULT 0,
    status TEXT DEFAULT 'active',  -- 'active', 'completed', 'archived'
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_clients_domain ON clients(domain);
CREATE INDEX IF NOT EXISTS idx_clients_status ON clients(status);
CREATE INDEX IF NOT EXISTS idx_clients_industry ON clients(industry);

-- ============================================================
-- AUDIT_RESULTS TABLE
-- Track all audits performed for clients
-- ============================================================
CREATE TABLE IF NOT EXISTS audit_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    audit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    audit_type TEXT NOT NULL,  -- 'technical', 'content', 'strategic', 'full'

    -- Performance Scores
    performance_score REAL,  -- 0-100
    seo_score REAL,  -- 0-100
    accessibility_score REAL,  -- 0-100
    content_quality_score REAL,  -- 0-100

    -- Technical Metrics
    pagespeed_score INTEGER,
    lcp_score REAL,  -- Largest Contentful Paint (seconds)
    fid_score REAL,  -- First Input Delay (milliseconds)
    cls_score REAL,  -- Cumulative Layout Shift
    page_size_bytes INTEGER,
    total_requests INTEGER,

    -- File Paths
    report_path TEXT,  -- Path to generated report file
    data_json_path TEXT,  -- Path to raw JSON data

    -- Metadata
    agent_executed TEXT,  -- Which agent performed the audit
    execution_time_seconds INTEGER,
    success BOOLEAN DEFAULT 1,
    error_message TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_audit_results_client ON audit_results(client_id);
CREATE INDEX IF NOT EXISTS idx_audit_results_type ON audit_results(audit_type);
CREATE INDEX IF NOT EXISTS idx_audit_results_date ON audit_results(audit_date);

-- ============================================================
-- API_USAGE TABLE
-- Track all API calls and costs
-- ============================================================
CREATE TABLE IF NOT EXISTS api_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_service TEXT NOT NULL,  -- 'serpapi', 'gtmetrix', 'jina', 'google'
    usage_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    client_id INTEGER,

    -- Usage Metrics
    calls_made INTEGER DEFAULT 1,
    tokens_used INTEGER,  -- For token-based APIs (JINA)
    searches_made INTEGER,  -- For search APIs (SerpAPI)
    tests_run INTEGER,  -- For testing APIs (GTMetrix)

    -- Cost Tracking
    cost_estimate REAL,  -- Estimated cost in USD

    -- Request Details
    endpoint TEXT,  -- Which API endpoint was called
    request_type TEXT,  -- e.g., 'search', 'performance_test', 'embedding'
    status TEXT DEFAULT 'success',  -- 'success', 'error', 'rate_limited'
    error_message TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_api_usage_service ON api_usage(api_service);
CREATE INDEX IF NOT EXISTS idx_api_usage_client ON api_usage(client_id);
CREATE INDEX IF NOT EXISTS idx_api_usage_date ON api_usage(usage_date);
CREATE INDEX IF NOT EXISTS idx_api_usage_status ON api_usage(status);

-- ============================================================
-- AUTOMATION_LOGS TABLE
-- Track all agent executions and system events
-- ============================================================
CREATE TABLE IF NOT EXISTS automation_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    event_type TEXT NOT NULL,  -- 'file_generated', 'agent_executed', 'error', 'api_call', 'automation_run'
    agent_name TEXT,
    client_id INTEGER,

    -- Event Details
    operation TEXT,  -- Specific operation performed
    file_path TEXT,  -- File created/modified
    tool_used TEXT,  -- Which tool was used (Write, Edit, WebFetch, etc.)

    -- Execution Metrics
    execution_time_seconds REAL,
    tokens_used INTEGER,
    success BOOLEAN DEFAULT 1,
    error_message TEXT,

    -- Context
    details TEXT,  -- JSON string with additional details

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_automation_logs_type ON automation_logs(event_type);
CREATE INDEX IF NOT EXISTS idx_automation_logs_agent ON automation_logs(agent_name);
CREATE INDEX IF NOT EXISTS idx_automation_logs_client ON automation_logs(client_id);
CREATE INDEX IF NOT EXISTS idx_automation_logs_timestamp ON automation_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_automation_logs_success ON automation_logs(success);

-- ============================================================
-- PERFORMANCE_METRICS TABLE
-- Track website performance over time
-- ============================================================
CREATE TABLE IF NOT EXISTS performance_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    metric_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Core Web Vitals
    lcp_score REAL,  -- Largest Contentful Paint (seconds)
    fid_score REAL,  -- First Input Delay (milliseconds)
    cls_score REAL,  -- Cumulative Layout Shift

    -- PageSpeed Metrics
    pagespeed_score INTEGER,  -- 0-100
    yslow_score INTEGER,  -- 0-100

    -- Loading Metrics
    fully_loaded_time_ms INTEGER,
    page_load_time_ms INTEGER,
    time_to_first_byte_ms INTEGER,

    -- Size Metrics
    page_size_bytes INTEGER,
    total_requests INTEGER,
    html_size_bytes INTEGER,
    css_size_bytes INTEGER,
    js_size_bytes INTEGER,
    image_size_bytes INTEGER,

    -- Test Configuration
    test_location TEXT DEFAULT 'Sydney, Australia',
    browser TEXT DEFAULT 'Chrome',
    device TEXT DEFAULT 'Desktop',

    -- Data Source
    source TEXT DEFAULT 'gtmetrix',  -- 'gtmetrix', 'lighthouse', 'manual'
    report_url TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_performance_metrics_client ON performance_metrics(client_id);
CREATE INDEX IF NOT EXISTS idx_performance_metrics_date ON performance_metrics(metric_date);

-- ============================================================
-- KEYWORD_RANKINGS TABLE
-- Track keyword rankings over time
-- ============================================================
CREATE TABLE IF NOT EXISTS keyword_rankings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    keyword TEXT NOT NULL,
    ranking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Ranking Data
    position INTEGER,  -- 1-100
    url TEXT,  -- Which page ranks
    previous_position INTEGER,  -- For tracking changes

    -- SERP Features
    has_featured_snippet BOOLEAN DEFAULT 0,
    has_local_pack BOOLEAN DEFAULT 0,
    has_knowledge_panel BOOLEAN DEFAULT 0,

    -- Search Volume (if available)
    monthly_search_volume INTEGER,
    competition_level TEXT,  -- 'low', 'medium', 'high'

    -- Data Source
    source TEXT DEFAULT 'serpapi',  -- 'serpapi', 'manual', 'gsc'

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_keyword_rankings_client ON keyword_rankings(client_id);
CREATE INDEX IF NOT EXISTS idx_keyword_rankings_keyword ON keyword_rankings(keyword);
CREATE INDEX IF NOT EXISTS idx_keyword_rankings_date ON keyword_rankings(ranking_date);

-- ============================================================
-- CONTENT_INVENTORY TABLE
-- Track all content created for clients
-- ============================================================
CREATE TABLE IF NOT EXISTS content_inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    content_type TEXT NOT NULL,  -- 'blog_post', 'service_page', 'pillar_page', 'landing_page'
    title TEXT NOT NULL,
    slug TEXT,

    -- Content Metrics
    word_count INTEGER,
    uniqueness_score REAL,  -- From JINA analysis (0-1)
    readability_score REAL,  -- Flesch reading ease

    -- SEO Metrics
    target_keyword TEXT,
    meta_title TEXT,
    meta_description TEXT,

    -- Status
    status TEXT DEFAULT 'draft',  -- 'draft', 'review', 'published', 'archived'
    published_date TIMESTAMP,

    -- File References
    file_path TEXT,
    google_drive_url TEXT,

    -- Quality Scores (from audits)
    content_quality_score REAL,
    seo_score REAL,
    ai_optimization_score REAL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_content_inventory_client ON content_inventory(client_id);
CREATE INDEX IF NOT EXISTS idx_content_inventory_type ON content_inventory(content_type);
CREATE INDEX IF NOT EXISTS idx_content_inventory_status ON content_inventory(status);
CREATE INDEX IF NOT EXISTS idx_content_inventory_keyword ON content_inventory(target_keyword);

-- ============================================================
-- COMPETITOR_TRACKING TABLE
-- Track competitor analysis over time
-- ============================================================
CREATE TABLE IF NOT EXISTS competitor_tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    competitor_domain TEXT NOT NULL,
    analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Competitive Metrics
    estimated_traffic INTEGER,
    domain_authority INTEGER,
    page_authority INTEGER,
    total_backlinks INTEGER,

    -- Content Metrics
    total_pages INTEGER,
    blog_post_count INTEGER,
    avg_word_count INTEGER,

    -- Ranking Overlap
    shared_keywords INTEGER,  -- How many keywords both rank for
    keywords_we_win INTEGER,
    keywords_they_win INTEGER,

    -- Data Source
    source TEXT DEFAULT 'serpapi',
    data_json_path TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_competitor_tracking_client ON competitor_tracking(client_id);
CREATE INDEX IF NOT EXISTS idx_competitor_tracking_competitor ON competitor_tracking(competitor_domain);
CREATE INDEX IF NOT EXISTS idx_competitor_tracking_date ON competitor_tracking(analysis_date);

-- ============================================================
-- SYSTEM_CONFIGURATION TABLE
-- Track system configuration and settings
-- ============================================================
CREATE TABLE IF NOT EXISTS system_configuration (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    config_key TEXT UNIQUE NOT NULL,
    config_value TEXT,
    config_type TEXT DEFAULT 'string',  -- 'string', 'integer', 'boolean', 'json'
    description TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default configuration
INSERT OR IGNORE INTO system_configuration (config_key, config_value, config_type, description) VALUES
('api_serpapi_monthly_limit', '5000', 'integer', 'Monthly SerpAPI search limit'),
('api_gtmetrix_monthly_limit', '250', 'integer', 'Monthly GTMetrix test limit'),
('api_jina_monthly_token_limit', '1000000', 'integer', 'Monthly JINA token limit'),
('automation_check_interval_minutes', '30', 'integer', 'How often to check for new automation tasks'),
('google_drive_auto_upload', 'true', 'boolean', 'Automatically upload reports to Google Drive'),
('database_backup_frequency_hours', '24', 'integer', 'How often to backup database'),
('system_version', '1.0.0', 'string', 'Current system version');

-- ============================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================

-- Client Performance Overview
CREATE VIEW IF NOT EXISTS v_client_performance_overview AS
SELECT
    c.id,
    c.domain,
    c.business_name,
    c.industry,
    c.total_audits,
    c.last_audit_date,
    (SELECT COUNT(*) FROM content_inventory WHERE client_id = c.id) as total_content,
    (SELECT AVG(performance_score) FROM audit_results WHERE client_id = c.id) as avg_performance,
    (SELECT AVG(seo_score) FROM audit_results WHERE client_id = c.id) as avg_seo_score,
    (SELECT SUM(calls_made) FROM api_usage WHERE client_id = c.id) as total_api_calls,
    (SELECT SUM(cost_estimate) FROM api_usage WHERE client_id = c.id) as total_api_cost
FROM clients c
WHERE c.status = 'active';

-- API Usage Summary by Service
CREATE VIEW IF NOT EXISTS v_api_usage_summary AS
SELECT
    api_service,
    DATE(usage_date) as usage_day,
    COUNT(*) as total_calls,
    SUM(tokens_used) as total_tokens,
    SUM(cost_estimate) as total_cost,
    AVG(cost_estimate) as avg_cost_per_call
FROM api_usage
GROUP BY api_service, DATE(usage_date)
ORDER BY usage_day DESC;

-- Recent Automation Activity
CREATE VIEW IF NOT EXISTS v_recent_automation_activity AS
SELECT
    a.timestamp,
    a.event_type,
    a.agent_name,
    c.domain as client_domain,
    a.operation,
    a.success,
    a.execution_time_seconds
FROM automation_logs a
LEFT JOIN clients c ON a.client_id = c.id
ORDER BY a.timestamp DESC
LIMIT 100;

-- Performance Trends (last 30 days)
CREATE VIEW IF NOT EXISTS v_performance_trends AS
SELECT
    c.domain,
    DATE(pm.metric_date) as test_date,
    pm.pagespeed_score,
    pm.lcp_score,
    pm.cls_score,
    pm.page_size_bytes,
    pm.fully_loaded_time_ms
FROM performance_metrics pm
JOIN clients c ON pm.client_id = c.id
WHERE pm.metric_date >= DATE('now', '-30 days')
ORDER BY c.domain, pm.metric_date DESC;
