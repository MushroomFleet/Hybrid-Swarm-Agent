# Integrating Hybrid Swarm with Claude Code Agents

## Overview

This guide explains how to properly integrate the Hybrid Swarm orchestration system with Claude Code's agent framework to enable multi-agent workflows with three-level emergent intelligence.

## Current Architecture

### What Exists Now

**Hybrid Swarm System (Standalone Python)**
```
src/
├── hybrid_swarm.py                  # Main orchestrator (3 levels)
├── adaptive_resonance.py            # Level 1: Specialist selection
├── dynamic_approach_manager.py      # Level 2: Approach lifecycle
├── pattern_analyzer.py              # Level 2: Pattern discovery
├── approach_evolution.py            # Level 2: Evolution & pruning
├── execution_history.py             # Level 2: Historical tracking
├── content_analyzer.py              # Level 2: Content analysis
└── stigmergic_coordination.py       # Level 3: Swarm signals

agent_tools/
├── get_coordination.py              # CLI: Get coordination decisions
├── report_result.py                 # CLI: Report execution results
└── agent_helper.py                  # Python: Programmatic access
```

**Claude Code Agent System**
```
.claude/agents/
├── hybrid-swarm.md                  # Coordination agent
├── researcher.md                    # Information gathering
├── writer.md                        # Content synthesis
└── critic-reviewer.md               # Quality validation
```

### Three-Level Coordination

**Level 1: Adaptive Resonance**
- Selects specialist based on task pattern matching
- Specialists emerge from task characteristics

**Level 2: Dynamic Approaches**
- Approaches emerge from successful execution patterns
- Pattern discovery clusters executions every 50 runs
- Approaches evolve based on performance
- Natural selection prunes ineffective approaches

**Level 3: Stigmergic Coordination**
- Blends pattern matching (70%) with swarm signals (30%)
- Signals amplify successful approaches
- Enables collective learning

## Integration Architecture

### Agent Communication Protocol

**Input Format:**
- Direct prompts: `@hybrid-swarm "Write a report on X"`
- Agent handoffs: Read from `artifacts/agent-output.md`

**Output Format:**
- Write to `artifacts/hybrid-swarm-output.md`
- Include metadata: specialist_id, approach_id, approach_metadata, quality_score

**Coordination Flow:**
```
User/Agent Request
    ↓
agent_tools/get_coordination.py
    ↓
[Three-Level Coordination]
├─ Adaptive Resonance → specialist_id
├─ Dynamic Approaches → approach_id + metadata
└─ Stigmergic Signals → weighted selection
    ↓
Agent generates content
    ↓
agent_tools/report_result.py
    ↓
System learns and evolves
```

## Agent Definition

**File: `.claude/agents/hybrid-swarm.md`**

```markdown
---
name: hybrid-swarm
description: Self-organizing agent using three-level coordination (specialists, dynamic approaches, swarm signals)
color: purple
model: sonnet
tools:
  - Execute_Command
  - Read
  - Write
---

# Hybrid Swarm Agent

You use three-level emergent coordination: adaptive resonance (specialists), dynamic approaches (pattern-based), and stigmergic coordination (swarm signals).

## How You Work

When invoked:
1. Get coordination decision from hybrid swarm system
2. Receive specialist + dynamic approach + pattern metadata
3. Generate actual content using your LLM capabilities following approach pattern
4. Report quality to enable system learning
5. Return result to calling agent or user

## Workflow Steps

### Step 1: Get Coordination

```bash
python agent_tools/get_coordination.py "{{PROMPT}}"
```

Returns JSON with:
- `task_id`: Unique execution identifier
- `specialist_id`: Which specialist handles this
- `approach_id`: Dynamic approach ID (e.g., "approach_coding_explain_bulleted")
- `approach_metadata`: Pattern signature + style characteristics + performance metrics
- `quality_target`: Expected quality level
- `coordination_details`: Match score, selection method, weights

### Step 2: Follow Dynamic Approach Pattern

The `approach_metadata` contains:
- **pattern_signature**: What tasks this approach is good for (domains, complexity, keywords)
- **style_characteristics**: How to generate content (structure, tone, depth, code requirements)
- **performance_metrics**: Historical quality, usage count, success rate

Follow the style_characteristics:
- `structure`: "bulleted" → use bullets; "sequential" → numbered steps; "hierarchical" → nested sections
- `tone`: "technical" → precise; "casual" → approachable; "formal" → professional
- `depth`: "concise" → brief; "moderate" → balanced; "comprehensive" → thorough
- `code_requirements`: "high" → substantial code; "medium" → key examples; "low" → minimal
- `example_density`: "high" → many examples; "medium" → key examples; "low" → few examples

### Step 3: Generate Real Content

Use YOUR LLM capabilities to generate content following the approach pattern:
- Not templates
- Real, thoughtful content
- Following the style characteristics precisely

### Step 4: Assess Quality

Honestly evaluate your output (0.0-1.0):
- 0.9-1.0: Excellent
- 0.8-0.9: Good
- 0.7-0.8: Adequate
- 0.5-0.7: Below expectations
- 0.0-0.5: Poor

### Step 5: Report Results

```bash
python agent_tools/report_result.py \
  --task-id {{TASK_ID}} \
  --specialist {{SPECIALIST_ID}} \
  --approach-id {{APPROACH_ID}} \
  --quality {{QUALITY}}
```

This enables:
- Execution history recording
- Pattern discovery (every 50 executions)
- Approach metrics updates
- Stigmergic signal updates
- System continuous learning

### Step 6: Write Output

Save to `artifacts/hybrid-swarm-output.md`:

```markdown
---
agent: hybrid-swarm
specialist: {{SPECIALIST_ID}}
approach: {{APPROACH_ID}}
approach_name: {{APPROACH_NAME}}
quality: {{QUALITY}}
timestamp: {{TIMESTAMP}}
pattern: {{STYLE_SUMMARY}}
---

[Your generated content here]

---
Coordination Metadata:
- Match score: {{MATCH_SCORE}}
- Selection method: {{METHOD}} (pattern weight: 70%, signal weight: 30%)
- Approach metrics: avg_quality={{AVG}}, usage_count={{COUNT}}
```

## Example Usage

User: `@hybrid-swarm Write a technical guide on async Python`

You execute:
1. `python agent_tools/get_coordination.py "Write a technical guide on async Python"`
2. Receive: `approach_coding_explain_bulleted` with bulleted structure, technical tone, high code
3. Generate real content following the pattern
4. Assess quality: 0.88
5. `python agent_tools/report_result.py --task-id task_123 --specialist spec_abc --approach-id approach_coding_explain_bulleted --quality 0.88`
6. Write to `artifacts/hybrid-swarm-output.md`

## Reading from Other Agents

```python
# Read previous agent output
content = Read("artifacts/research-output.md")

# Extract metadata from frontmatter
# Use content as context for coordination
prompt = f"Create video essay from: {content}"

# Get coordination with enriched context
python agent_tools/get_coordination.py "{prompt}"
```

## Key Principles

- **Coordination intelligence, execution capability**: System provides pattern, you provide content
- **Always report results**: Even failures help system learn
- **Follow patterns faithfully**: System learns from what actually works
- **Dynamic not static**: Approaches evolve, new patterns emerge
- **Collective learning**: Your quality reports improve future coordination
```

## Multi-Agent Workflow Patterns

### Pattern 1: Research → Hybrid Swarm → Writer

**Use case**: Structured content creation with multiple perspectives

```
Step 1: Researcher
@researcher "AI developments in 2025"
  ↓ artifacts/research-output.md

Step 2: Hybrid Swarm Coordination
@hybrid-swarm "Create video essay from research"
  ↓ Coordination returns dynamic approach
  ↓ e.g., "approach_writing_tutorial_sequentialsteps"
  ↓ Pattern: sequential structure, educational tone
  ↓ artifacts/hybrid-swarm-output.md

Step 3: Writer Polish
@writer "Polish for Substack"
  ↓ artifacts/substack-essay.md
```

**Hybrid Swarm adds:**
- Intelligent approach selection (pattern matching + swarm signals)
- Style guidance from discovered patterns
- Historical quality insights
- Execution tracking for continuous learning

### Pattern 2: Hybrid Swarm → Critic → Refine

**Use case**: Quality validation and iterative improvement

```
Step 1: Initial Generation
@hybrid-swarm "Generate technical guide on Docker"
  ↓ approach_id: "approach_coding_explain_bulleted"
  ↓ artifacts/hybrid-swarm-output.md

Step 2: Quality Review
@critic-reviewer "Validate technical accuracy"
  ↓ artifacts/feedback.md
  ↓ Issues: Missing security concerns, examples too basic

Step 3: Refinement
@hybrid-swarm "Refine based on feedback"
  ↓ approach_id may change based on feedback
  ↓ e.g., "approach_coding_comprehensive_security"
  ↓ artifacts/hybrid-swarm-output-v2.md
```

**Learning loop:**
- Initial quality reported (e.g., 0.75)
- Critic identifies issues
- Refined version quality improves (e.g., 0.88)
- System learns which approaches need refinement

### Pattern 3: Parallel Hybrid Swarms

**Use case**: Multiple specialist viewpoints

```
Parallel Execution:

@hybrid-swarm "Research perspective on AI safety"
  ↓ approach_id: "approach_analysis_compare_bulleted"
  ↓ artifacts/research-perspective.md

@hybrid-swarm "Technical perspective on AI safety"
  ↓ approach_id: "approach_coding_explain_bulleted"
  ↓ artifacts/technical-perspective.md

@hybrid-swarm "Policy perspective on AI safety"
  ↓ approach_id: "approach_writing_comprehensive_formal"
  ↓ artifacts/policy-perspective.md

Synthesis:
@writer "Synthesize all three perspectives"
  ↓ artifacts/synthesis.md
```

**Coordination benefits:**
- Different specialists selected for each perspective
- Different dynamic approaches matched to domains
- Each execution feeds pattern discovery
- Approaches evolve based on perspective quality

## Example: Complete Multi-Agent Workflow

### Scenario: Create Technical Blog Post

**Step 1: Research Agent**
```markdown
@researcher "Latest Python async patterns"

Output: artifacts/research-output.md
---
agent: researcher
quality: 0.92
---

# Python Async Patterns Research

## Key Findings
- asyncio.TaskGroup (Python 3.11+)
- Structured concurrency patterns
- Performance best practices

[detailed research...]
```

**Step 2: Hybrid Swarm Coordination**
```bash
@hybrid-swarm "Create technical tutorial from: artifacts/research-output.md"

Executes:
python agent_tools/get_coordination.py "Create technical tutorial from research on Python async patterns"

Returns:
{
  "task_id": "task_202510_001",
  "specialist_id": "specialist_coding_tutorial",
  "approach_id": "approach_coding_explain_bulleted",
  "approach_metadata": {
    "name": "Technical Coding Explanation (Bulleted)",
    "style_characteristics": {
      "structure": "bulleted",
      "tone": "technical",
      "depth": "moderate",
      "code_requirements": "high",
      "example_density": "medium"
    },
    "performance_metrics": {
      "avg_quality": 0.82,
      "usage_count": 45,
      "success_rate": 0.89
    }
  }
}
```

**Step 3: Generate Content**
```markdown
Output: artifacts/hybrid-swarm-output.md
---
agent: hybrid-swarm
specialist: specialist_coding_tutorial
approach: approach_coding_explain_bulleted
approach_name: Technical Coding Explanation (Bulleted)
quality: 0.87
pattern: Bulleted structure, technical tone, high code density
---

# Modern Python Async Patterns: A Technical Guide

## asyncio.TaskGroup (Python 3.11+)

**What it solves:**
• Structured concurrency pattern
• Automatic exception handling
• Resource cleanup guarantees

**Basic usage:**
```python
import asyncio

async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(fetch_user(1))
        task2 = tg.create_task(fetch_user(2))
    # Both tasks complete or all cancel
```

**Key benefits:**
• All tasks in group share lifetime
• Exception in any task cancels all
• Context manager ensures cleanup

## Structured Concurrency Patterns

[Complete technical content following bulleted pattern...]

---
Coordination Metadata:
- Match score: 0.87
- Selection: hybrid (pattern: 70%, signals: 30%)
- Historical: avg_quality=0.82, usage=45 times
```

**Step 4: Report Results**
```bash
python agent_tools/report_result.py \
  --task-id task_202510_001 \
  --specialist specialist_coding_tutorial \
  --approach-id approach_coding_explain_bulleted \
  --quality 0.87

System Response:
✓ Execution recorded to data/execution_history/2025-10/records_20251022.jsonl
✓ Approach metrics updated (avg_quality: 0.82 → 0.823)
✓ Stigmergic signals reinforced (+2.1 strength)
✓ Pattern discovery: 48/50 executions (triggers at 50)
```

**Step 5: Writer Polish**
```markdown
@writer "Polish for technical blog: artifacts/hybrid-swarm-output.md"

Output: artifacts/blog-post.md
---
agent: writer
source: hybrid-swarm-output.md
quality: 0.93
---

# Modern Python Async Patterns Every Developer Should Know

*Updated for Python 3.11+ with asyncio.TaskGroup*

Python's async capabilities have evolved significantly...

[Polished version with:]
- Engaging introduction
- Smooth transitions
- SEO optimization
- Call to action
```

## Pattern Discovery in Action

### Initial State (Week 1)
```
Available approaches:
- legacy_approach_a_comprehensive
- legacy_approach_b_tutorial
- legacy_approach_c_summary
```

### After 50 Executions (Week 3)
```
Pattern discovery triggered!

Discovered patterns:
- Cluster 1: Technical coding content with bullets
  → Creates: approach_coding_explain_bulleted
  
- Cluster 2: Writing tutorials with steps
  → Creates: approach_writing_tutorial_sequentialsteps
  
- Cluster 3: Analysis with comparisons
  → Creates: approach_analysis_compare_bulleted
```

### After 150 Executions (Week 6)
```
Approach evolution triggered!

approach_coding_explain_bulleted evolved:
- Code density increased (medium → high)
- Example focus sharpened (general → specific)
- Performance improved (0.78 → 0.85)

approach_writing_tutorial_sequentialsteps evolved:
- Step structure refined (basic → progressive)
- Hands-on emphasis increased
- Quality improved (0.82 → 0.87)
```

### After 300 Executions (Week 10)
```
Natural selection in action:

Successful approaches (reinforced):
✓ approach_coding_explain_bulleted (avg_quality: 0.85)
✓ approach_writing_tutorial_sequentialsteps (avg_quality: 0.87)
✓ approach_analysis_compare_bulleted (avg_quality: 0.83)

Pruned approaches:
✗ legacy_approach_c_summary (superseded)
✗ approach_experimental_mixed (low quality: 0.62)

New discoveries:
+ approach_coding_comprehensive_security (security-focused)
+ approach_writing_casual_conversational (blog style)
```

## Integration Benefits

### Why Use Hybrid Swarm in Multi-Agent Workflows?

**1. Emergent Intelligence**
- No hardcoded routing rules
- Specialists emerge from patterns
- Approaches discovered from success
- System improves automatically

**2. Pattern-Based Coordination**
- Approaches match task characteristics
- Style guidance from proven patterns
- Quality predictions from history
- Continuous pattern refinement

**3. Collective Learning**
- Multiple agents contribute to knowledge
- Swarm signals encode "what works"
- Pattern discovery finds common themes
- Natural selection removes poor patterns

**4. Transparent & Auditable**
- See which specialist selected
- Understand approach pattern
- Review historical performance
- Track quality evolution

**5. Adaptive & Self-Improving**
- Learns from every execution
- Discovers new effective patterns
- Evolves approaches based on feedback
- Prunes ineffective approaches

## Implementation Guidelines

### 1. Agent Setup

Create `.claude/agents/hybrid-swarm.md` with proper workflow definition (see Agent Definition section above).

### 2. Coordination Protocol

**Always use this sequence:**
```bash
# 1. Get coordination
python agent_tools/get_coordination.py "{{PROMPT}}"

# 2. Generate content (using LLM)

# 3. Report results
python agent_tools/report_result.py \
  --task-id {{TASK_ID}} \
  --specialist {{SPECIALIST_ID}} \
  --approach-id {{APPROACH_ID}} \
  --quality {{QUALITY}}
```

### 3. Metadata Propagation

Include coordination metadata in outputs:
```markdown
---
agent: hybrid-swarm
specialist: {{SPECIALIST_ID}}
approach: {{APPROACH_ID}}
approach_name: {{APPROACH_NAME}}
quality: {{QUALITY}}
pattern: {{STYLE_SUMMARY}}
---

[Content]

---
Coordination Metadata:
- Match score: {{SCORE}}
- Selection: hybrid (70% pattern, 30% signals)
- Performance: avg={{AVG}}, count={{COUNT}}
```

### 4. Quality Assessment

Be honest and consistent:
- Use 6-criteria checklist (accuracy, completeness, clarity, relevance, examples, structure)
- Report even low-quality results
- System learns from all outcomes

### 5. Pattern Discovery

Monitor system evolution:
```bash
# Check for new approaches
python scripts/generate_system_report.py

# Review discovered patterns
cat data/patterns/discovered_patterns.json
```

## Testing Multi-Agent Integration

### Test 1: Basic Agent Flow

```bash
# Test coordination
@hybrid-swarm "Write async Python guide"

# Verify:
- ✓ Coordination executed
- ✓ Dynamic approach selected
- ✓ Content generated
- ✓ Results reported
- ✓ Output written to artifacts/
```

### Test 2: Multi-Agent Pipeline

```bash
# Full pipeline
@researcher "Python async best practices"
@hybrid-swarm "Create tutorial from: artifacts/research-output.md"
@writer "Polish for Substack: artifacts/hybrid-swarm-output.md"

# Verify:
- ✓ Each agent reads previous output
- ✓ Metadata propagated
- ✓ Hybrid swarm pattern matched research context
- ✓ Quality improves through pipeline
```

### Test 3: Learning Verification

```bash
# Execute same prompt twice
@hybrid-swarm "Write async guide"  # First time
@hybrid-swarm "Write async guide"  # Second time

# Check:
- Same specialist reused? (should be)
- Approach selected improved? (possibly)
- Quality higher? (likely if first was good)
- Signal strength changed? (check system report)
```

## Troubleshooting

### Agent Not Found
```
Error: No agent named 'hybrid-swarm'
Solution: Create .claude/agents/hybrid-swarm.md with proper definition
```

### Coordination Returns Error
```
Error: agent_tools/get_coordination.py failed
Solution: Check Python environment, verify agent_tools/ exists
```

### Approaches Seem Static
```
Issue: Same approach always selected
Check: Is it actually performing well? High avg_quality? Strong signals?
Solution: May be correct! If concerned, check pattern discovery execution count.
```

### No New Approaches Discovered
```
Issue: Pattern discovery not creating new approaches
Check:
- Execution count >= 50?
- Sufficient task variety?
- Quality scores >= 0.7 for most executions?
Solution: Continue reporting results, ensure task diversity
```

### Quality Reports Not Affecting Selection
```
Issue: System doesn't seem to learn from quality reports
Check:
- Are you calling report_result.py after each execution?
- Are approach_id values correct?
- Is execution history being written? (check data/execution_history/)
Solution: Verify report_result.py completes successfully
```

## Conclusion

Proper integration of Hybrid Swarm with Claude Code agents creates a powerful emergent multi-agent system where:

- **Three-level coordination** provides intelligent routing
- **Pattern discovery** finds effective approaches automatically
- **Approach evolution** improves patterns over time
- **Natural selection** removes ineffective approaches
- **Collective learning** benefits all agents
- **Real LLM execution** provides actual capability

The result is adaptive, self-improving intelligence that gets smarter with every interaction.

---

*For detailed workflow steps, see [AGENT_WORKFLOW.md](AGENT_WORKFLOW.md)*
