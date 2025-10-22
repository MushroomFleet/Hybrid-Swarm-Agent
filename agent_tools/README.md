# Agent Tools

Command-line tools for integrating Hybrid-swarm coordination with Claude Code agent.

## Overview

These tools enable the Claude Code agent to:
1. Get intelligent coordination decisions from the hybrid swarm system
2. Generate real LLM responses based on approach guidance
3. Report actual execution results back for system learning

## Tools

### get_coordination.py

Get coordination decision for a user prompt.

**Usage:**
```bash
python agent_tools/get_coordination.py "User's question here"
```

**Example:**
```bash
python agent_tools/get_coordination.py "How do I use Python async/await?"
```

**Output:**
```json
{
  "task_id": "task_1729559234",
  "specialist_id": "specialist_abc",
  "approach": "approach_B",
  "quality_target": 0.85,
  "task_context": {
    "domain": "writing",
    "complexity": 0.6,
    "keywords": ["python", "async"],
    "output_type": "tutorial"
  },
  "prompt": "How do I use Python async/await?"
}
```

### report_result.py

Report actual execution results back to coordination system.

**Usage:**
```bash
python agent_tools/report_result.py \
  --task-id TASK_ID \
  --specialist SPECIALIST_ID \
  --quality QUALITY_SCORE \
  [--no-success]
```

**Example:**
```bash
python agent_tools/report_result.py \
  --task-id task_1729559234 \
  --specialist specialist_abc \
  --quality 0.90
```

**Quality Scale:**
- 0.9-1.0 = Excellent
- 0.8-0.9 = Good  
- 0.7-0.8 = Adequate
- 0.5-0.7 = Below expectations
- 0.0-0.5 = Poor

### agent_helper.py

Python utilities for programmatic access.

**Usage:**
```python
from agent_tools.agent_helper import CoordinationClient, ApproachGuide, QualityAssessment

# Get coordination
client = CoordinationClient()
coord = client.get_coordination("How do I use Python async/await?")

# Get approach guide
guide = ApproachGuide.get_approach_guide(coord['approach'])
print(guide['name'])
print(guide['characteristics'])

# Assess quality
quality = QualityAssessment.estimate_quality(
    accuracy=0.95,
    completeness=0.90,
    clarity=0.85,
    relevance=0.90,
    examples=0.85,
    structure=0.90
)

# Report result
client.report_result(
    task_id=coord['task_id'],
    specialist_id=coord['specialist_id'],
    quality=quality
)
```

## Approach Styles

### Approach A: Comprehensive Research
- Multi-source analysis
- Detailed, thorough coverage
- Evidence-based conclusions
- Multiple perspectives

### Approach B: Step-by-Step Tutorial
- Clear sequential steps
- Practical hands-on examples
- Progressive complexity
- Actionable instructions

### Approach C: Summary & Key Points
- Executive summary first
- Bullet-point format
- Concise examples
- Quick reference

## Complete Workflow

1. **Get Coordination:**
   ```bash
   python agent_tools/get_coordination.py "User question"
   ```

2. **Parse Response:**
   - Note the `specialist_id`
   - Note the `approach` (A/B/C)
   - Note the `task_id`
   - Use `task_context` for guidance

3. **Generate Answer:**
   - Follow the approach style guidelines
   - Use Claude's LLM capabilities
   - Generate real, helpful content

4. **Assess Quality:**
   - Evaluate based on 6 criteria
   - Be honest and realistic
   - Use 0.0-1.0 scale

5. **Report Results:**
   ```bash
   python agent_tools/report_result.py \
     --task-id TASK_ID \
     --specialist SPECIALIST_ID \
     --quality ACTUAL_QUALITY
   ```

6. **System Learns:**
   - Adaptive layer updates specialist profiles
   - Stigmergic layer reinforces/attenuates approach signals
   - Future coordination becomes more intelligent

## Documentation

See `docs/AGENT_WORKFLOW.md` for complete workflow guide and examples.

See `.claude/agents/hybrid-swarm.md` for agent-specific instructions.

## Testing

Test the tools:

```bash
# Test coordination
python agent_tools/get_coordination.py "Test question about Python"

# Test result reporting
python agent_tools/report_result.py \
  --task-id test_001 \
  --specialist specialist_test \
  --quality 0.85

# Test helper utilities
python agent_tools/agent_helper.py
```

## Requirements

- Python 3.8+
- Hybrid-swarm core system (src/)
- No external dependencies

## Integration with Claude Code Agent

These tools are designed to work seamlessly with Claude Code agent:

1. Agent receives user question
2. Agent executes `get_coordination.py` via Execute_Command
3. Agent parses JSON response
4. Agent generates real answer using approach guidance
5. Agent executes `report_result.py` to update system
6. System learns and improves

This creates a powerful feedback loop between coordination intelligence and execution capability!
