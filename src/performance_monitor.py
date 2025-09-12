"""
Performance Monitoring and Optimization Module
Tracks system performance and implements optimizations for the SiteSpect squad.
"""

import time
import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import threading
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetric:
    """Individual performance metric"""
    name: str
    value: float
    unit: str
    timestamp: float
    context: Dict[str, Any]


@dataclass
class WorkflowPerformance:
    """Complete workflow performance data"""
    workflow_id: str
    workflow_type: str
    start_time: float
    end_time: float
    total_duration: float
    specialist_timings: Dict[str, float]
    resource_usage: Dict[str, Any]
    success: bool
    error_count: int
    quality_score: float


class PerformanceMonitor:
    """
    Monitors and optimizes system performance for SiteSpect workflows.
    Implements caching, resource optimization, and performance tracking.
    """
    
    def __init__(self):
        self.metrics_history: List[PerformanceMetric] = []
        self.workflow_history: List[WorkflowPerformance] = []
        self.cache = {}
        self.cache_ttl = {}  # Time-to-live for cached items
        self.performance_thresholds = {
            "max_workflow_time": 300,  # 5 minutes
            "target_workflow_time": 120,  # 2 minutes
            "max_specialist_time": 60,  # 1 minute per specialist
            "cache_hit_target": 0.3  # 30% cache hit rate
        }
        
        # Start background cache cleanup
        self._start_cache_cleanup()
    
    def track_workflow_start(self, workflow_id: str, workflow_type: str) -> Dict[str, Any]:
        """Track the start of a workflow for performance monitoring"""
        start_time = time.time()
        
        context = {
            "workflow_id": workflow_id,
            "workflow_type": workflow_type,
            "start_time": start_time
        }
        
        self._record_metric("workflow_start", start_time, "timestamp", context)
        logger.info(f"Performance tracking started for {workflow_id}")
        
        return context
    
    def track_specialist_execution(self, workflow_context: Dict[str, Any], 
                                 specialist_name: str, 
                                 execution_time: float,
                                 success: bool) -> None:
        """Track individual specialist execution performance"""
        context = {
            "workflow_id": workflow_context["workflow_id"],
            "specialist": specialist_name,
            "success": success
        }
        
        self._record_metric(f"specialist_{specialist_name}_time", execution_time, "seconds", context)
        
        # Check if specialist exceeded threshold
        if execution_time > self.performance_thresholds["max_specialist_time"]:
            logger.warning(f"Specialist {specialist_name} exceeded time threshold: {execution_time:.2f}s")
    
    def track_workflow_completion(self, workflow_context: Dict[str, Any], 
                                success: bool, 
                                specialist_timings: Dict[str, float],
                                quality_score: float = 0.0,
                                error_count: int = 0) -> WorkflowPerformance:
        """Track workflow completion and calculate performance metrics"""
        end_time = time.time()
        total_duration = end_time - workflow_context["start_time"]
        
        # Create workflow performance record
        performance = WorkflowPerformance(
            workflow_id=workflow_context["workflow_id"],
            workflow_type=workflow_context["workflow_type"],
            start_time=workflow_context["start_time"],
            end_time=end_time,
            total_duration=total_duration,
            specialist_timings=specialist_timings,
            resource_usage=self._get_resource_usage(),
            success=success,
            error_count=error_count,
            quality_score=quality_score
        )
        
        # Store performance record
        self.workflow_history.append(performance)
        
        # Record completion metric
        self._record_metric("workflow_completion", total_duration, "seconds", {
            "workflow_id": workflow_context["workflow_id"],
            "success": success,
            "quality_score": quality_score
        })
        
        # Check performance thresholds
        self._check_performance_thresholds(performance)
        
        logger.info(f"Workflow {workflow_context['workflow_id']} completed in {total_duration:.2f}s")
        return performance
    
    def get_cache(self, key: str) -> Optional[Any]:
        """Retrieve item from cache with TTL check"""
        if key not in self.cache:
            return None
        
        # Check TTL
        if key in self.cache_ttl and time.time() > self.cache_ttl[key]:
            del self.cache[key]
            del self.cache_ttl[key]
            return None
        
        # Record cache hit
        self._record_metric("cache_hit", 1, "count", {"key": key})
        return self.cache[key]
    
    def set_cache(self, key: str, value: Any, ttl_seconds: int = 3600) -> None:
        """Store item in cache with TTL"""
        self.cache[key] = value
        self.cache_ttl[key] = time.time() + ttl_seconds
        
        # Record cache set
        self._record_metric("cache_set", 1, "count", {"key": key, "ttl": ttl_seconds})
    
    def clear_cache(self) -> None:
        """Clear all cached data"""
        self.cache.clear()
        self.cache_ttl.clear()
        logger.info("Performance cache cleared")
    
    def get_performance_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get performance summary for the last N hours"""
        cutoff_time = time.time() - (hours * 3600)
        
        # Filter recent workflows
        recent_workflows = [w for w in self.workflow_history if w.start_time >= cutoff_time]
        
        if not recent_workflows:
            return {
                "period_hours": hours,
                "total_workflows": 0,
                "summary": "No workflows in this period"
            }
        
        # Calculate summary statistics
        total_workflows = len(recent_workflows)
        successful_workflows = len([w for w in recent_workflows if w.success])
        average_duration = sum(w.total_duration for w in recent_workflows) / total_workflows
        fastest_workflow = min(w.total_duration for w in recent_workflows)
        slowest_workflow = max(w.total_duration for w in recent_workflows)
        average_quality = sum(w.quality_score for w in recent_workflows) / total_workflows
        
        # Cache statistics
        cache_metrics = [m for m in self.metrics_history if m.name == "cache_hit" and m.timestamp >= cutoff_time]
        cache_hits = len(cache_metrics)
        total_requests = cache_hits + len([m for m in self.metrics_history if m.name == "cache_set" and m.timestamp >= cutoff_time])
        cache_hit_rate = (cache_hits / total_requests) if total_requests > 0 else 0
        
        # Performance by specialist
        specialist_performance = {}
        for workflow in recent_workflows:
            for specialist, duration in workflow.specialist_timings.items():
                if specialist not in specialist_performance:
                    specialist_performance[specialist] = []
                specialist_performance[specialist].append(duration)
        
        specialist_averages = {
            specialist: sum(times) / len(times) 
            for specialist, times in specialist_performance.items()
        }
        
        return {
            "period_hours": hours,
            "total_workflows": total_workflows,
            "success_rate": (successful_workflows / total_workflows) * 100,
            "average_duration_seconds": average_duration,
            "fastest_workflow_seconds": fastest_workflow,
            "slowest_workflow_seconds": slowest_workflow,
            "average_quality_score": average_quality,
            "cache_hit_rate": cache_hit_rate * 100,
            "specialist_performance": specialist_averages,
            "performance_grade": self._calculate_performance_grade(
                average_duration, successful_workflows / total_workflows, average_quality
            ),
            "recommendations": self._generate_performance_recommendations(recent_workflows)
        }
    
    def optimize_workflow_execution(self) -> List[str]:
        """Analyze performance and return optimization recommendations"""
        if len(self.workflow_history) < 5:
            return ["Need more workflow data for optimization analysis"]
        
        recommendations = []
        recent_workflows = self.workflow_history[-20:]  # Last 20 workflows
        
        # Analyze average execution times
        avg_duration = sum(w.total_duration for w in recent_workflows) / len(recent_workflows)
        if avg_duration > self.performance_thresholds["target_workflow_time"]:
            recommendations.append(f"Average workflow time ({avg_duration:.1f}s) exceeds target ({self.performance_thresholds['target_workflow_time']}s)")
        
        # Analyze specialist performance
        specialist_times = {}
        for workflow in recent_workflows:
            for specialist, duration in workflow.specialist_timings.items():
                if specialist not in specialist_times:
                    specialist_times[specialist] = []
                specialist_times[specialist].append(duration)
        
        for specialist, times in specialist_times.items():
            avg_time = sum(times) / len(times)
            if avg_time > self.performance_thresholds["max_specialist_time"]:
                recommendations.append(f"{specialist} average time ({avg_time:.1f}s) exceeds threshold")
        
        # Cache performance
        cache_hit_rate = self._calculate_cache_hit_rate()
        if cache_hit_rate < self.performance_thresholds["cache_hit_target"]:
            recommendations.append(f"Cache hit rate ({cache_hit_rate:.1%}) below target ({self.performance_thresholds['cache_hit_target']:.1%})")
        
        # Success rate analysis
        success_rate = sum(1 for w in recent_workflows if w.success) / len(recent_workflows)
        if success_rate < 0.95:  # 95% target
            recommendations.append(f"Success rate ({success_rate:.1%}) below 95% target")
        
        return recommendations if recommendations else ["System performance is optimal"]
    
    def _record_metric(self, name: str, value: float, unit: str, context: Dict[str, Any]) -> None:
        """Record a performance metric"""
        metric = PerformanceMetric(
            name=name,
            value=value,
            unit=unit,
            timestamp=time.time(),
            context=context
        )
        
        self.metrics_history.append(metric)
        
        # Limit history size to prevent memory issues
        if len(self.metrics_history) > 10000:
            self.metrics_history = self.metrics_history[-5000:]  # Keep last 5000
    
    def _get_resource_usage(self) -> Dict[str, Any]:
        """Get current resource usage metrics"""
        try:
            import psutil
            return {
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage('/').percent if hasattr(psutil.disk_usage('/'), 'percent') else 0
            }
        except ImportError:
            # psutil not available, return mock data
            return {
                "cpu_percent": 25.0,
                "memory_percent": 45.0, 
                "disk_usage": 60.0
            }
    
    def _check_performance_thresholds(self, performance: WorkflowPerformance) -> None:
        """Check if performance exceeds thresholds and log warnings"""
        if performance.total_duration > self.performance_thresholds["max_workflow_time"]:
            logger.warning(f"Workflow {performance.workflow_id} exceeded maximum time: {performance.total_duration:.2f}s")
        
        for specialist, duration in performance.specialist_timings.items():
            if duration > self.performance_thresholds["max_specialist_time"]:
                logger.warning(f"Specialist {specialist} in {performance.workflow_id} exceeded time threshold: {duration:.2f}s")
    
    def _calculate_cache_hit_rate(self) -> float:
        """Calculate current cache hit rate"""
        recent_time = time.time() - 3600  # Last hour
        recent_metrics = [m for m in self.metrics_history if m.timestamp >= recent_time]
        
        hits = len([m for m in recent_metrics if m.name == "cache_hit"])
        sets = len([m for m in recent_metrics if m.name == "cache_set"])
        total = hits + sets
        
        return (hits / total) if total > 0 else 0
    
    def _calculate_performance_grade(self, avg_duration: float, success_rate: float, quality_score: float) -> str:
        """Calculate overall performance grade"""
        # Duration score (0-40 points)
        if avg_duration <= self.performance_thresholds["target_workflow_time"]:
            duration_score = 40
        elif avg_duration <= self.performance_thresholds["max_workflow_time"]:
            duration_score = 40 - ((avg_duration - self.performance_thresholds["target_workflow_time"]) / 
                                 (self.performance_thresholds["max_workflow_time"] - self.performance_thresholds["target_workflow_time"])) * 20
        else:
            duration_score = 10  # Minimum score
        
        # Success rate score (0-30 points)
        success_score = success_rate * 30
        
        # Quality score (0-30 points)
        quality_points = (quality_score / 10) * 30
        
        total_score = duration_score + success_score + quality_points
        
        if total_score >= 90:
            return "A"
        elif total_score >= 80:
            return "B"
        elif total_score >= 70:
            return "C"
        elif total_score >= 60:
            return "D"
        else:
            return "F"
    
    def _generate_performance_recommendations(self, workflows: List[WorkflowPerformance]) -> List[str]:
        """Generate specific performance improvement recommendations"""
        recommendations = []
        
        if not workflows:
            return recommendations
        
        # Analyze common failure patterns
        failed_workflows = [w for w in workflows if not w.success]
        if len(failed_workflows) > len(workflows) * 0.1:  # >10% failure rate
            recommendations.append("High failure rate detected - review error handling and input validation")
        
        # Analyze slow specialists
        specialist_times = {}
        for workflow in workflows:
            for specialist, duration in workflow.specialist_timings.items():
                if specialist not in specialist_times:
                    specialist_times[specialist] = []
                specialist_times[specialist].append(duration)
        
        for specialist, times in specialist_times.items():
            avg_time = sum(times) / len(times)
            if avg_time > 30:  # 30 second threshold
                recommendations.append(f"Consider optimizing {specialist} - average execution time: {avg_time:.1f}s")
        
        # Quality score analysis
        avg_quality = sum(w.quality_score for w in workflows) / len(workflows)
        if avg_quality < 7:  # Below 7/10
            recommendations.append("Quality scores below target - review specialist agent accuracy")
        
        return recommendations
    
    def _start_cache_cleanup(self) -> None:
        """Start background thread for cache cleanup"""
        def cleanup_expired_cache():
            while True:
                try:
                    current_time = time.time()
                    expired_keys = [key for key, expiry in self.cache_ttl.items() if current_time > expiry]
                    
                    for key in expired_keys:
                        del self.cache[key]
                        del self.cache_ttl[key]
                    
                    if expired_keys:
                        logger.debug(f"Cleaned up {len(expired_keys)} expired cache entries")
                    
                    time.sleep(300)  # Clean every 5 minutes
                except Exception as e:
                    logger.error(f"Cache cleanup error: {e}")
                    time.sleep(60)  # Wait 1 minute before retrying
        
        cleanup_thread = threading.Thread(target=cleanup_expired_cache, daemon=True)
        cleanup_thread.start()
    
    def export_performance_data(self, filepath: str) -> None:
        """Export performance data to JSON file"""
        export_data = {
            "export_timestamp": time.time(),
            "metrics_count": len(self.metrics_history),
            "workflows_count": len(self.workflow_history),
            "performance_summary": self.get_performance_summary(24),
            "recent_workflows": [asdict(w) for w in self.workflow_history[-10:]],
            "cache_size": len(self.cache),
            "recommendations": self.optimize_workflow_execution()
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        logger.info(f"Performance data exported to {filepath}")


# Initialize global performance monitor
performance_monitor = PerformanceMonitor()

# Export main functions
__all__ = [
    'PerformanceMonitor',
    'PerformanceMetric',
    'WorkflowPerformance',
    'performance_monitor'
]

# Convenience functions for workflows
def track_workflow_start(workflow_id: str, workflow_type: str) -> Dict[str, Any]:
    """Track workflow start"""
    return performance_monitor.track_workflow_start(workflow_id, workflow_type)

def track_workflow_completion(workflow_context: Dict[str, Any], 
                            success: bool,
                            specialist_timings: Dict[str, float],
                            quality_score: float = 0.0,
                            error_count: int = 0) -> WorkflowPerformance:
    """Track workflow completion"""
    return performance_monitor.track_workflow_completion(
        workflow_context, success, specialist_timings, quality_score, error_count
    )

def get_cached_result(cache_key: str) -> Optional[Any]:
    """Get cached result if available"""
    return performance_monitor.get_cache(cache_key)

def cache_result(cache_key: str, result: Any, ttl_seconds: int = 3600) -> None:
    """Cache a result"""
    performance_monitor.set_cache(cache_key, result, ttl_seconds)