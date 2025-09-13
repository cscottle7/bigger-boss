#!/usr/bin/env python3
"""
System Health Monitor - Automated System Reliability Framework
Ensures long-term functionality of all system components
"""

import os
import json
import time
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import requests
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class HealthCheck:
    name: str
    status: str  # 'healthy', 'warning', 'critical', 'unknown'
    message: str
    timestamp: datetime
    response_time: Optional[float] = None
    details: Optional[Dict] = None

class SystemHealthMonitor:
    """
    Comprehensive system health monitoring and maintenance
    """
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.parent
        self.reports_dir = self.base_dir / "system" / "maintenance" / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Load environment variables
        self.env_vars = self._load_env_vars()
        
        # Health check results
        self.health_results = []
        
    def _load_env_vars(self) -> Dict[str, str]:
        """Load environment variables from .env file"""
        env_file = self.base_dir / ".env"
        env_vars = {}
        
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()
        
        return env_vars
    
    async def run_comprehensive_health_check(self) -> Dict[str, any]:
        """Run all health checks and return comprehensive status"""
        logger.info("🔍 Starting comprehensive system health check")
        
        # Run all health checks
        checks = [
            self._check_api_connectivity(),
            self._check_file_system_health(),
            self._check_agent_configurations(),
            self._check_workflow_integrity(),
            self._check_performance_metrics(),
            self._check_dependencies()
        ]
        
        # Execute checks concurrently
        results = await asyncio.gather(*checks, return_exceptions=True)
        
        # Process results
        overall_status = self._determine_overall_status()
        
        # Generate report
        report = self._generate_health_report(overall_status)
        
        # Save report
        self._save_health_report(report)
        
        logger.info(f"✅ Health check complete. Overall status: {overall_status}")
        return report
    
    async def _check_api_connectivity(self) -> List[HealthCheck]:
        """Check all API endpoints for connectivity"""
        checks = []
        
        # SerpAPI Check
        if 'SERPAPI_API_KEY' in self.env_vars:
            check = await self._test_serpapi()
            checks.append(check)
        
        # Jina API Check
        if 'JINA_API_KEY' in self.env_vars:
            check = await self._test_jina_api()
            checks.append(check)
        
        # GTMetrix API Check
        if 'GTMETRIX_API_KEY' in self.env_vars:
            check = await self._test_gtmetrix_api()
            checks.append(check)
        
        return checks
    
    async def _test_serpapi(self) -> HealthCheck:
        """Test SerpAPI connectivity"""
        start_time = time.time()
        
        try:
            api_key = self.env_vars.get('SERPAPI_API_KEY')
            url = "https://serpapi.com/search"
            params = {
                'q': 'test query',
                'api_key': api_key,
                'num': 1
            }
            
            response = requests.get(url, params=params, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if 'search_metadata' in data:
                    return HealthCheck(
                        name="SerpAPI Connectivity",
                        status="healthy",
                        message="SerpAPI responding normally",
                        timestamp=datetime.now(),
                        response_time=response_time
                    )
            
            return HealthCheck(
                name="SerpAPI Connectivity",
                status="warning",
                message=f"Unexpected response: {response.status_code}",
                timestamp=datetime.now(),
                response_time=response_time
            )
            
        except Exception as e:
            return HealthCheck(
                name="SerpAPI Connectivity",
                status="critical",
                message=f"SerpAPI connection failed: {str(e)}",
                timestamp=datetime.now(),
                response_time=time.time() - start_time
            )
    
    async def _test_jina_api(self) -> HealthCheck:
        """Test Jina AI API connectivity"""
        start_time = time.time()
        
        try:
            api_key = self.env_vars.get('JINA_API_KEY')
            url = "https://api.jina.ai/v1/embeddings"
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            data = {
                'input': ['test'],
                'model': 'jina-embeddings-v2-base-en'
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                return HealthCheck(
                    name="Jina AI Connectivity",
                    status="healthy",
                    message="Jina AI API responding normally",
                    timestamp=datetime.now(),
                    response_time=response_time
                )
            
            return HealthCheck(
                name="Jina AI Connectivity",
                status="warning",
                message=f"Unexpected response: {response.status_code}",
                timestamp=datetime.now(),
                response_time=response_time
            )
            
        except Exception as e:
            return HealthCheck(
                name="Jina AI Connectivity",
                status="critical",
                message=f"Jina AI connection failed: {str(e)}",
                timestamp=datetime.now(),
                response_time=time.time() - start_time
            )
    
    async def _test_gtmetrix_api(self) -> HealthCheck:
        """Test GTMetrix API connectivity"""
        start_time = time.time()
        
        try:
            api_key = self.env_vars.get('GTMETRIX_API_KEY')
            url = "https://gtmetrix.com/api/2.0/status"
            
            response = requests.get(url, auth=(api_key, ''), timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                return HealthCheck(
                    name="GTMetrix API Connectivity",
                    status="healthy",
                    message="GTMetrix API responding normally",
                    timestamp=datetime.now(),
                    response_time=response_time
                )
            
            return HealthCheck(
                name="GTMetrix API Connectivity",
                status="warning",
                message=f"Unexpected response: {response.status_code}",
                timestamp=datetime.now(),
                response_time=response_time
            )
            
        except Exception as e:
            return HealthCheck(
                name="GTMetrix API Connectivity",
                status="critical",
                message=f"GTMetrix connection failed: {str(e)}",
                timestamp=datetime.now(),
                response_time=time.time() - start_time
            )
    
    async def _check_file_system_health(self) -> List[HealthCheck]:
        """Check file system integrity"""
        checks = []
        
        # Check critical directories
        critical_dirs = [
            "system/core_tools",
            "system/agents",
            "system/maintenance",
            "clients"
        ]
        
        for dir_path in critical_dirs:
            full_path = self.base_dir / dir_path
            if full_path.exists():
                checks.append(HealthCheck(
                    name=f"Directory: {dir_path}",
                    status="healthy",
                    message="Directory exists and accessible",
                    timestamp=datetime.now()
                ))
            else:
                checks.append(HealthCheck(
                    name=f"Directory: {dir_path}",
                    status="critical",
                    message="Critical directory missing",
                    timestamp=datetime.now()
                ))
        
        # Check critical files
        critical_files = [
            "CLAUDE.md",
            ".env",
            "system/core_tools/enhanced_api_integrations.py",
            "system/agents/ai_content_specialist.py"
        ]
        
        for file_path in critical_files:
            full_path = self.base_dir / file_path
            if full_path.exists():
                checks.append(HealthCheck(
                    name=f"File: {file_path}",
                    status="healthy",
                    message="File exists and accessible",
                    timestamp=datetime.now()
                ))
            else:
                checks.append(HealthCheck(
                    name=f"File: {file_path}",
                    status="critical",
                    message="Critical file missing",
                    timestamp=datetime.now()
                ))
        
        return checks
    
    async def _check_agent_configurations(self) -> List[HealthCheck]:
        """Check agent configuration validity"""
        checks = []
        
        # Check if agent files can be imported
        agent_files = [
            "system.agents.ai_content_specialist",
            "system.core_tools.enhanced_api_integrations",
            "system.core_tools.mandatory_date_research"
        ]
        
        for agent_module in agent_files:
            try:
                # Simulate import check
                module_path = self.base_dir / agent_module.replace('.', '/')
                if module_path.with_suffix('.py').exists():
                    checks.append(HealthCheck(
                        name=f"Agent Module: {agent_module}",
                        status="healthy",
                        message="Module file exists and accessible",
                        timestamp=datetime.now()
                    ))
                else:
                    checks.append(HealthCheck(
                        name=f"Agent Module: {agent_module}",
                        status="critical",
                        message="Module file missing",
                        timestamp=datetime.now()
                    ))
            except Exception as e:
                checks.append(HealthCheck(
                    name=f"Agent Module: {agent_module}",
                    status="critical",
                    message=f"Module error: {str(e)}",
                    timestamp=datetime.now()
                ))
        
        return checks
    
    async def _check_workflow_integrity(self) -> List[HealthCheck]:
        """Check workflow configuration integrity"""
        checks = []
        
        # Check CLAUDE.md compliance
        claude_md = self.base_dir / "CLAUDE.md"
        if claude_md.exists():
            with open(claude_md, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for key sections
            required_sections = [
                "Project Overview",
                "CLIENT FOLDER STRUCTURE",
                "Iterative Feedback Loop System",
                "Content Quality Standards"
            ]
            
            for section in required_sections:
                if section in content:
                    checks.append(HealthCheck(
                        name=f"CLAUDE.md Section: {section}",
                        status="healthy",
                        message="Required section present",
                        timestamp=datetime.now()
                    ))
                else:
                    checks.append(HealthCheck(
                        name=f"CLAUDE.md Section: {section}",
                        status="warning",
                        message="Required section missing or modified",
                        timestamp=datetime.now()
                    ))
        
        return checks
    
    async def _check_performance_metrics(self) -> List[HealthCheck]:
        """Check system performance metrics"""
        checks = []
        
        # Check disk space
        try:
            import shutil
            total, used, free = shutil.disk_usage(self.base_dir)
            free_percentage = (free / total) * 100
            
            if free_percentage > 20:
                status = "healthy"
                message = f"Disk space: {free_percentage:.1f}% free"
            elif free_percentage > 10:
                status = "warning"
                message = f"Low disk space: {free_percentage:.1f}% free"
            else:
                status = "critical"
                message = f"Critical disk space: {free_percentage:.1f}% free"
            
            checks.append(HealthCheck(
                name="Disk Space",
                status=status,
                message=message,
                timestamp=datetime.now()
            ))
        except Exception as e:
            checks.append(HealthCheck(
                name="Disk Space",
                status="unknown",
                message=f"Cannot check disk space: {str(e)}",
                timestamp=datetime.now()
            ))
        
        return checks
    
    async def _check_dependencies(self) -> List[HealthCheck]:
        """Check system dependencies"""
        checks = []
        
        # Check Python packages
        required_packages = [
            'requests',
            'asyncio',
            'pathlib',
            'json',
            'datetime'
        ]
        
        for package in required_packages:
            try:
                __import__(package)
                checks.append(HealthCheck(
                    name=f"Python Package: {package}",
                    status="healthy",
                    message="Package available",
                    timestamp=datetime.now()
                ))
            except ImportError:
                checks.append(HealthCheck(
                    name=f"Python Package: {package}",
                    status="critical",
                    message="Package missing",
                    timestamp=datetime.now()
                ))
        
        return checks
    
    def _determine_overall_status(self) -> str:
        """Determine overall system status from individual checks"""
        if not self.health_results:
            return "unknown"
        
        critical_count = sum(1 for check in self.health_results if check.status == "critical")
        warning_count = sum(1 for check in self.health_results if check.status == "warning")
        
        if critical_count > 0:
            return "critical"
        elif warning_count > 0:
            return "warning"
        else:
            return "healthy"
    
    def _generate_health_report(self, overall_status: str) -> Dict:
        """Generate comprehensive health report"""
        return {
            "timestamp": datetime.now().isoformat(),
            "overall_status": overall_status,
            "summary": {
                "total_checks": len(self.health_results),
                "healthy": sum(1 for c in self.health_results if c.status == "healthy"),
                "warning": sum(1 for c in self.health_results if c.status == "warning"),
                "critical": sum(1 for c in self.health_results if c.status == "critical"),
                "unknown": sum(1 for c in self.health_results if c.status == "unknown")
            },
            "checks": [
                {
                    "name": check.name,
                    "status": check.status,
                    "message": check.message,
                    "timestamp": check.timestamp.isoformat(),
                    "response_time": check.response_time,
                    "details": check.details
                }
                for check in self.health_results
            ],
            "recommendations": self._generate_recommendations()
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations based on health checks"""
        recommendations = []
        
        critical_checks = [c for c in self.health_results if c.status == "critical"]
        warning_checks = [c for c in self.health_results if c.status == "warning"]
        
        if critical_checks:
            recommendations.append("🚨 CRITICAL ISSUES DETECTED - Immediate attention required")
            for check in critical_checks:
                recommendations.append(f"  - Fix: {check.name} - {check.message}")
        
        if warning_checks:
            recommendations.append("⚠️  Warning issues detected - Schedule maintenance")
            for check in warning_checks:
                recommendations.append(f"  - Review: {check.name} - {check.message}")
        
        # API-specific recommendations
        api_issues = [c for c in self.health_results if "API" in c.name and c.status != "healthy"]
        if api_issues:
            recommendations.append("🔌 API Issues detected:")
            recommendations.append("  - Verify API keys in .env file")
            recommendations.append("  - Check API service status")
            recommendations.append("  - Review API usage limits")
        
        return recommendations
    
    def _save_health_report(self, report: Dict):
        """Save health report to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"health_report_{timestamp}.json"
        filepath = self.reports_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        # Also save as latest report
        latest_filepath = self.reports_dir / "latest_health_report.json"
        with open(latest_filepath, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"Health report saved to {filepath}")

# CLI Interface
if __name__ == "__main__":
    async def main():
        monitor = SystemHealthMonitor()
        report = await monitor.run_comprehensive_health_check()
        
        print(f"\n{'='*60}")
        print(f"🏥 SYSTEM HEALTH REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        print(f"Overall Status: {report['overall_status'].upper()}")
        print(f"Total Checks: {report['summary']['total_checks']}")
        print(f"✅ Healthy: {report['summary']['healthy']}")
        print(f"⚠️  Warning: {report['summary']['warning']}")
        print(f"🚨 Critical: {report['summary']['critical']}")
        
        if report['recommendations']:
            print(f"\n📋 RECOMMENDATIONS:")
            for rec in report['recommendations']:
                print(rec)
        
        print(f"\nDetailed report saved to: system/maintenance/reports/")
    
    asyncio.run(main())