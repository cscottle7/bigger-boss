# AGENT SOP INTEGRATION MASTER REFERENCE

**MANDATORY READING**: Every agent MUST reference applicable SOPs before executing tasks.

**System Date**: 03/09/2025 (September 2025)
**Status**: ACTIVE ENFORCEMENT

---

## **AGENT WORKFLOW INTEGRATION REQUIREMENTS**

### **1. CONTENT CREATION AGENTS**
**Must Follow**: `system/sops/SOP_2025_Content_Creation_Standards.md`

**Key Requirements**:
- **Content Length Limits**: Service pages 800-1,500 words, Blog posts 1,500-2,500 words
- **British English Standards**: -ise endings, -our endings, -re endings
- **Token Optimization**: Apply 40% compression techniques from SOP_Token_Optimization_2025.md
- **Schema Markup**: Implement required structured data

**Integration Command**: Before generating content, agents must state:
```
"Following SOP_2025_Content_Creation_Standards.md for content length, British English, and token optimization requirements."
```

### **2. ALL AGENTS - TOKEN OPTIMIZATION**
**Must Follow**: `system/sops/SOP_Token_Optimization_2025.md`

**Key Requirements**:
- **Prompt Compression**: 40% reduction in all system prompts
- **Parallel Tool Execution**: Batch independent tool calls
- **Structured Tag Format**: Use <task>, <context>, <output_format>, <success_criteria>
- **Result Caching**: Implement for expensive operations

**Integration Command**: At task start, agents must state:
```
"Applying SOP_Token_Optimization_2025.md - Using compressed prompts, parallel execution, and structured format."
```

### **3. CONTENT REFINEMENT WORKFLOWS**
**Must Follow**: `system/sops/SOP_Automated_Content_Refinement_2025.md`

**Key Requirements**:
- Structured audit-based revisions
- Verification of changes implemented
- Quality gate checkpoints
- Progressive refinement cycles

### **4. DOCUMENT PROCESSING**
**Must Follow**: `system/sops/SOP_Document_Conversion_System.md`

**Key Requirements**:
- Standardized conversion workflows
- Format consistency maintenance
- Metadata preservation
- Quality validation

### **5. GOOGLE DRIVE INTEGRATION**
**Must Follow**: `system/sops/SOP_Google_Drive_Integration.md`

**Key Requirements**:
- Standardized file naming conventions
- Version control procedures
- Access permission management
- Sync verification protocols

---

## **CURRENT DATE ENFORCEMENT**

**System Date**: 03/09/2025 (September 3, 2025)
**Mandate**: ALL agents must use current date context. No January 2025 references permitted.

**Date Format Standards**:
- Analysis dates: "03/09/2025" or "September 3, 2025"
- File timestamps: Use current system date
- Report headers: Include current analysis date

---

## **SOP FILE LOCATIONS**

### **2025 Standards (PRIORITY)**
- `C:\Apps\Agents\Bigger Boss\bigger-boss\system\sops\SOP_Token_Optimization_2025.md`
- `C:\Apps\Agents\Bigger Boss\bigger-boss\system\sops\SOP_2025_Content_Creation_Standards.md`
- `C:\Apps\Agents\Bigger Boss\bigger-boss\system\sops\SOP_Automated_Content_Refinement_2025.md`
- `C:\Apps\Agents\Bigger Boss\bigger-boss\system\sops\SOP_Document_Conversion_System.md`
- `C:\Apps\Agents\Bigger Boss\bigger-boss\system\sops\SOP_Google_Drive_Integration.md`

### **Legacy SOPs (REFERENCE)**
- `C:\Apps\Agents\Bigger Boss\bigger-boss\system\sops\sop_*.md` (Existing procedures)

---

## **MANDATORY AGENT CHECKLIST**

Before starting any task, agents must:

- [ ] Check applicable SOP from master list above
- [ ] State which SOP requirements are being followed
- [ ] Use current system date (03/09/2025)
- [ ] Apply token optimization techniques
- [ ] Follow content length guidelines
- [ ] Use British English standards (where applicable)

**Failure to follow SOP integration requirements will result in task rejection.**

---

**Last Updated**: 03/09/2025
**Review Frequency**: Weekly
**Enforcement**: MANDATORY
