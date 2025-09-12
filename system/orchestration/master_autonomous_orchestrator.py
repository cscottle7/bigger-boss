"""
Master Autonomous Orchestrator
Central coordinator for all autonomous analysis operations
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import json

# Core system imports
from system.orchestration.autonomous_operation_manager import autonomous_manager
from system.orchestration.natural_language_processor import nlp_processor
from system.core_tools.error_recovery_system import error_recovery_system, with_error_recovery
from system.core_tools.comprehensive_seo_crawler import ComprehensiveSEOCrawler
from system.core_tools.api_integrations import gtmetrix_api, serpapi_integration, google_api

class MasterAutonomousOrchestrator:
    """Master orchestrator for autonomous website analysis operations"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        
    def setup_logging(self):
        """Setup comprehensive logging for autonomous operations"""
        log_dir = Path("system/reports")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create orchestrator handler
        handler = logging.FileHandler(
            log_dir / f"autonomous_orchestrator_{datetime.now().strftime('%Y%m%d')}.log"
        )
        handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        self.logger.addHandler(handler)
    
    async def execute_autonomous_analysis(self, command: str) -> Tuple[bool, Dict]:
        """
        Execute autonomous analysis based on natural language command
        Main entry point for autonomous operations
        """
        self.logger.info(f"Starting autonomous analysis: {command}")
        
        try:
            # Process the natural language command
            success, result = await nlp_processor.process_command(command)
            
            if not success:
                self.logger.error(f"Command processing failed: {result}")
                return False, result
            
            # Execute the analysis with error recovery
            analysis_result = await self._execute_comprehensive_analysis(result)
            
            # Generate executive summary
            executive_summary = self._generate_executive_summary(analysis_result)
            
            # Log completion
            autonomous_manager.log_operation(
                'autonomous_analysis',
                'completed',
                {
                    'command': command,
                    'domain': result.get('analysis_config', {}).get('domain'),
                    'analysis_types': list(analysis_result.get('results', {}).keys()),
                    'success': True
                }
            )
            
            return True, {
                'success': True,
                'command': command,
                'analysis_result': analysis_result,
                'executive_summary': executive_summary,
                'session_status': autonomous_manager.get_session_status(),
                'error_summary': error_recovery_system.get_error_summary()
            }
            
        except Exception as e:
            self.logger.error(f"Autonomous analysis failed: {e}")
            
            # Log the failure
            autonomous_manager.log_operation(
                'autonomous_analysis',
                'failed',
                {
                    'command': command,
                    'error': str(e)
                }
            )
            
            return False, {
                'success': False,
                'error': str(e),
                'command': command,
                'session_status': autonomous_manager.get_session_status()
            }
    
    @with_error_recovery(max_retries=2, backoff_factor=3.0)
    async def _execute_comprehensive_analysis(self, command_result: Dict) -> Dict:
        """Execute comprehensive analysis with error recovery"""
        
        analysis_config = command_result.get('analysis_config', {})
        domain = analysis_config.get('domain')
        client_domain = domain.replace('.', '_').replace('-', '_') if domain else 'unknown'
        
        results = {
            'domain': domain,
            'client_domain': client_domain,
            'analysis_timestamp': datetime.now().isoformat(),
            'results': {}
        }
        
        # Execute SEO analysis if requested
        if 'seo_analysis' in command_result.get('results', {}):
            self.logger.info(f"Executing SEO analysis for {domain}")
            seo_result = await self._execute_seo_analysis_with_recovery(
                analysis_config['full_url'],
                analysis_config.get('page_limit', 50),
                client_domain
            )
            results['results']['seo_analysis'] = seo_result
        
        # Execute performance analysis if requested  
        if 'performance_analysis' in command_result.get('results', {}):
            self.logger.info(f"Executing performance analysis for {domain}")
            perf_result = await self._execute_performance_analysis_with_recovery(
                analysis_config['full_url'],
                client_domain
            )
            results['results']['performance_analysis'] = perf_result
        
        # Execute competitive analysis if requested
        if 'competitive_analysis' in command_result.get('results', {}):
            self.logger.info(f"Executing competitive analysis for {domain}")
            comp_result = await self._execute_competitive_analysis_with_recovery(
                domain,
                client_domain
            )
            results['results']['competitive_analysis'] = comp_result
        
        # Save comprehensive analysis report
        await self._save_comprehensive_report(results, client_domain)
        
        return results
    
    @with_error_recovery(max_retries=3, backoff_factor=2.0)
    async def _execute_seo_analysis_with_recovery(self, url: str, page_limit: int, client_domain: str) -> Dict:
        """Execute SEO analysis with error recovery"""
        
        # Check permissions
        can_crawl, message = autonomous_manager.can_perform_operation('web_crawling')
        if not can_crawl:
            return {'status': 'error', 'error': message}
        
        # Create and execute crawler
        crawler = ComprehensiveSEOCrawler(
            url,
            max_pages=page_limit,
            client_domain=client_domain,
            autonomous=True
        )
        
        # Track concurrent operations
        autonomous_manager.session_tracker.increment('concurrent_crawls', 1)
        autonomous_manager.session_tracker.increment('analysis_runs', 1)
        
        try:
            report, report_file = await crawler.crawl_all_pages()
            
            return {
                'status': 'success',
                'report_file': str(report_file),
                'summary': {
                    'pages_analyzed': report['scan_metadata']['pages_crawled'],
                    'average_seo_score': report['executive_summary']['average_seo_score'],
                    'critical_issues': report['executive_summary']['critical_issues'],
                    'warnings': report['executive_summary']['warnings'],
                    'pages_failed': report['scan_metadata']['pages_failed']
                },
                'detailed_results': report
            }
            
        finally:
            autonomous_manager.session_tracker.increment('concurrent_crawls', -1)
    
    @with_error_recovery(max_retries=2, backoff_factor=5.0)
    async def _execute_performance_analysis_with_recovery(self, url: str, client_domain: str) -> Dict:
        """Execute performance analysis with error recovery"""
        
        # Check API permissions
        can_api, message = autonomous_manager.can_perform_operation('api_calls', service='gtmetrix')
        if not can_api:
            return {'status': 'error', 'error': message}
        
        # Execute GTmetrix performance test
        result = await gtmetrix_api.test_website_performance(url, client_domain)
        
        return result
    
    @with_error_recovery(max_retries=2, backoff_factor=4.0)
    async def _execute_competitive_analysis_with_recovery(self, domain: str, client_domain: str) -> Dict:
        """Execute competitive analysis with error recovery"""
        
        # Check API permissions
        can_api, message = autonomous_manager.can_perform_operation('api_calls', service='serpapi')
        if not can_api:
            return {'status': 'error', 'error': message}
        
        # Generate keywords based on domain (simplified approach)
        keywords = self._generate_analysis_keywords(domain)
        
        # Execute competitive analysis
        result = await serpapi_integration.analyze_competitors(domain, keywords, client_domain)
        
        return result
    
    def _generate_analysis_keywords(self, domain: str) -> List[str]:
        """Generate relevant keywords for competitive analysis"""
        # Extract business type from domain (simplified approach)
        domain_parts = domain.replace('.com.au', '').replace('.com', '').split('.')
        main_domain = domain_parts[0] if domain_parts else domain
        
        # Generate basic keywords - in a full implementation this would be more sophisticated
        keywords = [
            main_domain,
            f"{main_domain} services",
            f"{main_domain} Sydney",
            f"{main_domain} Australia",
            "professional services Sydney"
        ]
        
        return keywords[:3]  # Limit to control API usage
    
    async def _save_comprehensive_report(self, results: Dict, client_domain: str) -> None:
        """Save comprehensive analysis report"""
        try:
            # Check file operation permissions
            client_folder = Path(f"clients/{client_domain}")
            can_write, message = autonomous_manager.can_perform_operation(
                'file_operations', 
                path=str(client_folder)
            )
            if not can_write:
                self.logger.error(f"Cannot save comprehensive report: {message}")
                return
            
            # Create client folder structure
            report_dir = client_folder / "reports"
            report_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate comprehensive report
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = report_dir / f"comprehensive_analysis_{timestamp}.json"
            
            # Add metadata
            report_data = {
                **results,
                'report_metadata': {
                    'generated_by': 'Master Autonomous Orchestrator',
                    'version': '1.0',
                    'generated_at': datetime.now().isoformat(),
                    'session_info': autonomous_manager.get_session_status()
                }
            }
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            # Track file operation
            autonomous_manager.session_tracker.increment('file_writes', 1)
            
            self.logger.info(f"Comprehensive analysis report saved: {report_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to save comprehensive report: {e}")
    
    def _generate_executive_summary(self, analysis_result: Dict) -> Dict:
        """Generate executive summary of analysis results"""
        summary = {
            'domain': analysis_result.get('domain'),
            'analysis_date': analysis_result.get('analysis_timestamp'),
            'analyses_performed': [],
            'key_findings': [],
            'recommendations': [],
            'overall_health_score': 0
        }
        
        results = analysis_result.get('results', {})
        scores = []
        
        # Process SEO analysis
        if 'seo_analysis' in results:
            seo_data = results['seo_analysis']
            if seo_data.get('status') == 'success':
                summary['analyses_performed'].append('Comprehensive SEO Analysis')
                seo_summary = seo_data.get('summary', {})
                
                avg_score = seo_summary.get('average_seo_score', 0)
                scores.append(avg_score)
                
                summary['key_findings'].append(
                    f"SEO Analysis: {seo_summary.get('pages_analyzed', 0)} pages analyzed, "
                    f"average SEO score {avg_score}/100"
                )
                
                if seo_summary.get('critical_issues', 0) > 0:
                    summary['recommendations'].append(
                        f"Address {seo_summary['critical_issues']} critical SEO issues immediately"
                    )
        
        # Process performance analysis
        if 'performance_analysis' in results:
            perf_data = results['performance_analysis']
            if perf_data.get('status') == 'success':
                summary['analyses_performed'].append('Performance Testing')
                perf_scores = perf_data.get('performance_scores', {})
                
                pagespeed = perf_scores.get('pagespeed_score', 0)
                if pagespeed:
                    scores.append(pagespeed)
                    summary['key_findings'].append(
                        f"Performance: PageSpeed score {pagespeed}/100"
                    )
        
        # Process competitive analysis
        if 'competitive_analysis' in results:
            comp_data = results['competitive_analysis']
            if comp_data.get('status') == 'success':
                summary['analyses_performed'].append('Competitive Analysis')
                competitors_data = comp_data.get('competitors_data', [])
                summary['key_findings'].append(
                    f"Competitive Analysis: {len(competitors_data)} keyword groups analyzed"
                )
        
        # Calculate overall health score
        if scores:
            summary['overall_health_score'] = round(sum(scores) / len(scores), 1)
        
        # Add general recommendations
        if summary['overall_health_score'] < 70:
            summary['recommendations'].append(
                "Website requires significant optimization - consider comprehensive SEO audit"
            )
        elif summary['overall_health_score'] < 85:
            summary['recommendations'].append(
                "Website performance is good but has room for improvement"
            )
        else:
            summary['recommendations'].append(
                "Website shows excellent performance - maintain current standards"
            )
        
        return summary
    
    def get_autonomous_capabilities(self) -> Dict:
        """Get summary of autonomous capabilities and current status"""
        return {
            'autonomous_operations': {
                'seo_crawling': autonomous_manager.can_perform_operation('web_crawling')[0],
                'performance_testing': autonomous_manager.can_perform_operation('api_calls', service='gtmetrix')[0],
                'competitive_analysis': autonomous_manager.can_perform_operation('api_calls', service='serpapi')[0],
                'file_operations': autonomous_manager.can_perform_operation('file_operations')[0]
            },
            'session_status': autonomous_manager.get_session_status(),
            'error_recovery': error_recovery_system.get_error_summary(),
            'supported_commands': nlp_processor.get_command_examples()
        }

# Global master orchestrator instance
master_orchestrator = MasterAutonomousOrchestrator()

# Convenience function for easy access
async def analyze_website_autonomously(command: str) -> Tuple[bool, Dict]:
    """Main entry point for autonomous website analysis"""
    return await master_orchestrator.execute_autonomous_analysis(command)