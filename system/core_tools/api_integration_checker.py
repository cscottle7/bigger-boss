#!/usr/bin/env python3
"""
Check for API integration capabilities - GTmetrix, SerpAPI, etc.
"""

import requests
import json
import os
from datetime import datetime

class APIIntegrationChecker:
    def __init__(self):
        self.results = {}
        self.website_url = "https://sydneycoachcharter.com.au"
        
    def check_gtmetrix_api(self):
        """Check GTmetrix API integration"""
        print("Checking GTmetrix API integration...")
        
        # Note: GTmetrix requires API credentials
        # This is a mock implementation showing what would be possible
        gtmetrix_check = {
            'api_available': False,
            'requires_credentials': True,
            'capabilities': [
                'Page Speed Analysis',
                'Core Web Vitals',
                'Performance Waterfall',
                'Detailed Timing Metrics',
                'Mobile/Desktop Testing',
                'Historical Performance Tracking'
            ],
            'sample_endpoint': 'https://gtmetrix.com/api/2.0/test',
            'authentication': 'API Key + Email',
            'note': 'API credentials required for actual testing'
        }
        
        # Check if we have credentials (environment variables)
        api_key = os.getenv('GTMETRIX_API_KEY')
        email = os.getenv('GTMETRIX_EMAIL')
        
        if api_key and email:
            try:
                # Would make actual API call here
                gtmetrix_check['api_available'] = True
                gtmetrix_check['credentials_found'] = True
            except:
                gtmetrix_check['credentials_found'] = False
        else:
            gtmetrix_check['credentials_found'] = False
            
        return gtmetrix_check
    
    def check_serpapi_integration(self):
        """Check SerpAPI integration"""
        print("Checking SerpAPI integration...")
        
        serpapi_check = {
            'api_available': False,
            'requires_credentials': True,
            'capabilities': [
                'Google Search Results',
                'Keyword Rankings',
                'SERP Features Analysis',
                'Local Search Results',
                'Google My Business Data',
                'Competitor Analysis'
            ],
            'sample_endpoint': 'https://serpapi.com/search',
            'authentication': 'API Key',
            'note': 'API credentials required for actual searches'
        }
        
        # Check if we have credentials
        api_key = os.getenv('SERPAPI_KEY')
        
        if api_key:
            try:
                # Test with a simple search
                params = {
                    'engine': 'google',
                    'q': 'sydney coach charter',
                    'api_key': api_key
                }
                response = requests.get('https://serpapi.com/search', params=params)
                if response.status_code == 200:
                    serpapi_check['api_available'] = True
                    serpapi_check['credentials_working'] = True
                    
                    # Get sample data
                    data = response.json()
                    serpapi_check['sample_data'] = {
                        'total_results': data.get('search_information', {}).get('total_results', 0),
                        'organic_results_count': len(data.get('organic_results', []))
                    }
                else:
                    serpapi_check['credentials_working'] = False
                    serpapi_check['error'] = f"HTTP {response.status_code}"
            except Exception as e:
                serpapi_check['credentials_working'] = False
                serpapi_check['error'] = str(e)
        else:
            serpapi_check['credentials_found'] = False
            
        return serpapi_check
    
    def check_pagespeed_api(self):
        """Check Google PageSpeed Insights API"""
        print("Checking Google PageSpeed Insights API...")
        
        pagespeed_check = {
            'api_available': True,
            'requires_credentials': False,
            'free_quota': True,
            'capabilities': [
                'Core Web Vitals',
                'Performance Score',
                'Accessibility Score',
                'Best Practices Score',
                'SEO Score',
                'Field Data (Real User Metrics)',
                'Lab Data (Simulated)',
                'Opportunities and Diagnostics'
            ]
        }
        
        try:
            # Test API call
            api_url = f"https://www.googleapis.com/pagespeed/v5/runPagespeed?url={self.website_url}&strategy=desktop"
            response = requests.get(api_url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                pagespeed_check['working'] = True
                pagespeed_check['sample_data'] = {
                    'performance_score': data.get('lighthouseResult', {}).get('categories', {}).get('performance', {}).get('score', 0) * 100,
                    'accessibility_score': data.get('lighthouseResult', {}).get('categories', {}).get('accessibility', {}).get('score', 0) * 100,
                    'best_practices_score': data.get('lighthouseResult', {}).get('categories', {}).get('best-practices', {}).get('score', 0) * 100,
                    'seo_score': data.get('lighthouseResult', {}).get('categories', {}).get('seo', {}).get('score', 0) * 100,
                    'first_contentful_paint': data.get('lighthouseResult', {}).get('audits', {}).get('first-contentful-paint', {}).get('displayValue', 'N/A'),
                    'largest_contentful_paint': data.get('lighthouseResult', {}).get('audits', {}).get('largest-contentful-paint', {}).get('displayValue', 'N/A')
                }
            else:
                pagespeed_check['working'] = False
                pagespeed_check['error'] = f"HTTP {response.status_code}"
                
        except Exception as e:
            pagespeed_check['working'] = False
            pagespeed_check['error'] = str(e)
            
        return pagespeed_check
    
    def check_lighthouse_ci_api(self):
        """Check Lighthouse CI capabilities"""
        print("Checking Lighthouse CI capabilities...")
        
        lighthouse_check = {
            'tool_available': True,
            'installation': 'npm install -g @lhci/cli',
            'capabilities': [
                'Automated Performance Testing',
                'CI/CD Integration',
                'Historical Performance Tracking',
                'Budget Assertions',
                'Multi-page Testing',
                'Custom Configurations'
            ],
            'sample_command': f'lhci autorun --upload.target=temporary-public-storage --collect.url={self.website_url}',
            'note': 'Requires Node.js and npm installation'
        }
        
        # Check if lighthouse CLI is available
        try:
            import subprocess
            result = subprocess.run(['npx', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                lighthouse_check['npx_available'] = True
            else:
                lighthouse_check['npx_available'] = False
        except:
            lighthouse_check['npx_available'] = False
            
        return lighthouse_check
    
    def check_semrush_api(self):
        """Check SEMrush API integration possibilities"""
        print("Checking SEMrush API...")
        
        semrush_check = {
            'api_available': False,
            'requires_subscription': True,
            'capabilities': [
                'Keyword Research',
                'Domain Analytics',
                'Backlink Analysis',
                'Competitor Research',
                'Ranking Tracking',
                'Site Audit Data'
            ],
            'sample_endpoint': 'https://api.semrush.com/',
            'authentication': 'API Key (paid subscription)',
            'note': 'Requires paid SEMrush subscription'
        }
        
        api_key = os.getenv('SEMRUSH_API_KEY')
        if api_key:
            semrush_check['credentials_found'] = True
        else:
            semrush_check['credentials_found'] = False
            
        return semrush_check
    
    def check_ahrefs_api(self):
        """Check Ahrefs API integration possibilities"""
        print("Checking Ahrefs API...")
        
        ahrefs_check = {
            'api_available': False,
            'requires_subscription': True,
            'capabilities': [
                'Backlink Data',
                'Keyword Research',
                'Content Gap Analysis',
                'Rank Tracking',
                'Site Explorer Data',
                'Domain Rating'
            ],
            'sample_endpoint': 'https://apiv2.ahrefs.com/',
            'authentication': 'API Token (paid subscription)',
            'note': 'Requires paid Ahrefs subscription'
        }
        
        api_key = os.getenv('AHREFS_API_KEY')
        if api_key:
            ahrefs_check['credentials_found'] = True
        else:
            ahrefs_check['credentials_found'] = False
            
        return ahrefs_check
    
    def check_web_vitals_api(self):
        """Check Chrome UX Report API for Web Vitals"""
        print("Checking Chrome UX Report API...")
        
        crux_check = {
            'api_available': True,
            'requires_credentials': True,  # API key needed
            'free_quota': True,
            'capabilities': [
                'Real User Metrics (RUM)',
                'Core Web Vitals Field Data',
                'Historic Performance Data',
                'Device/Connection Breakdown',
                'Origin vs URL Level Data'
            ]
        }
        
        api_key = os.getenv('GOOGLE_API_KEY')
        if api_key:
            try:
                api_url = f"https://chromeuxreport.googleapis.com/v1/records:queryRecord?key={api_key}"
                payload = {
                    "origin": self.website_url,
                    "metrics": ["largest_contentful_paint", "first_input_delay", "cumulative_layout_shift"]
                }
                response = requests.post(api_url, json=payload)
                
                if response.status_code == 200:
                    crux_check['working'] = True
                    data = response.json()
                    crux_check['sample_data'] = data
                else:
                    crux_check['working'] = False
                    crux_check['error'] = f"HTTP {response.status_code}"
            except Exception as e:
                crux_check['working'] = False
                crux_check['error'] = str(e)
        else:
            crux_check['credentials_found'] = False
            
        return crux_check
    
    def run_comprehensive_api_check(self):
        """Run comprehensive API integration check"""
        print("=== COMPREHENSIVE API INTEGRATION CHECK ===")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'website_tested': self.website_url,
            'api_integrations': {
                'gtmetrix': self.check_gtmetrix_api(),
                'serpapi': self.check_serpapi_integration(),
                'google_pagespeed': self.check_pagespeed_api(),
                'lighthouse_ci': self.check_lighthouse_ci_api(),
                'semrush': self.check_semrush_api(),
                'ahrefs': self.check_ahrefs_api(),
                'chrome_ux_report': self.check_web_vitals_api()
            },
            'summary': self.generate_api_summary()
        }
        
        return results
    
    def generate_api_summary(self):
        """Generate API integration summary"""
        return {
            'free_apis_available': [
                'Google PageSpeed Insights',
                'Chrome UX Report (with API key)',
                'Lighthouse CI'
            ],
            'paid_apis_available': [
                'GTmetrix (API plan)',
                'SerpAPI',
                'SEMrush API',
                'Ahrefs API'
            ],
            'immediate_opportunities': [
                'Google PageSpeed Insights for Core Web Vitals',
                'Lighthouse CI for automated testing',
                'SerpAPI for keyword ranking tracking (if credentials available)'
            ],
            'recommended_integrations': [
                'Google PageSpeed Insights - Free, comprehensive performance data',
                'SerpAPI - Keyword ranking and SERP analysis',
                'GTmetrix - Detailed performance monitoring'
            ]
        }

def run_api_integration_check():
    """Run API integration check"""
    checker = APIIntegrationChecker()
    
    try:
        results = checker.run_comprehensive_api_check()
        
        # Save results
        with open('api_integration_results.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        return results
        
    except Exception as e:
        return {"error": f"API integration check failed: {str(e)}"}

if __name__ == "__main__":
    print("Starting API integration capabilities check...")
    results = run_api_integration_check()
    
    print("\nAPI Integration Check complete! Results saved to api_integration_results.json")
    
    # Print summary
    if 'summary' in results:
        print("\n=== API INTEGRATION SUMMARY ===")
        print("Free APIs Available:")
        for api in results['summary']['free_apis_available']:
            print(f"  - {api}")
        
        print("\nPaid APIs Available:")
        for api in results['summary']['paid_apis_available']:
            print(f"  - {api}")
        
        print("\nImmediate Opportunities:")
        for opportunity in results['summary']['immediate_opportunities']:
            print(f"  - {opportunity}")
    
    print(f"\nDetailed results: {json.dumps(results, indent=2, default=str)}")