# Complete Content Quality Assurance Cycle Design

## 🔄 **The Perfect Content Loop**

**Goal**: Content gets written → reviewed by multiple expert personas → refined → reviewed again → refined → continues until perfection

---

## 📊 **Workflow Architecture**

### **Phase 1: Content Creation**
```
User Request → content_generator → Initial Draft Created
```

### **Phase 2: Multi-Persona Review Cycle**
```
Draft → enhanced_content_auditor (4 review personas) → Comprehensive Audit Report
```

### **Phase 3: Systematic Refinement** 
```
Audit Report + Original Draft → content_refiner → Improved Version
```

### **Phase 4: Quality Gate Decision**
```
Improved Version → quality_gate_orchestrator → PASS/CONTINUE CYCLE
```

### **Phase 5: Iterative Loop (Until Perfect)**
```
If CONTINUE: Improved Version → Phase 2 (Multi-Persona Review) → Phase 3 (Refine) → Phase 4 (Quality Gate) → Repeat
If PASS: Final Approval → content_finaliser → Published Content
```

---

## 🎭 **Multi-Persona Review System**

### **Enhanced Content Auditor - 4 Review Personas:**

#### **Persona 1: The Technical SEO Specialist**
- **Focus**: SEO compliance, keyword integration, technical structure
- **Reviews**: Meta tags, headings hierarchy, internal linking opportunities
- **Standards**: Technical SEO best practices, search optimisation

#### **Persona 2: The Brand Consistency Guardian** 
- **Focus**: Brand voice, messaging alignment, British English compliance
- **Reviews**: Tone consistency, terminology, cultural appropriateness
- **Standards**: Brand guidelines, British English rules, Australian market context

#### **Persona 3: The User Experience Advocate**
- **Focus**: Readability, user journey, conversion optimisation
- **Reviews**: Content flow, call-to-actions, user engagement
- **Standards**: UX principles, accessibility, conversion best practices

#### **Persona 4: The Content Quality Perfectionist**
- **Focus**: Accuracy, credibility, E-E-A-T compliance
- **Reviews**: Factual accuracy, source attribution, expertise demonstration
- **Standards**: E-E-A-T guidelines, content credibility, quality metrics

---

## 🛠️ **Agent Implementation Plan**

### **1. Enhanced Content Auditor** 
**File**: `enhanced_content_auditor.md`
```yaml
tools: ["WebFetch", "WebSearch", "Write", "Edit", "MultiEdit", "Read", "Glob", "Grep", "LS", "TodoWrite", "NotebookEdit"]
```

**Capabilities**:
- 4-persona systematic review process
- Comprehensive audit reporting with specific improvement recommendations
- Quality scoring system (0-100 per persona, overall score)
- British English compliance checking
- SOP compliance verification

### **2. Content Refiner**
**File**: `content_refiner.md`
```yaml
tools: ["WebFetch", "WebSearch", "Write", "Edit", "MultiEdit", "Read", "Glob", "Grep", "LS", "NotebookEdit"]
```

**Capabilities**:
- Takes audit reports and systematically implements improvements
- Maintains content voice while addressing all feedback
- Tracks which improvements have been applied
- Creates revision logs for transparency

### **3. Quality Gate Orchestrator**
**File**: `quality_gate_orchestrator.md` 
```yaml
tools: ["Write", "Edit", "MultiEdit", "Read", "TodoWrite", "NotebookEdit"]
```

**Capabilities**:
- Evaluates overall content quality scores
- Determines if content needs another review cycle
- Manages iterative improvement process
- Sets quality thresholds and approval criteria

### **4. Content Finaliser**
**File**: `content_finaliser.md`
```yaml  
tools: ["Write", "Edit", "MultiEdit", "Read", "TodoWrite"]
```

**Capabilities**:
- Final polish and formatting
- Metadata addition and SEO finalisation
- Publication-ready content preparation
- Archive creation and documentation

---

## 📋 **Quality Scoring System**

### **Individual Persona Scores (0-100)**
- **Technical SEO Score**: 0-100 (keyword integration, structure, technical elements)
- **Brand Consistency Score**: 0-100 (voice, British English, cultural alignment)
- **User Experience Score**: 0-100 (readability, flow, conversion elements)
- **Content Quality Score**: 0-100 (accuracy, credibility, expertise)

### **Overall Quality Thresholds**
- **85+ Average**: Content approved for publication
- **75-84 Average**: One more review cycle recommended  
- **65-74 Average**: Major revisions required, continue cycle
- **Below 65**: Significant issues, multiple cycles needed

### **British English Compliance**
- **100% Required**: Zero tolerance for American English
- **Automatic Fail**: Any American spelling/terminology = immediate cycle continuation

---

## 🔄 **Iterative Improvement Process**

### **Cycle 1: Initial Review**
1. **Input**: First draft from content_generator
2. **Process**: Enhanced_content_auditor (4 personas) → Comprehensive audit
3. **Output**: Detailed audit report with persona-specific feedback
4. **Action**: Content_refiner applies improvements → Version 2

### **Cycle 2: Refinement Review**  
1. **Input**: Version 2 (refined content)
2. **Process**: Enhanced_content_auditor reviews improvements
3. **Output**: Updated audit report showing progress + remaining issues
4. **Decision**: Quality_gate_orchestrator evaluates scores
5. **Action**: If needed, content_refiner creates Version 3

### **Cycle 3+: Continued Refinement**
**Continues until**: All persona scores ≥85 AND overall average ≥85 AND 100% British English compliance

### **Final Cycle: Approval & Finalisation**
1. **Input**: Approved content version
2. **Process**: Content_finaliser adds final polish
3. **Output**: Publication-ready content with metadata
4. **Archive**: Version history and improvement tracking saved

---

## 🚀 **Automation Rules for CLAUDE.md**

### **Automatic QA Cycle Triggers**
```markdown
### Content Quality Assurance Cycle
**Trigger Phrases**: "review this content", "improve this content", "quality check this content", "refine this content"

**Auto-Execute Process**:
1. enhanced_content_auditor.md - Multi-persona review with quality scoring
2. IF scores < 85 average → content_refiner.md - Apply improvements  
3. quality_gate_orchestrator.md - Evaluate if another cycle needed
4. REPEAT steps 1-3 until quality thresholds met
5. content_finaliser.md - Final polish and publication prep

**Generate Report**: Content Quality Assurance Report with version history and improvement tracking
```

### **Content Creation with Built-in QA**
```markdown
**Trigger Phrases**: "create content for", "write content about", "draft content on"

**Auto-Execute Sequential Process**:
**Phase 1**: content_generator.md - Create initial draft
**Phase 2**: enhanced_content_auditor.md - Multi-persona review  
**Phase 3**: content_refiner.md - Apply improvements
**Phase 4**: quality_gate_orchestrator.md - Quality evaluation
**Phase 5**: IF needed, repeat Phase 2-4 until approved
**Phase 6**: content_finaliser.md - Final publication preparation

**Generate Report**: Complete Content Development Report with QA cycle documentation
```

---

## 📊 **Expected Benefits**

### **Quality Improvements**
- **Comprehensive Review**: 4 expert perspectives on every piece of content
- **Iterative Refinement**: Content improves with each cycle
- **Objective Scoring**: Clear quality metrics and thresholds
- **British English Guarantee**: 100% compliance enforcement

### **Process Benefits**
- **Systematic Approach**: Consistent, repeatable quality process
- **Transparency**: Clear audit trails and improvement documentation
- **Efficiency**: Automated workflow reduces manual oversight
- **Scalability**: Can handle multiple content pieces simultaneously

### **Business Impact**
- **Higher Quality Content**: Multiple expert reviews ensure excellence
- **Brand Consistency**: Guaranteed voice and style compliance
- **SEO Performance**: Technical optimisation in every piece
- **User Engagement**: UX-focused content drives better results

---

This system creates a **relentless pursuit of content perfection** through systematic, multi-perspective review and iterative improvement until every piece meets the highest standards.