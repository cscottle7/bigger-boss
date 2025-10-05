#!/usr/bin/env python3
"""
Bigger Boss Agent System - Performance Monitor Hook
Tracks system performance, response times, and resource usage for optimization.

Usage: Called automatically by hook system during agent operations
"""

import argparse
import json
import logging
import os
import psutil
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """System performance monitoring and optimization tracking."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.logs_dir = self.project_root / '.claude' / 'logs'
        self.logs_dir.mkdir(exist_ok=True)

        self.performance_log = self.logs_dir / 'performance_metrics.jsonl'
        self.alerts_log = self.logs_dir / 'performance_alerts.log'

        # Performance thresholds
        self.thresholds = {
            'response_time_warning': 30.0,  # seconds
            'response_time_critical': 60.0,  # seconds
            'memory_usage_warning': 80.0,  # percentage
            'memory_usage_critical': 90.0,  # percentage
            'cpu_usage_warning': 80.0,  # percentage
            'cpu_usage_critical': 95.0,  # percentage
            'disk_usage_warning': 85.0,  # percentage
            'disk_usage_critical': 95.0  # percentage
        }

    def get_system_metrics(self) -> Dict:
        """Collect current system performance metrics."""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()

            # Memory metrics
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_available = memory.available / (1024**3)  # GB
            memory_total = memory.total / (1024**3)  # GB

            # Disk metrics
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_free = disk.free / (1024**3)  # GB
            disk_total = disk.total / (1024**3)  # GB

            # Process-specific metrics
            process = psutil.Process()
            process_memory = process.memory_info().rss / (1024**2)  # MB
            process_cpu = process.cpu_percent()

            return {
                'cpu_percent': cpu_percent,
                'cpu_count': cpu_count,
                'memory_percent': memory_percent,
                'memory_available_gb': round(memory_available, 2),
                'memory_total_gb': round(memory_total, 2),
                'disk_percent': disk_percent,
                'disk_free_gb': round(disk_free, 2),
                'disk_total_gb': round(disk_total, 2),
                'process_memory_mb': round(process_memory, 2),
                'process_cpu_percent': process_cpu
            }

        except Exception as e:
            logger.error(f"Failed to collect system metrics: {e}")
            return {}

    def record_agent_performance(
        self,
        agent_name: str,
        operation: str,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
        success: bool = True,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """Record agent performance metrics."""
        try:
            # Calculate timing
            if start_time and end_time:
                response_time = end_time - start_time
            else:
                response_time = None

            # Collect system metrics
            system_metrics = self.get_system_metrics()

            # Create performance record
            performance_record = {
                'timestamp': datetime.now().isoformat(),
                'agent_name': agent_name,
                'operation': operation,
                'response_time_seconds': response_time,
                'success': success,
                'system_metrics': system_metrics,
                'metadata': metadata or {}
            }

            # Write to performance log
            with open(self.performance_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(performance_record) + '\n')

            # Check for performance alerts
            self.check_performance_alerts(performance_record)

            return performance_record

        except Exception as e:
            logger.error(f"Failed to record agent performance: {e}")
            return {}

    def check_performance_alerts(self, record: Dict) -> None:
        """Check performance record against thresholds and generate alerts."""
        try:
            alerts = []

            # Check response time
            response_time = record.get('response_time_seconds')
            if response_time:
                if response_time >= self.thresholds['response_time_critical']:
                    alerts.append({
                        'level': 'CRITICAL',
                        'metric': 'response_time',
                        'value': response_time,
                        'threshold': self.thresholds['response_time_critical'],
                        'message': f"Agent {record['agent_name']} took {response_time:.2f}s (critical threshold: {self.thresholds['response_time_critical']}s)"
                    })
                elif response_time >= self.thresholds['response_time_warning']:
                    alerts.append({
                        'level': 'WARNING',
                        'metric': 'response_time',
                        'value': response_time,
                        'threshold': self.thresholds['response_time_warning'],
                        'message': f"Agent {record['agent_name']} took {response_time:.2f}s (warning threshold: {self.thresholds['response_time_warning']}s)"
                    })

            # Check system metrics
            system_metrics = record.get('system_metrics', {})

            # Memory usage
            memory_percent = system_metrics.get('memory_percent')
            if memory_percent:
                if memory_percent >= self.thresholds['memory_usage_critical']:
                    alerts.append({
                        'level': 'CRITICAL',
                        'metric': 'memory_usage',
                        'value': memory_percent,
                        'threshold': self.thresholds['memory_usage_critical'],
                        'message': f"Memory usage critical: {memory_percent:.1f}%"
                    })
                elif memory_percent >= self.thresholds['memory_usage_warning']:
                    alerts.append({
                        'level': 'WARNING',
                        'metric': 'memory_usage',
                        'value': memory_percent,
                        'threshold': self.thresholds['memory_usage_warning'],
                        'message': f"Memory usage high: {memory_percent:.1f}%"
                    })

            # CPU usage
            cpu_percent = system_metrics.get('cpu_percent')
            if cpu_percent:
                if cpu_percent >= self.thresholds['cpu_usage_critical']:
                    alerts.append({
                        'level': 'CRITICAL',
                        'metric': 'cpu_usage',
                        'value': cpu_percent,
                        'threshold': self.thresholds['cpu_usage_critical'],
                        'message': f"CPU usage critical: {cpu_percent:.1f}%"
                    })
                elif cpu_percent >= self.thresholds['cpu_usage_warning']:
                    alerts.append({
                        'level': 'WARNING',
                        'metric': 'cpu_usage',
                        'value': cpu_percent,
                        'threshold': self.thresholds['cpu_usage_warning'],
                        'message': f"CPU usage high: {cpu_percent:.1f}%"
                    })

            # Disk usage
            disk_percent = system_metrics.get('disk_percent')
            if disk_percent:
                if disk_percent >= self.thresholds['disk_usage_critical']:
                    alerts.append({
                        'level': 'CRITICAL',
                        'metric': 'disk_usage',
                        'value': disk_percent,
                        'threshold': self.thresholds['disk_usage_critical'],
                        'message': f"Disk usage critical: {disk_percent:.1f}%"
                    })
                elif disk_percent >= self.thresholds['disk_usage_warning']:
                    alerts.append({
                        'level': 'WARNING',
                        'metric': 'disk_usage',
                        'value': disk_percent,
                        'threshold': self.thresholds['disk_usage_warning'],
                        'message': f"Disk usage high: {disk_percent:.1f}%"
                    })

            # Log alerts
            if alerts:
                with open(self.alerts_log, 'a', encoding='utf-8') as f:
                    for alert in alerts:
                        alert_record = {
                            'timestamp': datetime.now().isoformat(),
                            'agent_name': record['agent_name'],
                            'operation': record['operation'],
                            **alert
                        }
                        f.write(json.dumps(alert_record) + '\n')

                        # Also log to console for immediate visibility
                        logger.warning(f"🚨 PERFORMANCE ALERT [{alert['level']}]: {alert['message']}")

        except Exception as e:
            logger.error(f"Failed to check performance alerts: {e}")

    def get_performance_summary(self, hours: int = 24) -> Dict:
        """Get performance summary for the specified time period."""
        try:
            if not self.performance_log.exists():
                return {'error': 'No performance data available'}

            # Read performance data
            records = []
            cutoff_time = datetime.now().timestamp() - (hours * 3600)

            with open(self.performance_log, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        record = json.loads(line.strip())
                        record_time = datetime.fromisoformat(record['timestamp']).timestamp()
                        if record_time >= cutoff_time:
                            records.append(record)
                    except (json.JSONDecodeError, KeyError, ValueError):
                        continue

            if not records:
                return {'error': 'No recent performance data'}

            # Calculate summary statistics
            response_times = [r.get('response_time_seconds') for r in records if r.get('response_time_seconds')]
            success_count = sum(1 for r in records if r.get('success', True))

            # Agent breakdown
            agent_stats = {}
            for record in records:
                agent_name = record.get('agent_name', 'unknown')
                if agent_name not in agent_stats:
                    agent_stats[agent_name] = {
                        'operations': 0,
                        'successes': 0,
                        'response_times': []
                    }

                agent_stats[agent_name]['operations'] += 1
                if record.get('success', True):
                    agent_stats[agent_name]['successes'] += 1

                if record.get('response_time_seconds'):
                    agent_stats[agent_name]['response_times'].append(record['response_time_seconds'])

            # Calculate agent summaries
            for agent_name, stats in agent_stats.items():
                if stats['response_times']:
                    stats['avg_response_time'] = sum(stats['response_times']) / len(stats['response_times'])
                    stats['max_response_time'] = max(stats['response_times'])
                    stats['min_response_time'] = min(stats['response_times'])
                else:
                    stats['avg_response_time'] = None
                    stats['max_response_time'] = None
                    stats['min_response_time'] = None

                stats['success_rate'] = (stats['successes'] / stats['operations'] * 100) if stats['operations'] > 0 else 0
                del stats['response_times']  # Remove raw data

            return {
                'period_hours': hours,
                'total_operations': len(records),
                'success_rate': (success_count / len(records) * 100) if records else 0,
                'avg_response_time': sum(response_times) / len(response_times) if response_times else None,
                'max_response_time': max(response_times) if response_times else None,
                'min_response_time': min(response_times) if response_times else None,
                'agent_breakdown': agent_stats,
                'system_health': self.get_system_metrics()
            }

        except Exception as e:
            logger.error(f"Failed to generate performance summary: {e}")
            return {'error': str(e)}

    def cleanup_old_logs(self, days_to_keep: int = 30) -> int:
        """Clean up old performance logs."""
        try:
            cleaned_count = 0
            cutoff_time = datetime.now().timestamp() - (days_to_keep * 24 * 3600)

            # Clean performance log
            if self.performance_log.exists():
                temp_file = self.performance_log.with_suffix('.tmp')

                with open(self.performance_log, 'r', encoding='utf-8') as infile:
                    with open(temp_file, 'w', encoding='utf-8') as outfile:
                        for line in infile:
                            try:
                                record = json.loads(line.strip())
                                record_time = datetime.fromisoformat(record['timestamp']).timestamp()
                                if record_time >= cutoff_time:
                                    outfile.write(line)
                                else:
                                    cleaned_count += 1
                            except (json.JSONDecodeError, KeyError, ValueError):
                                # Keep malformed records to avoid data loss
                                outfile.write(line)

                # Replace original file
                temp_file.replace(self.performance_log)

            # Clean alerts log
            if self.alerts_log.exists():
                temp_file = self.alerts_log.with_suffix('.tmp')

                with open(self.alerts_log, 'r', encoding='utf-8') as infile:
                    with open(temp_file, 'w', encoding='utf-8') as outfile:
                        for line in infile:
                            try:
                                record = json.loads(line.strip())
                                record_time = datetime.fromisoformat(record['timestamp']).timestamp()
                                if record_time >= cutoff_time:
                                    outfile.write(line)
                            except (json.JSONDecodeError, KeyError, ValueError):
                                outfile.write(line)

                temp_file.replace(self.alerts_log)

            logger.info(f"Cleaned up {cleaned_count} old performance records")
            return cleaned_count

        except Exception as e:
            logger.error(f"Failed to cleanup old logs: {e}")
            return 0


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(
        description='Bigger Boss Performance Monitor'
    )

    parser.add_argument('--agent', required=True, help='Agent name')
    parser.add_argument('--operation', default='unknown', help='Operation type')
    parser.add_argument('--start-time', type=float, help='Start timestamp')
    parser.add_argument('--end-time', type=float, help='End timestamp')
    parser.add_argument('--success', type=bool, default=True, help='Operation success status')
    parser.add_argument('--memory-usage', action='store_true', help='Include memory usage tracking')
    parser.add_argument('--summary', type=int, help='Show performance summary for N hours')
    parser.add_argument('--cleanup', type=int, help='Clean up logs older than N days')

    args = parser.parse_args()

    monitor = PerformanceMonitor()

    try:
        if args.summary:
            summary = monitor.get_performance_summary(args.summary)
            print(json.dumps(summary, indent=2))

        elif args.cleanup:
            cleaned = monitor.cleanup_old_logs(args.cleanup)
            print(f"Cleaned up {cleaned} old records")

        else:
            # Record performance
            record = monitor.record_agent_performance(
                agent_name=args.agent,
                operation=args.operation,
                start_time=args.start_time,
                end_time=args.end_time,
                success=args.success
            )

            if record:
                print(f"✅ Performance recorded for {args.agent}")
            else:
                print(f"❌ Failed to record performance for {args.agent}")
                sys.exit(1)

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()