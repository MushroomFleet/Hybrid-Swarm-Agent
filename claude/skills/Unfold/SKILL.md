---
name: unfold
description: Stage-based planning methodology for breaking complex development plans into manageable phase and substage documents with detailed step-by-step instructions and code examples
license: MIT
---

# Unfold Skill

## Overview

The Unfold skill provides a systematic methodology for breaking down complex development plans into manageable, high-fidelity stage-based documents. This process creates detailed handoff documents with step-by-step instructions and code examples, enabling clear execution tracking and team coordination.

## Core Concepts

### Stage-Based Tiling
Plans are divided into sequential phases, starting with Phase 0 (overview) and progressing through numbered phases (Phase 1, Phase 2, etc.). Each phase can be further divided into substages for granular execution.

### Character Limits
All documents are constrained to less than 45,000 characters to ensure:
- Focused, digestible content
- Clear scope boundaries
- Efficient context management
- Practical handoff documents

### Document Hierarchy
```
Phase0.md (Overview of all phases)
├── Phase1.md (Detailed first phase)
│   ├── Substage1.1.md
│   ├── Substage1.2.md
│   └── Substage1.3.md
├── Phase2.md (Detailed second phase)
│   ├── Substage2.1.md
│   ├── Substage2.2.md
│   └── Substage2.3.md
└── Phase3.md (Detailed third phase)
    └── ...
```

## Tool 1: Unfold_Plan

### Purpose
Transform a high-level development plan into a series of Phase documents, each containing detailed step-by-step instructions and code examples.

### Input
- A development plan (markdown format)
- Can be comprehensive or high-level
- May exceed character limits in original form

### Process

1. **Analyze the Plan**
   - Identify major milestones and logical groupings
   - Determine natural phase boundaries
   - Assess total scope and complexity

2. **Create Phase 0 (Overview)**
   - Summarize the entire project
   - List all phases with brief descriptions
   - Define dependencies between phases
   - Outline success criteria
   - Include architecture overview
   - Character budget: aim for 15,000-25,000 characters

3. **Create Phase Documents**
   - Start with Phase 1 (foundation/setup)
   - Each phase focuses on a major milestone
   - Include detailed step-by-step instructions
   - Provide complete code examples
   - Add configuration details
   - Include testing procedures
   - Character budget: aim for 35,000-44,000 characters per phase

4. **Ensure Continuity**
   - Each phase references prerequisites from previous phases
   - Clear handoff points between phases
   - Consistent terminology and structure

### Output Structure

**Phase0.md Template:**
```markdown
# Project Name - Phase 0: Overview

## Project Summary
[Brief description of the entire project]

## Architecture Overview
[High-level architecture diagram and explanation]

## Phase Breakdown

### Phase 1: [Phase Name]
**Goal:** [Primary objective]
**Duration:** [Estimated time]
**Dependencies:** None
**Deliverables:**
- [Key deliverable 1]
- [Key deliverable 2]

### Phase 2: [Phase Name]
**Goal:** [Primary objective]
**Duration:** [Estimated time]
**Dependencies:** Phase 1
**Deliverables:**
- [Key deliverable 1]
- [Key deliverable 2]

[Continue for all phases]

## Success Criteria
[How to measure completion]

## Technology Stack
[List of technologies, frameworks, tools]

## Team Structure
[Recommended team composition]
```

**Phase[N].md Template:**
```markdown
# Phase [N]: [Phase Name]

## Phase Overview
**Goal:** [Primary objective]
**Prerequisites:** [What must be completed first]
**Estimated Duration:** [Time estimate]
**Key Deliverables:**
- [Deliverable 1]
- [Deliverable 2]

## Step-by-Step Implementation

### Step 1: [Step Name]
**Purpose:** [Why this step is necessary]
**Duration:** [Estimated time]

#### Instructions
1. [Detailed instruction 1]
2. [Detailed instruction 2]

#### Code Example
```[language]
[Complete, runnable code example]
```

#### Configuration
```[format]
[Configuration files or settings]
```

#### Verification
- [ ] [Check 1]
- [ ] [Check 2]

### Step 2: [Step Name]
[Repeat structure]

## Testing Procedures
[How to test this phase]

## Troubleshooting
[Common issues and solutions]

## Next Steps
[How to proceed to the next phase]
```

### Usage Example

When presented with a plan, Claude should:

```markdown
I'll unfold this plan into phase documents. Let me analyze the structure first.

[Analysis of the plan structure]

I'll create:
- Phase0.md: Project overview with all phases
- Phase1.md: Foundation and basic setup (< 45,000 chars)
- Phase2.md: Core functionality implementation (< 45,000 chars)
- Phase3.md: Advanced features (< 45,000 chars)
[etc.]
```

## Tool 2: Unfold_Phase

### Purpose
Take a single Phase document and break it down into Substage documents for even more granular execution tracking.

### Input
- A Phase[N].md document
- Typically used when a phase is complex or involves multiple team members

### Process

1. **Analyze the Phase**
   - Identify logical substages within the phase
   - Look for natural breaking points (features, components, layers)
   - Assess dependencies between substages

2. **Create Substage Documents**
   - Each substage is a focused, executable unit of work
   - Numbered as Substage[N].[M].md
   - Include complete code examples
   - Add detailed implementation notes
   - Character budget: 25,000-40,000 characters per substage

3. **Maintain Traceability**
   - Reference parent phase
   - Clear prerequisites from previous substages
   - Integration points with other substages

### Output Structure

**Substage[N].[M].md Template:**
```markdown
# Substage [N].[M]: [Substage Name]

## Substage Overview
**Parent Phase:** Phase [N]: [Phase Name]
**Goal:** [Specific objective]
**Prerequisites:**
- [Prerequisite 1]
- [Prerequisite 2]
**Estimated Duration:** [Time estimate]

## Context
[Why this substage exists and how it fits into the larger phase]

## Detailed Implementation

### Task 1: [Task Name]
**Objective:** [What this task accomplishes]

#### Implementation Steps
1. [Detailed step 1]
   - [Sub-step or clarification]
2. [Detailed step 2]

#### Code Implementation
```[language]
[Complete, production-ready code example]
```

#### Explanation
[Line-by-line or section-by-section explanation]

#### Testing
```[language]
[Test code]
```

### Task 2: [Task Name]
[Repeat structure]

## Integration Points
[How this substage connects with others]

## Validation Checklist
- [ ] [Validation item 1]
- [ ] [Validation item 2]
- [ ] [Validation item 3]

## Common Issues
[Known problems and solutions]

## Next Substage
[Preview of what comes next]
```

### Usage Example

When asked to unfold a phase:

```markdown
I'll unfold Phase2.md into substages. Let me analyze the phase structure.

[Analysis of Phase2 steps]

I'll create:
- Substage2.1.md: Database schema and models (< 45,000 chars)
- Substage2.2.md: API endpoints implementation (< 45,000 chars)
- Substage2.3.md: Frontend components (< 45,000 chars)
- Substage2.4.md: Integration and testing (< 45,000 chars)
```

## Execution Workflow

### Starting a Project

1. **Read Phase0.md** to understand the entire project
2. **Begin with Phase1.md** for detailed implementation
3. **If Phase1 is complex**, unfold it into substages first
4. **Create substage documents** in `/docs/instruct/` directory
5. **Track progress** by checking off validation items
6. **Complete each substage** before moving to the next
7. **When Phase1 is complete**, move to Phase2.md

### Directory Structure

```
/docs/
├── Phase0.md           (Overview)
├── Phase1.md           (Foundation)
├── Phase2.md           (Core features)
├── Phase3.md           (Advanced features)
└── instruct/           (Substage documents for active phase)
    ├── Substage1.1.md
    ├── Substage1.2.md
    ├── Substage1.3.md
    └── progress.md     (Optional tracking document)
```

## Best Practices

### When Creating Phase Documents

1. **Start with the big picture** (Phase0)
2. **Use concrete examples** in every phase
3. **Include complete code snippets**, not pseudocode
4. **Add verification steps** for each major step
5. **Keep phases focused** on a single major milestone
6. **Provide context** for why decisions are made
7. **Include error handling** in code examples
8. **Add troubleshooting sections**

### When Creating Substage Documents

1. **Make substages atomic** - each should be completable independently
2. **Include integration notes** for connecting substages
3. **Provide exhaustive examples** since substages are highly focused
4. **Add inline comments** in code examples
5. **Include test cases** specific to the substage
6. **Document assumptions** explicitly
7. **Reference files and line numbers** when modifying existing code

### Character Management

1. **Monitor document length** as you write
2. **Prioritize essential information**
3. **Use concise but complete code examples**
4. **Avoid repetition** between documents
5. **Reference previous documents** instead of repeating content
6. **If approaching 45,000 characters**, consider splitting into additional phases/substages

### Code Examples

1. **Always include complete, runnable code**
2. **Show imports and dependencies**
3. **Include error handling**
4. **Add comments explaining non-obvious logic**
5. **Use realistic variable names**
6. **Show integration with existing code**
7. **Include configuration examples**

## Quality Checklist

### For Phase Documents
- [ ] Clear phase objective stated
- [ ] Prerequisites listed
- [ ] Step-by-step instructions included
- [ ] Complete code examples provided
- [ ] Testing procedures defined
- [ ] Troubleshooting section added
- [ ] Next steps identified
- [ ] Under 45,000 characters

### For Substage Documents
- [ ] Parent phase referenced
- [ ] Focused on single objective
- [ ] Detailed implementation steps
- [ ] Production-ready code examples
- [ ] Integration points documented
- [ ] Validation checklist included
- [ ] Common issues addressed
- [ ] Under 45,000 characters

## Advanced Patterns

### Parallel Phases
Some phases can be worked on simultaneously if they don't have dependencies:

```markdown
## Phase Breakdown

### Phase 2A: Backend API (parallel with 2B)
**Dependencies:** Phase 1

### Phase 2B: Frontend Foundation (parallel with 2A)
**Dependencies:** Phase 1

### Phase 3: Integration
**Dependencies:** Phase 2A, Phase 2B
```

### Iterative Refinement
Phases can include iteration loops:

```markdown
### Phase 3: Core Features (Iterative)
**Iterations:** 3 planned
- Iteration 1: Basic functionality
- Iteration 2: Enhanced features
- Iteration 3: Performance optimization
```

### Optional Phases
Some phases may be optional based on requirements:

```markdown
### Phase 4 (Optional): Advanced Analytics
**Condition:** If analytics dashboard is required
```

## Examples

### Example 1: Web Application

**Phase0.md** would include:
- Project summary: E-commerce platform
- Phase 1: Setup and infrastructure
- Phase 2: User authentication
- Phase 3: Product catalog
- Phase 4: Shopping cart
- Phase 5: Payment integration
- Phase 6: Deployment

**Phase2.md** (User Authentication) would include:
- Step 1: Database schema for users
- Step 2: Registration endpoint
- Step 3: Login endpoint
- Step 4: JWT token implementation
- Step 5: Password reset flow
- Step 6: Email verification
- Complete code examples for each

**Substage2.2.md** (Login Endpoint) would include:
- Task 1: Route definition
- Task 2: Request validation
- Task 3: Database query
- Task 4: Password verification
- Task 5: Token generation
- Task 6: Response formatting
- Detailed code for each task

### Example 2: Data Pipeline

**Phase0.md** overview:
- Phase 1: Infrastructure setup (AWS, databases)
- Phase 2: Data ingestion pipeline
- Phase 3: Data transformation
- Phase 4: Data storage
- Phase 5: Analytics layer
- Phase 6: Monitoring and alerts

**Phase3.md** (Data Transformation) substages:
- Substage3.1: ETL framework setup
- Substage3.2: Data validation rules
- Substage3.3: Transformation logic
- Substage3.4: Error handling
- Substage3.5: Testing framework

## Triggering the Unfold Process

### Unfold_Plan Triggers
Claude should initiate Unfold_Plan when:
- User provides a comprehensive development plan
- User says "unfold this plan"
- User says "create phase documents from this"
- User says "break this into phases"
- Plan appears too large or complex for single document

### Unfold_Phase Triggers
Claude should initiate Unfold_Phase when:
- User says "unfold Phase[N]"
- User says "create substages for Phase[N]"
- User says "break down Phase[N] into substages"
- A phase is complex with many steps
- User is ready to execute a specific phase

## Integration with Development

The Unfold skill works best when:
1. **Planning precedes execution** - Complete phase documents before coding
2. **Iterative refinement** - Update documents as requirements change
3. **Team coordination** - Multiple developers can work on different substages
4. **Progress tracking** - Check off completed items in validation checklists
5. **Knowledge transfer** - Documents serve as onboarding material

## Conclusion

The Unfold skill provides a structured approach to managing complex development projects. By breaking plans into phases and substages, teams can:
- Maintain clarity throughout the project
- Track progress systematically
- Enable parallel development
- Reduce cognitive load
- Create valuable documentation
- Facilitate knowledge transfer

Always remember: the goal is to create practical, executable documents that guide real development work, not just theoretical plans.