"""
Human Review Gateway
Implements human-on-the-loop gates with SLA compliance for audit approvals.
"""

import asyncio
import json
import logging
import time
from typing import Dict, List, Optional, Any, Union, Callable
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import threading
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ReviewStatus(str, Enum):
    """Review status enumeration"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ESCALATED = "escalated"
    EXPIRED = "expired"


class ReviewPriority(str, Enum):
    """Review priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ReviewRequest:
    """Review request structure"""
    review_id: str
    workflow_type: str
    item_type: str  # "audit_report", "content_brief", "strategy_document"
    content: Dict[str, Any]
    requester: str
    priority: ReviewPriority
    created_at: float
    sla_deadline: float
    escalation_deadline: float
    status: ReviewStatus = ReviewStatus.PENDING
    reviewer_email: Optional[str] = None
    review_notes: Optional[str] = None
    reviewed_at: Optional[float] = None


@dataclass
class ReviewResponse:
    """Review response structure"""
    review_id: str
    status: ReviewStatus
    approved: bool
    feedback: str
    reviewer: str
    reviewed_at: float
    next_actions: List[str]


class HumanReviewGateway:
    """
    Manages human-on-the-loop approval gates with SLA compliance.
    Implements 24-hour SLA with 12-hour escalation as per risk mitigation strategy.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._default_config()
        self.pending_reviews: Dict[str, ReviewRequest] = {}
        self.review_history: List[ReviewRequest] = []
        self.active_timers: Dict[str, threading.Timer] = {}
        
        # Initialize review dashboard data
        self.dashboard_data = {
            "active_reviews": 0,
            "pending_escalations": 0,
            "sla_compliance_rate": 100.0,
            "average_review_time": 0.0
        }
    
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for review gateway"""
        return {
            "sla_hours": 24,
            "escalation_hours": 12,
            "reminder_hours": [6, 18],  # Send reminders at 6h and 18h
            "reviewers": {
                "audit_report": ["seo.manager@company.com"],
                "content_brief": ["content.director@company.com"],
                "strategy_document": ["strategy.lead@company.com"]
            },
            "escalation_contacts": ["director@company.com", "manager@company.com"],
            "email": {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "sender_email": "system@company.com",
                "sender_password": "app_password_here"  # Use app password in production
            },
            "approval_interface": {
                "base_url": "https://company.com/review",
                "timeout_minutes": 30
            }
        }
    
    async def submit_for_review(self, 
                              workflow_type: str,
                              item_type: str,
                              content: Dict[str, Any],
                              priority: ReviewPriority = ReviewPriority.MEDIUM,
                              requester: str = "system") -> str:
        """
        Submit item for human review with SLA tracking.
        
        Args:
            workflow_type: Type of workflow (sitespect, contentforge, etc.)
            item_type: Type of item being reviewed
            content: The content requiring review
            priority: Review priority level
            requester: Who requested the review
            
        Returns:
            Review ID for tracking
        """
        review_id = f"review_{int(time.time())}_{len(self.pending_reviews)}"
        
        # Calculate SLA deadlines based on priority
        sla_hours = self._get_sla_hours(priority)
        escalation_hours = self._get_escalation_hours(priority)
        
        current_time = time.time()
        review_request = ReviewRequest(
            review_id=review_id,
            workflow_type=workflow_type,
            item_type=item_type,
            content=content,
            requester=requester,
            priority=priority,
            created_at=current_time,
            sla_deadline=current_time + (sla_hours * 3600),
            escalation_deadline=current_time + (escalation_hours * 3600)
        )
        
        # Store review request
        self.pending_reviews[review_id] = review_request
        self._update_dashboard_metrics()
        
        # Send initial review notification
        await self._send_review_notification(review_request, "new_review")
        
        # Schedule reminders and escalation
        self._schedule_review_timers(review_request)
        
        logger.info(f"Submitted {item_type} for review: {review_id} (Priority: {priority.value})")
        return review_id
    
    async def check_review_status(self, review_id: str) -> Optional[ReviewStatus]:
        """Check the current status of a review request"""
        if review_id in self.pending_reviews:
            request = self.pending_reviews[review_id]
            
            # Check if review has expired
            if time.time() > request.sla_deadline and request.status == ReviewStatus.PENDING:
                request.status = ReviewStatus.EXPIRED
                await self._handle_expired_review(request)
            
            return request.status
        
        # Check review history
        for review in self.review_history:
            if review.review_id == review_id:
                return review.status
        
        return None
    
    async def wait_for_approval(self, review_id: str, timeout_hours: Optional[float] = None) -> ReviewResponse:
        """
        Wait for review approval with optional timeout.
        
        Args:
            review_id: Review ID to wait for
            timeout_hours: Maximum time to wait (defaults to SLA deadline)
            
        Returns:
            ReviewResponse with approval status and feedback
        """
        if review_id not in self.pending_reviews:
            raise ValueError(f"Review ID not found: {review_id}")
        
        request = self.pending_reviews[review_id]
        timeout_seconds = (timeout_hours * 3600) if timeout_hours else (request.sla_deadline - time.time())
        
        logger.info(f"Waiting for approval on {review_id} (timeout: {timeout_seconds/3600:.1f} hours)")
        
        # Poll for status changes
        start_time = time.time()
        while time.time() - start_time < timeout_seconds:
            current_status = await self.check_review_status(review_id)
            
            if current_status in [ReviewStatus.APPROVED, ReviewStatus.REJECTED, ReviewStatus.EXPIRED]:
                # Review completed, return response
                final_request = self.pending_reviews.get(review_id)
                if not final_request:
                    # Check history
                    final_request = next((r for r in self.review_history if r.review_id == review_id), None)
                
                if final_request:
                    return ReviewResponse(
                        review_id=review_id,
                        status=final_request.status,
                        approved=(final_request.status == ReviewStatus.APPROVED),
                        feedback=final_request.review_notes or "",
                        reviewer=final_request.reviewer_email or "system",
                        reviewed_at=final_request.reviewed_at or time.time(),
                        next_actions=self._generate_next_actions(final_request)
                    )
            
            await asyncio.sleep(30)  # Check every 30 seconds
        
        # Timeout reached
        logger.warning(f"Review timeout reached for {review_id}")
        return ReviewResponse(
            review_id=review_id,
            status=ReviewStatus.EXPIRED,
            approved=False,
            feedback="Review timeout exceeded",
            reviewer="system",
            reviewed_at=time.time(),
            next_actions=["Consider proceeding without approval", "Escalate to management"]
        )
    
    def submit_review_response(self, 
                             review_id: str,
                             approved: bool,
                             feedback: str,
                             reviewer_email: str) -> bool:
        """
        Submit review response (simulates human reviewer interface).
        In production, this would be called by the web interface.
        """
        if review_id not in self.pending_reviews:
            logger.error(f"Review ID not found: {review_id}")
            return False
        
        request = self.pending_reviews[review_id]
        request.status = ReviewStatus.APPROVED if approved else ReviewStatus.REJECTED
        request.reviewer_email = reviewer_email
        request.review_notes = feedback
        request.reviewed_at = time.time()
        
        # Move to history and remove from pending
        self.review_history.append(request)
        del self.pending_reviews[review_id]
        
        # Cancel any active timers
        self._cancel_review_timers(review_id)
        
        # Update dashboard metrics
        self._update_dashboard_metrics()
        
        logger.info(f"Review {review_id} {'approved' if approved else 'rejected'} by {reviewer_email}")
        return True
    
    def get_review_dashboard(self) -> Dict[str, Any]:
        """Get current review dashboard data"""
        # Update real-time metrics
        self._update_dashboard_metrics()
        
        # Get pending reviews summary
        pending_summary = []
        for request in self.pending_reviews.values():
            time_remaining = max(0, request.sla_deadline - time.time())
            pending_summary.append({
                "review_id": request.review_id,
                "item_type": request.item_type,
                "priority": request.priority.value,
                "hours_remaining": time_remaining / 3600,
                "escalation_due": time.time() > request.escalation_deadline,
                "created_at": datetime.fromtimestamp(request.created_at).isoformat()
            })
        
        return {
            "dashboard_metrics": self.dashboard_data,
            "pending_reviews": pending_summary,
            "recent_reviews": [
                {
                    "review_id": r.review_id,
                    "item_type": r.item_type,
                    "status": r.status.value,
                    "reviewer": r.reviewer_email,
                    "reviewed_at": datetime.fromtimestamp(r.reviewed_at).isoformat() if r.reviewed_at else None
                } for r in self.review_history[-10:]  # Last 10 reviews
            ]
        }
    
    async def _send_review_notification(self, request: ReviewRequest, notification_type: str):
        """Send email notification for review request"""
        try:
            # Determine recipients based on item type
            recipients = self.config["reviewers"].get(request.item_type, [])
            if not recipients:
                logger.warning(f"No reviewers configured for {request.item_type}")
                return
            
            # Create email content
            if notification_type == "new_review":
                subject = f"New Review Required: {request.item_type} ({request.priority.value} priority)"
                body = self._create_review_email_body(request)
            elif notification_type == "reminder":
                subject = f"Review Reminder: {request.review_id}"
                body = self._create_reminder_email_body(request)
            elif notification_type == "escalation":
                subject = f"ESCALATION: Overdue Review {request.review_id}"
                body = self._create_escalation_email_body(request)
                recipients.extend(self.config["escalation_contacts"])
            else:
                return
            
            # In production, this would send actual emails
            # For now, we'll just log the notification
            logger.info(f"Email notification ({notification_type}) sent for {request.review_id}")
            logger.debug(f"Recipients: {recipients}")
            logger.debug(f"Subject: {subject}")
            
        except Exception as e:
            logger.error(f"Failed to send notification for {request.review_id}: {e}")
    
    def _create_review_email_body(self, request: ReviewRequest) -> str:
        """Create email body for new review request"""
        approval_url = f"{self.config['approval_interface']['base_url']}/{request.review_id}"
        
        return f"""
A new {request.item_type} requires your review.

Review ID: {request.review_id}
Workflow: {request.workflow_type}
Priority: {request.priority.value}
Requested by: {request.requester}
SLA Deadline: {datetime.fromtimestamp(request.sla_deadline).strftime('%Y-%m-%d %H:%M:%S')}

Review Content Summary:
{json.dumps(request.content, indent=2)[:500]}...

Please review and approve/reject at: {approval_url}

This review must be completed within {self._get_sla_hours(request.priority)} hours to meet SLA requirements.
"""
    
    def _create_reminder_email_body(self, request: ReviewRequest) -> str:
        """Create email body for review reminder"""
        hours_remaining = max(0, (request.sla_deadline - time.time()) / 3600)
        
        return f"""
REMINDER: Review {request.review_id} is still pending.

Time remaining: {hours_remaining:.1f} hours
Priority: {request.priority.value}
Item: {request.item_type}

Please complete your review to meet SLA requirements.
Review URL: {self.config['approval_interface']['base_url']}/{request.review_id}
"""
    
    def _create_escalation_email_body(self, request: ReviewRequest) -> str:
        """Create email body for review escalation"""
        hours_overdue = (time.time() - request.escalation_deadline) / 3600
        
        return f"""
ESCALATION: Review {request.review_id} is overdue.

Overdue by: {hours_overdue:.1f} hours
Priority: {request.priority.value}
Item: {request.item_type}
Original Deadline: {datetime.fromtimestamp(request.sla_deadline).strftime('%Y-%m-%d %H:%M:%S')}

This review requires immediate management attention.
Review URL: {self.config['approval_interface']['base_url']}/{request.review_id}
"""
    
    def _schedule_review_timers(self, request: ReviewRequest):
        """Schedule reminder and escalation timers for review request"""
        review_id = request.review_id
        
        # Schedule reminders
        for reminder_hours in self.config["reminder_hours"]:
            reminder_time = request.created_at + (reminder_hours * 3600)
            if reminder_time < request.escalation_deadline:  # Don't send reminders after escalation
                delay = max(0, reminder_time - time.time())
                
                timer = threading.Timer(delay, self._send_reminder, [request])
                timer.daemon = True
                timer.start()
                
                self.active_timers[f"{review_id}_reminder_{reminder_hours}"] = timer
        
        # Schedule escalation
        escalation_delay = max(0, request.escalation_deadline - time.time())
        escalation_timer = threading.Timer(escalation_delay, self._handle_escalation, [request])
        escalation_timer.daemon = True
        escalation_timer.start()
        
        self.active_timers[f"{review_id}_escalation"] = escalation_timer
    
    def _send_reminder(self, request: ReviewRequest):
        """Send reminder notification (called by timer)"""
        if request.review_id in self.pending_reviews and request.status == ReviewStatus.PENDING:
            asyncio.create_task(self._send_review_notification(request, "reminder"))
    
    def _handle_escalation(self, request: ReviewRequest):
        """Handle review escalation (called by timer)"""
        if request.review_id in self.pending_reviews and request.status == ReviewStatus.PENDING:
            request.status = ReviewStatus.ESCALATED
            asyncio.create_task(self._send_review_notification(request, "escalation"))
            logger.warning(f"Review {request.review_id} escalated due to missed deadline")
    
    async def _handle_expired_review(self, request: ReviewRequest):
        """Handle expired review that exceeded SLA"""
        logger.error(f"Review {request.review_id} expired (exceeded SLA deadline)")
        
        # Move to history
        self.review_history.append(request)
        if request.review_id in self.pending_reviews:
            del self.pending_reviews[request.review_id]
        
        # Cancel timers
        self._cancel_review_timers(request.review_id)
        
        # Update metrics
        self._update_dashboard_metrics()
    
    def _cancel_review_timers(self, review_id: str):
        """Cancel all timers associated with a review"""
        timers_to_cancel = [key for key in self.active_timers.keys() if key.startswith(review_id)]
        
        for timer_key in timers_to_cancel:
            timer = self.active_timers.pop(timer_key)
            timer.cancel()
    
    def _get_sla_hours(self, priority: ReviewPriority) -> int:
        """Get SLA hours based on priority"""
        sla_mapping = {
            ReviewPriority.CRITICAL: 4,
            ReviewPriority.HIGH: 8,
            ReviewPriority.MEDIUM: 24,
            ReviewPriority.LOW: 48
        }
        return sla_mapping.get(priority, 24)
    
    def _get_escalation_hours(self, priority: ReviewPriority) -> int:
        """Get escalation hours based on priority"""
        escalation_mapping = {
            ReviewPriority.CRITICAL: 2,
            ReviewPriority.HIGH: 4,
            ReviewPriority.MEDIUM: 12,
            ReviewPriority.LOW: 24
        }
        return escalation_mapping.get(priority, 12)
    
    def _update_dashboard_metrics(self):
        """Update dashboard metrics"""
        self.dashboard_data["active_reviews"] = len(self.pending_reviews)
        self.dashboard_data["pending_escalations"] = sum(
            1 for r in self.pending_reviews.values() 
            if r.status == ReviewStatus.ESCALATED
        )
        
        # Calculate SLA compliance rate
        total_completed = len([r for r in self.review_history if r.status in [ReviewStatus.APPROVED, ReviewStatus.REJECTED]])
        sla_compliant = len([r for r in self.review_history 
                           if r.status in [ReviewStatus.APPROVED, ReviewStatus.REJECTED]
                           and r.reviewed_at and r.reviewed_at <= r.sla_deadline])
        
        if total_completed > 0:
            self.dashboard_data["sla_compliance_rate"] = (sla_compliant / total_completed) * 100
        
        # Calculate average review time
        completed_reviews = [r for r in self.review_history 
                           if r.status in [ReviewStatus.APPROVED, ReviewStatus.REJECTED] and r.reviewed_at]
        if completed_reviews:
            avg_time = sum(r.reviewed_at - r.created_at for r in completed_reviews) / len(completed_reviews)
            self.dashboard_data["average_review_time"] = avg_time / 3600  # Convert to hours
    
    def _generate_next_actions(self, request: ReviewRequest) -> List[str]:
        """Generate next actions based on review result"""
        if request.status == ReviewStatus.APPROVED:
            return ["Proceed with workflow execution", "Implement approved plan"]
        elif request.status == ReviewStatus.REJECTED:
            return ["Revise based on feedback", "Resubmit for review"]
        elif request.status == ReviewStatus.EXPIRED:
            return ["Escalate to management", "Consider proceeding with caution"]
        elif request.status == ReviewStatus.ESCALATED:
            return ["Await management decision", "Prepare alternative approaches"]
        else:
            return ["Continue monitoring"]


# Initialize global review gateway
review_gateway = HumanReviewGateway()

# Export main functions
__all__ = [
    'HumanReviewGateway',
    'ReviewRequest', 
    'ReviewResponse',
    'ReviewStatus',
    'ReviewPriority',
    'review_gateway'
]

# Convenience functions for workflows
async def submit_audit_for_review(audit_result: Dict[str, Any], priority: ReviewPriority = ReviewPriority.MEDIUM) -> str:
    """Submit audit result for human review"""
    return await review_gateway.submit_for_review(
        workflow_type="sitespect",
        item_type="audit_report", 
        content=audit_result,
        priority=priority,
        requester="sitespect_orchestrator"
    )

async def wait_for_audit_approval(review_id: str) -> ReviewResponse:
    """Wait for audit approval"""
    return await review_gateway.wait_for_approval(review_id)

async def submit_content_brief_for_review(content_brief: Dict[str, Any], priority: ReviewPriority = ReviewPriority.MEDIUM) -> str:
    """Submit content brief for human review"""
    return await review_gateway.submit_for_review(
        workflow_type="contentforge",
        item_type="content_brief",
        content=content_brief,
        priority=priority,
        requester="content_orchestrator"
    )

async def wait_for_content_approval(review_id: str) -> ReviewResponse:
    """Wait for content brief approval"""
    return await review_gateway.wait_for_approval(review_id)