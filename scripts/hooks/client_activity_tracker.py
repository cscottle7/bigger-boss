#!/usr/bin/env python3
"""
Bigger Boss Agent System - Client Activity Tracker Hook
Tracks all client-related activities for comprehensive reporting and project management.

Usage: Called automatically by hook system during client operations
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ClientActivityTracker:
    """Comprehensive client activity tracking and reporting system."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.logs_dir = self.project_root / '.claude' / 'logs'
        self.reports_dir = self.project_root / 'reports'

        # Create directories
        self.logs_dir.mkdir(exist_ok=True)
        self.reports_dir.mkdir(exist_ok=True)

        self.activity_log = self.logs_dir / 'client_activities.jsonl'
        self.daily_summary_log = self.logs_dir / 'daily_client_summary.jsonl'

        # Activity categories and their scoring
        self.activity_categories = {
            'content_creation': {'weight': 1.0, 'description': 'Blog posts, pages, articles'},
            'seo_analysis': {'weight': 0.8, 'description': 'SEO audits, keyword research'},
            'technical_audit': {'weight': 0.9, 'description': 'Website technical analysis'},
            'strategy_development': {'weight': 1.2, 'description': 'Strategic planning, research'},
            'competitor_analysis': {'weight': 0.7, 'description': 'Competitive intelligence'},
            'research': {'weight': 0.6, 'description': 'Market research, audience analysis'},
            'implementation': {'weight': 1.1, 'description': 'Project execution, deployment'},
            'reporting': {'weight': 0.4, 'description': 'Status reports, summaries'},
            'quality_assurance': {'weight': 0.5, 'description': 'Content review, validation'},
            'document_processing': {'weight': 0.3, 'description': 'File conversion, formatting'}
        }

    def extract_client_info(self, file_path: str) -> Dict[str, Optional[str]]:
        """Extract client information from file path."""
        try:
            path_parts = Path(file_path).parts

            # Look for 'clients' folder in path
            if 'clients' in path_parts:
                clients_index = path_parts.index('clients')

                if len(path_parts) > clients_index + 1:
                    client_domain = path_parts[clients_index + 1]

                    # Extract project phase
                    project_phase = None
                    if len(path_parts) > clients_index + 2:
                        phase_folder = path_parts[clients_index + 2]
                        if phase_folder in ['strategy', 'research', 'content', 'technical', 'implementation']:
                            project_phase = phase_folder

                    # Clean up client domain for display
                    client_name = client_domain.replace('_', ' ').replace('.com.au', '').replace('.net.au', '').title()

                    return {
                        'client_domain': client_domain,
                        'client_name': client_name,
                        'project_phase': project_phase,
                        'full_path': str(file_path)
                    }

            return {
                'client_domain': None,
                'client_name': None,
                'project_phase': None,
                'full_path': str(file_path)
            }

        except Exception as e:
            logger.error(f"Failed to extract client info from {file_path}: {e}")
            return {
                'client_domain': None,
                'client_name': None,
                'project_phase': None,
                'full_path': str(file_path)
            }

    def determine_activity_category(self, file_path: str, activity_type: str) -> str:
        """Determine activity category based on file path and activity type."""
        path_str = str(file_path).lower()
        activity_type = activity_type.lower()

        # Direct matches from activity type
        if 'seo' in activity_type or 'keyword' in activity_type:
            return 'seo_analysis'
        elif 'strategy' in activity_type or 'planning' in activity_type:
            return 'strategy_development'
        elif 'competitor' in activity_type or 'competitive' in activity_type:
            return 'competitor_analysis'
        elif 'technical' in activity_type or 'audit' in activity_type:
            return 'technical_audit'
        elif 'research' in activity_type:
            return 'research'
        elif 'implementation' in activity_type or 'deploy' in activity_type:
            return 'implementation'
        elif 'report' in activity_type or 'summary' in activity_type:
            return 'reporting'
        elif 'quality' in activity_type or 'review' in activity_type:
            return 'quality_assurance'

        # Path-based categorization
        if '/strategy/' in path_str:
            return 'strategy_development'
        elif '/research/' in path_str:
            if 'competitor' in path_str:
                return 'competitor_analysis'
            else:
                return 'research'
        elif '/content/' in path_str:
            return 'content_creation'
        elif '/technical/' in path_str:
            return 'technical_audit'
        elif '/implementation/' in path_str:
            return 'implementation'
        elif 'checklist' in path_str or 'summary' in path_str or 'report' in path_str:
            return 'reporting'

        # File extension based
        if path_str.endswith(('.docx', '.pdf')):
            return 'document_processing'

        # Default fallback
        return 'content_creation'

    def calculate_activity_score(self, category: str, file_size: Optional[int] = None,
                               duration: Optional[float] = None) -> float:
        """Calculate weighted activity score."""
        base_weight = self.activity_categories.get(category, {}).get('weight', 1.0)

        score = base_weight

        # Size-based multiplier
        if file_size:
            if file_size > 50000:  # >50KB
                score *= 1.5
            elif file_size > 10000:  # >10KB
                score *= 1.2

        # Duration-based multiplier
        if duration:
            if duration > 300:  # >5 minutes
                score *= 1.3
            elif duration > 60:  # >1 minute
                score *= 1.1

        return round(score, 2)

    def record_activity(
        self,
        client: str,
        activity_type: str,
        file_path: str,
        agent_name: Optional[str] = None,
        success: bool = True,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """Record client activity."""
        try:
            # Extract client information
            client_info = self.extract_client_info(file_path)

            # Use provided client or extract from path
            if not client and client_info['client_domain']:
                client = client_info['client_domain']

            # Determine activity category
            category = self.determine_activity_category(file_path, activity_type)

            # Get file information
            file_size = None
            if Path(file_path).exists():
                file_size = Path(file_path).stat().st_size

            # Calculate activity score
            activity_score = self.calculate_activity_score(
                category,
                file_size,
                metadata.get('duration') if metadata else None
            )

            # Create activity record
            activity_record = {
                'timestamp': datetime.now().isoformat(),
                'client_domain': client or client_info['client_domain'],
                'client_name': client_info['client_name'] or client,
                'activity_type': activity_type,
                'activity_category': category,
                'activity_score': activity_score,
                'project_phase': client_info['project_phase'],
                'file_path': file_path,
                'file_size_bytes': file_size,
                'agent_name': agent_name,
                'success': success,
                'metadata': metadata or {}
            }

            # Write to activity log
            with open(self.activity_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(activity_record) + '\n')

            logger.info(f"📊 Activity recorded: {client_info['client_name']} - {activity_type} ({category})")

            return activity_record

        except Exception as e:
            logger.error(f"Failed to record client activity: {e}")
            return {}

    def generate_daily_summary(self, target_date: Optional[str] = None) -> Dict:
        """Generate daily activity summary for all clients."""
        try:
            if target_date:
                target_datetime = datetime.fromisoformat(target_date)
            else:
                target_datetime = datetime.now()

            # Define date range for the day
            start_of_day = target_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + timedelta(days=1)

            if not self.activity_log.exists():
                return {'error': 'No activity data available'}

            # Read and filter activities for the target date
            daily_activities = []

            with open(self.activity_log, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        record = json.loads(line.strip())
                        activity_time = datetime.fromisoformat(record['timestamp'])

                        if start_of_day <= activity_time < end_of_day:
                            daily_activities.append(record)

                    except (json.JSONDecodeError, KeyError, ValueError):
                        continue

            if not daily_activities:
                return {
                    'date': target_datetime.date().isoformat(),
                    'total_activities': 0,
                    'clients': {},
                    'category_breakdown': {},
                    'total_score': 0
                }

            # Analyze activities by client
            client_summaries = {}
            category_breakdown = {}
            total_score = 0

            for activity in daily_activities:
                client_domain = activity.get('client_domain')
                client_name = activity.get('client_name', client_domain)
                category = activity.get('activity_category', 'unknown')
                score = activity.get('activity_score', 0)

                # Client summary
                if client_domain not in client_summaries:
                    client_summaries[client_domain] = {
                        'client_name': client_name,
                        'activities': 0,
                        'score': 0,
                        'categories': {},
                        'project_phases': set(),
                        'success_rate': 0,
                        'successes': 0
                    }

                client_summaries[client_domain]['activities'] += 1
                client_summaries[client_domain]['score'] += score

                if category not in client_summaries[client_domain]['categories']:
                    client_summaries[client_domain]['categories'][category] = 0
                client_summaries[client_domain]['categories'][category] += 1

                if activity.get('project_phase'):
                    client_summaries[client_domain]['project_phases'].add(activity['project_phase'])

                if activity.get('success', True):
                    client_summaries[client_domain]['successes'] += 1

                # Category breakdown
                if category not in category_breakdown:
                    category_breakdown[category] = {
                        'count': 0,
                        'score': 0,
                        'description': self.activity_categories.get(category, {}).get('description', 'Unknown category')
                    }
                category_breakdown[category]['count'] += 1
                category_breakdown[category]['score'] += score

                total_score += score

            # Calculate success rates and convert sets to lists
            for client_data in client_summaries.values():
                if client_data['activities'] > 0:
                    client_data['success_rate'] = (client_data['successes'] / client_data['activities']) * 100
                client_data['project_phases'] = list(client_data['project_phases'])
                del client_data['successes']  # Remove intermediate calculation

            # Create daily summary
            daily_summary = {
                'date': target_datetime.date().isoformat(),
                'total_activities': len(daily_activities),
                'total_score': round(total_score, 2),
                'unique_clients': len(client_summaries),
                'clients': client_summaries,
                'category_breakdown': category_breakdown,
                'top_client': max(client_summaries.keys(), key=lambda k: client_summaries[k]['score']) if client_summaries else None,
                'most_active_category': max(category_breakdown.keys(), key=lambda k: category_breakdown[k]['count']) if category_breakdown else None
            }

            # Save daily summary
            summary_record = {
                'timestamp': datetime.now().isoformat(),
                'summary_date': target_datetime.date().isoformat(),
                'summary': daily_summary
            }

            with open(self.daily_summary_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(summary_record) + '\n')

            return daily_summary

        except Exception as e:
            logger.error(f"Failed to generate daily summary: {e}")
            return {'error': str(e)}

    def generate_client_report(self, client_domain: str, days: int = 7) -> Dict:
        """Generate comprehensive client activity report."""
        try:
            if not self.activity_log.exists():
                return {'error': 'No activity data available'}

            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            # Read and filter activities for the client
            client_activities = []

            with open(self.activity_log, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        record = json.loads(line.strip())
                        activity_time = datetime.fromisoformat(record['timestamp'])

                        if (start_date <= activity_time <= end_date and
                            record.get('client_domain') == client_domain):
                            client_activities.append(record)

                    except (json.JSONDecodeError, KeyError, ValueError):
                        continue

            if not client_activities:
                return {
                    'error': f'No activity data for client {client_domain} in the last {days} days'
                }

            # Analyze client activities
            client_name = client_activities[0].get('client_name', client_domain)

            # Daily breakdown
            daily_breakdown = {}
            category_summary = {}
            phase_summary = {}
            total_score = 0
            success_count = 0

            for activity in client_activities:
                # Daily breakdown
                activity_date = datetime.fromisoformat(activity['timestamp']).date().isoformat()
                if activity_date not in daily_breakdown:
                    daily_breakdown[activity_date] = {'count': 0, 'score': 0, 'categories': set()}

                daily_breakdown[activity_date]['count'] += 1
                daily_breakdown[activity_date]['score'] += activity.get('activity_score', 0)
                daily_breakdown[activity_date]['categories'].add(activity.get('activity_category', 'unknown'))

                # Category summary
                category = activity.get('activity_category', 'unknown')
                if category not in category_summary:
                    category_summary[category] = {
                        'count': 0,
                        'score': 0,
                        'recent_files': []
                    }
                category_summary[category]['count'] += 1
                category_summary[category]['score'] += activity.get('activity_score', 0)

                # Keep track of recent files
                file_name = Path(activity.get('file_path', '')).name
                if len(category_summary[category]['recent_files']) < 3:
                    category_summary[category]['recent_files'].append(file_name)

                # Phase summary
                phase = activity.get('project_phase')
                if phase:
                    if phase not in phase_summary:
                        phase_summary[phase] = 0
                    phase_summary[phase] += 1

                # Totals
                total_score += activity.get('activity_score', 0)
                if activity.get('success', True):
                    success_count += 1

            # Convert sets to lists in daily breakdown
            for day_data in daily_breakdown.values():
                day_data['categories'] = list(day_data['categories'])

            # Create client report
            client_report = {
                'client_domain': client_domain,
                'client_name': client_name,
                'report_period_days': days,
                'report_start_date': start_date.date().isoformat(),
                'report_end_date': end_date.date().isoformat(),
                'total_activities': len(client_activities),
                'total_score': round(total_score, 2),
                'success_rate': (success_count / len(client_activities)) * 100,
                'average_daily_activities': round(len(client_activities) / days, 2),
                'average_daily_score': round(total_score / days, 2),
                'daily_breakdown': daily_breakdown,
                'category_summary': category_summary,
                'project_phase_breakdown': phase_summary,
                'most_active_day': max(daily_breakdown.keys(),
                                     key=lambda k: daily_breakdown[k]['count']) if daily_breakdown else None,
                'highest_scoring_day': max(daily_breakdown.keys(),
                                         key=lambda k: daily_breakdown[k]['score']) if daily_breakdown else None,
                'dominant_category': max(category_summary.keys(),
                                       key=lambda k: category_summary[k]['count']) if category_summary else None
            }

            return client_report

        except Exception as e:
            logger.error(f"Failed to generate client report: {e}")
            return {'error': str(e)}

    def export_activity_report(self, output_file: str, client_domain: Optional[str] = None,
                              days: int = 7, format: str = 'json') -> bool:
        """Export activity report to file."""
        try:
            if client_domain:
                report_data = self.generate_client_report(client_domain, days)
            else:
                # Generate summary for all clients
                report_data = {
                    'report_type': 'all_clients_summary',
                    'period_days': days,
                    'generated_at': datetime.now().isoformat()
                }

                # Get recent daily summaries
                summaries = []
                if self.daily_summary_log.exists():
                    with open(self.daily_summary_log, 'r', encoding='utf-8') as f:
                        for line in f:
                            try:
                                record = json.loads(line.strip())
                                summary_date = datetime.fromisoformat(record['summary_date'])
                                if summary_date >= datetime.now() - timedelta(days=days):
                                    summaries.append(record['summary'])
                            except (json.JSONDecodeError, KeyError, ValueError):
                                continue

                report_data['daily_summaries'] = summaries

            # Write report to file
            output_path = Path(output_file)

            if format.lower() == 'json':
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(report_data, f, indent=2, ensure_ascii=False)
            else:
                return False

            logger.info(f"📄 Activity report exported to: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to export activity report: {e}")
            return False


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(
        description='Bigger Boss Client Activity Tracker'
    )

    parser.add_argument('--client', help='Client domain')
    parser.add_argument('--activity', required=True, help='Activity type')
    parser.add_argument('--file', help='File path related to activity')
    parser.add_argument('--agent', help='Agent name performing the activity')
    parser.add_argument('--success', type=bool, default=True, help='Activity success status')

    parser.add_argument('--daily-summary', help='Generate daily summary for date (YYYY-MM-DD)')
    parser.add_argument('--client-report', help='Generate client report for specified client')
    parser.add_argument('--days', type=int, default=7, help='Number of days for reports')
    parser.add_argument('--export', help='Export report to file')

    args = parser.parse_args()

    tracker = ClientActivityTracker()

    try:
        if args.daily_summary:
            summary = tracker.generate_daily_summary(args.daily_summary)
            print(json.dumps(summary, indent=2))

        elif args.client_report:
            report = tracker.generate_client_report(args.client_report, args.days)
            print(json.dumps(report, indent=2))

        elif args.export:
            success = tracker.export_activity_report(
                args.export,
                args.client_report,
                args.days
            )
            if success:
                print(f"✅ Report exported to {args.export}")
            else:
                print("❌ Failed to export report")
                sys.exit(1)

        else:
            # Record activity
            if not args.file:
                print("❌ --file is required for activity recording")
                sys.exit(1)

            record = tracker.record_activity(
                client=args.client,
                activity_type=args.activity,
                file_path=args.file,
                agent_name=args.agent,
                success=args.success
            )

            if record:
                print(f"✅ Activity recorded for {record.get('client_name', 'Unknown Client')}")
            else:
                print("❌ Failed to record activity")
                sys.exit(1)

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()