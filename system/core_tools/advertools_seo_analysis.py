#!/usr/bin/env python3
"""
Comprehensive SEO analysis using Advertools for Sydney Coach Charter
Real SEO data extraction and analysis
"""

import advertools as adv
import pandas as pd
import json
from datetime import datetime
import requests
from urllib.parse import urljoin, urlparse

class AdvertoolsSEOAnalyzer:
    def __init__(self):
        self.base_url = "https://sydneycoachcharter.com.au"
        self.results = {}
        
    def comprehensive_seo_analysis(self):
        """Run comprehensive SEO analysis using Advertools"""
        print("=== COMPREHENSIVE ADVERTOOLS SEO ANALYSIS ===")
        
        # 1. Sitemap Analysis
        sitemap_data = self.analyze_sitemap()
        
        # 2. Robots.txt Analysis  
        robots_data = self.analyze_robots_txt()
        
        # 3. On-page SEO Analysis
        onpage_data = self.analyze_onpage_seo()
        
        # 4. Technical SEO Analysis
        technical_data = self.analyze_technical_seo()
        
        # 5. Content Analysis
        content_data = self.analyze_content()
        
        # 6. Local SEO Analysis
        local_seo_data = self.analyze_local_seo()
        
        # 7. Schema Markup Analysis
        schema_data = self.analyze_schema_markup()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'base_url': self.base_url,
            'sitemap_analysis': sitemap_data,
            'robots_analysis': robots_data,
            'onpage_analysis': onpage_data,
            'technical_analysis': technical_data,
            'content_analysis': content_data,
            'local_seo_analysis': local_seo_data,
            'schema_analysis': schema_data
        }
    
    def analyze_sitemap(self):
        """Analyze XML sitemap using Advertools"""
        print("Analyzing XML sitemap...")
        try:
            sitemap_url = urljoin(self.base_url, '/sitemap.xml')
            sitemap_df = adv.sitemap_to_df(sitemap_url)
            
            if not sitemap_df.empty:
                analysis = {
                    'sitemap_url': sitemap_url,
                    'total_urls': len(sitemap_df),
                    'url_breakdown': sitemap_df['loc'].tolist()[:20],  # First 20 URLs
                    'has_lastmod': 'lastmod' in sitemap_df.columns,
                    'has_changefreq': 'changefreq' in sitemap_df.columns,
                    'has_priority': 'priority' in sitemap_df.columns,
                }
                
                if 'lastmod' in sitemap_df.columns:
                    analysis['last_modified_dates'] = sitemap_df['lastmod'].dropna().tolist()[:10]
                
                return analysis
            else:
                return {'error': 'Sitemap found but empty or unreadable'}
                
        except Exception as e:
            return {'error': f'Sitemap analysis failed: {str(e)}'}
    
    def analyze_robots_txt(self):
        """Analyze robots.txt file"""
        print("Analyzing robots.txt...")
        try:
            robots_url = urljoin(self.base_url, '/robots.txt')
            robots_df = adv.robotstxt_to_df(robots_url)
            
            if not robots_df.empty:
                return {
                    'robots_url': robots_url,
                    'directives_count': len(robots_df),
                    'directives': robots_df.to_dict('records'),
                    'user_agents': robots_df['user_agent'].unique().tolist() if 'user_agent' in robots_df.columns else [],
                    'has_sitemap': any('sitemap' in str(directive).lower() for directive in robots_df.get('directive', []))
                }
            else:
                return {'error': 'Robots.txt found but empty or unreadable'}
                
        except Exception as e:
            return {'error': f'Robots.txt analysis failed: {str(e)}'}
    
    def analyze_onpage_seo(self):
        """Analyze on-page SEO elements"""
        print("Analyzing on-page SEO...")
        try:
            # URLs to analyze
            urls_to_crawl = [
                self.base_url,
                urljoin(self.base_url, '/contact-sydney-coach-charter/'),
                urljoin(self.base_url, '/about-sydney-coach-charter/'),
                urljoin(self.base_url, '/corporate-bus-and-coach-charters/'),
                urljoin(self.base_url, '/wedding-celebration-bus-and-coach-charters/')
            ]
            
            # Crawl URLs for SEO analysis
            crawl_df = adv.crawl(urls_to_crawl, 
                               follow_links=False, 
                               custom_settings={
                                   'USER_AGENT': 'AdvertoolsSEOAnalyzer/1.0',
                                   'DOWNLOAD_DELAY': 1
                               })
            
            if not crawl_df.empty:
                analysis = {
                    'pages_analyzed': len(crawl_df),
                    'page_analysis': []
                }
                
                for _, row in crawl_df.iterrows():
                    page_analysis = {
                        'url': row.get('url', ''),
                        'title': row.get('title', ''),
                        'title_length': len(row.get('title', '')) if row.get('title') else 0,
                        'meta_desc': row.get('meta_desc', ''),
                        'meta_desc_length': len(row.get('meta_desc', '')) if row.get('meta_desc') else 0,
                        'h1': row.get('h1', []),
                        'h2': row.get('h2', []),
                        'h3': row.get('h3', []),
                        'status_code': row.get('status', 0),
                        'redirect': row.get('redirect_urls', []),
                        'canonical': row.get('canonical', ''),
                        'og_title': row.get('og:title', ''),
                        'og_description': row.get('og:description', ''),
                        'og_image': row.get('og:image', ''),
                        'twitter_card': row.get('twitter:card', ''),
                        'lang': row.get('lang', ''),
                        'charset': row.get('charset', ''),
                        'viewport': row.get('viewport', ''),
                        'body_text_length': len(str(row.get('body_text', '')))
                    }
                    analysis['page_analysis'].append(page_analysis)
                
                return analysis
            else:
                return {'error': 'No pages could be crawled for on-page analysis'}
                
        except Exception as e:
            return {'error': f'On-page SEO analysis failed: {str(e)}'}
    
    def analyze_technical_seo(self):
        """Analyze technical SEO aspects"""
        print("Analyzing technical SEO...")
        try:
            # Check SSL certificate
            ssl_check = self.check_ssl_certificate()
            
            # Check page speed insights (if available)
            speed_check = self.check_basic_performance()
            
            # Check mobile-friendliness indicators
            mobile_check = self.check_mobile_indicators()
            
            return {
                'ssl_analysis': ssl_check,
                'performance_analysis': speed_check,
                'mobile_analysis': mobile_check,
                'domain_analysis': self.analyze_domain()
            }
            
        except Exception as e:
            return {'error': f'Technical SEO analysis failed: {str(e)}'}
    
    def check_ssl_certificate(self):
        """Check SSL certificate status"""
        try:
            response = requests.head(self.base_url, timeout=10)
            return {
                'has_ssl': self.base_url.startswith('https://'),
                'response_status': response.status_code,
                'headers': dict(response.headers)
            }
        except Exception as e:
            return {'error': f'SSL check failed: {str(e)}'}
    
    def check_basic_performance(self):
        """Basic performance check"""
        try:
            response = requests.get(self.base_url, timeout=30)
            return {
                'response_time_seconds': response.elapsed.total_seconds(),
                'page_size_bytes': len(response.content),
                'status_code': response.status_code,
                'content_type': response.headers.get('content-type', ''),
                'server': response.headers.get('server', ''),
                'cache_control': response.headers.get('cache-control', ''),
                'compression': response.headers.get('content-encoding', '')
            }
        except Exception as e:
            return {'error': f'Performance check failed: {str(e)}'}
    
    def check_mobile_indicators(self):
        """Check mobile-friendliness indicators"""
        try:
            response = requests.get(self.base_url)
            content = response.text.lower()
            
            return {
                'has_viewport_meta': 'viewport' in content,
                'has_responsive_images': 'srcset' in content or 'sizes' in content,
                'has_media_queries': '@media' in content,
                'mobile_friendly_score': self.calculate_mobile_score(content)
            }
        except Exception as e:
            return {'error': f'Mobile check failed: {str(e)}'}
    
    def calculate_mobile_score(self, content):
        """Calculate basic mobile-friendliness score"""
        score = 0
        indicators = [
            ('viewport', 'viewport' in content),
            ('responsive_images', 'srcset' in content),
            ('media_queries', '@media' in content),
            ('bootstrap', 'bootstrap' in content),
            ('responsive', 'responsive' in content)
        ]
        
        for indicator, present in indicators:
            if present:
                score += 20
        
        return min(score, 100)
    
    def analyze_domain(self):
        """Analyze domain characteristics"""
        parsed_url = urlparse(self.base_url)
        return {
            'domain': parsed_url.netloc,
            'tld': parsed_url.netloc.split('.')[-1],
            'subdomain': parsed_url.netloc.split('.')[0] if len(parsed_url.netloc.split('.')) > 2 else None,
            'is_www': parsed_url.netloc.startswith('www.'),
            'protocol': parsed_url.scheme
        }
    
    def analyze_content(self):
        """Analyze content for SEO relevance"""
        print("Analyzing content...")
        try:
            response = requests.get(self.base_url)
            content = response.text
            
            # Extract text content
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            text_content = soup.get_text().lower()
            
            # Keyword analysis
            target_keywords = [
                'sydney', 'coach', 'charter', 'bus', 'hire', 'nsw', 
                'wedding', 'corporate', 'school', 'transport', 'tours',
                'accredited', 'licensed', 'professional', 'experienced'
            ]
            
            keyword_density = {}
            total_words = len(text_content.split())
            
            for keyword in target_keywords:
                count = text_content.count(keyword)
                density = (count / total_words) * 100 if total_words > 0 else 0
                keyword_density[keyword] = {
                    'count': count,
                    'density_percent': round(density, 2)
                }
            
            return {
                'total_words': total_words,
                'keyword_analysis': keyword_density,
                'content_quality_indicators': {
                    'has_contact_info': any(indicator in text_content for indicator in ['phone', 'email', 'contact', 'call']),
                    'has_service_descriptions': any(service in text_content for service in ['wedding', 'corporate', 'school', 'tour']),
                    'has_location_info': any(location in text_content for location in ['sydney', 'nsw', 'australia']),
                    'has_credentials': any(cred in text_content for cred in ['accredited', 'licensed', 'certified', 'experience'])
                }
            }
            
        except Exception as e:
            return {'error': f'Content analysis failed: {str(e)}'}
    
    def analyze_local_seo(self):
        """Analyze local SEO factors"""
        print("Analyzing local SEO...")
        try:
            response = requests.get(self.base_url)
            content = response.text.lower()
            
            local_indicators = {
                'sydney_mentions': content.count('sydney'),
                'nsw_mentions': content.count('nsw') + content.count('new south wales'),
                'australia_mentions': content.count('australia'),
                'phone_number_present': '(02)' in content or '02 ' in content,
                'address_indicators': any(indicator in content for indicator in ['street', 'road', 'avenue', 'suburb']),
                'local_landmarks': any(landmark in content for landmark in ['harbour bridge', 'opera house', 'cbd', 'airport']),
                'service_areas': any(area in content for area in ['western sydney', 'eastern suburbs', 'north shore', 'inner west'])
            }
            
            return {
                'local_seo_score': sum(1 for v in local_indicators.values() if v) * 10,
                'indicators': local_indicators,
                'recommendations': self.generate_local_seo_recommendations(local_indicators)
            }
            
        except Exception as e:
            return {'error': f'Local SEO analysis failed: {str(e)}'}
    
    def generate_local_seo_recommendations(self, indicators):
        """Generate local SEO recommendations"""
        recommendations = []
        
        if not indicators['phone_number_present']:
            recommendations.append("Add local phone number with area code (02) prominently")
        
        if not indicators['address_indicators']:
            recommendations.append("Include business address or service areas")
        
        if indicators['sydney_mentions'] < 5:
            recommendations.append("Increase mentions of 'Sydney' throughout content")
        
        if not indicators['local_landmarks']:
            recommendations.append("Reference local Sydney landmarks or areas")
        
        return recommendations
    
    def analyze_schema_markup(self):
        """Analyze structured data/schema markup"""
        print("Analyzing schema markup...")
        try:
            response = requests.get(self.base_url)
            content = response.text
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            
            # Look for JSON-LD structured data
            json_ld_scripts = soup.find_all('script', type='application/ld+json')
            structured_data = []
            
            for script in json_ld_scripts:
                try:
                    data = json.loads(script.string)
                    structured_data.append(data)
                except json.JSONDecodeError:
                    continue
            
            # Look for microdata
            microdata_items = soup.find_all(attrs={"itemtype": True})
            
            return {
                'json_ld_count': len(json_ld_scripts),
                'microdata_count': len(microdata_items),
                'structured_data': structured_data,
                'schema_types': self.extract_schema_types(structured_data),
                'recommendations': self.generate_schema_recommendations(structured_data)
            }
            
        except Exception as e:
            return {'error': f'Schema markup analysis failed: {str(e)}'}
    
    def extract_schema_types(self, structured_data):
        """Extract schema.org types from structured data"""
        types = set()
        for data in structured_data:
            if isinstance(data, dict):
                if '@type' in data:
                    if isinstance(data['@type'], list):
                        types.update(data['@type'])
                    else:
                        types.add(data['@type'])
                elif '@graph' in data:
                    for item in data['@graph']:
                        if '@type' in item:
                            if isinstance(item['@type'], list):
                                types.update(item['@type'])
                            else:
                                types.add(item['@type'])
        return list(types)
    
    def generate_schema_recommendations(self, structured_data):
        """Generate schema markup recommendations"""
        recommendations = []
        types = self.extract_schema_types(structured_data)
        
        recommended_schemas = ['LocalBusiness', 'Organization', 'TransportationCompany', 'Service']
        missing_schemas = [schema for schema in recommended_schemas if schema not in types]
        
        if missing_schemas:
            recommendations.append(f"Consider adding schema markup for: {', '.join(missing_schemas)}")
        
        if not any('address' in str(data).lower() for data in structured_data):
            recommendations.append("Add structured address data to schema markup")
        
        if not any('telephone' in str(data).lower() for data in structured_data):
            recommendations.append("Add telephone number to schema markup")
        
        return recommendations

def run_advertools_analysis():
    """Run comprehensive Advertools SEO analysis"""
    analyzer = AdvertoolsSEOAnalyzer()
    
    try:
        results = analyzer.comprehensive_seo_analysis()
        
        # Save results
        with open('advertools_seo_analysis.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        return results
        
    except Exception as e:
        return {"error": f"Advertools analysis failed: {str(e)}"}

if __name__ == "__main__":
    print("Starting comprehensive Advertools SEO analysis...")
    results = run_advertools_analysis()
    
    print("\nAnalysis complete! Results saved to advertools_seo_analysis.json")
    print(json.dumps(results, indent=2, default=str))