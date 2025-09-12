# Library Usage Guide for TEST_SYSTEM Agents

## 🔍 **Key Libraries and Their Agent Usage**

### **📊 ChromaDB (Vector Database & RAG)**
```python
# Line 25-26: chromadb>=0.4.0, sentence-transformers>=2.2.0
```

**Should Agents Use This?** **YES - For Advanced Content Analysis**

#### **ChromaDB Agent Use Cases:**
1. **content_strategist** - Store and search similar content strategies
2. **competitive_intelligence_searcher** - Vector search competitor content
3. **niche_trend_researcher** - Find similar discussions across platforms
4. **keyword_researcher** - Semantic keyword clustering and expansion

#### **How to Use ChromaDB:**
```bash
# Agent instruction for ChromaDB usage:
cd "C:/Apps/Agents/bigger-boss-agent-1/TEST_SYSTEM"
python -c "
import chromadb
from sentence_transformers import SentenceTransformer

# Initialize ChromaDB client
client = chromadb.Client()
collection = client.create_collection('content_analysis')

# Use sentence transformers for embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Store competitor content for semantic search
competitor_content = ['extracted content from Jina AI']
embeddings = model.encode(competitor_content)
collection.add(embeddings=embeddings, documents=competitor_content, ids=['comp1'])

# Semantic search for similar content
query = 'target keyword strategy'
query_embedding = model.encode([query])
results = collection.query(query_embeddings=query_embedding, n_results=5)
print(f'Found {len(results[\"documents\"][0])} similar content pieces')
"
```

### **🕷️ Scrapy (Advanced Web Crawling)**
```python
# Line 21: scrapy>=2.11.0
```

**Should Agents Use This?** **YES - For Systematic Site Crawling**

#### **Scrapy Agent Use Cases:**
1. **technical_seo_analyst** - Crawl entire websites (not just homepage)
2. **competitive_intelligence_searcher** - Systematic competitor site analysis
3. **content_performance_analyst** - Crawl content libraries for analysis

#### **How to Use Scrapy:**
```bash
# Agent instruction for Scrapy usage:
cd "C:/Apps/Agents/bigger-boss-agent-1/TEST_SYSTEM"
python -c "
import scrapy
from scrapy.crawler import CrawlerProcess

class SEOSpider(scrapy.Spider):
    name = 'seo_crawler'
    
    def __init__(self, start_url):
        self.start_urls = [start_url]
    
    def parse(self, response):
        yield {
            'url': response.url,
            'title': response.css('title::text').get(),
            'meta_description': response.css('meta[name=\"description\"]::attr(content)').get(),
            'h1_tags': response.css('h1::text').getall(),
            'status_code': response.status
        }
        
        # Follow internal links
        for link in response.css('a[href]'):
            yield response.follow(link, self.parse)

# Run spider
process = CrawlerProcess({
    'FEEDS': {'seo_data.json': {'format': 'json'}},
    'USER_AGENT': 'DWS-SEO-Agent/1.0'
})
process.crawl(SEOSpider, start_url='TARGET_WEBSITE_URL')
process.start()
"
```

### **🔧 Advertools (SEO Analysis)**
```python
# Line 22: advertools>=0.14.0
```

**Should Agents Use This?** **YES - For Advanced SEO Capabilities**

#### **Advertools Agent Use Cases:**
1. **technical_seo_analyst** - Sitemap analysis, robots.txt analysis
2. **keyword_researcher** - Keyword expansion and clustering
3. **content_performance_analyst** - Search console data analysis

#### **How to Use Advertools:**
```bash
# Agent instruction for Advertools usage:
cd "C:/Apps/Agents/bigger-boss-agent-1/TEST_SYSTEM"
python -c "
import advertools as adv
import pandas as pd

# Sitemap analysis (we don't have this capability currently)
sitemap_df = adv.sitemap_to_df('https://example.com/sitemap.xml')
print(f'Sitemap contains {len(sitemap_df)} URLs')
print(sitemap_df[['loc', 'lastmod', 'changefreq']].head())

# Robots.txt analysis
robots_df = adv.robotstxt_to_df('https://example.com/robots.txt')
print(f'Robots.txt analysis: {robots_df}')

# Keyword expansion
expanded_keywords = adv.kw_generate(['SEO', 'marketing'], ['tools', 'strategy'])
print(f'Generated {len(expanded_keywords)} keyword combinations')
"
```

### **📄 Document Processing Libraries**
```python
# Lines 8-10: PyPDF2, pdfplumber, openpyxl
```

**Should Agents Use This?** **YES - For Real File Processing**

#### **Document Processing Use Cases:**
1. **content_strategist** - Process brand guideline PDFs
2. **keyword_researcher** - Process keyword research Excel files
3. **competitive_intelligence_searcher** - Extract competitor reports

#### **Enhanced Document Processing:**
```bash
# Agent instruction for document processing:
cd "C:/Apps/Agents/bigger-boss-agent-1/TEST_SYSTEM"
python -c "
import pandas as pd
import pdfplumber
import openpyxl

# Real Excel processing (not mock)
if 'keyword_data.xlsx' in uploaded_files:
    df = pd.read_excel('keyword_data.xlsx', sheet_name='Keywords')
    print(f'Processed {len(df)} keywords from Excel file')
    print(df.groupby('search_intent')['search_volume'].sum())

# Real PDF processing (not mock)
if 'brand_guidelines.pdf' in uploaded_files:
    with pdfplumber.open('brand_guidelines.pdf') as pdf:
        brand_colors = []
        for page in pdf.pages:
            text = page.extract_text()
            # Extract actual brand colors, fonts, guidelines
        print(f'Extracted brand guidelines from {len(pdf.pages)} pages')
"
```

### **🌐 Web Automation Libraries**
```python
# Lines 13-19: playwright, beautifulsoup4, requests, httpx
```

**Already Covered** - Agents updated with Playwright MCP and API integration

### **🧠 AI/ML Libraries (Optional but Powerful)**
```python
# Lines 25-26: chromadb, sentence-transformers
# Lines 47-49: google-api-python-client (Google APIs)
```

**Should Agents Use Google APIs?** **YES - For Search Console Data**

#### **Google Search Console Integration:**
```bash
# For SEO agents with Search Console access:
cd "C:/Apps/Agents/bigger-boss-agent-1/TEST_SYSTEM"
python -c "
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# If you have Google Search Console access
# credentials = Credentials.from_service_account_file('service-account.json')
# service = build('searchconsole', 'v1', credentials=credentials)
# 
# # Get actual search performance data
# response = service.searchanalytics().query(
#     siteUrl='https://example.com',
#     body={
#         'startDate': '2025-01-01',
#         'endDate': '2025-01-31',
#         'dimensions': ['query']
#     }
# ).execute()
print('Google Search Console integration ready (requires credentials)')
"
```

## 🎯 **Updated Agent Priorities**

### **High Priority Additions:**
1. **ChromaDB** - Add to content and competitive intelligence agents
2. **Scrapy** - Add to technical SEO and competitive analysis agents  
3. **Advertools** - Add to SEO and keyword research agents

### **Medium Priority:**
1. **Google APIs** - If you have Search Console access
2. **Advanced document processing** - For brand and strategy agents

### **Agent Updates Needed:**
1. **technical_seo_analyst** → Add Scrapy for full site crawling
2. **competitive_intelligence_searcher** → Add ChromaDB for semantic search
3. **keyword_researcher** → Add Advertools for keyword expansion
4. **content_strategist** → Add ChromaDB for content similarity analysis

Would you like me to update specific agents with these library integrations?