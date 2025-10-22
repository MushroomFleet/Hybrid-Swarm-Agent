# Hybrid-Swarm Agent Workflow Guide

Complete guide for using the Hybrid-swarm coordination system with Claude Code agent for real LLM execution.

## Overview

The Hybrid-swarm system provides **intelligent coordination** through three levels of emergent intelligence while YOU provide **real execution** using Claude's LLM capabilities.

**Separation of Concerns:**
- **Python coordination system** → WHO handles it (specialist) + HOW to approach it (dynamic approach pattern) + collective wisdom (swarm signals)
- **Claude agent (YOU)** → WHAT to say (actual content using LLM capabilities)

## Three-Level Coordination Architecture

### Level 1: Adaptive Resonance Layer
- Selects specialist based on task pattern matching
- Specialists emerge organically from task characteristics
- Learns and adapts specialist profiles over time

### Level 2: Dynamic Approaches Layer
- Approaches **emerge from successful execution patterns** (not hardcoded)
- Pattern discovery clusters similar successful executions
- Approaches evolve based on performance feedback
- Natural selection prunes ineffective approaches

### Level 3: Stigmergic Coordination Layer
- Blends pattern matching with swarm signals
- 70% pattern-based + 30% collective wisdom
- Signals amplify successful approaches
- Enables collective learning

## Complete Workflow

### Step 1: Get Coordination Decision

When a user asks a question, first get the coordination decision:

```bash
python agent_tools/get_coordination.py "How do I use Python async/await?"
```

**Returns JSON:**
```json
{
  "task_id": "task_1729559234",
  "specialist_id": "specialist_abc",
  "approach_id": "approach_coding_explain_bulleted",
  "approach_metadata": {
    "name": "Technical Coding Explanation (Bulleted)",
    "description": "Explains coding concepts with clear structure and bullet points",
    "pattern_signature": {
      "domain_weights": {
        "coding": 0.85,
        "writing": 0.6
      },
      "complexity_range": [0.5, 0.8],
      "keywords": ["code", "python", "technical", "explain"],
      "output_type": "tutorial"
    },
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
  },
  "quality_target": 0.85,
  "task_context": {
    "domain_weights": {
      "coding": 0.8,
      "writing": 0.5
    },
    "complexity": 0.6,
    "keywords": ["python", "async"],
    "output_type": "tutorial"
  },
  "coordination_details": {
    "match_score": 0.87,
    "selection_method": "hybrid",
    "pattern_weight": 0.7,
    "signal_weight": 0.3
  }
}
```

### Step 2: Understand the Dynamic Approach

The system selects approaches based on discovered patterns, not hardcoded templates. Use the `approach_metadata` to understand:

#### Pattern Signature
Defines **what tasks** this approach is good for:
- **Domain weights**: Primary domains (coding: 0.85, writing: 0.6)
- **Complexity range**: Best for mid-level complexity [0.5-0.8]
- **Keywords**: Common terms in successful executions
- **Output type**: Expected format (tutorial, analysis, guide, etc.)

#### Style Characteristics
Defines **how content** should be generated:
- **Structure**: bulleted, sequential, hierarchical, prose, or mixed
- **Tone**: technical, casual, formal, educational
- **Depth**: concise, moderate, comprehensive
- **Code requirements**: none, low, medium, high
- **Example density**: low, medium, high

#### Performance Metrics
Shows **how well** this approach has performed:
- **Average quality**: Historical quality score
- **Usage count**: How many times used
- **Success rate**: Percentage of successful executions

### Step 3: Generate Content Following the Pattern

Use the style characteristics to guide your content generation:

**Example for approach above:**
```python
# Based on metadata:
# - structure: "bulleted" → Use bullet points extensively
# - tone: "technical" → Use precise technical language
# - depth: "moderate" → Balance detail with readability
# - code_requirements: "high" → Include substantial code examples
# - example_density: "medium" → Show key examples, not every variation

# Your LLM generation:
"""
# Python Async/Await Explained

## Core Concepts

**Async functions** create coroutines:
• Defined with `async def`
• Return coroutine objects
• Must be awaited or run with asyncio

**Await expression** pauses execution:
• Only valid inside async functions
• Waits for coroutine to complete
• Returns the result

## Basic Example

```python
import asyncio

async def fetch_data():
    await asyncio.sleep(1)  # Simulates I/O
    return {"data": "example"}

# Run the coroutine
result = asyncio.run(fetch_data())
```

## When to Use

**Best for:**
• Network requests (HTTP, database)
• File I/O operations
• Multiple concurrent tasks

**Avoid for:**
• CPU-intensive calculations
• Simple synchronous operations
• When order matters strictly

## Common Patterns

**Pattern 1: Gather multiple tasks**
```python
results = await asyncio.gather(
    fetch_user(1),
    fetch_user(2),
    fetch_user(3)
)
```

**Pattern 2: Create tasks**
```python
task1 = asyncio.create_task(fetch_user(1))
task2 = asyncio.create_task(fetch_user(2))
results = await asyncio.gather(task1, task2)
```
"""
```

**Key Principles:**
1. **Follow the structure pattern** - If "bulleted", use bullets; if "sequential", use numbered steps
2. **Match the tone** - Technical content needs precision; casual needs approachability
3. **Respect depth level** - Concise means brief; comprehensive means thorough
4. **Include appropriate code** - High code_requirements = substantial examples
5. **Balance examples** - Medium density = key examples, not every variation

### Step 4: Assess Quality

After generating content, assess its quality honestly:

**Quality Scale:**
- **0.9-1.0** = Excellent (comprehensive, accurate, perfectly structured)
- **0.8-0.9** = Good (solid answer, meets all requirements)
- **0.7-0.8** = Adequate (acceptable, minor improvements possible)
- **0.5-0.7** = Below expectations (incomplete or significant issues)
- **0.0-0.5** = Poor (major problems, needs rework)

**Quality Criteria:**
- **Accuracy**: Information is correct and factual
- **Completeness**: All aspects addressed
- **Clarity**: Easy to understand and well-organized
- **Relevance**: Directly answers the question
- **Examples**: Includes helpful, working examples
- **Structure**: Follows the pattern's style characteristics

### Step 5: Report Results

Report actual execution results to enable system learning:

```bash
python agent_tools/report_result.py \
  --task-id task_1729559234 \
  --specialist specialist_abc \
  --approach-id approach_coding_explain_bulleted \
  --quality 0.88
```

**What happens:**
1. **Execution recorded** to history (JSONL format)
2. **Pattern discovery** triggered every 50 executions
3. **Approach metrics** updated with your quality score
4. **Stigmergic signals** reinforced or attenuated
5. **System learns** from your real execution outcome

This creates a continuous learning loop!

## Understanding Dynamic Approaches

### How Approaches Emerge

1. **Execution History**: Every task execution recorded with context and quality
2. **Pattern Discovery**: System clusters successful executions (every 50 executions)
3. **Signature Extraction**: Common patterns extracted from clusters
4. **Approach Creation**: New approaches created from discovered patterns
5. **Evolution**: Approaches evolve based on performance trends
6. **Pruning**: Ineffective approaches removed (soft delete)

### Approach Lifecycle

```
Execution → History Recording → Pattern Analysis → Cluster Discovery
                                                          ↓
                                                    New Approach Created
                                                          ↓
                                                    Usage & Learning
                                                          ↓
                                        ┌─────────────────┴─────────────────┐
                                        ↓                                   ↓
                                   Evolves (improves)               Pruned (underperforms)
                                        ↓
                                   Refined Pattern
```

### Example: Approach Discovery

**Initial State**: 3 legacy approaches (comprehensive, tutorial, summary)

**After 50 executions**: System discovers:
- "Coding explanations with bullets" pattern (technical domain, bulleted structure)
- "Writing tutorials with sequential steps" pattern (educational domain, step-by-step)
- "Analysis with comparisons" pattern (research domain, comparative structure)

**After 150 executions**: Approaches evolve:
- Bullet approach refines for higher code density
- Tutorial approach adds more hands-on examples
- Analysis approach improves comparison tables

**After 300 executions**: Natural selection:
- Successful approaches reinforced
- Underperforming approaches pruned
- Novel patterns continue emerging

## Complete Example

### User Question
"How do I use Python async/await?"

### Full Workflow

**1. Get Coordination:**
```bash
python agent_tools/get_coordination.py "How do I use Python async/await?"
```

Returns:
```json
{
  "approach_id": "approach_coding_explain_bulleted",
  "approach_metadata": {
    "style_characteristics": {
      "structure": "bulleted",
      "tone": "technical",
      "depth": "moderate",
      "code_requirements": "high"
    }
  },
  "quality_target": 0.85
}
```

**2. Interpret Pattern:**
- Structure: bulleted → Use extensive bullet points
- Tone: technical → Precise language, no fluff
- Depth: moderate → Balance detail and clarity
- Code requirements: high → Include substantial examples

**3. Generate Real Content:**
[Use Claude LLM to generate content following the pattern]

**4. Assess Quality:**
- Accuracy: 0.90 (all technical info correct)
- Completeness: 0.88 (all key concepts covered)
- Clarity: 0.86 (well-organized, clear explanations)
- Relevance: 0.90 (directly answers question)
- Examples: 0.88 (good working code examples)
- Structure: 0.85 (follows bulleted pattern well)

**Overall**: 0.88 (Good quality)

**5. Report Results:**
```bash
python agent_tools/report_result.py \
  --task-id task_1729559234 \
  --specialist specialist_abc \
  --approach-id approach_coding_explain_bulleted \
  --quality 0.88
```

**6. System Learning:**
- Execution recorded to `data/execution_history/2025-10/records_20251022.jsonl`
- Approach metrics updated: avg_quality, usage_count, success_rate
- Stigmergic signals reinforced (quality > 0.7)
- If 50th execution: pattern discovery triggered

**7. Present to User:**
```
🎯 Coordination Decision
Specialist: specialist_abc (coding specialist)
Approach: approach_coding_explain_bulleted (Technical Coding Explanation)
Pattern: Bulleted structure, technical tone, high code density
Quality Target: 85% → Achieved: 88%

📝 Answer
[Your real LLM-generated content here]

📊 System Learning
✓ Execution recorded to history
✓ Approach metrics updated (avg: 0.82 → 0.83)
✓ Stigmergic signals reinforced (+2.5 strength)
✓ Pattern discovery: 48/50 executions (triggers at 50)
```

## Tips for Success

### 1. Follow Pattern Characteristics Faithfully
The system learns by observing what works. If you ignore the pattern:
- System can't learn effectively
- Quality suffers
- Wrong patterns get reinforced

**Good**: Follow "bulleted" → use bullets extensively
**Bad**: Follow "bulleted" → write prose paragraphs

### 2. Be Honest in Quality Assessment
Under-rating prevents good patterns from emerging.
Over-rating reinforces poor approaches.

**Good**: Assess objectively against criteria
**Bad**: Always rate 0.9+ to "help" the system

### 3. Use Approach Metadata
The metadata tells you what worked before:
- High avg_quality (>0.8) = proven pattern
- High usage_count = frequently selected
- High success_rate = reliable approach

### 4. Report Every Execution
Even failed attempts help the system learn:
```bash
python agent_tools/report_result.py \
  --task-id task_xyz \
  --specialist specialist_abc \
  --approach-id approach_xyz \
  --quality 0.45
```

Low quality signal → approach attenuated → better selection next time

### 5. Watch Pattern Discovery
Every 50 executions, check for new approaches:
```bash
python scripts/generate_system_report.py
```

New approaches = system discovered effective patterns!

## Advanced: Programmatic Integration

For advanced users, use Python directly:

```python
from agent_tools.agent_helper import CoordinationClient

# Get coordination
client = CoordinationClient()
coord = client.get_coordination("How do I use Python async/await?")

print(f"Specialist: {coord['specialist_id']}")
print(f"Approach: {coord['approach_id']}")
print(f"Style: {coord['approach_metadata']['style_characteristics']}")

# Generate answer using LLM based on style characteristics
style = coord['approach_metadata']['style_characteristics']
answer = your_llm_function(
    prompt=coord['task_context']['description'],
    structure=style['structure'],
    tone=style['tone'],
    depth=style['depth'],
    code_level=style['code_requirements']
)

# Assess quality
quality = assess_quality(answer)

# Report result
client.report_result(
    task_id=coord['task_id'],
    specialist_id=coord['specialist_id'],
    approach_id=coord['approach_id'],
    quality=quality
)
```

## Troubleshooting

### "Approach doesn't match the question"
Early in learning, matching may be exploratory. The system improves through:
- Your quality reports teaching what works
- Pattern discovery finding better matches
- Natural selection removing poor patterns

### "Same approach used repeatedly"
This is normal if it's performing well:
- Check approach metrics: high avg_quality?
- Stigmergic signals: strong reinforcement?
- If it works, the system will keep using it

### "New approaches not appearing"
Pattern discovery requires:
- 50+ executions recorded
- Sufficient variety in tasks
- Quality scores >0.7 for clustering
- Check: `data/patterns/discovered_patterns.json`

### "Quality hard to assess"
Use the 6-criteria checklist:
1. Accuracy (facts correct?)
2. Completeness (all aspects covered?)
3. Clarity (easy to understand?)
4. Relevance (answers the question?)
5. Examples (helpful illustrations?)
6. Structure (follows pattern?)

Average the scores for overall quality.

## System Evolution Timeline

**Weeks 1-2**: System uses initial approaches, explores patterns
**Weeks 3-4**: First pattern discovery, new approaches emerge
**Weeks 5-8**: Approaches evolve, specialization increases
**Weeks 9+**: Mature system with diverse, specialized approaches

**Key Insight**: The system gets smarter with every execution you report!

## Summary

**The Hybrid-swarm Three-Level Advantage:**

1. **Adaptive Resonance** - Right specialist for the task
2. **Dynamic Approaches** - Patterns that emerge from success
3. **Stigmergic Coordination** - Collective wisdom guides selection
4. **Pattern Discovery** - New approaches discovered automatically
5. **Continuous Evolution** - Approaches improve over time
6. **Natural Selection** - Poor approaches pruned naturally

**Your Role:**
- Get coordination decision (specialist + dynamic approach)
- Follow pattern characteristics faithfully
- Generate real content using LLM
- Assess quality honestly
- Report results consistently

This creates an emergent intelligence system where coordination and execution reinforce each other through continuous learning!
