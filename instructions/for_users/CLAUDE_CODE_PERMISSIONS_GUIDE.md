# CLAUDE CODE PERMISSIONS GUIDE
## For Bigger Boss Agent System

### 🚨 REQUIRED PERMISSIONS

#### **1. MCP Server Access**
```bash
# Essential MCP servers for full functionality
claude mcp add playwright -- cmd /c npx -y @executeautomation/playwright-mcp-server
claude mcp add websearch -- cmd /c npx -y @modelcontextprotocol/server-websearch
```

#### **2. File System Permissions**
- ✅ **Read Access:** All client folders and system directories
- ✅ **Write Access:** Client report generation in `clients/*/` folders  
- ✅ **Execute Access:** Python scripts in `system/` directory

#### **3. Web Access Permissions**
- ✅ **HTTP/HTTPS Requests:** Website crawling and analysis
- ✅ **Browser Automation:** Playwright for real-time data extraction
- ✅ **API Access:** GTmetrix, search engines, competitive intelligence tools
- ✅ **WebFetch Domains:** greenpowersolutions.com.au, precisionuppergisurgery.com.au, sydneycoachcharter.com.au

#### **4. Python Environment Access**
- ✅ **Package Installation:** pip install for required dependencies
- ✅ **Script Execution:** Running custom analysis tools
- ✅ **Async Operations:** AsyncIO for concurrent crawling

### 🎯 CURRENT WORKING SETUP

#### **What's Currently Enabled:**
- ✅ **Basic Website Crawling** - Playwright MCP working
- ✅ **SEO Data Extraction** - Real page titles, meta descriptions, H1s
- ✅ **File System Operations** - Client folder creation and report saving
- ✅ **Python Script Execution** - Custom crawlers operational
- ✅ **Page-by-Page Analysis** - Complete SEO reports generated

#### **What Needs Additional Setup:**
- ⚠️  **Performance Testing APIs** - GTmetrix integration needed
- ⚠️  **Advanced Competitive Analysis** - Additional API keys required
- ⚠️  **Automated Report Distribution** - Email/sharing permissions

### 📋 PERMISSION VERIFICATION COMMANDS

#### **Test MCP Server Access:**
```bash
claude mcp list
# Should show: playwright, websearch (if configured)
```

#### **Test File System Access:**
```bash
python test_crawling.py
# Should create files in clients/ folder
```

#### **Test Web Crawling:**
```bash
python system/core_tools/comprehensive_seo_crawler.py https://sydneycoachcharter.com.au 3
# Should extract real website data
```

### 🔧 PERMISSION TROUBLESHOOTING

#### **If crawling fails:**
1. Check MCP server status: `claude mcp list`
2. Verify Playwright installation: `python -m playwright install`
3. Test basic web access with simple URL fetch

#### **If file operations fail:**
1. Check folder permissions in Windows
2. Verify Claude Code can write to project directory
3. Test with simple file creation script

#### **If Python scripts fail:**
1. Verify Python environment accessible
2. Check all required packages installed: `pip list`
3. Test script execution permissions

### 🎯 RECOMMENDED PERMISSION SETTINGS

#### **For Development Environment:**
```json
{
  "permissions": {
    "file_system": "full_access",
    "web_access": "enabled", 
    "script_execution": "python_only",
    "mcp_servers": ["playwright", "websearch"],
    "working_directories": [
      "C:\\Apps\\Agents\\Bigger Boss\\bigger-boss",
      "C:\\Apps\\Agents\\Bigger Boss\\bigger-boss\\clients"
    ]
  }
}
```

#### **For Production Environment:**
```json
{
  "permissions": {
    "file_system": "project_only",
    "web_access": "whitelist_domains",
    "script_execution": "sandboxed",
    "mcp_servers": ["playwright", "websearch", "performance"],
    "api_access": ["gtmetrix", "google_apis"]
  }
}
```

### 📚 DOCUMENTATION REFERENCES

#### **Official Claude Code Documentation:**
- MCP Server Configuration: https://docs.anthropic.com/en/docs/claude-code/mcp
- Permission Settings: Check Claude Code settings panel
- Tool Integration: See Claude Code developer documentation

#### **System-Specific Documentation:**
- `SYSTEM_IMPLEMENTATION_GUIDE.md` - Complete setup guide
- `test_crawling.py` - Permission verification script
- Client folder structure examples in `clients/` directory

### 🚀 CURRENT SYSTEM STATUS

#### **✅ CONFIRMED WORKING:**
- Real website data extraction
- Page-by-page SEO analysis  
- Tool usage tracking
- Comprehensive audit orchestration
- Natural language crawling interface
- Scrapy-based deep crawling

#### **🔄 READY FOR USE:**
Your Bigger Boss Agent System now has full crawling capabilities with proper permissions. The system can automatically trigger website analysis when agents request it using natural language.

---

*Last updated: 2025-09-05*
*System version: 1.0*