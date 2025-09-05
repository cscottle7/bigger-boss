#!/usr/bin/env python3
"""
Comprehensive Page-by-Page SEO Analysis Script for Sydney Coach Charter
This script will systematically analyze all 19 pages identified in the sitemap
"""

import requests
from bs4 import BeautifulSoup
import csv
import json
import time
from urllib.parse import urljoin
import re

# List of all pages from sitemap analysis
PAGES = [
    "https://sydneycoachcharter.com.au/",
    "https://sydneycoachcharter.com.au/about-sydney-coach-charter/",
    "https://sydneycoachcharter.com.au/school-transport-bus-coach-charters/",
    "https://sydneycoachcharter.com.au/school-sporting-transfers/",
    "https://sydneycoachcharter.com.au/about-sydney-coach-charter/our-fleet/",
    "https://sydneycoachcharter.com.au/school-camps/",
    "https://sydneycoachcharter.com.au/school-excursions/",
    "https://sydneycoachcharter.com.au/corporate-bus-and-coach-charters/",
    "https://sydneycoachcharter.com.au/company-transfers/",
    "https://sydneycoachcharter.com.au/conferences-and-meetings/",
    "https://sydneycoachcharter.com.au/company-events/",
    "https://sydneycoachcharter.com.au/airport-and-hotel-transfers/",
    "https://sydneycoachcharter.com.au/conference-support/",
    "https://sydneycoachcharter.com.au/vip-and-guest-bus-and-coach-transfers/",
    "https://sydneycoachcharter.com.au/conference-delegate-transfers/",
    "https://sydneycoachcharter.com.au/contact-sydney-coach-charter/",
    "https://sydneycoachcharter.com.au/about-sydney-coach-charter/testimonials/",
    "https://sydneycoachcharter.com.au/about-sydney-coach-charter/frequently-asked-questions/",
    "https://sydneycoachcharter.com.au/get-a-quote/"
]

def analyze_page(url):
    """Analyze a single page for SEO metrics"""
    try:
        # Add headers to mimic a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract SEO elements
        analysis = {
            'url': url,
            'title': '',
            'meta_description': '',
            'meta_description_length': 0,
            'h1': '',
            'word_count': 0,
            'internal_links': 0,
            'seo_score': 0,
            'key_issues': [],
            'page_load_time': response.elapsed.total_seconds(),
            'mobile_friendly': 'Unknown',
            'status_code': response.status_code
        }
        
        # Title tag
        title_tag = soup.find('title')
        if title_tag:
            analysis['title'] = title_tag.get_text().strip()
        else:
            analysis['key_issues'].append('Missing title tag')
            
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            analysis['meta_description'] = meta_desc.get('content', '').strip()
            analysis['meta_description_length'] = len(analysis['meta_description'])
        else:
            analysis['key_issues'].append('Missing meta description')
            
        # H1 tag
        h1_tags = soup.find_all('h1')
        if h1_tags:
            analysis['h1'] = h1_tags[0].get_text().strip()
            if len(h1_tags) > 1:
                analysis['key_issues'].append('Multiple H1 tags')
        else:
            analysis['key_issues'].append('Missing H1 tag')
            
        # Word count (approximate)
        text_content = soup.get_text()
        words = re.findall(r'\b\w+\b', text_content.lower())
        analysis['word_count'] = len(words)
        
        # Internal links count
        base_domain = 'sydneycoachcharter.com.au'
        internal_links = soup.find_all('a', href=True)
        internal_count = 0
        for link in internal_links:
            href = link['href']
            if base_domain in href or href.startswith('/'):
                internal_count += 1
        analysis['internal_links'] = internal_count
        
        # Mobile friendly check (basic)
        viewport_meta = soup.find('meta', attrs={'name': 'viewport'})
        if viewport_meta:
            analysis['mobile_friendly'] = 'Y'
        else:
            analysis['mobile_friendly'] = 'N'
            analysis['key_issues'].append('No viewport meta tag')
            
        # Calculate SEO Score (1-10 scale)
        score = 10
        if not analysis['title']:
            score -= 2
        if not analysis['meta_description']:
            score -= 2
        if not analysis['h1']:
            score -= 2
        if analysis['meta_description_length'] > 160:
            score -= 1
        if analysis['word_count'] < 300:
            score -= 1
        if len(analysis['key_issues']) > 2:
            score -= 1
            
        analysis['seo_score'] = max(score, 1)
        analysis['key_issues'] = '; '.join(analysis['key_issues']) if analysis['key_issues'] else 'None'
        
        return analysis
        
    except Exception as e:
        return {
            'url': url,
            'title': f'Error: {str(e)}',
            'meta_description': '',
            'meta_description_length': 0,
            'h1': '',
            'word_count': 0,
            'internal_links': 0,
            'seo_score': 1,
            'key_issues': f'Analysis failed: {str(e)}',
            'page_load_time': 0,
            'mobile_friendly': 'Unknown',
            'status_code': 'Error'
        }

def main():
    """Main analysis function"""
    all_results = []
    
    print(f"Starting analysis of {len(PAGES)} pages...")
    
    for i, url in enumerate(PAGES, 1):
        print(f"Analyzing page {i}/{len(PAGES)}: {url}")
        
        result = analyze_page(url)
        all_results.append(result)
        
        # Be respectful to the server
        time.sleep(2)
    
    # Write results to CSV
    csv_filename = 'sydneycoachcharter_comprehensive_seo_analysis.csv'
    
    fieldnames = [
        'URL', 'Page Title', 'Meta Description', 'Meta Description Length',
        'H1 Tag', 'Word Count', 'SEO Score (1-10)', 'Key Issues',
        'Page Load Time', 'Mobile Friendly (Y/N)', 'Internal Links Count'
    ]
    
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for result in all_results:
            writer.writerow({
                'URL': result['url'],
                'Page Title': result['title'],
                'Meta Description': result['meta_description'],
                'Meta Description Length': result['meta_description_length'],
                'H1 Tag': result['h1'],
                'Word Count': result['word_count'],
                'SEO Score (1-10)': result['seo_score'],
                'Key Issues': result['key_issues'],
                'Page Load Time': f"{result['page_load_time']:.2f}s",
                'Mobile Friendly (Y/N)': result['mobile_friendly'],
                'Internal Links Count': result['internal_links']
            })
    
    print(f"Analysis complete! Results saved to {csv_filename}")
    
    # Summary statistics
    total_pages = len(all_results)
    avg_seo_score = sum(r['seo_score'] for r in all_results) / total_pages
    pages_with_issues = sum(1 for r in all_results if r['key_issues'] != 'None')
    
    print(f"\nSUMMARY:")
    print(f"Total pages analyzed: {total_pages}")
    print(f"Average SEO score: {avg_seo_score:.1f}/10")
    print(f"Pages with SEO issues: {pages_with_issues}")
    
    return all_results

if __name__ == "__main__":
    results = main()