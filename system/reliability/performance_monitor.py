"""
Advanced Performance Monitoring and Bottleneck Identification System
Real-time performance tracking, bottleneck detection, and optimisation recommendations
"""

import asyncio
import logging
import json
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable, Tuple
from pathlib import Path
from dataclasses import dataclass, field, asdict
from enum import Enum
import psutil
import statistics
from collections import deque, defaultdict
import functools
import resource
import gc

from system.orchestration.autonomous_operation_manager import autonomous_manager

class PerformanceMetric(Enum):
    """Types of performance metrics"""
    RESPONSE_TIME = "response_time"
    MEMORY_USAGE = "memory_usage"
    CPU_USAGE = "cpu_usage"
    DISK_IO = "disk_io"
    NETWORK_IO = "network_io"
    API_LATENCY = "api_latency"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    QUEUE_SIZE = "queue_size"

class BottleneckType(Enum):
    """Types of performance bottlenecks"""
    CPU_BOUND = "cpu_bound"
    MEMORY_BOUND = "memory_bound"
    IO_BOUND = "io_bound"
    NETWORK_BOUND = "network_bound"
    API_RATE_LIMITED = "api_rate_limited"
    CONCURRENCY_LIMITED = "concurrency_limited"
    DATABASE_SLOW = "database_slow"

class AlertLevel(Enum):
    """Performance alert levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

@dataclass
class PerformanceDataPoint:
    """Single performance measurement"""
    metric_type: PerformanceMetric
    value: float
    timestamp: datetime
    context: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)

@dataclass
class PerformanceAlert:
    """Performance alert"""
    alert_level: AlertLevel
    metric_type: PerformanceMetric
    current_value: float
    threshold_value: float
    message: str
    timestamp: datetime
    context: Dict[str, Any] = field(default_factory=dict)

@dataclass
class BottleneckAnalysis:
    """Bottleneck analysis result"""
    bottleneck_type: BottleneckType
    severity: float  # 0-1 scale
    affected_operations: List[str]
    root_cause: str
    recommendations: List[str]
    estimated_impact: str
    detected_at: datetime

class PerformanceThresholds:
    """Performance thresholds configuration"""
    
    def __init__(self):
        self.thresholds = {
            PerformanceMetric.RESPONSE_TIME: {
                'warning': 2.0,    # seconds
                'critical': 5.0,
                'emergency': 10.0
            },
            PerformanceMetric.MEMORY_USAGE: {
                'warning': 80.0,   # percentage
                'critical': 90.0,
                'emergency': 95.0
            },
            PerformanceMetric.CPU_USAGE: {
                'warning': 80.0,   # percentage
                'critical': 90.0,
                'emergency': 95.0
            },
            PerformanceMetric.ERROR_RATE: {
                'warning': 5.0,    # percentage
                'critical': 10.0,
                'emergency': 25.0
            },
            PerformanceMetric.API_LATENCY: {
                'warning': 3.0,    # seconds
                'critical': 8.0,
                'emergency': 15.0
            },
            PerformanceMetric.THROUGHPUT: {
                'warning': 10.0,   # operations/second (minimum)
                'critical': 5.0,
                'emergency': 1.0
            }
        }
    
    def get_alert_level(self, metric: PerformanceMetric, value: float) -> Optional[AlertLevel]:
        """Get alert level for metric value"""
        if metric not in self.thresholds:
            return None
        
        thresholds = self.thresholds[metric]
        
        # For throughput, lower values are worse
        if metric == PerformanceMetric.THROUGHPUT:
            if value <= thresholds['emergency']:
                return AlertLevel.EMERGENCY
            elif value <= thresholds['critical']:
                return AlertLevel.CRITICAL
            elif value <= thresholds['warning']:
                return AlertLevel.WARNING
            else:
                return None
        else:
            # For other metrics, higher values are worse
            if value >= thresholds['emergency']:
                return AlertLevel.EMERGENCY
            elif value >= thresholds['critical']:
                return AlertLevel.CRITICAL
            elif value >= thresholds['warning']:
                return AlertLevel.WARNING
            else:
                return None

class PerformanceCollector:
    """Collects performance metrics from various sources"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.Collector")
        self.collection_active = False
        self.collection_interval = 5.0  # seconds
        self.collection_thread = None
    
    def start_collection(self):
        """Start continuous performance data collection"""
        if self.collection_active:
            return
        
        self.collection_active = True
        self.collection_thread = threading.Thread(
            target=self._collection_loop,
            daemon=True
        )
        self.collection_thread.start()
        self.logger.info("Performance collection started")
    
    def stop_collection(self):
        """Stop performance data collection"""
        self.collection_active = False
        if self.collection_thread:
            self.collection_thread.join(timeout=5.0)
        self.logger.info("Performance collection stopped")
    
    def _collection_loop(self):
        """Main collection loop"""
        while self.collection_active:
            try:
                # Collect system metrics
                self._collect_system_metrics()
                
                # Collect application metrics
                self._collect_application_metrics()
                
                time.sleep(self.collection_interval)
            
            except Exception as e:
                self.logger.error(f"Error in performance collection: {e}")
                time.sleep(self.collection_interval)
    
    def _collect_system_metrics(self):
        """Collect system-level performance metrics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            performance_monitor.record_metric(
                PerformanceMetric.CPU_USAGE,
                cpu_percent,
                context={'cores': psutil.cpu_count()}
            )
            
            # Memory usage
            memory = psutil.virtual_memory()
            performance_monitor.record_metric(
                PerformanceMetric.MEMORY_USAGE,
                memory.percent,
                context={
                    'available_gb': memory.available / (1024**3),
                    'total_gb': memory.total / (1024**3)
                }
            )
            
            # Disk I/O
            disk_io = psutil.disk_io_counters()
            if disk_io:
                performance_monitor.record_metric(
                    PerformanceMetric.DISK_IO,
                    disk_io.read_bytes + disk_io.write_bytes,
                    context={
                        'read_bytes': disk_io.read_bytes,
                        'write_bytes': disk_io.write_bytes
                    }
                )
            
            # Network I/O
            network_io = psutil.net_io_counters()
            if network_io:
                performance_monitor.record_metric(
                    PerformanceMetric.NETWORK_IO,
                    network_io.bytes_sent + network_io.bytes_recv,
                    context={
                        'bytes_sent': network_io.bytes_sent,
                        'bytes_recv': network_io.bytes_recv
                    }
                )
        
        except Exception as e:
            self.logger.error(f"Error collecting system metrics: {e}")
    
    def _collect_application_metrics(self):
        """Collect application-specific metrics"""
        try:
            # Process-specific metrics
            process = psutil.Process()
            
            # Memory usage for this process
            memory_info = process.memory_info()
            performance_monitor.record_metric(
                PerformanceMetric.MEMORY_USAGE,
                (memory_info.rss / (1024**3)),  # GB
                context={'process_memory': True, 'pid': process.pid},
                tags=['process_specific']
            )
            
            # CPU usage for this process
            cpu_percent = process.cpu_percent()
            performance_monitor.record_metric(
                PerformanceMetric.CPU_USAGE,
                cpu_percent,
                context={'process_cpu': True, 'pid': process.pid},
                tags=['process_specific']
            )
            
            # Garbage collection statistics
            gc_stats = gc.get_stats()
            if gc_stats:
                performance_monitor.record_metric(
                    PerformanceMetric.MEMORY_USAGE,
                    len(gc.get_objects()),
                    context={'gc_objects': True, 'gc_stats': gc_stats},
                    tags=['garbage_collection']
                )
        
        except Exception as e:
            self.logger.error(f"Error collecting application metrics: {e}")

class BottleneckDetector:
    """Detects performance bottlenecks and provides analysis"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.BottleneckDetector")
        self.detection_rules = self._initialize_detection_rules()
    
    def _initialize_detection_rules(self) -> Dict[BottleneckType, Dict]:
        """Initialize bottleneck detection rules"""
        return {
            BottleneckType.CPU_BOUND: {
                'conditions': [
                    {'metric': PerformanceMetric.CPU_USAGE, 'threshold': 85.0, 'duration': 30},
                    {'metric': PerformanceMetric.RESPONSE_TIME, 'threshold': 3.0, 'duration': 30}
                ],
                'indicators': ['high_cpu_long_response']
            },
            BottleneckType.MEMORY_BOUND: {
                'conditions': [
                    {'metric': PerformanceMetric.MEMORY_USAGE, 'threshold': 85.0, 'duration': 30}
                ],
                'indicators': ['high_memory_usage', 'frequent_gc']
            },
            BottleneckType.IO_BOUND: {
                'conditions': [
                    {'metric': PerformanceMetric.DISK_IO, 'threshold': 100*1024*1024, 'duration': 30},  # 100MB/s
                    {'metric': PerformanceMetric.RESPONSE_TIME, 'threshold': 2.0, 'duration': 30}
                ],
                'indicators': ['high_disk_io', 'slow_file_operations']
            },
            BottleneckType.NETWORK_BOUND: {
                'conditions': [
                    {'metric': PerformanceMetric.NETWORK_IO, 'threshold': 50*1024*1024, 'duration': 30},  # 50MB/s
                    {'metric': PerformanceMetric.API_LATENCY, 'threshold': 5.0, 'duration': 30}
                ],
                'indicators': ['high_network_usage', 'api_timeouts']
            },
            BottleneckType.API_RATE_LIMITED: {
                'conditions': [
                    {'metric': PerformanceMetric.API_LATENCY, 'threshold': 10.0, 'duration': 60},
                    {'metric': PerformanceMetric.ERROR_RATE, 'threshold': 15.0, 'duration': 60}
                ],
                'indicators': ['api_rate_limit_errors', 'increasing_latency']
            }
        }
    
    def analyse_bottlenecks(
        self, 
        metrics_window: List[PerformanceDataPoint]
    ) -> List[BottleneckAnalysis]:
        """Analyse metrics window for bottlenecks"""
        bottlenecks = []
        
        # Group metrics by type
        metrics_by_type = defaultdict(list)
        for metric in metrics_window:
            metrics_by_type[metric.metric_type].append(metric)
        
        # Check each bottleneck type
        for bottleneck_type, rules in self.detection_rules.items():
            analysis = self._check_bottleneck_rules(
                bottleneck_type,
                rules,
                metrics_by_type
            )
            
            if analysis:
                bottlenecks.append(analysis)
        
        return bottlenecks
    
    def _check_bottleneck_rules(
        self,
        bottleneck_type: BottleneckType,
        rules: Dict,
        metrics_by_type: Dict[PerformanceMetric, List[PerformanceDataPoint]]
    ) -> Optional[BottleneckAnalysis]:
        """Check if bottleneck rules are met"""
        
        conditions_met = 0
        total_conditions = len(rules['conditions'])
        
        current_time = datetime.now()
        
        for condition in rules['conditions']:
            metric_type = condition['metric']
            threshold = condition['threshold']
            duration = condition['duration']
            
            if metric_type not in metrics_by_type:
                continue
            
            # Check if threshold exceeded for required duration
            recent_metrics = [
                m for m in metrics_by_type[metric_type]
                if (current_time - m.timestamp).total_seconds() <= duration
            ]
            
            if not recent_metrics:
                continue
            
            # Calculate statistics
            values = [m.value for m in recent_metrics]
            
            if metric_type == PerformanceMetric.THROUGHPUT:
                # For throughput, lower is worse
                if statistics.mean(values) <= threshold:
                    conditions_met += 1
            else:
                # For other metrics, higher is worse
                if statistics.mean(values) >= threshold:
                    conditions_met += 1
        
        # If majority of conditions met, we have a bottleneck
        if conditions_met >= (total_conditions * 0.6):  # 60% threshold
            return self._create_bottleneck_analysis(
                bottleneck_type,
                conditions_met / total_conditions,
                metrics_by_type
            )
        
        return None
    
    def _create_bottleneck_analysis(
        self,
        bottleneck_type: BottleneckType,
        severity: float,
        metrics_by_type: Dict[PerformanceMetric, List[PerformanceDataPoint]]
    ) -> BottleneckAnalysis:
        """Create bottleneck analysis with recommendations"""
        
        recommendations = self._get_bottleneck_recommendations(bottleneck_type)
        root_cause = self._identify_root_cause(bottleneck_type, metrics_by_type)
        affected_operations = self._identify_affected_operations(bottleneck_type)
        estimated_impact = self._estimate_impact(bottleneck_type, severity)
        
        return BottleneckAnalysis(
            bottleneck_type=bottleneck_type,
            severity=severity,
            affected_operations=affected_operations,
            root_cause=root_cause,
            recommendations=recommendations,
            estimated_impact=estimated_impact,
            detected_at=datetime.now()
        )
    
    def _get_bottleneck_recommendations(self, bottleneck_type: BottleneckType) -> List[str]:
        """Get recommendations for specific bottleneck type"""
        recommendations = {
            BottleneckType.CPU_BOUND: [
                "Consider implementing async/await for I/O operations",
                "Optimise CPU-intensive algorithms",
                "Add caching for expensive computations",
                "Scale horizontally or upgrade CPU resources"
            ],
            BottleneckType.MEMORY_BOUND: [
                "Implement memory-efficient data structures",
                "Add garbage collection optimisation",
                "Use streaming for large datasets",
                "Increase available memory or optimise memory usage"
            ],
            BottleneckType.IO_BOUND: [
                "Implement connection pooling",
                "Add caching for frequently accessed data",
                "Optimise database queries",
                "Use faster storage solutions (SSD)"
            ],
            BottleneckType.NETWORK_BOUND: [
                "Implement request batching",
                "Add CDN for static content",
                "Optimise API payload sizes",
                "Use compression for data transfer"
            ],
            BottleneckType.API_RATE_LIMITED: [
                "Implement exponential backoff",
                "Add request queuing and rate limiting",
                "Use multiple API keys if available",
                "Cache API responses where possible"
            ]
        }
        
        return recommendations.get(bottleneck_type, ["Monitor system performance and optimise as needed"])
    
    def _identify_root_cause(
        self,
        bottleneck_type: BottleneckType,
        metrics_by_type: Dict[PerformanceMetric, List[PerformanceDataPoint]]
    ) -> str:
        """Identify root cause of bottleneck"""
        
        # Analyse metric patterns to identify root cause
        if bottleneck_type == BottleneckType.CPU_BOUND:
            return "High CPU utilisation likely due to computational operations or inefficient algorithms"
        elif bottleneck_type == BottleneckType.MEMORY_BOUND:
            return "High memory usage possibly due to memory leaks, large datasets, or inefficient data structures"
        elif bottleneck_type == BottleneckType.IO_BOUND:
            return "High I/O operations likely due to frequent file access, database queries, or network requests"
        elif bottleneck_type == BottleneckType.API_RATE_LIMITED:
            return "API rate limiting detected, possibly due to exceeding quota or concurrent requests"
        else:
            return f"Performance bottleneck of type {bottleneck_type.value} detected"
    
    def _identify_affected_operations(self, bottleneck_type: BottleneckType) -> List[str]:
        """Identify operations likely affected by bottleneck"""
        
        affected_ops = {
            BottleneckType.CPU_BOUND: ["data_processing", "analysis_operations", "content_generation"],
            BottleneckType.MEMORY_BOUND: ["large_dataset_processing", "caching_operations", "report_generation"],
            BottleneckType.IO_BOUND: ["file_operations", "database_queries", "web_scraping"],
            BottleneckType.NETWORK_BOUND: ["api_requests", "web_scraping", "remote_data_access"],
            BottleneckType.API_RATE_LIMITED: ["search_operations", "performance_testing", "data_collection"]
        }
        
        return affected_ops.get(bottleneck_type, ["general_system_operations"])
    
    def _estimate_impact(self, bottleneck_type: BottleneckType, severity: float) -> str:
        """Estimate impact of bottleneck"""
        
        if severity >= 0.8:
            impact_level = "severe"
        elif severity >= 0.6:
            impact_level = "moderate"
        else:
            impact_level = "minor"
        
        return f"{impact_level.title()} impact on system performance ({severity*100:.0f}% severity)"

class PerformanceMonitor:
    """Main performance monitoring system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.data_points = deque(maxlen=10000)  # Keep last 10k data points
        self.alerts = deque(maxlen=1000)  # Keep last 1k alerts
        self.thresholds = PerformanceThresholds()
        self.collector = PerformanceCollector()
        self.bottleneck_detector = BottleneckDetector()
        self.monitoring_active = False
        self.setup_performance_logging()
    
    def setup_performance_logging(self):
        """Setup performance monitoring logs"""
        perf_log_dir = Path("system/reports/performance")
        perf_log_dir.mkdir(parents=True, exist_ok=True)
        
        perf_handler = logging.FileHandler(
            perf_log_dir / f"performance_{datetime.now().strftime('%Y%m%d')}.log"
        )
        perf_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        perf_handler.setFormatter(formatter)
        
        self.logger.addHandler(perf_handler)
    
    def start_monitoring(self):
        """Start performance monitoring"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.collector.start_collection()
        self.logger.info("Performance monitoring started")
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring_active = False
        self.collector.stop_collection()
        self.logger.info("Performance monitoring stopped")
    
    def record_metric(
        self,
        metric_type: PerformanceMetric,
        value: float,
        context: Dict[str, Any] = None,
        tags: List[str] = None
    ):
        """Record a performance metric"""
        
        data_point = PerformanceDataPoint(
            metric_type=metric_type,
            value=value,
            timestamp=datetime.now(),
            context=context or {},
            tags=tags or []
        )
        
        self.data_points.append(data_point)
        
        # Check for alerts
        alert_level = self.thresholds.get_alert_level(metric_type, value)
        if alert_level:
            self._create_alert(data_point, alert_level)
        
        # Log autonomous operation
        autonomous_manager.log_operation(
            'performance_monitoring',
            'metric_recorded',
            {
                'metric_type': metric_type.value,
                'value': value,
                'context': context or {},
                'alert_level': alert_level.value if alert_level else None
            }
        )
    
    def _create_alert(self, data_point: PerformanceDataPoint, alert_level: AlertLevel):
        """Create performance alert"""
        
        threshold_value = self.thresholds.thresholds[data_point.metric_type][alert_level.value]
        
        alert = PerformanceAlert(
            alert_level=alert_level,
            metric_type=data_point.metric_type,
            current_value=data_point.value,
            threshold_value=threshold_value,
            message=f"{data_point.metric_type.value} {alert_level.value}: {data_point.value:.2f} > {threshold_value:.2f}",
            timestamp=data_point.timestamp,
            context=data_point.context
        )
        
        self.alerts.append(alert)
        
        # Log alert
        self.logger.warning(f"Performance alert: {alert.message}")
        
        # Save alert if critical or emergency
        if alert_level in [AlertLevel.CRITICAL, AlertLevel.EMERGENCY]:
            self._save_critical_alert(alert)
    
    def _save_critical_alert(self, alert: PerformanceAlert):
        """Save critical alert to file"""
        try:
            alerts_dir = Path("system/reports/alerts")
            alerts_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = alert.timestamp.strftime('%Y%m%d_%H%M%S')
            alert_file = alerts_dir / f"performance_alert_{alert.alert_level.value}_{timestamp}.json"
            
            alert_data = asdict(alert)
            alert_data['timestamp'] = alert.timestamp.isoformat()
            
            with open(alert_file, 'w', encoding='utf-8') as f:
                json.dump(alert_data, f, indent=2, ensure_ascii=False, default=str)
            
            self.logger.info(f"Critical performance alert saved: {alert_file}")
        
        except Exception as e:
            self.logger.error(f"Failed to save critical alert: {e}")
    
    def get_recent_metrics(
        self,
        metric_type: PerformanceMetric = None,
        minutes: int = 60
    ) -> List[PerformanceDataPoint]:
        """Get recent performance metrics"""
        
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        
        recent_metrics = [
            dp for dp in self.data_points
            if dp.timestamp > cutoff_time
        ]
        
        if metric_type:
            recent_metrics = [
                dp for dp in recent_metrics
                if dp.metric_type == metric_type
            ]
        
        return recent_metrics
    
    def get_performance_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get performance summary for specified time period"""
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        recent_data = [
            dp for dp in self.data_points
            if dp.timestamp > cutoff_time
        ]
        
        recent_alerts = [
            alert for alert in self.alerts
            if alert.timestamp > cutoff_time
        ]
        
        # Group metrics by type
        metrics_by_type = defaultdict(list)
        for dp in recent_data:
            metrics_by_type[dp.metric_type].append(dp.value)
        
        # Calculate statistics
        summary = {
            'time_period_hours': hours,
            'total_data_points': len(recent_data),
            'total_alerts': len(recent_alerts),
            'alert_breakdown': defaultdict(int),
            'metric_statistics': {}
        }
        
        # Alert breakdown
        for alert in recent_alerts:
            summary['alert_breakdown'][alert.alert_level.value] += 1
        
        # Metric statistics
        for metric_type, values in metrics_by_type.items():
            if values:
                summary['metric_statistics'][metric_type.value] = {
                    'count': len(values),
                    'min': min(values),
                    'max': max(values),
                    'mean': statistics.mean(values),
                    'median': statistics.median(values),
                    'std_dev': statistics.stdev(values) if len(values) > 1 else 0
                }
        
        return summary
    
    async def run_bottleneck_analysis(self) -> List[BottleneckAnalysis]:
        """Run comprehensive bottleneck analysis"""
        
        # Get recent metrics (last hour)
        recent_metrics = self.get_recent_metrics(minutes=60)
        
        if not recent_metrics:
            return []
        
        # Run bottleneck detection
        bottlenecks = self.bottleneck_detector.analyse_bottlenecks(recent_metrics)
        
        # Save bottleneck analysis if any found
        if bottlenecks:
            self._save_bottleneck_analysis(bottlenecks)
        
        return bottlenecks
    
    def _save_bottleneck_analysis(self, bottlenecks: List[BottleneckAnalysis]):
        """Save bottleneck analysis to file"""
        try:
            analysis_dir = Path("system/reports/performance")
            analysis_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            analysis_file = analysis_dir / f"bottleneck_analysis_{timestamp}.json"
            
            analysis_data = {
                'analysis_timestamp': datetime.now().isoformat(),
                'bottlenecks_detected': len(bottlenecks),
                'bottlenecks': [asdict(b) for b in bottlenecks]
            }
            
            with open(analysis_file, 'w', encoding='utf-8') as f:
                json.dump(analysis_data, f, indent=2, ensure_ascii=False, default=str)
            
            self.logger.info(f"Bottleneck analysis saved: {analysis_file}")
        
        except Exception as e:
            self.logger.error(f"Failed to save bottleneck analysis: {e}")
    
    def generate_performance_report(self, hours: int = 24) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        
        summary = self.get_performance_summary(hours)
        
        # Get recent bottleneck analysis
        analysis_dir = Path("system/reports/performance")
        bottleneck_files = []
        
        if analysis_dir.exists():
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            for file_path in analysis_dir.glob("bottleneck_analysis_*.json"):
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_time > cutoff_time:
                    bottleneck_files.append(str(file_path))
        
        # Current system status
        current_status = {
            'monitoring_active': self.monitoring_active,
            'data_points_stored': len(self.data_points),
            'alerts_stored': len(self.alerts),
            'recent_bottleneck_analyses': len(bottleneck_files)
        }
        
        # Performance trends
        trends = self._analyse_performance_trends(hours)
        
        report = {
            'report_generated': datetime.now().isoformat(),
            'time_period_hours': hours,
            'current_status': current_status,
            'performance_summary': summary,
            'performance_trends': trends,
            'bottleneck_analysis_files': bottleneck_files,
            'recommendations': self._generate_performance_recommendations(summary, trends)
        }
        
        # Save report
        self._save_performance_report(report)
        
        return report
    
    def _analyse_performance_trends(self, hours: int) -> Dict[str, Any]:
        """Analyse performance trends over time period"""
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        # Get data points in time order
        recent_data = [
            dp for dp in sorted(self.data_points, key=lambda x: x.timestamp)
            if dp.timestamp > cutoff_time
        ]
        
        if len(recent_data) < 10:  # Need minimum data for trend analysis
            return {'insufficient_data': True}
        
        # Group by metric type and analyse trends
        trends = {}
        
        metrics_by_type = defaultdict(list)
        for dp in recent_data:
            metrics_by_type[dp.metric_type].append((dp.timestamp, dp.value))
        
        for metric_type, data_points in metrics_by_type.items():
            if len(data_points) < 5:
                continue
            
            # Simple trend analysis
            values = [dp[1] for dp in data_points]
            time_points = [(dp[0] - cutoff_time).total_seconds() for dp in data_points]
            
            # Calculate trend (simple linear regression)
            if len(values) > 1:
                # Calculate correlation between time and values
                mean_time = statistics.mean(time_points)
                mean_value = statistics.mean(values)
                
                numerator = sum((t - mean_time) * (v - mean_value) for t, v in zip(time_points, values))
                denominator = sum((t - mean_time) ** 2 for t in time_points)
                
                if denominator > 0:
                    slope = numerator / denominator
                    
                    trends[metric_type.value] = {
                        'trend_direction': 'increasing' if slope > 0 else 'decreasing',
                        'trend_strength': abs(slope),
                        'recent_average': statistics.mean(values[-10:]),  # Last 10 values
                        'overall_average': mean_value,
                        'data_points': len(values)
                    }
        
        return trends
    
    def _generate_performance_recommendations(
        self,
        summary: Dict[str, Any],
        trends: Dict[str, Any]
    ) -> List[str]:
        """Generate performance optimisation recommendations"""
        
        recommendations = []
        
        # Check alert levels
        alert_breakdown = summary.get('alert_breakdown', {})
        if alert_breakdown.get('critical', 0) > 0 or alert_breakdown.get('emergency', 0) > 0:
            recommendations.append("URGENT: Critical performance issues detected - immediate investigation required")
        
        # Check metric statistics
        metric_stats = summary.get('metric_statistics', {})
        
        if 'cpu_usage' in metric_stats:
            cpu_stats = metric_stats['cpu_usage']
            if cpu_stats['mean'] > 80:
                recommendations.append("High CPU usage detected - consider optimising CPU-intensive operations")
        
        if 'memory_usage' in metric_stats:
            memory_stats = metric_stats['memory_usage']
            if memory_stats['mean'] > 80:
                recommendations.append("High memory usage detected - review memory allocation and consider optimisation")
        
        if 'response_time' in metric_stats:
            response_stats = metric_stats['response_time']
            if response_stats['mean'] > 2.0:
                recommendations.append("Slow response times detected - optimise critical path operations")
        
        # Check trends
        if not trends.get('insufficient_data'):
            for metric, trend_data in trends.items():
                if trend_data['trend_direction'] == 'increasing' and trend_data['trend_strength'] > 0.1:
                    if metric in ['cpu_usage', 'memory_usage', 'response_time']:
                        recommendations.append(f"Increasing trend detected in {metric} - monitor and optimise proactively")
        
        # General recommendations
        if len(recommendations) == 0:
            recommendations.append("Performance appears stable - continue monitoring")
        else:
            recommendations.append("Review performance logs and consider implementing recommended optimisations")
        
        return recommendations
    
    def _save_performance_report(self, report: Dict[str, Any]):
        """Save performance report to file"""
        try:
            reports_dir = Path("system/reports/performance")
            reports_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = reports_dir / f"performance_report_{timestamp}.json"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False, default=str)
            
            self.logger.info(f"Performance report saved: {report_file}")
        
        except Exception as e:
            self.logger.error(f"Failed to save performance report: {e}")

# Performance monitoring decorator
def monitor_performance(
    operation_name: str = None,
    track_memory: bool = True,
    track_time: bool = True
):
    """Decorator to monitor function performance"""
    def decorator(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            op_name = operation_name or func.__name__
            
            # Track start metrics
            start_time = time.time()
            start_memory = None
            
            if track_memory:
                try:
                    process = psutil.Process()
                    start_memory = process.memory_info().rss
                except:
                    pass
            
            try:
                # Execute function
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
                
                # Record success metrics
                if track_time:
                    duration = time.time() - start_time
                    performance_monitor.record_metric(
                        PerformanceMetric.RESPONSE_TIME,
                        duration,
                        context={'operation': op_name, 'status': 'success'},
                        tags=['operation_timing']
                    )
                
                if track_memory and start_memory:
                    try:
                        process = psutil.Process()
                        memory_used = (process.memory_info().rss - start_memory) / (1024 * 1024)  # MB
                        performance_monitor.record_metric(
                            PerformanceMetric.MEMORY_USAGE,
                            memory_used,
                            context={'operation': op_name, 'status': 'success'},
                            tags=['operation_memory']
                        )
                    except:
                        pass
                
                return result
            
            except Exception as e:
                # Record error metrics
                if track_time:
                    duration = time.time() - start_time
                    performance_monitor.record_metric(
                        PerformanceMetric.RESPONSE_TIME,
                        duration,
                        context={'operation': op_name, 'status': 'error', 'error': str(e)},
                        tags=['operation_timing', 'error']
                    )
                
                raise e
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(async_wrapper(*args, **kwargs))
            finally:
                loop.close()
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

# Global performance monitor instance
performance_monitor = PerformanceMonitor()

async def run_performance_analysis():
    """Run comprehensive performance analysis"""
    try:
        print("Running comprehensive performance analysis...")
        
        # Start monitoring temporarily
        performance_monitor.start_monitoring()
        
        # Wait to collect some data
        await asyncio.sleep(10)
        
        # Run bottleneck analysis
        bottlenecks = await performance_monitor.run_bottleneck_analysis()
        
        # Generate performance report
        report = performance_monitor.generate_performance_report(hours=1)
        
        # Stop monitoring
        performance_monitor.stop_monitoring()
        
        print(f"Performance analysis completed")
        print(f"Bottlenecks detected: {len(bottlenecks)}")
        print(f"Total alerts: {report['performance_summary']['total_alerts']}")
        print(f"Recommendations: {len(report['recommendations'])}")
        
        for recommendation in report['recommendations']:
            print(f"  - {recommendation}")
        
        return report
    
    except Exception as e:
        print(f"Performance analysis failed: {e}")
        logging.error(f"Performance analysis failed: {e}")
        return None

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Performance Monitor')
    parser.add_argument('--start', action='store_true', help='Start continuous monitoring')
    parser.add_argument('--analyse', action='store_true', help='Run performance analysis')
    parser.add_argument('--report', type=int, default=24, help='Generate report for N hours')
    
    args = parser.parse_args()
    
    if args.start:
        performance_monitor.start_monitoring()
        print("Performance monitoring started. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            performance_monitor.stop_monitoring()
            print("Performance monitoring stopped.")
    elif args.analyse:
        asyncio.run(run_performance_analysis())
    else:
        report = performance_monitor.generate_performance_report(hours=args.report)
        print(f"Performance report generated for last {args.report} hours")
        print(f"Report saved to system/reports/performance/")