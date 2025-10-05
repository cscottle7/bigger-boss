# MCP Context Window Optimization Guide

**Date**: 30 September 2025
**Status**: Best Practices for Efficient MCP Server Usage
**Target**: Reduce token usage in Playwright and JINA MCP integrations

---

## Executive Summary

**Problem**: MCP servers (Playwright, JINA) can consume large amounts of context window tokens, reducing available space for actual work.

**Solution**: Implement accessibility tree snapshots, optimize tool descriptions, and use efficient data formats to reduce token usage by **60-90%**.

---

## Understanding the Context Window Problem

### Traditional Approach (High Token Usage):
```
Browser Automation → Full HTML DOM → 50,000+ tokens
Image/Screenshot → Base64 encoded → 20,000+ tokens
Verbose tool descriptions → 5,000 tokens per tool
```

### Optimized Approach (Low Token Usage):
```
Browser Automation → Accessibility tree → 2,000-5,000 tokens (90% reduction)
Semantic snapshot → Structured text → 1,000-3,000 tokens
Concise tool descriptions → 500 tokens per tool
```

---

## Part 1: Playwright MCP Optimization

### Current Problem

**Your system uses Playwright MCP** for browser automation which can consume:
- **50,000-100,000 tokens** for full HTML DOM snapshots
- **20,000-40,000 tokens** for screenshot-based approaches
- Results in context exhaustion after 2-3 page interactions

### Solution: Accessibility Tree Approach

**Microsoft's Playwright MCP** already implements this optimization:

#### How It Works:

```yaml
Traditional Approach:
  method: Full HTML DOM parsing
  tokens_per_page: 50,000+
  interactions_possible: 2-3

Accessibility Tree Approach:
  method: Structured accessibility snapshot
  tokens_per_page: 2,000-5,000
  interactions_possible: 15-20
  reduction: 90%
```

### Implementation in Your System

**Current Configuration** (`.claude/mcp-settings.json`):

```json
{
  "mcpServers": {
    "playwright": {
      "command": "node",
      "args": ["path/to/playwright-mcp-server"],
      "env": {
        "PLAYWRIGHT_HEADLESS": "true",
        "PLAYWRIGHT_SNAPSHOT_MODE": "accessibility"  // KEY SETTING
      }
    }
  }
}
```

**Verify Current Mode**:
```bash
# Check your MCP settings
cat .claude/mcp-settings.json | grep SNAPSHOT_MODE
```

### Optimization Techniques

#### 1. Always Use Accessibility Snapshots (Default)

```python
# When using Playwright MCP tools, ensure snapshot mode is set
browser_snapshot_tool_config = {
    "mode": "accessibility",  # Not "html" or "visual"
    "includeMetadata": False,  # Reduces token usage
    "maxDepth": 3  # Limit tree depth
}
```

#### 2. Limit Snapshot Scope

```python
# Instead of full page snapshots
snapshot = await browser.snapshot()  # 50,000 tokens

# Target specific elements
snapshot = await browser.snapshot(
    selector="#main-content",  # Only relevant section
    maxDepth=2  # Limit depth
)  # 2,000 tokens (96% reduction)
```

#### 3. Use Headless Mode

```json
{
  "PLAYWRIGHT_HEADLESS": "true",  // Reduces overhead
  "PLAYWRIGHT_DISABLE_IMAGES": "true",  // Don't load images
  "PLAYWRIGHT_DISABLE_CSS": "false"  // Keep CSS for accessibility tree
}
```

#### 4. Cache Repeated Snapshots

```python
# Bad: Snapshot on every interaction
for url in urls:
    snapshot = await browser.snapshot(url)  # 5,000 tokens × 10 = 50,000 tokens

# Good: Cache static elements
page_structure = await browser.snapshot(url, cacheKey="page_structure")
# Only snapshot dynamic content
dynamic_content = await browser.snapshot("#content-area")  # 500 tokens
```

### Visual Tasks Fallback

**Only use Vision Mode when absolutely necessary:**

```python
# Accessibility Mode (preferred) - 2,000 tokens
accessibility_result = await browser_snapshot(url)

# Vision Mode (fallback) - 20,000 tokens
# Only use for:
# - Captchas
# - Canvas elements
# - Visual verification tasks
visual_result = await browser_screenshot(url, mode="vision")
```

---

## Part 2: JINA MCP Optimization

### Current Problem

**Your system has JINA MCP configured** for:
- Content embeddings and semantic search
- Web scraping and content extraction
- Can consume significant tokens with verbose responses

### Solution: Efficient Data Formats and Deduplication

#### 1. Use Binary/Base64 Encodings for Embeddings

```python
# Bad: Float embeddings (full precision)
embeddings = jina.embed(
    texts=["example text"],
    encoding="float"  # 768 dimensions × 4 bytes = 3,072 bytes per embedding
)

# Good: Binary embeddings (90% smaller)
embeddings = jina.embed(
    texts=["example text"],
    encoding="binary"  # 768 bits = 96 bytes per embedding
)
# Result: 96% size reduction, 5x faster retrieval

# Best: Base64 for transmission
embeddings = jina.embed(
    texts=["example text"],
    encoding="base64"  # Efficient transmission, easy decoding
)
```

#### 2. Batch Processing (Up to 2048 Texts)

```python
# Bad: Individual API calls
results = []
for text in texts:  # 1000 texts
    result = jina.embed([text])  # 1000 API calls, high overhead
    results.append(result)

# Good: Batch processing
results = jina.embed(
    texts=texts[:2048],  # Max 2048 per call
    encoding="binary"
)
# Result: 1 API call, 99.9% overhead reduction
```

#### 3. Use Reader API for Web Content Extraction

```python
# Bad: Full HTML fetch via Playwright
html = await browser.get_html(url)  # 50,000 tokens
cleaned_html = clean_html(html)  # Still 20,000 tokens

# Good: JINA Reader API (markdown conversion)
content = jina.reader(url)  # 2,000-5,000 tokens
# Returns clean markdown with:
# - Main content only
# - No navigation/ads
# - Structured format
```

**Configuration**:
```python
jina_reader_config = {
    "url": "target_url",
    "options": {
        "include_links": False,  # Reduce token usage
        "include_images": False,  # Focus on text
        "max_content_length": 5000  # Limit response size
    }
}
```

#### 4. Deduplication Tools

```python
# Use JINA's built-in deduplication
deduplicated = jina.deduplicate_strings(
    strings=all_content_pieces,
    threshold=0.85  # 85% similarity = duplicate
)
# Result: Reduces redundant content in context
```

---

## Part 3: General MCP Optimization Strategies

### 1. Optimize Tool Descriptions

**Current Issue**: Verbose tool descriptions consume context before work begins

**Bad Example**:
```json
{
  "name": "web_search",
  "description": "This tool performs a comprehensive web search using advanced search algorithms and returns results in a structured format. It can handle various types of queries including keyword searches, phrase searches, and complex boolean queries. The tool supports multiple search engines and can filter results by date, domain, and other criteria. It implements rate limiting to prevent API abuse and includes error handling for network issues. The results are returned in JSON format with detailed metadata including title, URL, snippet, and relevance score. This tool is particularly useful for gathering information from the web, conducting competitive analysis, researching market trends, and discovering new content related to specific topics..."
}
```
**Token Count**: ~500 tokens for ONE tool

**Good Example**:
```json
{
  "name": "web_search",
  "description": "Search the web for query. Returns title, URL, snippet. Supports date/domain filters."
}
```
**Token Count**: ~30 tokens (94% reduction)

### 2. Implement Tool Output Schemas

**New MCP Feature** - Pre-define expected output structure:

```json
{
  "name": "web_search",
  "description": "Search web for query",
  "output_schema": {
    "type": "object",
    "properties": {
      "results": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "title": {"type": "string"},
            "url": {"type": "string"},
            "snippet": {"type": "string"}
          }
        }
      }
    }
  }
}
```

**Benefits**:
- LLM knows output format ahead of time
- Reduces need for verbose explanations
- Enables efficient result parsing
- 30-40% token reduction on tool responses

### 3. Dynamic Context Prioritization

**Implement smart context management**:

```python
class ContextManager:
    """Intelligent context window management"""

    def __init__(self, max_tokens=100000):
        self.max_tokens = max_tokens
        self.context_budget = {
            "system_prompt": 2000,      # 2%
            "tool_descriptions": 5000,   # 5%
            "work_context": 70000,       # 70%
            "response_buffer": 23000     # 23%
        }

    def prioritize_context(self, items):
        """Prioritize what goes into context window"""
        scored_items = []

        for item in items:
            score = self.calculate_relevance(item)
            scored_items.append((score, item))

        # Sort by relevance, keep top items within budget
        scored_items.sort(reverse=True)

        selected = []
        token_count = 0

        for score, item in scored_items:
            item_tokens = self.count_tokens(item)

            if token_count + item_tokens <= self.context_budget["work_context"]:
                selected.append(item)
                token_count += item_tokens
            else:
                break

        return selected

    def calculate_relevance(self, item):
        """Score item relevance (0-1)"""
        # Recent items more relevant
        recency_score = item.age_penalty()

        # More specific items more relevant
        specificity_score = item.specificity()

        # Frequently accessed items more relevant
        frequency_score = item.access_frequency()

        return (recency_score * 0.4 +
                specificity_score * 0.4 +
                frequency_score * 0.2)
```

### 4. Externalized Memory Pattern

**Store context externally, reference by ID**:

```python
# Bad: Full content in context
context = {
    "competitor_analysis": """
    [50,000 tokens of competitor data]
    """,
    "keyword_research": """
    [30,000 tokens of keyword data]
    """
}

# Good: Reference-based context
context = {
    "competitor_analysis_id": "comp_analysis_20250930",
    "keyword_research_id": "kw_research_20250930"
}

# Retrieve only when needed
if needs_competitor_data:
    data = retrieve_from_storage("comp_analysis_20250930")
```

**Implementation**:
```python
class ExternalMemory:
    """External memory for large context items"""

    def __init__(self, storage_path="context_storage/"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)

    def store(self, key: str, content: str) -> str:
        """Store content externally, return reference ID"""
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        storage_id = f"{key}_{content_hash}"

        file_path = self.storage_path / f"{storage_id}.json"
        with open(file_path, 'w') as f:
            json.dump({
                "key": key,
                "content": content,
                "timestamp": datetime.now().isoformat()
            }, f)

        return storage_id

    def retrieve(self, storage_id: str) -> str:
        """Retrieve content by ID"""
        file_path = self.storage_path / f"{storage_id}.json"

        with open(file_path, 'r') as f:
            data = json.load(f)
            return data["content"]

    def summarize(self, storage_id: str) -> str:
        """Return summary instead of full content"""
        content = self.retrieve(storage_id)

        # Create 90% smaller summary
        summary = create_summary(content, max_length=len(content) // 10)
        return summary
```

---

## Part 4: Practical Implementation for Your System

### Configuration Changes Needed

#### 1. Update MCP Settings (`.claude/mcp-settings.json`)

```json
{
  "mcpServers": {
    "playwright": {
      "command": "node",
      "args": ["path/to/playwright-mcp-server"],
      "env": {
        "PLAYWRIGHT_HEADLESS": "true",
        "PLAYWRIGHT_SNAPSHOT_MODE": "accessibility",
        "PLAYWRIGHT_DISABLE_IMAGES": "true",
        "PLAYWRIGHT_MAX_SNAPSHOT_DEPTH": "3"
      }
    },
    "jina": {
      "command": "python",
      "args": ["-m", "jina_mcp_server"],
      "env": {
        "JINA_API_KEY": "${JINA_API_KEY}",
        "JINA_ENCODING_FORMAT": "binary",
        "JINA_MAX_BATCH_SIZE": "2048",
        "JINA_READER_MAX_LENGTH": "5000"
      }
    }
  }
}
```

#### 2. Update Agent Instructions

**Add to `.claude/agents/master_orchestrator.md`:**

```markdown
## MCP Context Window Management

**CRITICAL**: Always use token-efficient MCP operations:

### Browser Automation:
- ✅ Use `browser_snapshot()` with accessibility mode (default)
- ✅ Target specific elements with selectors
- ✅ Cache repeated page structures
- ❌ Avoid full HTML DOM snapshots
- ❌ Avoid screenshots unless visually necessary

### Content Analysis:
- ✅ Use JINA Reader API for web content extraction (2,000-5,000 tokens)
- ✅ Use binary encoding for embeddings (96% smaller)
- ✅ Batch process up to 2,048 texts per call
- ❌ Avoid Playwright HTML fetch for content (50,000+ tokens)

### Token Budget Per Operation:
- Browser snapshot: Max 5,000 tokens
- Content extraction: Max 5,000 tokens
- Embedding generation: Max 1,000 tokens
- Total MCP usage: Max 15% of context window
```

#### 3. Create Context Monitoring

**New File**: `system/monitoring/context_usage_monitor.py`

```python
"""
Context Window Usage Monitor
Tracks token usage and alerts when approaching limits
"""

import logging
from typing import Dict
from datetime import datetime

logger = logging.getLogger(__name__)

class ContextUsageMonitor:
    """Monitor context window token usage"""

    def __init__(self, max_context_window=200000):
        self.max_tokens = max_context_window
        self.usage = {
            "system": 0,
            "tools": 0,
            "mcp_playwright": 0,
            "mcp_jina": 0,
            "work_context": 0,
            "response": 0
        }
        self.alerts = []

    def track_usage(self, category: str, tokens: int):
        """Track token usage by category"""
        self.usage[category] += tokens

        # Check if approaching limit
        total_used = sum(self.usage.values())
        usage_percent = (total_used / self.max_tokens) * 100

        if usage_percent > 75:
            self.alert(f"High context usage: {usage_percent:.1f}%")

    def alert(self, message: str):
        """Log usage alert"""
        self.alerts.append({
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "usage": self.usage.copy()
        })
        logger.warning(f"Context Alert: {message}")

    def get_budget_remaining(self, category: str) -> int:
        """Get remaining token budget for category"""
        budgets = {
            "system": 2000,
            "tools": 5000,
            "mcp_playwright": 10000,
            "mcp_jina": 5000,
            "work_context": 150000,
            "response": 28000
        }

        used = self.usage.get(category, 0)
        budget = budgets.get(category, 0)

        return max(0, budget - used)

    def can_afford(self, category: str, tokens: int) -> bool:
        """Check if operation is within budget"""
        remaining = self.get_budget_remaining(category)
        return tokens <= remaining

    def optimize_for_mcp(self) -> Dict:
        """Get optimization recommendations"""
        recommendations = []

        # Check Playwright usage
        if self.usage["mcp_playwright"] > 10000:
            recommendations.append({
                "tool": "Playwright MCP",
                "issue": "High token usage",
                "suggestion": "Use accessibility snapshots, target specific selectors"
            })

        # Check JINA usage
        if self.usage["mcp_jina"] > 5000:
            recommendations.append({
                "tool": "JINA MCP",
                "issue": "High token usage",
                "suggestion": "Use binary encodings, enable deduplication"
            })

        return {
            "total_usage": sum(self.usage.values()),
            "usage_percent": (sum(self.usage.values()) / self.max_tokens) * 100,
            "recommendations": recommendations
        }


# Global instance
context_monitor = ContextUsageMonitor()
```

---

## Part 5: Testing and Validation

### Test 1: Verify Accessibility Mode

```bash
# Run this test to confirm Playwright uses accessibility snapshots
python system/core_tools/analysis_tools/test_playwright_mode.py
```

**Expected Output**:
```
Testing Playwright snapshot mode...
✓ Snapshot mode: accessibility
✓ Token count: 2,347 (expected <5,000)
✓ Snapshot depth: 3
✓ Context optimization: ENABLED
```

### Test 2: JINA Binary Encoding

```bash
# Test JINA embedding efficiency
python -c "from system.core_tools.enhanced_api_integrations import EnhancedJinaAPIIntegration; jina = EnhancedJinaAPIIntegration(); result = jina.create_embeddings(['test'], encoding='binary'); print('Encoding format:', result.data['encoding']); print('Size reduction:', result.data.get('size_reduction', 'N/A'))"
```

### Test 3: Context Usage Monitoring

```bash
# Monitor context usage during a workflow
python scripts/test_context_monitoring.py --client=test_client_com_au
```

**Expected Output**:
```
Context Usage Report:
- System: 1,234 tokens (1.2%)
- Tools: 3,456 tokens (3.5%)
- MCP Playwright: 4,567 tokens (4.6%)
- MCP JINA: 2,345 tokens (2.3%)
- Work Context: 45,678 tokens (45.7%)
- Response: 10,234 tokens (10.2%)

Total: 67,514 / 200,000 tokens (33.8%)
Status: ✓ Optimal
```

---

## Best Practices Summary

### DO:
✅ Use accessibility tree for browser automation (90% reduction)
✅ Use JINA Reader API for web content (60% reduction)
✅ Use binary encoding for embeddings (96% reduction)
✅ Batch process JINA operations (up to 2,048 items)
✅ Cache repeated snapshots
✅ Target specific elements with selectors
✅ Optimize tool descriptions (reduce to essentials)
✅ Monitor context usage proactively

### DON'T:
❌ Use full HTML DOM snapshots
❌ Use screenshots unless visually necessary
❌ Fetch content via Playwright when JINA Reader works
❌ Use float encodings for embeddings
❌ Make individual API calls for batch operations
❌ Include verbose tool descriptions
❌ Ignore context budget limits

---

## Expected Results

**Before Optimization**:
- Playwright: 50,000 tokens per page
- JINA: 10,000 tokens per embedding batch
- Tool descriptions: 5,000 tokens
- **Total**: 65,000 tokens for basic workflow
- **Pages possible**: 3-4

**After Optimization**:
- Playwright: 3,000 tokens per page (94% reduction)
- JINA: 500 tokens per embedding batch (95% reduction)
- Tool descriptions: 500 tokens (90% reduction)
- **Total**: 4,000 tokens for same workflow
- **Pages possible**: 40-50 (10x improvement)

---

**This guide provides comprehensive strategies for reducing MCP context window usage by 60-90%, enabling significantly more work within the same token budget.**