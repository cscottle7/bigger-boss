"""
Data Validation Framework
Implements pre-flight validation using Pydantic models to prevent malformed input failures.
"""

from pydantic import BaseModel, HttpUrl, Field, validator
from typing import List, Optional, Dict, Any
from enum import Enum
import re
from pathlib import Path


class AuditType(str, Enum):
    """Types of audits that can be performed"""
    FULL = "full"
    TECHNICAL_SEO = "technical_seo"
    PERFORMANCE = "performance"
    ACCESSIBILITY = "accessibility"
    UX_FLOW = "ux_flow"
    AI_READINESS = "ai_readiness"


class ContentType(str, Enum):
    """Types of content that can be created"""
    BLOG_POST = "blog_post"
    LANDING_PAGE = "landing_page"
    PRODUCT_DESCRIPTION = "product_description"
    EMAIL_CAMPAIGN = "email_campaign"
    SOCIAL_MEDIA = "social_media"


class SiteAuditRequest(BaseModel):
    """Validation model for website audit requests"""
    url: HttpUrl = Field(..., description="The website URL to audit")
    audit_types: List[AuditType] = Field(default=[AuditType.FULL], description="Types of audits to perform")
    depth: int = Field(default=3, ge=1, le=5, description="Crawl depth (1-5 pages)")
    include_subdomains: bool = Field(default=False, description="Whether to include subdomains")
    custom_headers: Optional[Dict[str, str]] = Field(default=None, description="Custom HTTP headers")
    
    @validator('url')
    def validate_url_accessible(cls, v):
        """Ensure URL is publicly accessible"""
        url_str = str(v)
        if any(blocked in url_str.lower() for blocked in ['localhost', '127.0.0.1', '192.168.', '10.0.0.']):
            raise ValueError('URL must be publicly accessible (no localhost or private IPs)')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "url": "https://example.com",
                "audit_types": ["full"],
                "depth": 3,
                "include_subdomains": False
            }
        }


class ContentCreationRequest(BaseModel):
    """Validation model for content creation requests"""
    topic: str = Field(..., min_length=3, max_length=200, description="Main content topic")
    content_type: ContentType = Field(..., description="Type of content to create")
    target_audience: str = Field(..., min_length=3, max_length=500, description="Description of target audience")
    keyword_file_path: Optional[Path] = Field(default=None, description="Path to keyword research CSV file")
    brand_guidelines_path: Optional[Path] = Field(default=None, description="Path to brand guidelines PDF")
    competitor_urls: Optional[List[HttpUrl]] = Field(default=None, max_items=5, description="Competitor URLs for analysis")
    word_count_target: int = Field(default=1000, ge=100, le=10000, description="Target word count")
    
    @validator('keyword_file_path', 'brand_guidelines_path')
    def validate_file_exists(cls, v):
        """Ensure referenced files exist"""
        if v and not v.exists():
            raise ValueError(f'File does not exist: {v}')
        return v
    
    @validator('keyword_file_path')
    def validate_csv_file(cls, v):
        """Ensure keyword file is CSV format"""
        if v and v.suffix.lower() not in ['.csv', '.xlsx']:
            raise ValueError('Keyword file must be CSV or Excel format')
        return v
    
    @validator('brand_guidelines_path')
    def validate_pdf_file(cls, v):
        """Ensure brand guidelines is PDF format"""
        if v and v.suffix.lower() != '.pdf':
            raise ValueError('Brand guidelines must be PDF format')
        return v


class FileValidation:
    """Utility class for file validation"""
    
    @staticmethod
    def validate_csv_structure(file_path: Path, required_columns: List[str]) -> Dict[str, Any]:
        """Validate CSV file structure and return metadata"""
        try:
            import pandas as pd
            df = pd.read_csv(file_path)
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return {
                    'valid': False,
                    'error': f'Missing required columns: {missing_columns}',
                    'columns_found': df.columns.tolist()
                }
            
            return {
                'valid': True,
                'row_count': len(df),
                'columns': df.columns.tolist(),
                'sample_data': df.head(3).to_dict('records')
            }
        except Exception as e:
            return {
                'valid': False,
                'error': f'Failed to parse CSV: {str(e)}'
            }
    
    @staticmethod
    def validate_pdf_readability(file_path: Path) -> Dict[str, Any]:
        """Validate PDF file readability and return metadata"""
        try:
            import PyPDF2
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                page_count = len(reader.pages)
                
                # Try to extract text from first page
                first_page_text = reader.pages[0].extract_text()
                
                return {
                    'valid': True,
                    'page_count': page_count,
                    'text_extractable': len(first_page_text.strip()) > 0,
                    'sample_text': first_page_text[:200] + '...' if first_page_text else ''
                }
        except Exception as e:
            return {
                'valid': False,
                'error': f'Failed to parse PDF: {str(e)}'
            }


class ValidationError(Exception):
    """Custom exception for validation failures"""
    def __init__(self, message: str, details: Dict[str, Any] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


def validate_site_audit_input(data: Dict[str, Any]) -> SiteAuditRequest:
    """Validate and parse site audit input data"""
    try:
        return SiteAuditRequest(**data)
    except Exception as e:
        raise ValidationError(f"Invalid site audit request: {str(e)}", {'input_data': data})


def validate_content_creation_input(data: Dict[str, Any]) -> ContentCreationRequest:
    """Validate and parse content creation input data"""
    try:
        request = ContentCreationRequest(**data)
        
        # Additional file validation if files are provided
        validation_results = {}
        
        if request.keyword_file_path:
            csv_validation = FileValidation.validate_csv_structure(
                request.keyword_file_path,
                ['keyword', 'search_volume', 'difficulty']  # Required CSV columns
            )
            validation_results['keyword_file'] = csv_validation
            if not csv_validation['valid']:
                raise ValidationError("Invalid keyword file", csv_validation)
        
        if request.brand_guidelines_path:
            pdf_validation = FileValidation.validate_pdf_readability(request.brand_guidelines_path)
            validation_results['brand_file'] = pdf_validation
            if not pdf_validation['valid']:
                raise ValidationError("Invalid brand guidelines file", pdf_validation)
        
        return request, validation_results
    except Exception as e:
        raise ValidationError(f"Invalid content creation request: {str(e)}", {'input_data': data})


# Pre-flight validation functions
def sanitize_url(url: str) -> str:
    """Sanitize URL input to prevent injection attacks"""
    # Remove any potentially dangerous characters
    url = re.sub(r'[<>"\']', '', url)
    
    # Ensure it starts with http/https
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    return url


def validate_workflow_input(workflow_type: str, input_data: Dict[str, Any]) -> tuple:
    """Main validation entry point for all workflow types"""
    if workflow_type == 'site_audit':
        request = validate_site_audit_input(input_data)
        return request, {}
    elif workflow_type == 'content_creation':
        return validate_content_creation_input(input_data)
    else:
        raise ValidationError(f"Unknown workflow type: {workflow_type}")