#!/usr/bin/env python3
"""
Multi-page SEO extraction table generator
Creates the table format: URL | Page Title | Title Length | Meta Description | Meta Desc Length | H1 Tag | First 3 H2 Tags
"""

import json
import pandas as pd
from datetime import datetime

def create_seo_extraction_table(crawl_file="analysis_tools/sydneycoachcharter_crawler/fixed_crawl.json"):
    """Create multi-page SEO extraction table from Scrapy results"""
    
    # Read crawl data (JSON array format)
    with open(crawl_file, 'r', encoding='utf-8') as f:
        content = f.read().strip()
        # Remove trailing comma and close bracket if needed
        if content.endswith(','):
            content = content[:-1] + ']'
        elif not content.endswith(']'):
            content = content + ']'
        pages = json.loads(content)
    
    seo_data = []
    
    for page in pages:
        # Clean up H1 and H2 tags (remove newlines and extra spaces)
        h1_clean = page.get('h1_tags', [''])[0].strip().replace('\n', ' ') if page.get('h1_tags') else ''
        h2_tags = [tag.strip().replace('\n', ' ') for tag in page.get('h2_tags', [])]
        first_3_h2 = ' | '.join(h2_tags[:3]) if h2_tags else ''
        
        seo_data.append({
            'URL': page.get('url', ''),
            'Page Title': page.get('title', ''),
            'Title Length': len(page.get('title', '')),
            'Meta Description': page.get('meta_description', ''),
            'Meta Desc Length': len(page.get('meta_description', '')) if page.get('meta_description') else 0,
            'H1 Tag': h1_clean,
            'First 3 H2 Tags': first_3_h2,
            'Page Type': page.get('page_type', ''),
            'Status Code': page.get('status_code', ''),
            'Images Missing Alt': page.get('images_without_alt', 0),
            'Quote Buttons': page.get('quote_buttons', 0)
        })
    
    # Create DataFrame and sort by importance
    df = pd.DataFrame(seo_data)
    
    # Define page importance order
    importance_order = ['homepage', 'contact', 'about', 'services', 'other']
    df['importance'] = df['Page Type'].apply(lambda x: importance_order.index(x) if x in importance_order else 999)
    df = df.sort_values('importance').drop('importance', axis=1)
    
    return df

def generate_seo_table_report(df):
    """Generate markdown report with SEO analysis"""
    
    report = f"""# Multi-Page SEO Extraction Table & Analysis

**Analysis Date**: {datetime.now().strftime('%d/%m/%Y')}  
**Total Pages Analysed**: {len(df)}  
**Data Source**: Real Scrapy web crawling  

## Complete SEO Data Extraction Table

| URL | Page Title | Title Length | Meta Description | Meta Desc Length | H1 Tag | First 3 H2 Tags |
|-----|------------|--------------|------------------|------------------|--------|------------------|
"""
    
    for _, row in df.iterrows():
        # Shorten URL for display
        short_url = row['URL'].replace('https://sydneycoachcharter.com.au', '').replace('/', '') or 'Homepage'
        # Truncate long fields for readability
        title = row['Page Title'][:50] + '...' if len(row['Page Title']) > 50 else row['Page Title']
        meta_desc = row['Meta Description'][:60] + '...' if len(row['Meta Description']) > 60 else row['Meta Description']
        h1 = row['H1 Tag'][:40] + '...' if len(row['H1 Tag']) > 40 else row['H1 Tag']
        h2s = row['First 3 H2 Tags'][:60] + '...' if len(row['First 3 H2 Tags']) > 60 else row['First 3 H2 Tags']
        
        report += f"| {short_url} | {title} | {row['Title Length']} | {meta_desc} | {row['Meta Desc Length']} | {h1} | {h2s} |\n"
    
    # Add analysis summary
    report += f"""

## SEO Analysis Summary

### Title Tag Analysis
- **Average Title Length**: {df['Title Length'].mean():.1f} characters
- **Titles Too Long (>60 chars)**: {len(df[df['Title Length'] > 60])} pages
- **Titles Too Short (<30 chars)**: {len(df[df['Title Length'] < 30])} pages
- **Optimal Length (30-60 chars)**: {len(df[(df['Title Length'] >= 30) & (df['Title Length'] <= 60)])} pages

### Meta Description Analysis
- **Pages with Meta Descriptions**: {len(df[df['Meta Desc Length'] > 0])} / {len(df)}
- **Average Meta Description Length**: {df[df['Meta Desc Length'] > 0]['Meta Desc Length'].mean():.1f} characters
- **Meta Descriptions Too Long (>160 chars)**: {len(df[df['Meta Desc Length'] > 160])} pages
- **Missing Meta Descriptions**: {len(df[df['Meta Desc Length'] == 0])} pages

### Heading Structure Analysis
- **Pages with H1 Tags**: {len(df[df['H1 Tag'] != ''])} / {len(df)}
- **Pages with H2 Tags**: {len(df[df['First 3 H2 Tags'] != ''])} / {len(df)}
- **Missing H1 Tags**: {len(df[df['H1 Tag'] == ''])} pages

### Critical Issues Identified
"""
    
    # Identify specific issues
    issues = []
    
    missing_meta = df[df['Meta Desc Length'] == 0]['URL'].tolist()
    if missing_meta:
        issues.append(f"**Missing Meta Descriptions**: {len(missing_meta)} pages need meta descriptions")
    
    long_titles = df[df['Title Length'] > 60]['URL'].tolist()
    if long_titles:
        issues.append(f"**Long Title Tags**: {len(long_titles)} pages have titles over 60 characters")
    
    missing_h1 = df[df['H1 Tag'] == '']['URL'].tolist()
    if missing_h1:
        issues.append(f"**Missing H1 Tags**: {len(missing_h1)} pages lack H1 headings")
    
    for issue in issues:
        report += f"- {issue}\\n"
    
    if not issues:
        report += "- No critical SEO issues detected in heading and meta tag implementation\\n"
    
    report += f"""

### Key Findings
- **Most Common Page Types**: {df['Page Type'].value_counts().head(3).to_dict()}
- **Average Images per Page**: {df['Images Missing Alt'].mean():.1f} images missing alt text
- **Average Quote Buttons per Page**: {df['Quote Buttons'].mean():.1f}

---

**Data Extraction Method**: Real Scrapy web crawling with comprehensive SEO element parsing  
**Confidence Level**: High (actual HTML extraction, no estimates)  
**Coverage**: {len(df)} pages crawled from website architecture  
"""
    
    return report

def main():
    """Generate complete multi-page SEO extraction"""
    print("Generating Multi-Page SEO Extraction Table...")
    
    # Create SEO extraction table
    df = create_seo_extraction_table()
    
    # Generate report
    report = generate_seo_table_report(df)
    
    # Save results
    df.to_csv("analysis_tools/multi_page_seo_extraction.csv", index=False)
    
    with open("analysis_tools/multi_page_seo_extraction_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"Complete! Analysed {len(df)} pages")
    print("Files created:")
    print("  - analysis_tools/multi_page_seo_extraction.csv")
    print("  - analysis_tools/multi_page_seo_extraction_report.md")
    
    # Show summary
    print(f"\nQuick Summary:")
    print(f"  Pages crawled: {len(df)}")
    print(f"  Missing meta descriptions: {len(df[df['Meta Desc Length'] == 0])}")
    print(f"  Pages with optimal title length: {len(df[(df['Title Length'] >= 30) & (df['Title Length'] <= 60)])}")
    print(f"  Pages missing H1 tags: {len(df[df['H1 Tag'] == ''])}")

if __name__ == "__main__":
    main()