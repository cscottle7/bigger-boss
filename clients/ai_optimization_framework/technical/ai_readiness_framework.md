# AI Readiness Assessment Framework - September 2025

## Executive Summary
This framework provides a comprehensive evaluation methodology for assessing website readiness for AI search systems. The scoring system evaluates technical infrastructure, content optimization, authority signals, and performance metrics across all major AI platforms including ChatGPT, Claude, Perplexity, and Google AI Overviews.

## Assessment Methodology Overview

### Overall Scoring Framework
**Total Score: 100 Points**
- **Module 1: Technical Foundation** (25 points)
- **Module 2: AI Citability Score** (25 points) 
- **Module 3: Authority & E-E-A-T Score** (25 points)
- **Module 4: Competitive AI Position** (25 points)

### Performance Rating Scale
- **90-100 points**: Excellent - AI optimization leader
- **80-89 points**: Good - Strong AI readiness with minor gaps
- **70-79 points**: Needs Improvement - Moderate optimization required
- **Below 70 points**: Poor - Significant AI optimization needed

## Module 1: Technical Foundation Assessment (25 Points)

### 1.1 AI Crawler Accessibility (8 points)

#### Google-Extended Access (3 points)
**Evaluation Criteria:**
- **3 points**: robots.txt explicitly allows Google-Extended
- **2 points**: No specific blocking of Google-Extended
- **1 point**: Partial blocking with some allowed directories
- **0 points**: Complete blocking of Google-Extended

**Assessment Method:**
```
Check robots.txt for:
User-agent: Google-Extended
Allow: /
```

#### GPTBot Access (3 points)
**Evaluation Criteria:**
- **3 points**: robots.txt explicitly allows GPTBot
- **2 points**: No specific blocking of GPTBot
- **1 point**: Partial blocking with core content accessible
- **0 points**: Complete blocking of GPTBot

**Assessment Method:**
```
Check robots.txt for:
User-agent: GPTBot
Allow: /
```

#### Other AI Crawler Support (2 points)
**Evaluation Criteria:**
- **2 points**: Supports Claude-Web, Perplexity, and other major AI crawlers
- **1 point**: Supports some additional AI crawlers
- **0 points**: No additional AI crawler support

### 1.2 llms.txt Protocol Implementation (4 points)

#### Protocol Presence (2 points)
**Evaluation Criteria:**
- **2 points**: llms.txt file present and properly formatted
- **1 point**: llms.txt present but incomplete
- **0 points**: No llms.txt implementation

#### Content Quality (2 points)
**Evaluation Criteria:**
- **2 points**: Comprehensive site description, key pages, and usage guidelines
- **1 point**: Basic implementation with minimal information
- **0 points**: Empty or invalid llms.txt content

### 1.3 Schema Markup Implementation (8 points)

#### Organization Schema (3 points)
**Evaluation Criteria:**
- **3 points**: Complete Organization schema with name, logo, address, sameAs links
- **2 points**: Basic Organization schema with core elements
- **1 point**: Partial Organization schema implementation
- **0 points**: No Organization schema

**Required Elements:**
- Organization name and description
- Logo and contact information
- Physical address (for local businesses)
- Social media profiles (sameAs)
- AHPRA registration number (where applicable)

#### Person Schema (3 points)
**Evaluation Criteria:**
- **3 points**: Comprehensive Person schema for key professionals with credentials
- **2 points**: Basic Person schema for main professionals
- **1 point**: Limited Person schema implementation
- **0 points**: No Person schema

**Required Elements for Australian Professionals:**
- Full professional credentials
- AHPRA registration numbers
- Professional affiliations
- Areas of expertise
- Education and qualifications

#### Additional Schema Types (2 points)
**Evaluation Criteria:**
- **2 points**: FAQ, Service, Review, and other relevant schema types implemented
- **1 point**: Some additional schema types present
- **0 points**: No additional schema implementation

### 1.4 Semantic HTML Structure (5 points)

#### Heading Hierarchy (2 points)
**Evaluation Criteria:**
- **2 points**: Perfect H1-H6 hierarchy with logical content structure
- **1 point**: Good hierarchy with minor inconsistencies
- **0 points**: Poor or missing heading structure

#### HTML5 Semantic Elements (2 points)
**Evaluation Criteria:**
- **2 points**: Proper use of article, section, nav, aside, header, footer elements
- **1 point**: Some semantic elements used correctly
- **0 points**: Limited or incorrect semantic markup

#### Accessibility Features (1 point)
**Evaluation Criteria:**
- **1 point**: Alt text, ARIA labels, and accessibility compliance present
- **0 points**: Missing accessibility features

## Module 2: AI Citability Score (25 Points)

### 2.1 Content Structure Optimization (10 points)

#### Question-Based Headings (3 points)
**Evaluation Criteria:**
- **3 points**: 80%+ of headings formatted as questions or clear topics
- **2 points**: 60-79% question-based headings
- **1 point**: 40-59% question-based headings
- **0 points**: Less than 40% question-based headings

#### Answer-First Format (3 points)
**Evaluation Criteria:**
- **3 points**: Direct answers provided within first 50 words of content sections
- **2 points**: Answers provided within first paragraph
- **1 point**: Answers provided within first section
- **0 points**: No clear answer-first structure

#### Content Block Structure (2 points)
**Evaluation Criteria:**
- **2 points**: Clear content blocks with semantic indicators ("in summary", etc.)
- **1 point**: Some content blocking present
- **0 points**: No clear content structure

#### Conversational Flow (2 points)
**Evaluation Criteria:**
- **2 points**: Natural language flow with conversational transitions
- **1 point**: Some conversational elements present
- **0 points**: Formal, non-conversational writing style

### 2.2 Factual Writing Quality (8 points)

#### Accuracy and Precision (3 points)
**Evaluation Criteria:**
- **3 points**: All factual claims verified with credible sources
- **2 points**: Most claims supported with sources
- **1 point**: Some source verification present
- **0 points**: Limited or no source verification

#### Professional Terminology (2 points)
**Evaluation Criteria:**
- **2 points**: Appropriate use of professional terminology with explanations
- **1 point**: Good terminology use with some explanations
- **0 points**: Limited professional terminology or explanations

#### Australian Context Integration (3 points)
**Evaluation Criteria:**
- **3 points**: Comprehensive Australian regulations, standards, and context
- **2 points**: Good Australian context with some specifics
- **1 point**: Basic Australian references
- **0 points**: No Australian context

### 2.3 Citation and Source Quality (7 points)

#### Source Authority (3 points)
**Evaluation Criteria:**
- **3 points**: All sources from authoritative, peer-reviewed, or government sources
- **2 points**: Most sources authoritative with some secondary sources
- **1 point**: Mixed source quality
- **0 points**: Poor or questionable source quality

#### Citation Format (2 points)
**Evaluation Criteria:**
- **2 points**: Consistent, AI-friendly citation format throughout
- **1 point**: Generally consistent citation format
- **0 points**: Inconsistent or poor citation format

#### Source Recency (2 points)
**Evaluation Criteria:**
- **2 points**: All sources within 2 years for dynamic fields, 5 years for stable topics
- **1 point**: Most sources recent with some older references
- **0 points**: Outdated source material

## Module 3: Authority & E-E-A-T Score (25 Points)

### 3.1 Expertise Signals (10 points)

#### Professional Credentials (4 points)
**Evaluation Criteria:**
- **4 points**: Complete professional credentials with AHPRA registration displayed
- **3 points**: Good credential display with most professional qualifications
- **2 points**: Basic credential information present
- **1 point**: Limited credential display
- **0 points**: No professional credentials shown

#### Experience Documentation (3 points)
**Evaluation Criteria:**
- **3 points**: Detailed experience history with specific achievements
- **2 points**: Good experience overview with some specifics
- **1 point**: Basic experience information
- **0 points**: No experience documentation

#### Specialization Areas (3 points)
**Evaluation Criteria:**
- **3 points**: Clear specialization areas with expertise depth
- **2 points**: Well-defined specializations
- **1 point**: Some specialization information
- **0 points**: No clear specialization focus

### 3.2 Authority Indicators (8 points)

#### Professional Associations (2 points)
**Evaluation Criteria:**
- **2 points**: Active membership in relevant professional associations
- **1 point**: Some professional association affiliations
- **0 points**: No professional association memberships

#### Industry Recognition (3 points)
**Evaluation Criteria:**
- **3 points**: Awards, speaking engagements, published works, media mentions
- **2 points**: Some industry recognition present
- **1 point**: Limited recognition indicators
- **0 points**: No industry recognition

#### Client Testimonials and Reviews (3 points)
**Evaluation Criteria:**
- **3 points**: Comprehensive testimonials with specific outcomes and verification
- **2 points**: Good testimonial quality with some specifics
- **1 point**: Basic testimonials present
- **0 points**: No testimonials or reviews

### 3.3 Trust Indicators (7 points)

#### Contact Information Transparency (2 points)
**Evaluation Criteria:**
- **2 points**: Complete contact information with physical address and multiple contact methods
- **1 point**: Good contact information with address
- **0 points**: Limited contact information

#### Privacy and Security (2 points)
**Evaluation Criteria:**
- **2 points**: SSL certificate, privacy policy, and security measures clearly communicated
- **1 point**: Basic security measures present
- **0 points**: Limited security indicators

#### Professional Insurance and Compliance (3 points)
**Evaluation Criteria:**
- **3 points**: Professional insurance, AHPRA compliance, and regulatory adherence documented
- **2 points**: Some compliance documentation present
- **1 point**: Basic compliance references
- **0 points**: No compliance documentation

## Module 4: Competitive AI Position Score (25 Points)

### 4.1 Current AI Citation Analysis (10 points)

#### Cross-Platform Presence (4 points)
**Evaluation Criteria:**
- **4 points**: Citations present across ChatGPT, Claude, Perplexity, and Google AI Overviews
- **3 points**: Citations on 3 major platforms
- **2 points**: Citations on 2 major platforms
- **1 point**: Citations on 1 major platform
- **0 points**: No identifiable AI citations

#### Citation Quality (3 points)
**Evaluation Criteria:**
- **3 points**: High-quality citations with full context and accurate representation
- **2 points**: Good citation quality with accurate information
- **1 point**: Basic citations with some accuracy
- **0 points**: Poor or inaccurate citations

#### Citation Frequency (3 points)
**Evaluation Criteria:**
- **3 points**: Regular citations for target topic areas (multiple per month)
- **2 points**: Moderate citation frequency (weekly)
- **1 point**: Occasional citations (monthly)
- **0 points**: Rare or no citations

### 4.2 Voice Search Performance (8 points)

#### Featured Snippet Capture (3 points)
**Evaluation Criteria:**
- **3 points**: 60%+ of target queries result in featured snippets
- **2 points**: 40-59% featured snippet capture
- **1 point**: 20-39% featured snippet capture
- **0 points**: Less than 20% featured snippet capture

#### Voice Query Ranking (3 points)
**Evaluation Criteria:**
- **3 points**: Top 3 ranking for conversational queries
- **2 points**: Top 5 ranking for most conversational queries
- **1 point**: Top 10 ranking for conversational queries
- **0 points**: Poor voice query ranking

#### Local Voice Search (2 points)
**Evaluation Criteria:**
- **2 points**: Strong performance for "near me" and local voice queries
- **1 point**: Moderate local voice search performance
- **0 points**: Poor local voice search ranking

### 4.3 Competitive Benchmarking (7 points)

#### Market Position (3 points)
**Evaluation Criteria:**
- **3 points**: Leading AI citation frequency in target market/topic area
- **2 points**: Top 3 position for AI citations in market
- **1 point**: Competitive AI citation presence
- **0 points**: Below average AI citation performance

#### Growth Trajectory (2 points)
**Evaluation Criteria:**
- **2 points**: Increasing AI citation frequency over past 6 months
- **1 point**: Stable AI citation frequency
- **0 points**: Declining AI citation frequency

#### Opportunity Identification (2 points)
**Evaluation Criteria:**
- **2 points**: Clear opportunities identified for citation improvement
- **1 point**: Some improvement opportunities present
- **0 points**: Limited improvement opportunities identified

## Assessment Implementation Process

### Step 1: Technical Audit
1. Analyze robots.txt for AI crawler accessibility
2. Verify llms.txt implementation and content quality
3. Evaluate schema markup completeness and accuracy
4. Assess semantic HTML structure and accessibility

### Step 2: Content Analysis
1. Review content structure for AI optimization
2. Evaluate answer-first formatting implementation
3. Assess question-based heading usage
4. Analyze citation quality and source authority

### Step 3: Authority Evaluation
1. Verify professional credentials and compliance
2. Assess expertise documentation and specialization
3. Evaluate trust indicators and transparency
4. Review authority signals and industry recognition

### Step 4: Competitive Position Analysis
1. Test AI platform citations through direct queries
2. Analyze voice search performance for target terms
3. Benchmark against top competitors in market
4. Identify improvement opportunities and gaps

## Scoring Report Template

### AI Readiness Assessment Report
```
Website: [Target URL]
Assessment Date: [Date]
Overall AI Readiness Score: [X/100]

Module Scores:
- Technical Foundation: [X/25]
- AI Citability Score: [X/25]
- Authority & E-E-A-T: [X/25]
- Competitive Position: [X/25]

Performance Rating: [Excellent/Good/Needs Improvement/Poor]

Critical Issues:
- [List priority issues requiring immediate attention]

Improvement Recommendations:
- [Top 3 recommendations for score improvement]

Implementation Timeline:
- [90-day improvement plan with milestones]
```

## Quality Assurance and Validation

### Assessment Accuracy Requirements
- All technical evaluations verified through automated tools where possible
- Manual verification of AI citations through direct platform testing
- Professional credential verification through official databases
- Source authority validation through recognized authority metrics

### Regular Assessment Updates
- Quarterly reassessment recommended for dynamic scoring elements
- Annual comprehensive review for all modules
- Immediate reassessment after major website changes or AI algorithm updates
- Competitive position monitoring on monthly basis

This framework provides the definitive methodology for evaluating AI readiness across all major platforms while ensuring Australian professional standards compliance and market competitiveness.