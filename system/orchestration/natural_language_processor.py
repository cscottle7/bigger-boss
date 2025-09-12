"""
Natural Language Processing Interface for Autonomous Operations
Interprets user commands and automatically triggers appropriate analysis workflows
"""

import re
import asyncio
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
import json

from system.orchestration.autonomous_operation_manager import autonomous_manager
from system.core_tools.comprehensive_seo_crawler import ComprehensiveSEOCrawler

class NaturalLanguageProcessor:
    """Processes natural language commands for autonomous website analysis"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.command_patterns = self._initialize_command_patterns()
        
    def _initialize_command_patterns(self) -> Dict:
        """Initialize regex patterns for different types of analysis commands"""
        return {
            'full_analysis': [
                r'analyze\s+(?:website\s+)?(?:https?://)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'audit\s+(?:website\s+)?(?:https?://)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'comprehensive\s+analysis\s+(?:of\s+)?(?:https?://)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'full\s+seo\s+audit\s+(?:for\s+)?(?:https?://)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
            ],
            'seo_only': [
                r'seo\s+analysis\s+(?:for\s+)?(?:https?://)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'check\s+seo\s+(?:for\s+)?(?:https?://)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'crawl\s+(?:https?://)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
            ],
            'performance_only': [
                r'performance\s+test\s+(?:https?://)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'speed\s+test\s+(?:https?://)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'page\s+speed\s+(?:analysis\s+)?(?:https?://)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
            ],
            'competitive_analysis': [
                r'competitor\s+analysis\s+(?:for\s+)?(?:https?://)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'competitive\s+audit\s+(?:https?://)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'compare\s+(?:https?://)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
            ],
            'with_page_limit': [
                r'(?:analyze|audit|crawl)\s+(?:https?://)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\s+(?:with\s+)?(\d+)\s+pages?',
                r'(?:analyze|audit|crawl)\s+(\d+)\s+pages?\s+(?:from\s+)?(?:https?://)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
            ]
        }
    
    async def process_command(self, command: str) -> Tuple[bool, Dict]:
        """
        Process natural language command and execute appropriate analysis
        Returns (success, result_dict)
        """
        command = command.lower().strip()
        self.logger.info(f"Processing command: {command}")
        
        # Extract domain and analysis type
        analysis_config = self._parse_command(command)
        
        if not analysis_config:
            return False, {
                'error': 'Could not understand the command. Try: "analyze website example.com"',
                'suggestions': [
                    'analyze website example.com',
                    'seo audit example.com',
                    'performance test example.com with 50 pages',
                    'competitor analysis example.com'
                ]
            }
        
        try:
            # Execute the appropriate analysis
            result = await self._execute_analysis(analysis_config)
            return True, result
            
        except Exception as e:
            self.logger.error(f"Analysis execution failed: {e}")
            return False, {
                'error': f"Analysis failed: {str(e)}",
                'command_parsed': analysis_config
            }
    
    def _parse_command(self, command: str) -> Optional[Dict]:
        """Parse command to extract domain, analysis type, and parameters"""
        
        # Check for page limit patterns first
        for pattern in self.command_patterns['with_page_limit']:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                groups = match.groups()
                if groups[0].isdigit():
                    domain, page_limit = groups[1], int(groups[0])
                else:
                    domain, page_limit = groups[0], int(groups[1])
                
                analysis_type = self._determine_analysis_type(command)
                return {
                    'domain': domain,
                    'analysis_type': analysis_type,
                    'page_limit': page_limit,
                    'full_url': self._construct_url(domain)
                }
        
        # Check other patterns
        for analysis_type, patterns in self.command_patterns.items():
            if analysis_type == 'with_page_limit':
                continue
                
            for pattern in patterns:
                match = re.search(pattern, command, re.IGNORECASE)
                if match:
                    domain = match.group(1)
                    return {
                        'domain': domain,
                        'analysis_type': analysis_type,
                        'page_limit': 50,  # Default page limit
                        'full_url': self._construct_url(domain)
                    }
        
        return None
    
    def _determine_analysis_type(self, command: str) -> str:
        """Determine analysis type from command when page limit is specified"""
        if any(keyword in command for keyword in ['seo', 'crawl']):
            return 'seo_only'
        elif any(keyword in command for keyword in ['performance', 'speed']):
            return 'performance_only'
        elif any(keyword in command for keyword in ['competitor', 'competitive', 'compare']):
            return 'competitive_analysis'
        else:
            return 'full_analysis'  # Default to full analysis
    
    def _construct_url(self, domain: str) -> str:
        """Construct full URL from domain"""
        if not domain.startswith(('http://', 'https://')):
            return f"https://{domain}"
        return domain
    
    async def _execute_analysis(self, config: Dict) -> Dict:
        """Execute the appropriate analysis based on configuration"""
        analysis_type = config['analysis_type']
        domain = config['domain']
        full_url = config['full_url']
        page_limit = config.get('page_limit', 50)
        
        # Log the autonomous operation
        autonomous_manager.log_operation(
            'natural_language_command',
            'starting',
            {
                'domain': domain,
                'analysis_type': analysis_type,
                'page_limit': page_limit
            }
        )
        
        results = {
            'analysis_config': config,
            'timestamp': datetime.now().isoformat(),
            'results': {}
        }
        
        if analysis_type in ['full_analysis', 'seo_only']:
            # Perform SEO crawling
            seo_results = await self._run_seo_analysis(full_url, page_limit, domain)
            results['results']['seo_analysis'] = seo_results
        
        if analysis_type in ['full_analysis', 'performance_only']:
            # Perform performance testing
            perf_results = await self._run_performance_analysis(full_url)
            results['results']['performance_analysis'] = perf_results
        
        if analysis_type in ['full_analysis', 'competitive_analysis']:
            # Perform competitive analysis
            comp_results = await self._run_competitive_analysis(domain)
            results['results']['competitive_analysis'] = comp_results
        
        # Log completion
        autonomous_manager.log_operation(
            'natural_language_command',
            'completed',
            {
                'domain': domain,
                'results_generated': list(results['results'].keys())
            }
        )
        
        return results
    
    async def _run_seo_analysis(self, url: str, page_limit: int, domain: str) -> Dict:
        """Run comprehensive SEO analysis"""
        try:
            # Check if we can perform web crawling
            can_crawl, message = autonomous_manager.can_perform_operation('web_crawling')
            if not can_crawl:
                return {'error': f"Cannot perform SEO analysis: {message}"}
            
            # Create and run crawler
            crawler = ComprehensiveSEOCrawler(
                url, 
                max_pages=page_limit, 
                client_domain=domain.replace('.', '_').replace('-', '_'),
                autonomous=True
            )
            
            # Track concurrent crawling
            autonomous_manager.session_tracker.increment('concurrent_crawls', 1)
            
            try:
                report, report_file = await crawler.crawl_all_pages()
                return {
                    'status': 'success',
                    'report_file': str(report_file),
                    'summary': {
                        'pages_analyzed': report['scan_metadata']['pages_crawled'],
                        'average_seo_score': report['executive_summary']['average_seo_score'],
                        'critical_issues': report['executive_summary']['critical_issues'],
                        'warnings': report['executive_summary']['warnings']
                    }
                }
            finally:
                # Release concurrent crawling counter
                autonomous_manager.session_tracker.increment('concurrent_crawls', -1)
                
        except Exception as e:
            return {'error': f"SEO analysis failed: {str(e)}"}
    
    async def _run_performance_analysis(self, url: str) -> Dict:
        """Run performance analysis (placeholder - would integrate with GTmetrix API)"""
        try:
            # Check API credentials
            if not credentials.has_service_credentials('gtmetrix'):
                return {
                    'status': 'skipped',
                    'reason': 'GTmetrix API credentials not configured'
                }
            
            # Placeholder for GTmetrix integration
            return {
                'status': 'todo',
                'message': 'Performance analysis integration coming soon'
            }
            
        except Exception as e:
            return {'error': f"Performance analysis failed: {str(e)}"}
    
    async def _run_competitive_analysis(self, domain: str) -> Dict:
        """Run competitive analysis (placeholder - would use SerpAPI)"""
        try:
            # Check API credentials
            if not credentials.has_service_credentials('serpapi'):
                return {
                    'status': 'skipped',
                    'reason': 'SerpAPI credentials not configured for competitive analysis'
                }
            
            # Placeholder for competitive analysis
            return {
                'status': 'todo',
                'message': 'Competitive analysis integration coming soon'
            }
            
        except Exception as e:
            return {'error': f"Competitive analysis failed: {str(e)}"}
    
    def get_command_examples(self) -> List[str]:
        """Get example commands for user reference"""
        return [
            "analyze website example.com",
            "seo audit example.com with 25 pages",
            "performance test example.com",
            "competitor analysis example.com",
            "comprehensive analysis of example.com with 100 pages",
            "crawl example.com",
            "speed test example.com"
        ]

# Global natural language processor instance
nlp_processor = NaturalLanguageProcessor()

# Convenience function for quick access
async def process_natural_command(command: str) -> Tuple[bool, Dict]:
    """Process a natural language command and return results"""
    return await nlp_processor.process_command(command)