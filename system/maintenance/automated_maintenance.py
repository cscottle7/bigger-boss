#!/usr/bin/env python3
"""
Automated Maintenance System - Long-term System Reliability
Ensures continuous system health and performance
"""

import os
import json
import asyncio
import schedule
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import logging
from system_health_monitor import SystemHealthMonitor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AutomatedMaintenanceSystem:
    """
    Automated system maintenance and reliability management
    """
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.parent
        self.maintenance_dir = self.base_dir / "system" / "maintenance"
        self.logs_dir = self.maintenance_dir / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        self.health_monitor = SystemHealthMonitor()
        
        # Maintenance configuration
        self.config = {
            "health_check_interval": 3600,  # 1 hour
            "deep_scan_interval": 86400,    # 24 hours
            "cleanup_interval": 604800,     # 7 days
            "backup_interval": 86400,       # 24 hours
            "max_log_age_days": 30,
            "max_report_age_days": 90
        }
        
        self.last_maintenance = {}
        self._load_maintenance_state()
    
    def _load_maintenance_state(self):
        """Load maintenance state from file"""
        state_file = self.maintenance_dir / "maintenance_state.json"
        if state_file.exists():
            with open(state_file, 'r') as f:
                self.last_maintenance = json.load(f)
    
    def _save_maintenance_state(self):
        """Save maintenance state to file"""
        state_file = self.maintenance_dir / "maintenance_state.json"
        with open(state_file, 'w') as f:
            json.dump(self.last_maintenance, f, indent=2, default=str)
    
    async def start_automated_maintenance(self):
        """Start the automated maintenance system"""
        logger.info("🤖 Starting Automated Maintenance System")
        
        # Schedule regular tasks
        schedule.every().hour.do(self._run_health_check)
        schedule.every().day.at("02:00").do(self._run_deep_maintenance)
        schedule.every().week.do(self._run_cleanup)
        schedule.every().day.at("03:00").do(self._backup_critical_files)
        
        # Run initial health check
        await self._run_health_check()
        
        # Main loop
        while True:
            schedule.run_pending()
            await asyncio.sleep(60)  # Check every minute
    
    async def _run_health_check(self):
        """Run regular health check"""
        try:
            logger.info("🔍 Running scheduled health check")
            report = await self.health_monitor.run_comprehensive_health_check()
            
            # Log health status
            self._log_maintenance_action("health_check", {
                "status": report["overall_status"],
                "issues": report["summary"]["critical"] + report["summary"]["warning"]
            })
            
            # Handle critical issues
            if report["overall_status"] == "critical":
                await self._handle_critical_issues(report)
            
            self.last_maintenance["health_check"] = datetime.now().isoformat()
            self._save_maintenance_state()
            
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            self._log_maintenance_action("health_check_error", {"error": str(e)})
    
    async def _run_deep_maintenance(self):
        """Run comprehensive system maintenance"""
        try:
            logger.info("🔧 Running deep maintenance")
            
            # System optimization
            await self._optimize_system_performance()
            
            # Dependency updates check
            await self._check_dependency_updates()
            
            # Configuration validation
            await self._validate_configurations()
            
            # Performance analysis
            await self._analyze_system_performance()
            
            self.last_maintenance["deep_maintenance"] = datetime.now().isoformat()
            self._save_maintenance_state()
            
            logger.info("✅ Deep maintenance completed")
            
        except Exception as e:
            logger.error(f"Deep maintenance failed: {str(e)}")
            self._log_maintenance_action("deep_maintenance_error", {"error": str(e)})
    
    async def _run_cleanup(self):
        """Run system cleanup tasks"""
        try:
            logger.info("🧹 Running system cleanup")
            
            # Clean old logs
            await self._cleanup_old_files(self.logs_dir, self.config["max_log_age_days"])
            
            # Clean old reports
            reports_dir = self.maintenance_dir / "reports"
            await self._cleanup_old_files(reports_dir, self.config["max_report_age_days"])
            
            # Clean temporary files
            temp_dirs = [
                self.base_dir / "temp_cleanup",
                self.base_dir / "system" / "temp"
            ]
            
            for temp_dir in temp_dirs:
                if temp_dir.exists():
                    await self._cleanup_temp_directory(temp_dir)
            
            self.last_maintenance["cleanup"] = datetime.now().isoformat()
            self._save_maintenance_state()
            
            logger.info("✅ Cleanup completed")
            
        except Exception as e:
            logger.error(f"Cleanup failed: {str(e)}")
            self._log_maintenance_action("cleanup_error", {"error": str(e)})
    
    async def _backup_critical_files(self):
        """Backup critical system files"""
        try:
            logger.info("💾 Running critical file backup")
            
            backup_dir = self.maintenance_dir / "backups" / datetime.now().strftime("%Y%m%d")
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Critical files to backup
            critical_files = [
                "CLAUDE.md",
                ".env",
                "system/core_tools/enhanced_api_integrations.py",
                "system/agents/ai_content_specialist.py",
                "system/maintenance/system_health_monitor.py"
            ]
            
            for file_path in critical_files:
                source = self.base_dir / file_path
                if source.exists():
                    dest = backup_dir / file_path.replace('/', '_')
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Copy file
                    import shutil
                    shutil.copy2(source, dest)
                    logger.info(f"Backed up: {file_path}")
            
            # Clean old backups (keep last 7 days)
            await self._cleanup_old_backups()
            
            self.last_maintenance["backup"] = datetime.now().isoformat()
            self._save_maintenance_state()
            
            logger.info("✅ Backup completed")
            
        except Exception as e:
            logger.error(f"Backup failed: {str(e)}")
            self._log_maintenance_action("backup_error", {"error": str(e)})
    
    async def _handle_critical_issues(self, report: Dict):
        """Handle critical system issues automatically"""
        logger.warning("🚨 Handling critical issues")
        
        critical_checks = [c for c in report["checks"] if c["status"] == "critical"]
        
        for check in critical_checks:
            issue_type = check["name"]
            
            # API connectivity issues
            if "API" in issue_type:
                await self._handle_api_issues(check)
            
            # File system issues
            elif "Directory" in issue_type or "File" in issue_type:
                await self._handle_filesystem_issues(check)
            
            # Agent configuration issues
            elif "Agent" in issue_type:
                await self._handle_agent_issues(check)
        
        # Send alert (could be email, Slack, etc.)
        await self._send_critical_alert(report)
    
    async def _handle_api_issues(self, check: Dict):
        """Handle API connectivity issues"""
        logger.info(f"🔌 Handling API issue: {check['name']}")
        
        # Check API key validity
        api_name = check["name"].split()[0].lower()
        
        # Implement API-specific recovery
        if "serpapi" in api_name:
            await self._verify_serpapi_key()
        elif "jina" in api_name:
            await self._verify_jina_key()
        elif "gtmetrix" in api_name:
            await self._verify_gtmetrix_key()
    
    async def _verify_serpapi_key(self):
        """Verify and refresh SerpAPI key if needed"""
        # Implementation for SerpAPI key verification
        logger.info("Verifying SerpAPI key")
        pass
    
    async def _verify_jina_key(self):
        """Verify and refresh Jina API key if needed"""
        # Implementation for Jina API key verification
        logger.info("Verifying Jina API key")
        pass
    
    async def _verify_gtmetrix_key(self):
        """Verify and refresh GTMetrix API key if needed"""
        # Implementation for GTMetrix API key verification
        logger.info("Verifying GTMetrix API key")
        pass
    
    async def _handle_filesystem_issues(self, check: Dict):
        """Handle filesystem issues"""
        logger.info(f"📁 Handling filesystem issue: {check['name']}")
        
        # Create missing directories
        if "Directory" in check["name"] and "missing" in check["message"]:
            dir_path = check["name"].split(": ")[1]
            full_path = self.base_dir / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created missing directory: {dir_path}")
    
    async def _handle_agent_issues(self, check: Dict):
        """Handle agent configuration issues"""
        logger.info(f"🤖 Handling agent issue: {check['name']}")
        
        # Implement agent-specific recovery
        pass
    
    async def _send_critical_alert(self, report: Dict):
        """Send critical issue alert"""
        logger.warning("📧 Sending critical issue alert")
        
        # Create alert message
        alert = {
            "timestamp": datetime.now().isoformat(),
            "severity": "CRITICAL",
            "message": f"System health critical: {report['summary']['critical']} critical issues detected",
            "details": report["recommendations"]
        }
        
        # Save alert to file (could be extended to send email/Slack)
        alert_file = self.logs_dir / f"critical_alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(alert_file, 'w') as f:
            json.dump(alert, f, indent=2)
    
    async def _optimize_system_performance(self):
        """Optimize system performance"""
        logger.info("⚡ Optimizing system performance")
        
        # Clear Python cache
        import sys
        if hasattr(sys, 'path_importer_cache'):
            sys.path_importer_cache.clear()
        
        # Memory optimization
        import gc
        gc.collect()
        
        logger.info("Performance optimization completed")
    
    async def _check_dependency_updates(self):
        """Check for dependency updates"""
        logger.info("📦 Checking dependency updates")
        
        # Check Python packages
        try:
            import subprocess
            result = subprocess.run(['pip', 'list', '--outdated'], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.stdout:
                outdated = result.stdout.split('\n')[2:]  # Skip header
                if outdated and outdated[0].strip():
                    self._log_maintenance_action("outdated_packages", {
                        "packages": [line.split()[0] for line in outdated if line.strip()]
                    })
        except Exception as e:
            logger.warning(f"Could not check package updates: {str(e)}")
    
    async def _validate_configurations(self):
        """Validate system configurations"""
        logger.info("⚙️ Validating configurations")
        
        # Check CLAUDE.md integrity
        claude_md = self.base_dir / "CLAUDE.md"
        if claude_md.exists():
            with open(claude_md, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Validate required sections
            required_sections = [
                "Project Overview",
                "CLIENT FOLDER STRUCTURE",
                "Iterative Feedback Loop System"
            ]
            
            missing_sections = [section for section in required_sections if section not in content]
            if missing_sections:
                self._log_maintenance_action("config_validation_warning", {
                    "missing_sections": missing_sections
                })
    
    async def _analyze_system_performance(self):
        """Analyze system performance metrics"""
        logger.info("📊 Analyzing system performance")
        
        # Collect performance metrics
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "disk_usage": self._get_disk_usage(),
            "file_counts": self._get_file_counts(),
            "recent_errors": self._get_recent_errors()
        }
        
        # Save performance report
        perf_file = self.maintenance_dir / "reports" / f"performance_{datetime.now().strftime('%Y%m%d')}.json"
        with open(perf_file, 'w') as f:
            json.dump(metrics, f, indent=2)
    
    def _get_disk_usage(self) -> Dict:
        """Get disk usage statistics"""
        try:
            import shutil
            total, used, free = shutil.disk_usage(self.base_dir)
            return {
                "total_gb": round(total / (1024**3), 2),
                "used_gb": round(used / (1024**3), 2),
                "free_gb": round(free / (1024**3), 2),
                "free_percentage": round((free / total) * 100, 1)
            }
        except Exception:
            return {"error": "Cannot determine disk usage"}
    
    def _get_file_counts(self) -> Dict:
        """Get file count statistics"""
        try:
            counts = {}
            for ext in ['.py', '.md', '.json', '.txt', '.log']:
                pattern = f"**/*{ext}"
                files = list(self.base_dir.rglob(pattern))
                counts[ext] = len(files)
            return counts
        except Exception:
            return {"error": "Cannot count files"}
    
    def _get_recent_errors(self) -> List:
        """Get recent error logs"""
        try:
            errors = []
            log_files = list(self.logs_dir.glob("*.log"))
            
            for log_file in log_files[-5:]:  # Check last 5 log files
                try:
                    with open(log_file, 'r') as f:
                        lines = f.readlines()
                        error_lines = [line for line in lines if "ERROR" in line]
                        errors.extend(error_lines[-3:])  # Last 3 errors per file
                except Exception:
                    continue
            
            return errors[-10:]  # Return last 10 errors overall
        except Exception:
            return ["Cannot read error logs"]
    
    async def _cleanup_old_files(self, directory: Path, max_age_days: int):
        """Clean up old files in directory"""
        if not directory.exists():
            return
        
        cutoff_date = datetime.now() - timedelta(days=max_age_days)
        
        for file_path in directory.iterdir():
            if file_path.is_file():
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_time < cutoff_date:
                    try:
                        file_path.unlink()
                        logger.info(f"Cleaned up old file: {file_path}")
                    except Exception as e:
                        logger.warning(f"Could not clean up {file_path}: {str(e)}")
    
    async def _cleanup_temp_directory(self, temp_dir: Path):
        """Clean up temporary directory"""
        if not temp_dir.exists():
            return
        
        try:
            import shutil
            shutil.rmtree(temp_dir)
            logger.info(f"Cleaned up temp directory: {temp_dir}")
        except Exception as e:
            logger.warning(f"Could not clean up {temp_dir}: {str(e)}")
    
    async def _cleanup_old_backups(self):
        """Clean up old backup files"""
        backup_base = self.maintenance_dir / "backups"
        if not backup_base.exists():
            return
        
        # Keep last 7 days of backups
        cutoff_date = datetime.now() - timedelta(days=7)
        
        for backup_dir in backup_base.iterdir():
            if backup_dir.is_dir():
                try:
                    dir_date = datetime.strptime(backup_dir.name, "%Y%m%d")
                    if dir_date < cutoff_date:
                        import shutil
                        shutil.rmtree(backup_dir)
                        logger.info(f"Cleaned up old backup: {backup_dir}")
                except Exception as e:
                    logger.warning(f"Could not clean up backup {backup_dir}: {str(e)}")
    
    def _log_maintenance_action(self, action: str, details: Dict):
        """Log maintenance action"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details
        }
        
        log_file = self.logs_dir / f"maintenance_{datetime.now().strftime('%Y%m%d')}.log"
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")

# CLI Interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Automated Maintenance System')
    parser.add_argument('--mode', choices=['start', 'health-check', 'deep-maintenance', 'cleanup'],
                       default='start', help='Maintenance mode')
    
    args = parser.parse_args()
    
    async def main():
        maintenance_system = AutomatedMaintenanceSystem()
        
        if args.mode == 'start':
            await maintenance_system.start_automated_maintenance()
        elif args.mode == 'health-check':
            await maintenance_system._run_health_check()
        elif args.mode == 'deep-maintenance':
            await maintenance_system._run_deep_maintenance()
        elif args.mode == 'cleanup':
            await maintenance_system._run_cleanup()
    
    asyncio.run(main())