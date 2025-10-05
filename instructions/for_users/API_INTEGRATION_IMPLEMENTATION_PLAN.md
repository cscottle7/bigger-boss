# API Integration Implementation Plan

**Date**: 30 September 2025
**Status**: Ready for Implementation
**Environment File**: `.env` configured with API keys

---

## Executive Summary

The system has **existing API integration infrastructure** but the APIs in `.env` are **not currently being used** by the automation workflows. This plan details how to properly integrate these APIs into the marketing automation system.

### Current State Analysis

✅ **API Keys Configured** (verified in `.env`):
- `SERPAPI_API_KEY` - ✓ Set
- `JINA_API_KEY` - ✓ Set
- `GTMETRIX_API_KEY` - ✓ Set
- `DATABASE_URL` - Set to `sqlite:///./test.db`

✅ **Integration Code Exists**:
- `system/config/api_credentials.py` - Credential manager (partially configured)
- `system/core_tools/api_integrations.py` - Basic API integration framework
- `system/core_tools/enhanced_api_integrations.py` - Enhanced API capabilities with JINA support

❌ **Current Problems**:
1. **API credential manager not loading all keys** - Only loads `SERPAPI_KEY` (wrong env var name), not `SERPAPI_API_KEY`
2. **APIs not invoked by automation workflows** - No integration with master_orchestrator or content agents
3. **JINA API partially implemented** but not activated
4. **Database not properly initialized** - Still using placeholder `test.db`
5. **No automatic API usage** in research/analysis workflows

---

## API Capabilities Overview

### 1. SERPAPI (Search Engine Results API)
**Purpose**: Real-time search engine results for competitive analysis
**Capabilities**:
- Google search results with Australian geo-targeting
- Competitor ranking analysis
- Keyword position tracking
- SERP feature extraction (featured snippets, people also ask, etc.)
- Related searches and trending queries

**Use Cases in System**:
- Automated competitive intelligence gathering
- Keyword gap analysis with real SERP data
- Content opportunity identification
- Competitor content strategy analysis
- Search intent analysis based on actual search results

**Pricing**: Free tier: 100 searches/month, Paid: $50/month for 5,000 searches

---

### 2. JINA AI API
**Purpose**: AI-powered embeddings, search, and content understanding
**Capabilities**:
- Text embeddings for semantic search
- Multi-modal search (text, images)
- Content similarity analysis
- Semantic content clustering
- Document understanding and extraction

**Use Cases in System**:
- Content similarity detection (avoid duplicate content)
- Semantic keyword clustering
- Topic modeling and content gap analysis
- Audience persona refinement through content analysis
- Automated content categorization

**Pricing**: Free tier: 1M tokens/month, Paid: $0.02 per 1M tokens

---

### 3. GTMETRIX API
**Purpose**: Website performance testing and Core Web Vitals analysis
**Capabilities**:
- PageSpeed scores
- YSlow scores
- Fully loaded time metrics
- Page size and request analysis
- Waterfall charts
- Core Web Vitals (LCP, FID, CLS)
- Sydney, Australia test location

**Use Cases in System**:
- Automated technical SEO audits
- Performance benchmarking for clients
- Competitor performance comparison
- Before/after optimization tracking
- Technical audit report generation

**Pricing**: Free tier: 10 tests/day (300/month), Paid: $14.95/month for 20 tests/day

---

## Current Integration Architecture Analysis

### Existing Components

#### 1. API Credential Manager (`system/config/api_credentials.py`)
**Current Issues**:
```python
# Line 38: Looking for wrong environment variable name
'serpapi': {
    'api_key': os.getenv('SERPAPI_KEY')  # ❌ Should be 'SERPAPI_API_KEY'
},
```

**Missing APIs**:
- No JINA_API_KEY loading
- No proper DATABASE_URL configuration

#### 2. Basic API Integrations (`system/core_tools/api_integrations.py`)
**Status**: ✅ Implemented but not activated
**Features**:
- GTMetrix integration with rate limiting
- SerpAPI competitive analysis
- Automatic report generation to `clients/{domain}/research/` and `clients/{domain}/technical/`
- Autonomous operation manager integration

**Problem**: Not invoked by any automation workflows

#### 3. Enhanced API Integrations (`system/core_tools/enhanced_api_integrations.py`)
**Status**: ✅ Partially implemented with JINA support
**Features**:
- EnhancedSerpAPIIntegration class
- JinaAIIntegration class (exists)
- ChromaVectorStore integration
- Standardized APIIntegrationResult dataclass

**Problem**: Not integrated with master_orchestrator or research workflows

---

## Implementation Roadmap

### Phase 1: Fix API Credential Loading (15 minutes)

**File**: `system/config/api_credentials.py`

**Changes Needed**:

```python
# Lines 32-44: Update environment variable mappings
env_credentials = {
    'gtmetrix': {
        'api_key': os.getenv('GTMETRIX_API_KEY'),  # Fixed: was correct
        'username': os.getenv('GTMETRIX_USERNAME')   # May not be needed
    },
    'serpapi': {
        'api_key': os.getenv('SERPAPI_API_KEY')  # FIXED: Was SERPAPI_KEY
    },
    'jina': {  # NEW: Add Jina AI credentials
        'api_key': os.getenv('JINA_API_KEY')
    },
    'google': {
        'api_key': os.getenv('GOOGLE_API_KEY'),
        'cse_id': os.getenv('GOOGLE_CSE_ID')
    }
}
```

**Testing**:
```bash
python -c "from system.config.api_credentials import credentials; print('SerpAPI:', credentials.has_service_credentials('serpapi')); print('JINA:', credentials.has_service_credentials('jina')); print('GTMetrix:', credentials.has_service_credentials('gtmetrix'))"
```

**Expected Output**:
```
SerpAPI: True
JINA: True
GTMetrix: True
```

---

### Phase 2: Integrate APIs into Research Workflows (30 minutes)

**Objective**: Make master_orchestrator automatically use APIs during research phases

#### Option A: Direct Integration (Recommended)

**File**: `.claude/agents/master_orchestrator.md`

**Add to Phase 2 - Competitive Intelligence section** (around line 250):

```markdown
### Automated API-Powered Competitive Analysis

**BEFORE writing competitive_analysis.md, USE THESE APIS:**

1. **SerpAPI Competitor Research**:
   ```python
   from system.core_tools.api_integrations import serpapi_integration

   # Get top keywords for client's niche
   keywords = ["primary keyword", "secondary keyword", "industry + location"]

   result = await serpapi_integration.analyze_competitors(
       domain=client_domain,
       keywords=keywords,
       client_domain=client_domain
   )

   # Result saved automatically to: clients/{domain}/research/competitive_analysis_{timestamp}.json
   ```

2. **GTMetrix Performance Analysis**:
   ```python
   from system.core_tools.api_integrations import gtmetrix_api

   result = await gtmetrix_api.test_website_performance(
       url=f"https://{client_domain.replace('_', '.')}",
       client_domain=client_domain
   )

   # Result saved automatically to: clients/{domain}/technical/gtmetrix_performance_report_{timestamp}.json
   ```

**THEN**: Use API results to write comprehensive competitive_analysis.md
```

#### Option B: Create API Research Agent

**New File**: `.claude/agents/api_research_specialist.md`

```markdown
# API Research Specialist Agent

You are an API Research Specialist that uses external APIs to gather real-time competitive intelligence and performance data.

## Your Capabilities

You have access to:
1. **SerpAPI** - Real-time search engine results
2. **GTMetrix API** - Website performance testing
3. **JINA AI** - Content similarity and semantic analysis

## When to Use APIs

- **SerpAPI**: When analyzing competitor rankings, keyword positions, SERP features
- **GTMetrix**: When conducting technical SEO audits or performance benchmarking
- **JINA**: When analyzing content similarity, clustering keywords, or detecting duplicate content

## API Usage Protocol

[Integration instructions]
```

---

### Phase 3: Activate GTMetrix in Technical Audits (20 minutes)

**File**: `.claude/agents/technical_seo_analyst.md` (if exists) or `master_orchestrator.md`

**Add to technical audit workflow**:

```markdown
### Performance Testing with GTMetrix API

**MANDATORY**: Run GTMetrix performance test for every technical audit:

```python
from system.core_tools.api_integrations import gtmetrix_api
import asyncio

result = asyncio.run(gtmetrix_api.test_website_performance(
    url="https://client-website.com.au",
    client_domain="client_website_com_au"
))

if result['status'] == 'success':
    scores = result['performance_scores']
    # Use these metrics in technical_audit.md:
    # - PageSpeed Score: {scores['pagespeed_score']}
    # - YSlow Score: {scores['yslow_score']}
    # - Fully Loaded Time: {scores['fully_loaded_time']}ms
    # - Page Size: {scores['page_size']} bytes
    # - Total Requests: {scores['requests']}
```

**Benefits**:
- Real performance data instead of estimates
- Competitor benchmarking
- Track improvements over time
```

---

### Phase 4: Implement JINA AI Content Analysis (45 minutes)

**Purpose**: Prevent content duplication and improve content strategy

**New File**: `system/core_tools/jina_content_analyzer.py`

```python
"""
JINA AI Content Analysis Integration
Provides semantic content analysis, similarity detection, and clustering
"""

import os
import requests
import json
import logging
from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

class JinaContentAnalyzer:
    """JINA AI integration for content analysis"""

    def __init__(self):
        self.api_key = os.getenv('JINA_API_KEY')
        self.base_url = "https://api.jina.ai/v1"

        if not self.api_key:
            logger.warning("JINA API key not configured")

    def generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate text embedding using JINA"""
        if not self.api_key:
            return None

        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }

            payload = {
                'input': text,
                'model': 'jina-embeddings-v2-base-en'
            }

            response = requests.post(
                f"{self.base_url}/embeddings",
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                return data['data'][0]['embedding']
            else:
                logger.error(f"JINA API error: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"JINA embedding generation failed: {e}")
            return None

    def calculate_similarity(self, text1: str, text2: str) -> Optional[float]:
        """Calculate semantic similarity between two texts"""

        embedding1 = self.generate_embedding(text1)
        embedding2 = self.generate_embedding(text2)

        if not embedding1 or not embedding2:
            return None

        # Calculate cosine similarity
        import numpy as np
        similarity = np.dot(embedding1, embedding2) / (
            np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
        )

        return float(similarity)

    def check_content_uniqueness(self, new_content: str, client_domain: str) -> Dict:
        """Check if content is unique compared to existing client content"""

        client_folder = Path(f"clients/{client_domain}/content")

        if not client_folder.exists():
            return {
                'status': 'success',
                'is_unique': True,
                'message': 'No existing content to compare against'
            }

        similarities = []

        # Check against existing markdown files
        for content_file in client_folder.glob("*.md"):
            try:
                existing_content = content_file.read_text(encoding='utf-8')
                similarity = self.calculate_similarity(new_content, existing_content)

                if similarity and similarity > 0.85:  # 85% similarity threshold
                    similarities.append({
                        'file': content_file.name,
                        'similarity': similarity
                    })
            except Exception as e:
                logger.warning(f"Could not compare with {content_file}: {e}")

        if similarities:
            return {
                'status': 'warning',
                'is_unique': False,
                'similar_content': similarities,
                'message': f'Content is {similarities[0]["similarity"]*100:.1f}% similar to existing content'
            }

        return {
            'status': 'success',
            'is_unique': True,
            'message': 'Content is unique'
        }

    def cluster_keywords(self, keywords: List[str]) -> Dict:
        """Cluster keywords by semantic similarity"""

        if not keywords or not self.api_key:
            return {'status': 'error', 'clusters': []}

        try:
            # Generate embeddings for all keywords
            embeddings = []
            for keyword in keywords:
                embedding = self.generate_embedding(keyword)
                if embedding:
                    embeddings.append({
                        'keyword': keyword,
                        'embedding': embedding
                    })

            if not embeddings:
                return {'status': 'error', 'clusters': []}

            # Simple clustering using similarity threshold
            from sklearn.cluster import DBSCAN
            import numpy as np

            X = np.array([e['embedding'] for e in embeddings])
            clustering = DBSCAN(eps=0.3, min_samples=2, metric='cosine').fit(X)

            clusters = {}
            for idx, label in enumerate(clustering.labels_):
                if label not in clusters:
                    clusters[label] = []
                clusters[label].append(embeddings[idx]['keyword'])

            return {
                'status': 'success',
                'num_clusters': len(clusters),
                'clusters': [
                    {
                        'cluster_id': k,
                        'keywords': v,
                        'primary_keyword': v[0] if v else None
                    }
                    for k, v in clusters.items()
                    if k != -1  # Exclude noise points
                ]
            }

        except Exception as e:
            logger.error(f"Keyword clustering failed: {e}")
            return {'status': 'error', 'error': str(e)}


# Global instance
jina_analyzer = JinaContentAnalyzer()
```

**Usage in Content Workflow**:

Add to `content_generator` agent or `master_orchestrator`:

```python
# Before generating content
from system.core_tools.jina_content_analyzer import jina_analyzer

# Check uniqueness
uniqueness_check = jina_analyzer.check_content_uniqueness(
    new_content=generated_content,
    client_domain=client_domain
)

if not uniqueness_check['is_unique']:
    # Flag for human review or regenerate
    logger.warning(f"Content similarity detected: {uniqueness_check['message']}")
```

---

### Phase 5: Database Setup and Migration (30 minutes)

**Current State**: `DATABASE_URL=sqlite:///./test.db` (placeholder)

**Decision Point**: SQLite vs PostgreSQL

#### Option A: SQLite (Recommended for Single-User)
**Pros**: No setup required, file-based, simple
**Cons**: Limited concurrency, not suitable for multi-user

**Configuration**:
```bash
# .env file
DATABASE_URL=sqlite:///./bigger_boss.db
```

#### Option B: PostgreSQL (Recommended for Production/Multi-User)
**Pros**: Better concurrency, full-featured, scalable
**Cons**: Requires PostgreSQL installation and setup

**Setup Steps**:
1. Install PostgreSQL
2. Create database:
   ```sql
   CREATE DATABASE bigger_boss_db;
   CREATE USER bigger_boss_user WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE bigger_boss_db TO bigger_boss_user;
   ```
3. Update `.env`:
   ```bash
   DATABASE_URL=postgresql://bigger_boss_user:secure_password@localhost:5432/bigger_boss_db
   ```

#### Database Schema Design

**Tables Needed**:

```sql
-- Client projects tracking
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    domain VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'active'
);

-- Audit results storage
CREATE TABLE audit_results (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES clients(id),
    audit_type VARCHAR(100) NOT NULL,  -- 'pre_delivery', 'technical', 'seo', etc.
    compliance_score DECIMAL(5,2),
    results JSONB,  -- Full audit results
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- API usage tracking
CREATE TABLE api_usage (
    id SERIAL PRIMARY KEY,
    service VARCHAR(50) NOT NULL,  -- 'serpapi', 'jina', 'gtmetrix'
    client_id INTEGER REFERENCES clients(id),
    request_type VARCHAR(100),
    cost_estimate DECIMAL(10,4),
    response_time_ms INTEGER,
    success BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Automation activity log
CREATE TABLE automation_logs (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES clients(id),
    workflow_type VARCHAR(100),  -- 'audit', 'conversion', 'upload'
    status VARCHAR(50),
    duration_seconds INTEGER,
    files_processed INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Performance metrics over time
CREATE TABLE performance_metrics (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES clients(id),
    metric_type VARCHAR(100),  -- 'gtmetrix', 'lighthouse', etc.
    scores JSONB,  -- PageSpeed, YSlow, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Migration Script** (`scripts/database/migrate_to_db.py`):

```python
"""
Database Migration Script
Migrates existing JSON activity logs to database
"""

import json
import psycopg2
from pathlib import Path
from datetime import datetime

def migrate_client_activity_logs():
    """Migrate client activity JSON files to database"""

    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cur = conn.cursor()

    # Scan for client activity logs
    activity_dir = Path('logs/client_activity')

    for activity_file in activity_dir.glob('*_automation_activity.json'):
        try:
            with open(activity_file, 'r') as f:
                data = json.load(f)

            client_domain = data['client_domain']

            # Insert client if not exists
            cur.execute("""
                INSERT INTO clients (domain, created_at)
                VALUES (%s, %s)
                ON CONFLICT (domain) DO NOTHING
                RETURNING id
            """, (client_domain, datetime.now()))

            result = cur.fetchone()
            if result:
                client_id = result[0]
            else:
                cur.execute("SELECT id FROM clients WHERE domain = %s", (client_domain,))
                client_id = cur.fetchone()[0]

            # Insert automation logs
            for workflow in data.get('workflows', []):
                cur.execute("""
                    INSERT INTO automation_logs
                    (client_id, workflow_type, status, duration_seconds, files_processed, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    client_id,
                    'full_automation',
                    workflow.get('status'),
                    workflow.get('duration_seconds'),
                    workflow.get('phases', {}).get('conversion', {}).get('files_converted', 0),
                    datetime.fromisoformat(workflow.get('timestamp'))
                ))

            conn.commit()
            print(f"✓ Migrated {activity_file.name}")

        except Exception as e:
            print(f"✗ Failed to migrate {activity_file.name}: {e}")
            conn.rollback()

    cur.close()
    conn.close()
    print("\nMigration complete!")

if __name__ == '__main__':
    migrate_client_activity_logs()
```

---

## Testing Strategy

### Phase 1: API Credential Testing

```bash
# Test 1: Verify credential loading
python -c "from system.config.api_credentials import credentials; \
print('SerpAPI:', credentials.has_service_credentials('serpapi')); \
print('JINA:', credentials.has_service_credentials('jina')); \
print('GTMetrix:', credentials.has_service_credentials('gtmetrix'))"

# Expected: All True
```

### Phase 2: API Integration Testing

```bash
# Test 2: SerpAPI search test
python system/core_tools/analysis_tools/test_api_integrations.py --service=serpapi

# Test 3: GTMetrix performance test
python system/core_tools/analysis_tools/test_api_integrations.py --service=gtmetrix

# Test 4: JINA content analysis test
python -c "from system.core_tools.jina_content_analyzer import jina_analyzer; \
result = jina_analyzer.calculate_similarity('SEO services Sydney', 'Sydney SEO agency'); \
print(f'Similarity: {result}')"

# Expected: Similarity score between 0.7-0.9
```

### Phase 3: End-to-End Workflow Testing

```bash
# Test 5: Full automation with API integration
python scripts/emergency_automation_fix.py --client=test_client_com_au --use-apis

# Expected:
# - SerpAPI competitive analysis generated
# - GTMetrix performance report generated
# - JINA content uniqueness check passed
# - All files converted and uploaded
```

---

## Cost Estimation & Rate Limits

### Monthly API Costs (Projected)

**Assuming 10 clients per month:**

| API | Free Tier | Cost/Client | Monthly Cost |
|-----|-----------|-------------|--------------|
| **SerpAPI** | 100 searches/mo | 5 searches | Free (50 searches) |
| **JINA AI** | 1M tokens/mo | 50K tokens | Free |
| **GTMetrix** | 300 tests/mo | 2 tests | Free (20 tests) |
| **Total** | - | - | **$0/month** (within free tiers) |

**At scale (100 clients/month):**

| API | Usage | Cost |
|-----|-------|------|
| **SerpAPI** | 500 searches | $50/month (5,000 search plan) |
| **JINA AI** | 500K tokens | Free (under 1M limit) |
| **GTMetrix** | 200 tests | $14.95/month (600 test plan) |
| **Total** | - | **$64.95/month** |

### Rate Limiting Strategy

**Already Implemented** in `api_integrations.py`:
- GTMetrix: 10 requests/minute (LimiterSession)
- SerpAPI: 60 requests/minute
- Automatic retry with exponential backoff
- Session tracking to prevent overuse

---

## Benefits After Implementation

### Immediate Benefits

1. **Real Competitive Data**: Actual search rankings instead of estimates
2. **Performance Benchmarking**: Real GTMetrix scores for technical audits
3. **Content Uniqueness**: Prevent duplicate content with JINA analysis
4. **Automated Intelligence**: No manual research needed

### Long-Term Benefits

1. **Historical Tracking**: Database stores performance over time
2. **ROI Measurement**: Track improvements with real metrics
3. **Competitive Edge**: Real-time market intelligence
4. **Scalability**: APIs handle volume as client base grows

---

## Implementation Checklist

- [ ] **Phase 1**: Fix `api_credentials.py` (change SERPAPI_KEY → SERPAPI_API_KEY, add JINA)
- [ ] **Phase 2**: Add API usage to `master_orchestrator.md` research phases
- [ ] **Phase 3**: Activate GTMetrix in technical audit workflow
- [ ] **Phase 4**: Create `jina_content_analyzer.py` and integrate
- [ ] **Phase 5**: Choose database (SQLite or PostgreSQL) and run migration
- [ ] **Testing**: Run all 5 test cases
- [ ] **Documentation**: Update USER_MANUAL.md with API usage instructions
- [ ] **Monitoring**: Set up API usage tracking and alerts

---

## Quick Start Commands

```bash
# 1. Fix API credentials
# Edit system/config/api_credentials.py (line 38)

# 2. Test API connections
python system/core_tools/analysis_tools/test_api_integrations.py

# 3. Run first API-powered workflow
python scripts/emergency_automation_fix.py --client=test_client_com_au --enable-apis

# 4. Check API usage logs
cat logs/api_usage.log

# 5. Verify database setup
python scripts/database/verify_db.py
```

---

## Next Steps

1. **Review this plan** and decide on database choice (SQLite vs PostgreSQL)
2. **Implement Phase 1** (credential fixes) - 15 minutes
3. **Test API connections** - 10 minutes
4. **Implement Phases 2-3** (integrate into workflows) - 50 minutes
5. **Optional: Implement Phase 4** (JINA content analysis) - 45 minutes
6. **Optional: Implement Phase 5** (database setup) - 30 minutes

**Total Implementation Time**: 2-3 hours for full integration

---

**This plan provides a complete roadmap for activating all configured APIs and integrating them into the marketing automation workflows, with real-time competitive intelligence, performance testing, and content analysis capabilities.**