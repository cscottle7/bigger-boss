"""
Database Manager for Bigger Boss Agent System
Handles SQLite database initialization, queries, and migrations
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database operations for the autonomous marketing system"""

    def __init__(self, db_path: str = "system/database/bigger_boss.db"):
        """Initialize database connection"""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        try:
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
            self.cursor = self.conn.cursor()
            logger.info(f"Connected to database: {self.db_path}")
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise

    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")

    def initialize_database(self):
        """Create all tables from schema.sql"""
        try:
            schema_path = Path("system/database/schema.sql")

            if not schema_path.exists():
                logger.error(f"Schema file not found: {schema_path}")
                return False

            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()

            # Execute schema (handles multiple statements)
            self.cursor.executescript(schema_sql)
            self.conn.commit()

            logger.info("Database initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Database initialization error: {e}")
            return False

    # ============================================================
    # CLIENT OPERATIONS
    # ============================================================

    def add_client(self, domain: str, business_name: str = None, industry: str = None,
                   location: str = None, notes: str = None) -> int:
        """Add new client to database"""
        try:
            self.cursor.execute("""
                INSERT INTO clients (domain, business_name, industry, location, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (domain, business_name, industry, location, notes))

            self.conn.commit()
            client_id = self.cursor.lastrowid
            logger.info(f"Added client: {domain} (ID: {client_id})")
            return client_id

        except sqlite3.IntegrityError:
            logger.warning(f"Client already exists: {domain}")
            return self.get_client_id(domain)
        except Exception as e:
            logger.error(f"Error adding client: {e}")
            return None

    def get_client_id(self, domain: str) -> Optional[int]:
        """Get client ID by domain"""
        self.cursor.execute("SELECT id FROM clients WHERE domain = ?", (domain,))
        result = self.cursor.fetchone()
        return result['id'] if result else None

    def get_client(self, domain: str) -> Optional[Dict]:
        """Get client details by domain"""
        self.cursor.execute("SELECT * FROM clients WHERE domain = ?", (domain,))
        result = self.cursor.fetchone()
        return dict(result) if result else None

    def update_client_audit_count(self, client_id: int):
        """Increment client audit count"""
        self.cursor.execute("""
            UPDATE clients
            SET total_audits = total_audits + 1,
                last_audit_date = CURRENT_TIMESTAMP,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (client_id,))
        self.conn.commit()

    # ============================================================
    # AUDIT OPERATIONS
    # ============================================================

    def log_audit_result(self, client_id: int, audit_type: str, scores: Dict,
                        report_path: str = None, agent_executed: str = None,
                        execution_time: int = None, success: bool = True,
                        error_message: str = None) -> int:
        """Log audit results to database"""
        try:
            self.cursor.execute("""
                INSERT INTO audit_results (
                    client_id, audit_type, performance_score, seo_score,
                    accessibility_score, content_quality_score, pagespeed_score,
                    lcp_score, fid_score, cls_score, page_size_bytes, total_requests,
                    report_path, agent_executed, execution_time_seconds, success, error_message
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                client_id, audit_type,
                scores.get('performance_score'),
                scores.get('seo_score'),
                scores.get('accessibility_score'),
                scores.get('content_quality_score'),
                scores.get('pagespeed_score'),
                scores.get('lcp_score'),
                scores.get('fid_score'),
                scores.get('cls_score'),
                scores.get('page_size_bytes'),
                scores.get('total_requests'),
                report_path, agent_executed, execution_time, success, error_message
            ))

            self.conn.commit()
            audit_id = self.cursor.lastrowid

            # Update client audit count
            self.update_client_audit_count(client_id)

            logger.info(f"Logged audit result (ID: {audit_id}) for client {client_id}")
            return audit_id

        except Exception as e:
            logger.error(f"Error logging audit result: {e}")
            return None

    def get_client_audit_history(self, client_id: int, limit: int = 10) -> List[Dict]:
        """Get audit history for a client"""
        self.cursor.execute("""
            SELECT * FROM audit_results
            WHERE client_id = ?
            ORDER BY audit_date DESC
            LIMIT ?
        """, (client_id, limit))

        return [dict(row) for row in self.cursor.fetchall()]

    # ============================================================
    # API USAGE TRACKING
    # ============================================================

    def log_api_usage(self, api_service: str, client_id: int = None,
                     calls_made: int = 1, tokens_used: int = None,
                     cost_estimate: float = None, endpoint: str = None,
                     request_type: str = None, status: str = 'success',
                     error_message: str = None) -> int:
        """Log API usage"""
        try:
            self.cursor.execute("""
                INSERT INTO api_usage (
                    api_service, client_id, calls_made, tokens_used, cost_estimate,
                    endpoint, request_type, status, error_message
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                api_service, client_id, calls_made, tokens_used, cost_estimate,
                endpoint, request_type, status, error_message
            ))

            self.conn.commit()
            usage_id = self.cursor.lastrowid
            logger.info(f"Logged API usage: {api_service} (ID: {usage_id})")
            return usage_id

        except Exception as e:
            logger.error(f"Error logging API usage: {e}")
            return None

    def get_api_usage_summary(self, days: int = 30) -> List[Dict]:
        """Get API usage summary for last N days"""
        self.cursor.execute("""
            SELECT api_service,
                   COUNT(*) as total_calls,
                   SUM(tokens_used) as total_tokens,
                   SUM(cost_estimate) as total_cost
            FROM api_usage
            WHERE usage_date >= DATE('now', ?)
            GROUP BY api_service
        """, (f'-{days} days',))

        return [dict(row) for row in self.cursor.fetchall()]

    def get_monthly_api_costs(self) -> Dict[str, float]:
        """Get current month API costs by service"""
        self.cursor.execute("""
            SELECT api_service,
                   SUM(cost_estimate) as monthly_cost
            FROM api_usage
            WHERE strftime('%Y-%m', usage_date) = strftime('%Y-%m', 'now')
            GROUP BY api_service
        """)

        results = self.cursor.fetchall()
        return {row['api_service']: row['monthly_cost'] or 0.0 for row in results}

    # ============================================================
    # AUTOMATION LOGGING
    # ============================================================

    def log_automation_event(self, event_type: str, agent_name: str = None,
                            client_id: int = None, operation: str = None,
                            file_path: str = None, tool_used: str = None,
                            execution_time: float = None, tokens_used: int = None,
                            success: bool = True, error_message: str = None,
                            details: Dict = None) -> int:
        """Log automation event"""
        try:
            details_json = json.dumps(details) if details else None

            self.cursor.execute("""
                INSERT INTO automation_logs (
                    event_type, agent_name, client_id, operation, file_path,
                    tool_used, execution_time_seconds, tokens_used, success,
                    error_message, details
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event_type, agent_name, client_id, operation, file_path,
                tool_used, execution_time, tokens_used, success,
                error_message, details_json
            ))

            self.conn.commit()
            log_id = self.cursor.lastrowid
            return log_id

        except Exception as e:
            logger.error(f"Error logging automation event: {e}")
            return None

    def get_recent_automation_logs(self, limit: int = 50) -> List[Dict]:
        """Get recent automation logs"""
        self.cursor.execute("""
            SELECT * FROM v_recent_automation_activity
            LIMIT ?
        """, (limit,))

        return [dict(row) for row in self.cursor.fetchall()]

    # ============================================================
    # PERFORMANCE TRACKING
    # ============================================================

    def log_performance_metrics(self, client_id: int, metrics: Dict,
                                test_location: str = 'Sydney, Australia',
                                source: str = 'gtmetrix') -> int:
        """Log performance metrics"""
        try:
            self.cursor.execute("""
                INSERT INTO performance_metrics (
                    client_id, lcp_score, fid_score, cls_score, pagespeed_score,
                    yslow_score, fully_loaded_time_ms, page_load_time_ms,
                    time_to_first_byte_ms, page_size_bytes, total_requests,
                    html_size_bytes, css_size_bytes, js_size_bytes, image_size_bytes,
                    test_location, source
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                client_id,
                metrics.get('lcp_score'),
                metrics.get('fid_score'),
                metrics.get('cls_score'),
                metrics.get('pagespeed_score'),
                metrics.get('yslow_score'),
                metrics.get('fully_loaded_time_ms'),
                metrics.get('page_load_time_ms'),
                metrics.get('time_to_first_byte_ms'),
                metrics.get('page_size_bytes'),
                metrics.get('total_requests'),
                metrics.get('html_size_bytes'),
                metrics.get('css_size_bytes'),
                metrics.get('js_size_bytes'),
                metrics.get('image_size_bytes'),
                test_location,
                source
            ))

            self.conn.commit()
            metric_id = self.cursor.lastrowid
            logger.info(f"Logged performance metrics (ID: {metric_id}) for client {client_id}")
            return metric_id

        except Exception as e:
            logger.error(f"Error logging performance metrics: {e}")
            return None

    def get_performance_trend(self, client_id: int, days: int = 30) -> List[Dict]:
        """Get performance trend for client"""
        self.cursor.execute("""
            SELECT metric_date, pagespeed_score, lcp_score, cls_score,
                   page_size_bytes, fully_loaded_time_ms
            FROM performance_metrics
            WHERE client_id = ?
            AND metric_date >= DATE('now', ?)
            ORDER BY metric_date DESC
        """, (client_id, f'-{days} days'))

        return [dict(row) for row in self.cursor.fetchall()]

    # ============================================================
    # CONTENT TRACKING
    # ============================================================

    def add_content(self, client_id: int, content_type: str, title: str,
                   word_count: int = None, target_keyword: str = None,
                   file_path: str = None, uniqueness_score: float = None) -> int:
        """Add content to inventory"""
        try:
            self.cursor.execute("""
                INSERT INTO content_inventory (
                    client_id, content_type, title, word_count, target_keyword,
                    file_path, uniqueness_score
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (client_id, content_type, title, word_count, target_keyword,
                  file_path, uniqueness_score))

            self.conn.commit()
            content_id = self.cursor.lastrowid
            logger.info(f"Added content (ID: {content_id}): {title}")
            return content_id

        except Exception as e:
            logger.error(f"Error adding content: {e}")
            return None

    def get_client_content(self, client_id: int) -> List[Dict]:
        """Get all content for a client"""
        self.cursor.execute("""
            SELECT * FROM content_inventory
            WHERE client_id = ?
            ORDER BY created_at DESC
        """, (client_id,))

        return [dict(row) for row in self.cursor.fetchall()]

    # ============================================================
    # REPORTING & ANALYTICS
    # ============================================================

    def get_client_overview(self, domain: str) -> Dict:
        """Get comprehensive client overview"""
        self.cursor.execute("""
            SELECT * FROM v_client_performance_overview
            WHERE domain = ?
        """, (domain,))

        result = self.cursor.fetchone()
        return dict(result) if result else None

    def get_system_stats(self) -> Dict:
        """Get overall system statistics"""
        stats = {}

        # Total clients
        self.cursor.execute("SELECT COUNT(*) as total FROM clients")
        stats['total_clients'] = self.cursor.fetchone()['total']

        # Active clients
        self.cursor.execute("SELECT COUNT(*) as total FROM clients WHERE status = 'active'")
        stats['active_clients'] = self.cursor.fetchone()['total']

        # Total audits
        self.cursor.execute("SELECT COUNT(*) as total FROM audit_results")
        stats['total_audits'] = self.cursor.fetchone()['total']

        # Total API calls this month
        self.cursor.execute("""
            SELECT COUNT(*) as total FROM api_usage
            WHERE strftime('%Y-%m', usage_date) = strftime('%Y-%m', 'now')
        """)
        stats['monthly_api_calls'] = self.cursor.fetchone()['total']

        # Monthly API costs
        stats['monthly_api_costs'] = self.get_monthly_api_costs()

        # Total content pieces
        self.cursor.execute("SELECT COUNT(*) as total FROM content_inventory")
        stats['total_content'] = self.cursor.fetchone()['total']

        return stats


# Global database instance
db = DatabaseManager()


def init_database():
    """Initialize database connection and schema"""
    db.connect()
    db.initialize_database()
    logger.info("Database ready for use")


def close_database():
    """Close database connection"""
    db.disconnect()
