#!/usr/bin/env python3
"""
GTMetrix Performance Analysis Script
Tests website performance using GTMetrix API and generates comprehensive report
"""

import os
import requests
import json
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GTMetrixPerformanceTester:
    def __init__(self):
        self.api_key = os.getenv('GTMETRIX_API_KEY')
        self.base_url = 'https://gtmetrix.com/api/2.0'
        self.headers = {'Content-Type': 'application/vnd.api+json'}
        
    def start_test(self, url):
        """Start a GTMetrix performance test"""
        data = {
            'data': {
                'type': 'test',
                'attributes': {
                    'url': url,
                    'location': 7,  # Sydney server
                    'browser': 'chrome',
                    'generate_video': True,
                    'retention': 30
                }
            }
        }
        
        print(f'Starting GTMetrix performance test for: {url}')
        print(f'API Key configured: {"Yes" if self.api_key else "No"}')
        
        response = requests.post(
            f'{self.base_url}/tests',
            auth=(self.api_key, ''),
            headers=self.headers,
            json=data,
            verify=False
        )
        
        if response.status_code in [200, 202]:
            result = response.json()
            test_id = result.get('data', {}).get('id')
            state = result.get('data', {}).get('attributes', {}).get('state')
            credits = result.get('meta', {}).get('credits_left')
            
            print(f'✓ Test successfully started!')
            print(f'Test ID: {test_id}')
            print(f'Current State: {state}')
            print(f'Credits Remaining: {credits}')
            print(f'Test URL: https://gtmetrix.com/reports/{test_id}')
            
            return test_id
        else:
            print(f'✗ GTMetrix API Error: {response.status_code}')
            print(f'Error Response: {response.text}')
            return None
    
    def get_test_status(self, test_id):
        """Check the status of a GTMetrix test"""
        response = requests.get(
            f'{self.base_url}/tests/{test_id}',
            auth=(self.api_key, ''),
            verify=False
        )
        
        if response.status_code == 200:
            result = response.json()
            state = result.get('data', {}).get('attributes', {}).get('state')
            return state, result
        return None, None
    
    def wait_for_completion(self, test_id, max_wait_minutes=10):
        """Wait for test completion with polling"""
        print(f'\nWaiting for test completion (max {max_wait_minutes} minutes)...')
        start_time = time.time()
        max_wait_seconds = max_wait_minutes * 60
        
        while time.time() - start_time < max_wait_seconds:
            state, result = self.get_test_status(test_id)
            
            if state == 'completed':
                print('✓ Test completed successfully!')
                return result
            elif state == 'error':
                print('✗ Test failed with error')
                return None
            else:
                print(f'  Status: {state}... waiting 15 seconds')
                time.sleep(15)
        
        print('✗ Test timed out')
        return None
    
    def analyze_results(self, result_data):
        """Analyze GTMetrix test results and extract key metrics"""
        if not result_data:
            return None
        
        attributes = result_data.get('data', {}).get('attributes', {})
        
        # Extract performance scores
        performance_score = attributes.get('performance_score')
        structure_score = attributes.get('structure_score')
        
        # Extract Core Web Vitals
        web_vitals = attributes.get('web_vitals', {})
        lcp = web_vitals.get('largest_contentful_paint')
        fid = web_vitals.get('first_input_delay')
        cls = web_vitals.get('cumulative_layout_shift')
        
        # Extract loading metrics
        fully_loaded_time = attributes.get('fully_loaded_time')
        html_bytes = attributes.get('html_bytes')
        page_bytes = attributes.get('page_bytes')
        requests = attributes.get('requests')
        
        # Extract PageSpeed scores
        pagespeed = attributes.get('pagespeed', {})
        lighthouse_performance = pagespeed.get('lighthouse_performance')
        
        analysis = {
            'test_info': {
                'url': attributes.get('url'),
                'test_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'location': 'Sydney, Australia',
                'browser': 'Chrome'
            },
            'performance_scores': {
                'gtmetrix_performance': performance_score,
                'gtmetrix_structure': structure_score,
                'lighthouse_performance': lighthouse_performance
            },
            'core_web_vitals': {
                'lcp': lcp,
                'fid': fid,
                'cls': cls
            },
            'loading_metrics': {
                'fully_loaded_time': fully_loaded_time,
                'html_bytes': html_bytes,
                'page_bytes': page_bytes,
                'total_requests': requests
            },
            'raw_data': result_data
        }
        
        return analysis
    
    def generate_performance_report(self, analysis):
        """Generate comprehensive performance report"""
        if not analysis:
            return "## Performance Analysis Status\n⚠️ **GTmetrix API Error**: Cannot provide accurate performance scores without API access"
        
        report = f"""# Website Performance Analysis Report

**Site Analyzed**: {analysis['test_info']['url']}
**Analysis Date**: {analysis['test_info']['test_date']}
**Testing Location**: {analysis['test_info']['location']}
**Browser**: {analysis['test_info']['browser']}

## Performance Summary

### GTMetrix Scores
- **Performance Score**: {analysis['performance_scores']['gtmetrix_performance']}/100
- **Structure Score**: {analysis['performance_scores']['gtmetrix_structure']}/100
- **Lighthouse Performance**: {analysis['performance_scores']['lighthouse_performance']}/100

## Core Web Vitals Analysis

### Largest Contentful Paint (LCP)
- **Current Score**: {analysis['core_web_vitals']['lcp']/1000:.2f} seconds
- **Status**: {'Good' if analysis['core_web_vitals']['lcp'] <= 2500 else 'Needs Improvement' if analysis['core_web_vitals']['lcp'] <= 4000 else 'Poor'}
- **Target**: <2.5 seconds

### First Input Delay (FID)  
- **Current Score**: {analysis['core_web_vitals']['fid']} milliseconds
- **Status**: {'Good' if analysis['core_web_vitals']['fid'] <= 100 else 'Needs Improvement' if analysis['core_web_vitals']['fid'] <= 300 else 'Poor'}
- **Target**: <100 milliseconds

### Cumulative Layout Shift (CLS)
- **Current Score**: {analysis['core_web_vitals']['cls']:.3f}
- **Status**: {'Good' if analysis['core_web_vitals']['cls'] <= 0.1 else 'Needs Improvement' if analysis['core_web_vitals']['cls'] <= 0.25 else 'Poor'}
- **Target**: <0.1

## Loading Performance Metrics
- **Fully Loaded Time**: {analysis['loading_metrics']['fully_loaded_time']/1000:.2f} seconds
- **Total Page Size**: {analysis['loading_metrics']['page_bytes']/1024/1024:.2f} MB
- **Total Requests**: {analysis['loading_metrics']['total_requests']}
- **HTML Size**: {analysis['loading_metrics']['html_bytes']/1024:.1f} KB

## Performance Assessment
{self._generate_performance_assessment(analysis)}

## Optimization Recommendations
{self._generate_optimization_recommendations(analysis)}
"""
        return report
    
    def _generate_performance_assessment(self, analysis):
        """Generate performance assessment based on scores"""
        perf_score = analysis['performance_scores']['gtmetrix_performance']
        lcp = analysis['core_web_vitals']['lcp']
        cls = analysis['core_web_vitals']['cls']
        
        assessment = "### Overall Performance Status\n"
        
        if perf_score >= 90:
            assessment += "✅ **Excellent Performance** - Your site performs exceptionally well\n"
        elif perf_score >= 80:
            assessment += "🟡 **Good Performance** - Minor optimizations recommended\n"
        elif perf_score >= 70:
            assessment += "🟠 **Fair Performance** - Significant optimization opportunities available\n"
        else:
            assessment += "🔴 **Poor Performance** - Critical optimization required\n"
        
        # Core Web Vitals assessment
        vitals_good = (lcp <= 2500) and (cls <= 0.1)
        if vitals_good:
            assessment += "✅ **Core Web Vitals**: Passing Google's standards\n"
        else:
            assessment += "❌ **Core Web Vitals**: Failing Google's standards - SEO impact likely\n"
        
        return assessment
    
    def _generate_optimization_recommendations(self, analysis):
        """Generate specific optimization recommendations"""
        recommendations = []
        
        # Performance score based recommendations
        perf_score = analysis['performance_scores']['gtmetrix_performance']
        if perf_score < 80:
            recommendations.append("🔧 **Critical**: Implement performance optimization strategy")
        
        # LCP recommendations
        lcp = analysis['core_web_vitals']['lcp']
        if lcp > 2500:
            recommendations.append("⚡ **LCP Optimization**: Optimize largest contentful paint")
            recommendations.append("  - Optimize images and implement lazy loading")
            recommendations.append("  - Improve server response times")
            recommendations.append("  - Implement CDN for faster content delivery")
        
        # CLS recommendations
        cls = analysis['core_web_vitals']['cls']
        if cls > 0.1:
            recommendations.append("🔧 **Layout Stability**: Reduce cumulative layout shift")
            recommendations.append("  - Add dimensions to images and embeds")
            recommendations.append("  - Reserve space for dynamic content")
            recommendations.append("  - Optimize font loading to prevent FOIT/FOUT")
        
        # Page size recommendations
        page_size_mb = analysis['loading_metrics']['page_bytes'] / 1024 / 1024
        if page_size_mb > 3:
            recommendations.append("📦 **Resource Optimization**: Reduce total page size")
            recommendations.append(f"  - Current size: {page_size_mb:.1f}MB, target: <3MB")
            recommendations.append("  - Compress images and implement WebP format")
            recommendations.append("  - Minify CSS and JavaScript")
        
        # Request count recommendations
        requests = analysis['loading_metrics']['total_requests']
        if requests > 100:
            recommendations.append("🔄 **Request Reduction**: Minimize HTTP requests")
            recommendations.append(f"  - Current: {requests} requests, target: <50")
            recommendations.append("  - Combine CSS and JS files")
            recommendations.append("  - Use CSS sprites for images")
        
        return "\n".join(recommendations) if recommendations else "✅ All metrics within acceptable ranges"

def main():
    """Main function to run performance analysis"""
    tester = GTMetrixPerformanceTester()
    target_url = 'https://sydneycoachcharter.com.au/'
    
    # Start the test
    test_id = tester.start_test(target_url)
    
    if not test_id:
        print("Failed to start GTMetrix test")
        return
    
    # Wait for completion
    result = tester.wait_for_completion(test_id, max_wait_minutes=10)
    
    if not result:
        print("Test did not complete successfully")
        return
    
    # Analyze results
    analysis = tester.analyze_results(result)
    
    # Generate report
    report = tester.generate_performance_report(analysis)
    
    # Save report to file
    with open('sydney_coach_charter_performance_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("\n" + "="*60)
    print("PERFORMANCE ANALYSIS COMPLETE")
    print("="*60)
    print(report)
    print("\n📄 Full report saved to: sydney_coach_charter_performance_report.md")

if __name__ == "__main__":
    main()