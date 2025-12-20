
"""
Metrics Collector
Track API performance and monitoring
"""

from typing import Dict, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class MetricsCollector:
    """Collect and track metrics"""
    
    def __init__(self):
        self.metrics: List[Dict] = []
    
    def record_metric(self, metric: Dict):
        """Record API call metric"""
        self.metrics.append(metric)
        
        if len(self.metrics) > 1000:
            self.metrics.pop(0)
        
        logger.info(f"Metric recorded: {metric.get('endpoint')}")
    
    def get_stats(self) -> Dict:
        """Get performance statistics"""
        if not self.metrics:
            return {}
        
        total = len(self.metrics)
        success = sum(1 for m in self.metrics if m.get("status") == "success")
        avg_time = sum(m.get("response_time_ms", 0) for m in self.metrics) / total
        
        return {
            "total_requests": total,
            "success_rate": (success / total) * 100,
            "avg_response_time_ms": round(avg_time, 2),
            "last_metric": self.metrics[-1] if self.metrics else None
        }
