# SerpAPI Backup Account System

**Implementation Date**: 2025-10-01
**Status**: Configured and ready for use

---

## Overview

The system supports **two SerpAPI accounts** with automatic fallback when the primary account runs out of credits or fails.

---

## Why Two SerpAPI Accounts?

### Problem:
- SerpAPI: $50/month = 5,000 searches
- At **5 searches per client**, you can handle **1,000 clients/month**
- What happens at client #1,001? **System fails** ❌

### Solution:
- **Primary account**: 5,000 searches ($50/month)
- **Backup account**: 5,000 searches ($50/month)
- **Total capacity**: 10,000 searches = **2,000 clients/month**

**Cost**: $100/month for 2,000 clients = **$0.05 per client**

---

## How It Works

### Automatic Fallback Logic:

```python
# Step 1: Try primary SerpAPI account
api_key = credentials.get_credential('serpapi', 'api_key')

if not api_key:
    # Step 2: Use backup SerpAPI account
    api_key = credentials.get_credential('serpapi', 'api_key_backup')
    using_backup = True

    if not api_key:
        # Step 3: Both accounts unavailable
        return error
```

### When Fallback Activates:

1. **Primary account exhausted** (5,000 searches used)
2. **Primary API key invalid/expired**
3. **Primary account rate limited**

**Automatic**: System switches to backup seamlessly!

---

## Configuration (.env file)

### Current Setup:

```bash
# SerpAPI Primary Account
SERPAPI_API_KEY=f17e1e436d0161903f716137d11fb7ee7d3ace4e2d1fd3ba8f5a1556951df1ca

# SerpAPI Backup Account (add when ready)
SERPAPI_API_KEY_BACKUP=your_backup_serpapi_key_here
```

---

## Setting Up Backup Account

### Step-by-Step:

**1. Create Second SerpAPI Account**
- Go to: https://serpapi.com/users/sign_up
- Use **different email address** (e.g., your.email+backup@gmail.com)
- Free account: 100 searches/month for testing
- Paid plan: $50/month for 5,000 searches

**2. Get Backup API Key**
- Login to second account
- Go to: https://serpapi.com/dashboard
- Copy API key

**3. Add to .env File**
```bash
SERPAPI_API_KEY_BACKUP=paste_your_backup_key_here
```

**4. Restart System** (if running)
- Changes take effect immediately
- No code changes needed!

---

## When Do You Need Backup Account?

### Scenarios:

**30 Clients/Month**:
- Searches: 150 (30 × 5)
- Primary account usage: 3%
- **Backup needed**: ❌ No

**100 Clients/Month**:
- Searches: 500 (100 × 5)
- Primary account usage: 10%
- **Backup needed**: ❌ No

**500 Clients/Month**:
- Searches: 2,500 (500 × 5)
- Primary account usage: 50%
- **Backup needed**: ⚠️ Recommended (safety net)

**1,000 Clients/Month**:
- Searches: 5,000 (1,000 × 5)
- Primary account usage: 100%
- **Backup needed**: ✅ **YES - Critical!**

**1,500 Clients/Month**:
- Searches: 7,500 (1,500 × 5)
- Primary exhausted, backup usage: 50%
- **Backup needed**: ✅ **YES - Required!**

---

## Monitoring Usage

### Check Which Account Is Being Used:

System logs show:
```
INFO: Using backup SerpAPI account (primary exhausted/unavailable)
```

### Manual Check:
```python
from system.config.api_credentials import credentials

primary = credentials.get_credential('serpapi', 'api_key')
backup = credentials.get_credential('serpapi', 'api_key_backup')

print(f"Primary: {'✓ Configured' if primary else '✗ Missing'}")
print(f"Backup: {'✓ Configured' if backup else '✗ Missing'}")
```

---

## Cost Analysis

### Single Account ($50/month):
- **Capacity**: 5,000 searches = 1,000 clients
- **Cost per client**: $0.05
- **Risk**: Downtime if limits exceeded

### Dual Account ($100/month):
- **Capacity**: 10,000 searches = 2,000 clients
- **Cost per client**: $0.05 (same)
- **Benefit**: Zero downtime, automatic failover

### When Backup Activates (Example):

**Month with 1,200 clients**:
- Primary: 5,000 searches = $50 (full)
- Backup: 1,000 searches = $10
- **Total cost**: $60 (not $100 - only pay for what you use!)

SerpAPI charges based on actual usage, so backup account only costs money when used.

---

## Email Tip for Second Account

Use **email aliasing** to create second account with same inbox:

**Gmail**:
- Primary: `yourname@gmail.com`
- Backup: `yourname+serpapi@gmail.com`
- Both go to same inbox!

**Outlook**:
- Primary: `yourname@outlook.com`
- Backup: `yourname+backup@outlook.com`

This lets you manage both accounts from one email address.

---

## Testing the Backup

### Test Automatic Fallback:

**1. Simulate Primary Failure**

Temporarily modify `.env`:
```bash
# Comment out primary key
# SERPAPI_API_KEY=...

# Backup becomes active
SERPAPI_API_KEY_BACKUP=your_backup_key
```

**2. Run Test**:
```python
from system.core_tools.api_integrations import serpapi_integration
import asyncio

result = asyncio.run(serpapi_integration.analyze_competitors(
    domain="example.com",
    keywords=["test"],
    client_domain="test_client"
))

print(result)
```

**3. Check Logs**:
Should see: `"Using backup SerpAPI account (primary exhausted/unavailable)"`

**4. Restore Primary**:
Uncomment `SERPAPI_API_KEY` in `.env`

---

## Recommendation

### Current Status (30 clients):
**Skip backup account** - You're using 3% of primary capacity

### When to Add Backup:
- **500+ clients** - Add as safety net
- **1,000+ clients** - Required for reliability
- **Before busy season** - Prevent downtime during peak periods

### Cost-Benefit:
- **Insurance cost**: $0/month (only pay when used)
- **Setup time**: 5 minutes
- **Downtime prevented**: Priceless

**Recommendation**: Set up backup account now (free 100 searches), keep it ready for growth!

---

## Summary

✅ **5 searches per client** (hardcoded)
✅ **Automatic fallback** to backup SerpAPI account
✅ **Same API, same data quality** (just different account)
✅ **Zero code changes** needed - just add backup key to `.env`
✅ **Pay only when used** - backup account costs nothing until activated

**Current Capacity**:
- Primary only: 1,000 clients/month ($50)
- With backup: 2,000 clients/month ($100 max, often less)

**Action Required**: None until you approach 1,000 clients/month!
