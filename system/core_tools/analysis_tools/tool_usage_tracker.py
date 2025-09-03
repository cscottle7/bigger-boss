#!/usr/bin/env python3
"""
Comprehensive Tool Usage Tracking System
Monitors which tools, agents, and APIs are actually used during analysis runs
"""

import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
import time

@dataclass
class ToolUsage:
    """Track usage of a specific tool"""
    name: str
    category: str
    used: bool = False
    execution_time: float = 0.0
    success: bool = False
    error_message: Optional[str] = None
    output_files: List[str] = None
    data_points_extracted: int = 0
    
    def __post_init__(self):
        if self.output_files is None:
            self.output_files = []

@dataclass
class AgentUsage:
    """Track usage of a specific agent"""
    name: str
    purpose: str
    invoked: bool = False
    execution_time: float = 0.0
    tools_used: List[str] = None
    success: bool = False
    output_quality: str = "not_assessed"  # not_assessed, high, medium, low
    limitations_found: List[str] = None
    
    def __post_init__(self):
        if self.tools_used is None:
            self.tools_used = []
        if self.limitations_found is None:
            self.limitations_found = []

class AnalysisRunTracker:
    """Main tracker for complete analysis runs"""
    
    def __init__(self, website_url: str, run_id: Optional[str] = None):
        self.website_url = website_url
        self.run_id = run_id or f"run_{int(time.time())}"
        self.start_time = datetime.now()
        self.end_time = None
        
        # Initialize all available tools
        self.tools = {
            # Core Analysis Tools
            "webfetch": ToolUsage("WebFetch", "core"),
            "websearch": ToolUsage("WebSearch", "core"),
            "playwright": ToolUsage("Playwright", "browser_automation"),
            "scrapy": ToolUsage("Scrapy", "web_crawling"),
            "advertools": ToolUsage("Advertools", "seo_analysis"),
            "pandas": ToolUsage("Pandas", "data_processing"),
            
            # API Integrations
            "serpapi": ToolUsage("SerpAPI", "keyword_research"),
            "gtmetrix": ToolUsage("GTmetrix", "performance"),
            "jina_ai": ToolUsage("Jina AI", "content_processing"),
            
            # Specialized Tools
            "multi_page_seo": ToolUsage("Multi-page SEO Extractor", "seo_analysis"),
            "performance_analyzer": ToolUsage("Performance Analyzer", "technical"),
            "accessibility_checker": ToolUsage("Accessibility Checker", "compliance"),
        }
        
        # Initialize all available agents
        self.agents = {
            # Master Orchestrators
            "master_orchestrator": AgentUsage("master_orchestrator", "Primary coordinator for complete marketing workflows"),
            "workflow_orchestrator": AgentUsage("workflow_orchestrator", "Executes complete project plans from task_deps.md"),
            
            # Technical Analysis
            "technical_seo_analyst": AgentUsage("technical_seo_analyst", "Comprehensive technical SEO analysis"),
            "performance_tester": AgentUsage("performance_tester", "Website performance and Core Web Vitals assessment"),
            "accessibility_checker": AgentUsage("accessibility_checker", "Web accessibility auditing and WCAG compliance"),
            
            # UX/UI Analysis
            "ux_ui_analyst": AgentUsage("ux-ui-analyst", "Comprehensive UX/UI analysis with browser automation"),
            "ux_flow_validator": AgentUsage("ux_flow_validator", "User experience analysis and conversion optimization"),
            
            # AI Optimization
            "ai_specialist_agent": AgentUsage("ai_specialist_agent", "Comprehensive AI readiness audits and optimization"),
            "ai_enhanced_auditor": AgentUsage("ai_enhanced_auditor", "Multi-persona AI implementation quality assurance"),
            
            # SEO Analysis
            "seo_strategist": AgentUsage("seo_strategist", "Advanced SEO strategies using topic modeling"),
            "keyword_researcher": AgentUsage("keyword_researcher", "Comprehensive SEO keyword analysis"),
            
            # Research & Intelligence
            "competitive_intelligence_searcher": AgentUsage("competitive_intelligence_searcher", "Multi-platform competitive research"),
            "niche_trend_researcher": AgentUsage("niche-trend-researcher", "Identifies emerging trends and market movements"),
            "brand_strategy_researcher": AgentUsage("brand_strategy_researcher", "Brand voice analysis and positioning assessment"),
            
            # Content Strategy
            "content_strategist": AgentUsage("content_strategist", "Transforms research into comprehensive content strategies"),
            "content_auditor": AgentUsage("content_auditor", "Analyses existing content performance"),
            "audience_intent_researcher": AgentUsage("audience_intent_researcher", "Understanding target audiences and personas"),
            
            # Quality Assurance
            "brand_compliance_auditor": AgentUsage("brand-compliance-auditor", "Brand compliance assessment including British English"),
            "limitation_resolution_agent": AgentUsage("limitation-resolution-agent", "Resolves estimated data with actual data"),
            "universal_quality_gate_orchestrator": AgentUsage("universal_quality_gate_orchestrator", "Multi-domain quality assessment"),
        }
        
        # Analysis metrics
        self.metrics = {
            "total_pages_analyzed": 0,
            "total_data_points_extracted": 0,
            "seo_issues_found": 0,
            "performance_score": 0,
            "accessibility_issues": 0,
            "api_calls_made": 0,
            "files_generated": 0,
            "screenshots_taken": 0
        }
        
        # Track what was actually requested vs delivered
        self.coverage = {
            "requested_analysis_types": [],
            "delivered_analysis_types": [],
            "missing_analysis_types": [],
            "unexpected_limitations": []
        }
    
    def mark_tool_used(self, tool_name: str, execution_time: float = 0, 
                      success: bool = True, error_message: str = None,
                      data_points: int = 0, output_files: List[str] = None):
        """Mark a tool as used with execution details"""
        if tool_name in self.tools:
            tool = self.tools[tool_name]
            tool.used = True
            tool.execution_time = execution_time
            tool.success = success
            tool.error_message = error_message
            tool.data_points_extracted = data_points
            if output_files:
                tool.output_files.extend(output_files)
    
    def mark_agent_invoked(self, agent_name: str, execution_time: float = 0,
                          tools_used: List[str] = None, success: bool = True,
                          output_quality: str = "not_assessed",
                          limitations: List[str] = None):
        """Mark an agent as invoked with execution details"""
        if agent_name in self.agents:
            agent = self.agents[agent_name]
            agent.invoked = True
            agent.execution_time = execution_time
            agent.success = success
            agent.output_quality = output_quality
            if tools_used:
                agent.tools_used.extend(tools_used)
            if limitations:
                agent.limitations_found.extend(limitations)
    
    def update_metrics(self, **kwargs):
        """Update analysis metrics"""
        for key, value in kwargs.items():
            if key in self.metrics:
                self.metrics[key] = value
    
    def add_coverage_info(self, requested: List[str] = None, delivered: List[str] = None,
                         missing: List[str] = None, limitations: List[str] = None):
        """Update coverage information"""
        if requested:
            self.coverage["requested_analysis_types"].extend(requested)
        if delivered:
            self.coverage["delivered_analysis_types"].extend(delivered)
        if missing:
            self.coverage["missing_analysis_types"].extend(missing)
        if limitations:
            self.coverage["unexpected_limitations"].extend(limitations)
    
    def finalize_run(self):
        """Finalize the analysis run"""
        self.end_time = datetime.now()
        
        # Calculate total execution time
        total_time = (self.end_time - self.start_time).total_seconds()
        
        # Calculate coverage percentages
        total_tools = len(self.tools)
        used_tools = sum(1 for tool in self.tools.values() if tool.used)
        tool_coverage = (used_tools / total_tools) * 100
        
        total_agents = len(self.agents)
        invoked_agents = sum(1 for agent in self.agents.values() if agent.invoked)
        agent_coverage = (invoked_agents / total_agents) * 100
        
        return {
            "run_summary": {
                "run_id": self.run_id,
                "website": self.website_url,
                "start_time": self.start_time.isoformat(),
                "end_time": self.end_time.isoformat(),
                "total_execution_time": total_time,
                "tool_coverage": f"{tool_coverage:.1f}%",
                "agent_coverage": f"{agent_coverage:.1f}%"
            },
            "tools_used": {name: asdict(tool) for name, tool in self.tools.items() if tool.used},
            "tools_unused": [name for name, tool in self.tools.items() if not tool.used],
            "agents_invoked": {name: asdict(agent) for name, agent in self.agents.items() if agent.invoked},
            "agents_unused": [name for name, agent in self.agents.items() if not agent.invoked],
            "metrics": self.metrics,
            "coverage": self.coverage
        }
    
    def generate_report(self) -> str:
        """Generate comprehensive usage report"""
        summary = self.finalize_run()
        
        report = f"""# Analysis Run Usage Report

## Run Summary
- **Run ID**: {summary['run_summary']['run_id']}
- **Website**: {summary['run_summary']['website']}  
- **Start Time**: {summary['run_summary']['start_time']}
- **End Time**: {summary['run_summary']['end_time']}
- **Total Execution Time**: {summary['run_summary']['total_execution_time']:.2f} seconds
- **Tool Coverage**: {summary['run_summary']['tool_coverage']} ({len(summary['tools_used'])}/{len(self.tools)} tools used)
- **Agent Coverage**: {summary['run_summary']['agent_coverage']} ({len(summary['agents_invoked'])}/{len(self.agents)} agents invoked)

## Tools Actually Used
"""
        
        # Group tools by category
        used_by_category = {}
        for name, tool_data in summary['tools_used'].items():
            category = tool_data['category']
            if category not in used_by_category:
                used_by_category[category] = []
            used_by_category[category].append((name, tool_data))
        
        for category, tools in used_by_category.items():
            report += f"\n### {category.title()} Tools\n"
            for name, tool_data in tools:
                status = "✅ SUCCESS" if tool_data['success'] else "❌ FAILED"
                report += f"- **{tool_data['name']}**: {status} ({tool_data['execution_time']:.2f}s"
                if tool_data['data_points_extracted'] > 0:
                    report += f", {tool_data['data_points_extracted']} data points"
                if tool_data['output_files']:
                    report += f", {len(tool_data['output_files'])} files"
                report += ")\n"
                
                if tool_data['error_message']:
                    report += f"  - Error: {tool_data['error_message']}\n"
        
        # Unused tools
        if summary['tools_unused']:
            report += f"\n## Tools NOT Used ({len(summary['tools_unused'])} tools)\n"
            for tool_name in summary['tools_unused']:
                tool = self.tools[tool_name]
                report += f"- **{tool.name}** ({tool.category})\n"
        
        # Agents invoked
        if summary['agents_invoked']:
            report += f"\n## Agents Actually Invoked ({len(summary['agents_invoked'])} agents)\n"
            for name, agent_data in summary['agents_invoked'].items():
                status = "✅ SUCCESS" if agent_data['success'] else "❌ FAILED"
                report += f"- **{agent_data['name']}**: {status} ({agent_data['execution_time']:.2f}s)\n"
                report += f"  - Purpose: {agent_data['purpose']}\n"
                report += f"  - Quality: {agent_data['output_quality']}\n"
                if agent_data['tools_used']:
                    report += f"  - Tools Used: {', '.join(agent_data['tools_used'])}\n"
                if agent_data['limitations_found']:
                    report += f"  - Limitations: {', '.join(agent_data['limitations_found'])}\n"
        
        # Unused agents
        if summary['agents_unused']:
            report += f"\n## Agents NOT Invoked ({len(summary['agents_unused'])} agents)\n"
            for agent_name in summary['agents_unused']:
                agent = self.agents[agent_name]
                report += f"- **{agent.name}**: {agent.purpose}\n"
        
        # Analysis metrics
        report += f"\n## Analysis Metrics\n"
        for metric, value in summary['metrics'].items():
            report += f"- **{metric.replace('_', ' ').title()}**: {value}\n"
        
        # Coverage analysis
        report += f"\n## Coverage Analysis\n"
        if self.coverage['requested_analysis_types']:
            report += f"- **Requested**: {', '.join(self.coverage['requested_analysis_types'])}\n"
        if self.coverage['delivered_analysis_types']:
            report += f"- **Delivered**: {', '.join(self.coverage['delivered_analysis_types'])}\n"
        if self.coverage['missing_analysis_types']:
            report += f"- **Missing**: {', '.join(self.coverage['missing_analysis_types'])}\n"
        if self.coverage['unexpected_limitations']:
            report += f"- **Limitations Found**: {', '.join(self.coverage['unexpected_limitations'])}\n"
        
        report += f"\n---\n*Report generated: {datetime.now().isoformat()}*"
        
        return report
    
    def save_report(self, filename: str = None):
        """Save usage report to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"analysis_tools/usage_reports/run_report_{timestamp}.md"
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        report = self.generate_report()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # Also save raw data as JSON
        json_filename = filename.replace('.md', '.json')
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(self.finalize_run(), f, indent=2, default=str)
        
        return filename

# Example usage decorator for automatic tracking
def track_tool_usage(tool_name: str, tracker: AnalysisRunTracker):
    """Decorator to automatically track tool usage"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                # Try to extract metrics from result
                data_points = 0
                output_files = []
                if isinstance(result, dict):
                    data_points = result.get('data_points', 0)
                    output_files = result.get('output_files', [])
                
                tracker.mark_tool_used(
                    tool_name, 
                    execution_time=execution_time,
                    success=True,
                    data_points=data_points,
                    output_files=output_files
                )
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                tracker.mark_tool_used(
                    tool_name,
                    execution_time=execution_time, 
                    success=False,
                    error_message=str(e)
                )
                raise
        return wrapper
    return decorator

if __name__ == "__main__":
    # Demo usage
    tracker = AnalysisRunTracker("https://example.com")
    
    # Simulate some tool usage
    tracker.mark_tool_used("webfetch", 2.5, True, data_points=15)
    tracker.mark_tool_used("scrapy", 45.2, True, data_points=280, output_files=["crawl_data.json"])
    tracker.mark_tool_used("playwright", 12.8, True, data_points=25, output_files=["screenshot1.png", "screenshot2.png"])
    
    # Simulate agent invocations
    tracker.mark_agent_invoked("technical_seo_analyst", 8.5, ["webfetch", "scrapy"], True, "high")
    tracker.mark_agent_invoked("ux_ui_analyst", 15.2, ["playwright"], True, "medium")
    
    # Update metrics
    tracker.update_metrics(total_pages_analyzed=28, seo_issues_found=5, screenshots_taken=3)
    
    # Generate and save report
    filename = tracker.save_report()
    print(f"Usage report saved to: {filename}")
    
    # Print summary
    print("\n" + tracker.generate_report()[:500] + "...")