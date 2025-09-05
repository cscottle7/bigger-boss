#!/usr/bin/env python3
"""
Tool Usage Tracking System for Bigger Boss Agent
Monitors and reports which tools agents actually use vs. specifications
"""

import json
import datetime
from pathlib import Path
import logging

class ToolUsageTracker:
    def __init__(self, client_domain=None):
        self.client_domain = client_domain
        self.usage_log = []
        self.report_path = Path("system/monitoring/tool_usage_reports")
        self.report_path.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def log_tool_use(self, agent_name, tool_name, operation, success=True, details=None, expected_tools=None):
        """Log tool usage for analysis"""
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "client": self.client_domain,
            "agent": agent_name,
            "tool": tool_name,
            "operation": operation,
            "success": success,
            "details": details or {},
            "expected_tools": expected_tools or []
        }
        self.usage_log.append(entry)
        self.logger.info(f"Tool usage logged: {agent_name} used {tool_name} - {'SUCCESS' if success else 'FAILED'}")
    
    def log_missing_tool(self, agent_name, expected_tool, reason="Tool not available or not called"):
        """Log when an expected tool was not used"""
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "client": self.client_domain,
            "agent": agent_name,
            "tool": expected_tool,
            "operation": "EXPECTED_NOT_USED",
            "success": False,
            "details": {"reason": reason, "issue_type": "missing_tool_usage"},
            "expected_tools": [expected_tool]
        }
        self.usage_log.append(entry)
        self.logger.warning(f"Expected tool not used: {agent_name} should have used {expected_tool} - {reason}")
    
    def generate_usage_report(self, agent_name=None):
        """Generate comprehensive tool usage report"""
        filtered_logs = [log for log in self.usage_log if not agent_name or log["agent"] == agent_name]
        
        report = {
            "report_metadata": {
                "generated": datetime.datetime.now().isoformat(),
                "client": self.client_domain,
                "total_operations": len(filtered_logs),
                "agents_analyzed": list(set(log["agent"] for log in filtered_logs)),
                "analysis_scope": agent_name if agent_name else "ALL_AGENTS"
            },
            "tool_usage_summary": {},
            "missing_tools_analysis": [],
            "failure_analysis": [],
            "agent_performance": {},
            "recommendations": []
        }
        
        # Analyze tool usage patterns
        for log in filtered_logs:
            tool = log["tool"]
            agent = log["agent"]
            
            # Initialize tool tracking
            if tool not in report["tool_usage_summary"]:
                report["tool_usage_summary"][tool] = {
                    "total_uses": 0, 
                    "success_count": 0,
                    "failure_count": 0,
                    "success_rate": 0, 
                    "agents_using": set(),
                    "failures": []
                }
            
            # Initialize agent tracking
            if agent not in report["agent_performance"]:
                report["agent_performance"][agent] = {
                    "tools_used": set(),
                    "total_operations": 0,
                    "successful_operations": 0,
                    "failed_operations": 0,
                    "missing_tools": []
                }
            
            # Update tool stats
            report["tool_usage_summary"][tool]["total_uses"] += 1
            report["tool_usage_summary"][tool]["agents_using"].add(agent)
            
            # Update agent stats
            report["agent_performance"][agent]["total_operations"] += 1
            report["agent_performance"][agent]["tools_used"].add(tool)
            
            if log["success"]:
                report["tool_usage_summary"][tool]["success_count"] += 1
                report["agent_performance"][agent]["successful_operations"] += 1
            else:
                report["tool_usage_summary"][tool]["failure_count"] += 1
                report["tool_usage_summary"][tool]["failures"].append(log)
                report["agent_performance"][agent]["failed_operations"] += 1
                
                # Track missing tools specifically
                if log["operation"] == "EXPECTED_NOT_USED":
                    report["missing_tools_analysis"].append({
                        "agent": agent,
                        "missing_tool": tool,
                        "reason": log["details"].get("reason", "Unknown"),
                        "timestamp": log["timestamp"]
                    })
                    report["agent_performance"][agent]["missing_tools"].append(tool)
                else:
                    report["failure_analysis"].append(log)
        
        # Calculate success rates and convert sets to lists for JSON serialization
        for tool, data in report["tool_usage_summary"].items():
            if data["total_uses"] > 0:
                data["success_rate"] = (data["success_count"] / data["total_uses"]) * 100
            data["agents_using"] = list(data["agents_using"])
        
        for agent, data in report["agent_performance"].items():
            data["tools_used"] = list(data["tools_used"])
            if data["total_operations"] > 0:
                data["success_rate"] = (data["successful_operations"] / data["total_operations"]) * 100
        
        # Generate recommendations
        report["recommendations"] = self._generate_recommendations(report)
        
        # Save report
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        client_prefix = f"{self.client_domain}_" if self.client_domain else ""
        agent_prefix = f"{agent_name}_" if agent_name else ""
        report_file = self.report_path / f"{client_prefix}{agent_prefix}usage_report_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Tool usage report generated: {report_file}")
        return report, str(report_file)
    
    def _generate_recommendations(self, report):
        """Generate actionable recommendations based on usage analysis"""
        recommendations = []
        
        # Check for tools with high failure rates
        high_failure_tools = [
            tool for tool, data in report["tool_usage_summary"].items() 
            if data["success_rate"] < 50 and data["total_uses"] > 1
        ]
        
        if high_failure_tools:
            recommendations.append({
                "priority": "HIGH",
                "category": "Tool Reliability",
                "issue": f"Tools with high failure rates: {', '.join(high_failure_tools)}",
                "action": "Investigate tool configuration and fix integration issues"
            })
        
        # Check for missing expected tools
        missing_tools = len(report["missing_tools_analysis"])
        if missing_tools > 0:
            recommendations.append({
                "priority": "HIGH",
                "category": "Tool Coverage",
                "issue": f"{missing_tools} expected tools were not used by agents",
                "action": "Review agent configurations and ensure proper tool integration"
            })
        
        # Check for agents with low success rates
        low_performance_agents = [
            agent for agent, data in report["agent_performance"].items()
            if data.get("success_rate", 0) < 70 and data["total_operations"] > 2
        ]
        
        if low_performance_agents:
            recommendations.append({
                "priority": "MEDIUM",
                "category": "Agent Performance",
                "issue": f"Agents with low success rates: {', '.join(low_performance_agents)}",
                "action": "Review agent implementations and improve error handling"
            })
        
        # Check for unused tools from requirements
        expected_tools = [
            "playwright", "scrapy", "advertools", "webfetch", "websearch", 
            "browser_navigate", "browser_take_screenshot", "browser_evaluate"
        ]
        
        used_tools = set(report["tool_usage_summary"].keys())
        unused_expected = [tool for tool in expected_tools if tool not in used_tools]
        
        if unused_expected:
            recommendations.append({
                "priority": "MEDIUM", 
                "category": "Tool Utilization",
                "issue": f"Expected tools not used: {', '.join(unused_expected)}",
                "action": "Verify tool availability and update agent workflows to use all required tools"
            })
        
        return recommendations

    def get_agent_expected_tools(self, agent_name):
        """Define expected tools for each agent type"""
        tool_expectations = {
            "sitespect_orchestrator": ["browser_navigate", "browser_take_screenshot", "webfetch", "websearch"],
            "technical_seo_analyst": ["browser_navigate", "browser_evaluate", "webfetch"],
            "ux-ui-analyst": ["browser_navigate", "browser_take_screenshot", "browser_evaluate"],
            "performance_tester": ["browser_navigate", "browser_evaluate"],
            "seo_strategist": ["webfetch", "websearch", "browser_navigate"],
            "competitor_analyzer": ["webfetch", "websearch", "browser_navigate"],
            "content_strategist": ["webfetch", "websearch"]
        }
        
        return tool_expectations.get(agent_name, [])

# Example usage and testing
def test_tracker():
    """Test the tool usage tracker"""
    tracker = ToolUsageTracker("sydneycoachcharter_com_au")
    
    # Simulate some tool usage
    tracker.log_tool_use("sitespect_orchestrator", "browser_navigate", "navigate_to_homepage", True, 
                        {"url": "https://sydneycoachcharter.com.au"})
    tracker.log_tool_use("technical_seo_analyst", "webfetch", "extract_metadata", False, 
                        {"error": "Connection timeout"})
    tracker.log_missing_tool("sitespect_orchestrator", "browser_take_screenshot", 
                           "Screenshot functionality not called during analysis")
    
    # Generate report
    report, report_file = tracker.generate_usage_report()
    
    print(f"Test report generated: {report_file}")
    print(f"Total operations: {report['report_metadata']['total_operations']}")
    print(f"Recommendations: {len(report['recommendations'])}")
    
    return report

if __name__ == "__main__":
    test_tracker()