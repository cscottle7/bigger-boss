# AGENT PROMPT TEMPLATE 2025 - TOKEN OPTIMIZED

**Implementation Date**: 03/09/2025
**Based on**: SOP_Token_Optimization_2025.md
**Purpose**: 40% token reduction while maintaining performance

---

## **MANDATORY PROMPT STRUCTURE**

All agent communications must use this optimized format:

```markdown
<task>
[Specific action required - max 20 words]
</task>

<context>
[Essential background only - max 50 words]
</context>

<output_format>
[Exact structure required]
</output_format>

<success_criteria>
[Measurable outcomes - max 30 words]
</success_criteria>
```

---

## **CONTENT LENGTH LIMITS**

### **Service Pages**
- **Target**: 800-1,500 words
- **Structure**: Problem → Solution → Benefits → Process → CTA

### **Blog Posts** 
- **SEO-focused**: 1,500-2,500 words
- **News/Updates**: 500-800 words
- **How-to Guides**: 1,000-2,000 words

### **Product Descriptions**
- **Target**: 150-300 words
- **Structure**: Benefit headline → Features → Specifications → Social proof

---

## **BRITISH ENGLISH REQUIREMENTS**

### **Mandatory Spelling**
- Use -ise endings: realise, organise, specialise
- Use -our endings: colour, flavour, behaviour  
- Use -re endings: centre, theatre, metre
- Use -ogue endings: catalogue, dialogue, analogue

### **Professional Tone**
- Formal but approachable language
- Understated confidence
- Use "we" and "our" to build partnership
- UK-relevant examples and regulations

---

## **TOOL EXECUTION OPTIMIZATION**

### **Parallel Execution Rules**
- Batch independent tool calls in single messages
- Combine related operations for 50% time reduction
- Example pattern:
```python
# Single message with multiple tool calls
tools = [
    ("WebFetch", website_url),
    ("WebSearch", "competitor analysis query"),
    ("Read", "existing_report.md")
]
```

### **Caching Implementation**
- Cache expensive operations (website crawls: 24 hours)
- Cache competitor analysis (7 days)
- Cache keyword research (3 days)
- Cache performance data (1 hour)

---

## **CURRENT DATE ENFORCEMENT**

**System Date**: 03/09/2025 (September 3, 2025)

**Required Format**:
- Analysis dates: "03/09/2025" or "September 3, 2025"
- Report headers: Include current analysis date
- File timestamps: Use current system date

**FORBIDDEN**: Any reference to "January 2025" or outdated dates

---

## **QUALITY GATES**

Before completing any task, verify:
- [ ] Content within specified word limits
- [ ] British English spelling applied
- [ ] Current date used (September 2025)
- [ ] Token optimization techniques applied
- [ ] Parallel tool execution used where possible
- [ ] Appropriate SOP referenced

---

**Template Version**: 1.0
**Last Updated**: 03/09/2025
**Compliance**: MANDATORY