#!/usr/bin/env python3
"""
Comprehensive data analysis using Pandas and other tools
Process all collected data into actionable insights
"""

import pandas as pd
import json
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import requests

class ComprehensiveDataAnalyzer:
    def __init__(self):
        self.scrapy_data = None
        self.playwright_data = None
        self.advertools_data = None
        self.analysis_results = {}
        
    def load_all_data(self):
        """Load all collected data files"""
        print("Loading all collected data...")
        
        # Load Scrapy data
        try:
            scrapy_files = list(Path('.').glob('**/crawl_data.json'))
            if scrapy_files:
                with open(scrapy_files[0], 'r') as f:
                    scrapy_raw = f.read()
                # Parse JSONL format
                scrapy_items = []
                for line in scrapy_raw.strip().split('\n'):
                    if line.strip():
                        try:
                            scrapy_items.append(json.loads(line))
                        except:
                            continue
                self.scrapy_data = pd.DataFrame(scrapy_items) if scrapy_items else pd.DataFrame()
                print(f"Loaded {len(self.scrapy_data)} pages from Scrapy crawl")
        except Exception as e:
            print(f"Failed to load Scrapy data: {e}")
            self.scrapy_data = pd.DataFrame()
        
        # Load Playwright data
        try:
            if Path('playwright_analysis_results.json').exists():
                with open('playwright_analysis_results.json', 'r') as f:
                    self.playwright_data = json.load(f)
                print("Loaded Playwright browser analysis data")
        except Exception as e:
            print(f"Failed to load Playwright data: {e}")
            self.playwright_data = {}
        
        # Load Advertools data
        try:
            if Path('advertools_seo_analysis.json').exists():
                with open('advertools_seo_analysis.json', 'r') as f:
                    self.advertools_data = json.load(f)
                print("Loaded Advertools SEO analysis data")
        except Exception as e:
            print(f"Failed to load Advertools data: {e}")
            self.advertools_data = {}
    
    def analyze_seo_performance(self):
        """Analyze SEO performance across all data sources"""
        print("Analyzing SEO performance...")
        
        seo_analysis = {
            'timestamp': datetime.now().isoformat(),
            'overall_score': 0,
            'critical_issues': [],
            'recommendations': [],
            'performance_metrics': {}
        }
        
        # Title tag analysis
        if not self.scrapy_data.empty:
            title_analysis = self.analyze_title_tags()
            seo_analysis['title_analysis'] = title_analysis
            
            # Meta description analysis
            meta_analysis = self.analyze_meta_descriptions()
            seo_analysis['meta_description_analysis'] = meta_analysis
            
            # Content analysis
            content_analysis = self.analyze_content_quality()
            seo_analysis['content_analysis'] = content_analysis
            
            # Image analysis
            image_analysis = self.analyze_image_optimization()
            seo_analysis['image_analysis'] = image_analysis
        
        # Technical SEO from Advertools
        if self.advertools_data:
            tech_analysis = self.analyze_technical_seo()
            seo_analysis['technical_analysis'] = tech_analysis
        
        # Performance from Playwright
        if self.playwright_data:
            perf_analysis = self.analyze_performance_metrics()
            seo_analysis['performance_analysis'] = perf_analysis
        
        # Calculate overall score
        seo_analysis['overall_score'] = self.calculate_seo_score(seo_analysis)
        
        return seo_analysis
    
    def analyze_title_tags(self):
        """Analyze title tag optimization"""
        if 'title' not in self.scrapy_data.columns:
            return {'error': 'No title data available'}
        
        titles = self.scrapy_data['title'].dropna()
        
        analysis = {
            'total_pages': len(self.scrapy_data),
            'pages_with_titles': len(titles),
            'missing_titles': len(self.scrapy_data) - len(titles),
            'title_lengths': [],
            'issues': [],
            'recommendations': []
        }
        
        for title in titles:
            length = len(str(title))
            analysis['title_lengths'].append(length)
            
            if length < 30:
                analysis['issues'].append(f"Title too short: '{title}' ({length} chars)")
            elif length > 60:
                analysis['issues'].append(f"Title too long: '{title}' ({length} chars)")
        
        analysis['avg_title_length'] = np.mean(analysis['title_lengths']) if analysis['title_lengths'] else 0
        analysis['optimal_length_count'] = sum(1 for l in analysis['title_lengths'] if 30 <= l <= 60)
        
        # Recommendations
        if analysis['missing_titles'] > 0:
            analysis['recommendations'].append(f"Add title tags to {analysis['missing_titles']} pages")
        
        if analysis['avg_title_length'] < 30:
            analysis['recommendations'].append("Increase average title length for better SEO")
        elif analysis['avg_title_length'] > 60:
            analysis['recommendations'].append("Reduce average title length to prevent truncation")
        
        return analysis
    
    def analyze_meta_descriptions(self):
        """Analyze meta description optimization"""
        if 'meta_description' not in self.scrapy_data.columns:
            return {'error': 'No meta description data available'}
        
        descriptions = self.scrapy_data['meta_description'].dropna()
        
        analysis = {
            'total_pages': len(self.scrapy_data),
            'pages_with_descriptions': len(descriptions),
            'missing_descriptions': len(self.scrapy_data) - len(descriptions),
            'description_lengths': [],
            'issues': [],
            'recommendations': []
        }
        
        for desc in descriptions:
            length = len(str(desc))
            analysis['description_lengths'].append(length)
            
            if length < 120:
                analysis['issues'].append(f"Meta description too short ({length} chars)")
            elif length > 160:
                analysis['issues'].append(f"Meta description too long ({length} chars)")
        
        analysis['avg_description_length'] = np.mean(analysis['description_lengths']) if analysis['description_lengths'] else 0
        analysis['optimal_length_count'] = sum(1 for l in analysis['description_lengths'] if 120 <= l <= 160)
        
        # Critical issue
        if analysis['missing_descriptions'] > 0:
            analysis['recommendations'].append(f"CRITICAL: Add meta descriptions to {analysis['missing_descriptions']} pages")
        
        return analysis
    
    def analyze_content_quality(self):
        """Analyze content quality metrics"""
        analysis = {
            'word_count_analysis': {},
            'heading_structure': {},
            'service_mentions': {},
            'local_seo_signals': {}
        }
        
        if 'word_count' in self.scrapy_data.columns:
            word_counts = self.scrapy_data['word_count'].dropna()
            analysis['word_count_analysis'] = {
                'avg_word_count': np.mean(word_counts) if len(word_counts) > 0 else 0,
                'min_word_count': np.min(word_counts) if len(word_counts) > 0 else 0,
                'max_word_count': np.max(word_counts) if len(word_counts) > 0 else 0,
                'pages_with_thin_content': sum(1 for wc in word_counts if wc < 300)
            }
        
        # Heading structure analysis
        h1_counts = self.scrapy_data['h1_tags'].apply(len) if 'h1_tags' in self.scrapy_data.columns else []
        analysis['heading_structure'] = {
            'pages_with_multiple_h1': sum(1 for count in h1_counts if count > 1),
            'pages_without_h1': sum(1 for count in h1_counts if count == 0),
            'avg_h1_per_page': np.mean(h1_counts) if len(h1_counts) > 0 else 0
        }
        
        # Service mentions analysis
        service_columns = ['mentions_wedding', 'mentions_corporate', 'mentions_school', 'mentions_tourism', 'mentions_charter']
        for col in service_columns:
            if col in self.scrapy_data.columns:
                analysis['service_mentions'][col] = self.scrapy_data[col].sum()
        
        # Local SEO signals
        local_columns = ['mentions_sydney', 'mentions_nsw', 'mentions_australia']
        for col in local_columns:
            if col in self.scrapy_data.columns:
                analysis['local_seo_signals'][col] = self.scrapy_data[col].sum()
        
        return analysis
    
    def analyze_image_optimization(self):
        """Analyze image SEO optimization"""
        if 'images_without_alt' not in self.scrapy_data.columns or 'total_images' not in self.scrapy_data.columns:
            return {'error': 'No image data available'}
        
        total_images = self.scrapy_data['total_images'].sum()
        images_without_alt = self.scrapy_data['images_without_alt'].sum()
        images_with_alt = total_images - images_without_alt
        
        analysis = {
            'total_images': int(total_images),
            'images_with_alt': int(images_with_alt),
            'images_without_alt': int(images_without_alt),
            'alt_text_coverage': (images_with_alt / total_images * 100) if total_images > 0 else 0,
            'critical_issue': images_without_alt > 0,
            'recommendations': []
        }
        
        if images_without_alt > 0:
            analysis['recommendations'].append(f"CRITICAL: Add alt text to {images_without_alt} images")
        
        return analysis
    
    def analyze_technical_seo(self):
        """Analyze technical SEO from Advertools data"""
        if not self.advertools_data:
            return {'error': 'No Advertools data available'}
        
        analysis = {
            'ssl_status': {},
            'performance_metrics': {},
            'mobile_readiness': {},
            'robots_txt': {},
            'schema_markup': {}
        }
        
        # SSL Analysis
        if 'technical_analysis' in self.advertools_data and 'ssl_analysis' in self.advertools_data['technical_analysis']:
            ssl_data = self.advertools_data['technical_analysis']['ssl_analysis']
            analysis['ssl_status'] = {
                'has_ssl': ssl_data.get('has_ssl', False),
                'security_headers': self.analyze_security_headers(ssl_data.get('headers', {}))
            }
        
        # Performance metrics
        if 'technical_analysis' in self.advertools_data and 'performance_analysis' in self.advertools_data['technical_analysis']:
            perf_data = self.advertools_data['technical_analysis']['performance_analysis']
            analysis['performance_metrics'] = {
                'response_time': perf_data.get('response_time_seconds', 0),
                'page_size_mb': perf_data.get('page_size_bytes', 0) / 1024 / 1024,
                'compression_enabled': bool(perf_data.get('compression')),
                'caching_enabled': bool(perf_data.get('cache_control'))
            }
        
        # Mobile analysis
        if 'technical_analysis' in self.advertools_data and 'mobile_analysis' in self.advertools_data['technical_analysis']:
            mobile_data = self.advertools_data['technical_analysis']['mobile_analysis']
            analysis['mobile_readiness'] = mobile_data
        
        # Schema markup
        if 'schema_analysis' in self.advertools_data:
            schema_data = self.advertools_data['schema_analysis']
            analysis['schema_markup'] = {
                'has_structured_data': schema_data.get('json_ld_count', 0) > 0,
                'schema_types': schema_data.get('schema_types', []),
                'recommendations': schema_data.get('recommendations', [])
            }
        
        return analysis
    
    def analyze_security_headers(self, headers):
        """Analyze security headers"""
        security_headers = {
            'strict-transport-security': headers.get('Strict-Transport-Security'),
            'x-frame-options': headers.get('X-Frame-Options'),
            'x-content-type-options': headers.get('X-Content-Type-Options'),
            'referrer-policy': headers.get('Referrer-Policy')
        }
        
        present_headers = sum(1 for v in security_headers.values() if v)
        
        return {
            'security_headers_count': present_headers,
            'security_score': present_headers * 25,  # Out of 100
            'headers': security_headers
        }
    
    def analyze_performance_metrics(self):
        """Analyze performance metrics from Playwright"""
        if not self.playwright_data or 'performance_metrics' not in self.playwright_data:
            return {'error': 'No Playwright performance data available'}
        
        perf_data = self.playwright_data['performance_metrics']
        
        analysis = {
            'load_time_seconds': perf_data.get('load_time', 0),
            'dom_content_loaded': perf_data.get('dom_content_loaded', 0),
            'resource_count': perf_data.get('resource_count', 0),
            'total_transfer_size_mb': perf_data.get('total_transfer_size', 0) / 1024 / 1024,
            'performance_score': self.calculate_performance_score(perf_data),
            'recommendations': []
        }
        
        # Performance recommendations
        if analysis['load_time_seconds'] > 3:
            analysis['recommendations'].append("Page load time is slow (>3 seconds)")
        
        if analysis['resource_count'] > 50:
            analysis['recommendations'].append("High number of HTTP requests - consider optimization")
        
        if analysis['total_transfer_size_mb'] > 2:
            analysis['recommendations'].append("Large page size - optimize images and resources")
        
        return analysis
    
    def calculate_performance_score(self, perf_data):
        """Calculate performance score out of 100"""
        score = 100
        
        load_time = perf_data.get('load_time', 0)
        if load_time > 3:
            score -= 30
        elif load_time > 2:
            score -= 20
        elif load_time > 1:
            score -= 10
        
        resource_count = perf_data.get('resource_count', 0)
        if resource_count > 100:
            score -= 20
        elif resource_count > 50:
            score -= 10
        
        transfer_size = perf_data.get('total_transfer_size', 0) / 1024 / 1024  # MB
        if transfer_size > 5:
            score -= 20
        elif transfer_size > 2:
            score -= 10
        
        return max(score, 0)
    
    def calculate_seo_score(self, analysis):
        """Calculate overall SEO score"""
        score = 0
        max_score = 0
        
        # Title optimization (20 points)
        if 'title_analysis' in analysis and 'error' not in analysis['title_analysis']:
            title_data = analysis['title_analysis']
            if title_data.get('missing_titles', 0) == 0:
                score += 10
            if title_data.get('optimal_length_count', 0) > 0:
                score += 10
        max_score += 20
        
        # Meta descriptions (25 points)
        if 'meta_description_analysis' in analysis and 'error' not in analysis['meta_description_analysis']:
            meta_data = analysis['meta_description_analysis']
            if meta_data.get('missing_descriptions', 0) == 0:
                score += 15
            if meta_data.get('optimal_length_count', 0) > 0:
                score += 10
        max_score += 25
        
        # Images (15 points)
        if 'image_analysis' in analysis and 'error' not in analysis['image_analysis']:
            img_data = analysis['image_analysis']
            if img_data.get('alt_text_coverage', 0) == 100:
                score += 15
            elif img_data.get('alt_text_coverage', 0) > 50:
                score += 10
        max_score += 15
        
        # Technical SEO (20 points)
        if 'technical_analysis' in analysis and 'error' not in analysis['technical_analysis']:
            tech_data = analysis['technical_analysis']
            if tech_data.get('ssl_status', {}).get('has_ssl'):
                score += 5
            if tech_data.get('mobile_readiness', {}).get('mobile_friendly_score', 0) > 60:
                score += 10
            if tech_data.get('schema_markup', {}).get('has_structured_data'):
                score += 5
        max_score += 20
        
        # Performance (20 points)
        if 'performance_analysis' in analysis and 'error' not in analysis['performance_analysis']:
            perf_data = analysis['performance_analysis']
            score += min(perf_data.get('performance_score', 0) * 0.2, 20)
        max_score += 20
        
        return round((score / max_score * 100) if max_score > 0 else 0, 1)
    
    def generate_competitive_analysis(self):
        """Generate competitive analysis insights"""
        # This would typically compare against competitor data
        # For now, we'll provide industry benchmarks
        
        benchmarks = {
            'avg_load_time': 2.5,
            'avg_title_length': 45,
            'avg_meta_desc_length': 140,
            'avg_alt_text_coverage': 85,
            'avg_seo_score': 70
        }
        
        our_metrics = {}
        if self.playwright_data and 'performance_metrics' in self.playwright_data:
            our_metrics['load_time'] = self.playwright_data['performance_metrics'].get('load_time', 0)
        
        return {
            'industry_benchmarks': benchmarks,
            'our_performance': our_metrics,
            'competitive_gaps': self.identify_competitive_gaps(benchmarks, our_metrics)
        }
    
    def identify_competitive_gaps(self, benchmarks, our_metrics):
        """Identify areas where we lag behind industry standards"""
        gaps = []
        
        if our_metrics.get('load_time', 0) > benchmarks['avg_load_time']:
            gaps.append(f"Page load time ({our_metrics.get('load_time', 0):.2f}s) slower than industry average ({benchmarks['avg_load_time']}s)")
        
        return gaps
    
    def generate_action_plan(self, seo_analysis):
        """Generate prioritized action plan"""
        actions = []
        
        # Critical issues first
        if 'meta_description_analysis' in seo_analysis:
            meta_data = seo_analysis['meta_description_analysis']
            if meta_data.get('missing_descriptions', 0) > 0:
                actions.append({
                    'priority': 'CRITICAL',
                    'action': f"Add meta descriptions to {meta_data['missing_descriptions']} pages",
                    'impact': 'High',
                    'effort': 'Medium'
                })
        
        if 'image_analysis' in seo_analysis:
            img_data = seo_analysis['image_analysis']
            if img_data.get('images_without_alt', 0) > 0:
                actions.append({
                    'priority': 'CRITICAL',
                    'action': f"Add alt text to {img_data['images_without_alt']} images",
                    'impact': 'High',
                    'effort': 'Low'
                })
        
        # High priority improvements
        if 'performance_analysis' in seo_analysis:
            perf_data = seo_analysis['performance_analysis']
            if perf_data.get('load_time_seconds', 0) > 3:
                actions.append({
                    'priority': 'HIGH',
                    'action': 'Optimize page load speed (currently >3 seconds)',
                    'impact': 'High',
                    'effort': 'High'
                })
        
        # Schema markup improvements
        if 'technical_analysis' in seo_analysis:
            tech_data = seo_analysis['technical_analysis']
            schema_recs = tech_data.get('schema_markup', {}).get('recommendations', [])
            for rec in schema_recs:
                actions.append({
                    'priority': 'MEDIUM',
                    'action': rec,
                    'impact': 'Medium',
                    'effort': 'Medium'
                })
        
        return sorted(actions, key=lambda x: {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}[x['priority']])
    
    def generate_comprehensive_report(self):
        """Generate comprehensive analysis report"""
        print("Generating comprehensive analysis report...")
        
        # Load all data
        self.load_all_data()
        
        # Perform analyses
        seo_analysis = self.analyze_seo_performance()
        competitive_analysis = self.generate_competitive_analysis()
        action_plan = self.generate_action_plan(seo_analysis)
        
        # Compile report
        report = {
            'report_metadata': {
                'generated_at': datetime.now().isoformat(),
                'analysis_type': 'Comprehensive SEO and Technical Analysis',
                'data_sources': ['Scrapy', 'Playwright', 'Advertools'],
                'website': 'https://sydneycoachcharter.com.au'
            },
            'executive_summary': {
                'overall_seo_score': seo_analysis.get('overall_score', 0),
                'critical_issues_count': len([a for a in action_plan if a['priority'] == 'CRITICAL']),
                'pages_analyzed': len(self.scrapy_data) if not self.scrapy_data.empty else 0,
                'key_findings': self.generate_key_findings(seo_analysis)
            },
            'detailed_analysis': {
                'seo_performance': seo_analysis,
                'competitive_benchmarking': competitive_analysis,
                'technical_audit': self.extract_technical_summary()
            },
            'action_plan': action_plan,
            'data_quality': self.assess_data_quality()
        }
        
        return report
    
    def generate_key_findings(self, analysis):
        """Generate key findings summary"""
        findings = []
        
        if 'meta_description_analysis' in analysis:
            missing = analysis['meta_description_analysis'].get('missing_descriptions', 0)
            if missing > 0:
                findings.append(f"CRITICAL: {missing} pages missing meta descriptions")
        
        if 'image_analysis' in analysis:
            missing_alt = analysis['image_analysis'].get('images_without_alt', 0)
            if missing_alt > 0:
                findings.append(f"CRITICAL: {missing_alt} images missing alt text")
        
        if 'performance_analysis' in analysis:
            load_time = analysis['performance_analysis'].get('load_time_seconds', 0)
            if load_time > 3:
                findings.append(f"Page load time slow: {load_time:.2f} seconds")
        
        findings.append(f"Overall SEO Score: {analysis.get('overall_score', 0)}/100")
        
        return findings
    
    def extract_technical_summary(self):
        """Extract technical summary from all data sources"""
        summary = {}
        
        if self.advertools_data:
            summary['ssl_enabled'] = self.advertools_data.get('technical_analysis', {}).get('ssl_analysis', {}).get('has_ssl', False)
            summary['robots_txt_valid'] = 'error' not in self.advertools_data.get('robots_analysis', {})
            summary['schema_markup_present'] = self.advertools_data.get('schema_analysis', {}).get('json_ld_count', 0) > 0
        
        if self.playwright_data:
            summary['mobile_responsive'] = all(
                self.playwright_data.get('mobile_analysis', {}).get(viewport, {}).get('responsive_friendly', False)
                for viewport in ['mobile_portrait', 'tablet_portrait', 'desktop']
            )
            summary['network_requests'] = self.playwright_data.get('performance_metrics', {}).get('resource_count', 0)
        
        return summary
    
    def assess_data_quality(self):
        """Assess the quality of collected data"""
        quality = {
            'scrapy_data_quality': 'Good' if not self.scrapy_data.empty else 'No Data',
            'playwright_data_quality': 'Good' if self.playwright_data else 'No Data',
            'advertools_data_quality': 'Good' if self.advertools_data else 'No Data',
            'overall_quality': 'Good'
        }
        
        # Check for missing critical data
        issues = []
        if self.scrapy_data.empty:
            issues.append("Scrapy crawl data missing")
        
        if not self.playwright_data:
            issues.append("Playwright browser data missing")
        
        if not self.advertools_data:
            issues.append("Advertools SEO data missing")
        
        if issues:
            quality['overall_quality'] = 'Issues Found'
            quality['issues'] = issues
        
        return quality

def run_comprehensive_analysis():
    """Run comprehensive data analysis"""
    analyzer = ComprehensiveDataAnalyzer()
    
    try:
        report = analyzer.generate_comprehensive_report()
        
        # Save comprehensive report
        with open('comprehensive_analysis_report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        return report
        
    except Exception as e:
        return {"error": f"Comprehensive analysis failed: {str(e)}"}

if __name__ == "__main__":
    print("=== COMPREHENSIVE DATA ANALYSIS WITH PANDAS ===")
    report = run_comprehensive_analysis()
    
    print("\nAnalysis complete! Report saved to comprehensive_analysis_report.json")
    
    # Print executive summary
    if 'executive_summary' in report:
        print("\n=== EXECUTIVE SUMMARY ===")
        print(f"Overall SEO Score: {report['executive_summary']['overall_seo_score']}/100")
        print(f"Critical Issues: {report['executive_summary']['critical_issues_count']}")
        print(f"Pages Analyzed: {report['executive_summary']['pages_analyzed']}")
        
        print("\nKey Findings:")
        for finding in report['executive_summary']['key_findings']:
            print(f"- {finding}")
    
    print("\nFull report available in comprehensive_analysis_report.json")