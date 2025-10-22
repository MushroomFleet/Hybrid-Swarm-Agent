# Using the Hybrid Swarm Agent in Claude Code

Quick reference for using the `@hybrid-swarm` agent in Claude Code.

## What is Hybrid Swarm?

A three-level self-organizing system that combines:
- **Level 1 - Adaptive Resonance**: Specialists emerge from task patterns
- **Level 2 - Dynamic Approaches**: Approaches emerge from successful executions
- **Level 3 - Stigmergic Coordination**: Swarm signals guide selection

Result: Vertical specialization + horizontal diversity + collective intelligence!

## Quick Start

### Method 1: Tag the Agent (Recommended)

Simply tag the agent with your question:

```
@hybrid-swarm How do I use Python async/await?
```

The agent will:
1. Get coordination from the hybrid system (specialist + dynamic approach)
2. Generate real content using Claude's LLM following the approach pattern
3. Report results back to enable system learning
4. Return the answer with coordination metadata

### Method 2: Demo Interface (Testing)

Run the demo interface with simulated answers:

```bash
# Single question
python hybrid_interface.py "Your question here"

# Interactive chat mode
python hybrid_interface.py --interactive
```

**Note**: This uses templates for testing. For real LLM execution, use `@hybrid-swarm`.

## Behind the Scenes

When you use `@hybrid-swarm`:

```
Your Question
    ↓
agent_tools/get_coordination.py
    ↓
[Three-Level Coordination]
├─ Adaptive Resonance → Selects specialist
├─ Dynamic Approaches → Matches approach pattern
└─ Stigmergic Signals → Incorporates swarm wisdom
    ↓
Claude generates real content
    ↓
agent_tools/report_result.py
    ↓
System learns and evolves
```

**Key difference**: System provides coordination intelligence, Claude provides content generation capability.

## Example Interactions

### Example 1: Technical Question
```
@hybrid-swarm Explain Python async/await

Coordination:
- Specialist: specialist_coding_tutorial
- Approach: approach_coding_explain_bulleted
- Pattern: Bulleted structure, technical tone, high code density

Output: Technical explanation with bullet points and code examples
Quality: 0.88 → System learns this approach works well
```

### Example 2: Tutorial Request
```
@hybrid-swarm Write a tutorial on Python threading

Coordination:
- Specialist: specialist_writing_tutorial
- Approach: approach_writing_tutorial_sequentialsteps
- Pattern: Sequential steps, educational tone, hands-on examples

Output: Step-by-step tutorial with progressive complexity
Quality: 0.91 → Approach reinforced, signals amplified
```

### Example 3: Research Task
```
@hybrid-swarm Research async/await vs threading trade-offs

Coordination:
- Specialist: specialist_analysis_research
- Approach: approach_analysis_compare_bulleted
- Pattern: Comparative structure, analytical tone, evidence-based

Output: Comparative analysis with trade-offs
Quality: 0.85 → Pattern discovery learns this combination works
```

## How Dynamic Approaches Work

### Approaches Emerge from Success

Unlike hardcoded templates, approaches are discovered from successful executions:

**Initial State (Week 1)**
```
3 legacy approaches (comprehensive, tutorial, summary)
```

**After 50 Executions (Week 3)**
```
Pattern discovery triggered!
✓ Discovered: approach_coding_explain_bulleted
✓ Discovered: approach_writing_tutorial_sequentialsteps
✓ Discovered: approach_analysis_compare_bulleted
```

**After 150 Executions (Week 6)**
```
Approaches evolve!
✓ approach_coding_explain_bulleted: Code density increased
✓ approach_writing_tutorial_sequentialsteps: Steps refined
Quality improvements: +5-10%
```

**After 300 Executions (Week 10)**
```
Natural selection!
✓ Successful approaches reinforced
✗ Poor approaches pruned
+ New patterns discovered
```

### Approach Metadata

Each dynamic approach includes:

**Pattern Signature** (what tasks it's good for):
- Domain weights: coding: 0.85, writing: 0.6
- Complexity range: [0.5, 0.8]
- Keywords: ["code", "python", "technical"]
- Output type: tutorial

**Style Characteristics** (how to generate content):
- Structure: bulleted, sequential, hierarchical, or prose
- Tone: technical, casual, formal, educational
- Depth: concise, moderate, comprehensive
- Code requirements: none, low, medium, high
- Example density: low, medium, high

**Performance Metrics** (how well it works):
- Average quality: 0.82
- Usage count: 45 times
- Success rate: 89%

## System Learning

The system continuously learns through three mechanisms:

### 1. Pattern Discovery (Every 50 Executions)
- Clusters successful executions by similarity
- Extracts common patterns (domain, structure, style)
- Creates new approaches from discovered patterns

### 2. Approach Evolution
- Refines pattern signatures based on performance
- Adjusts style characteristics for better quality
- Improves approach definitions incrementally

### 3. Natural Selection
- Successful approaches amplified via signals
- Underperforming approaches pruned
- System adapts to what actually works

## System Files & Monitoring

### Agent Configuration
```
.claude/agents/hybrid-swarm.md - Agent definition
```

### Core System (Python)
```
src/
├── hybrid_swarm.py                  # Main orchestrator
├── adaptive_resonance.py            # Level 1: Specialists
├── dynamic_approach_manager.py      # Level 2: Approaches
├── pattern_analyzer.py              # Level 2: Pattern discovery
├── approach_evolution.py            # Level 2: Evolution
└── stigmergic_coordination.py       # Level 3: Signals
```

### Agent Tools (Real LLM Integration)
```
agent_tools/
├── get_coordination.py              # Get coordination decision
├── report_result.py                 # Report execution results
└── agent_helper.py                  # Programmatic access
```

### Data Storage
```
data/
├── specialists/                     # Specialist profiles (JSON)
├── approaches/                      # Dynamic approach definitions
│   ├── manifest.json                # Approach registry
│   ├── legacy_approach_*.json       # Initial seed approaches
│   └── approach_*.json              # Discovered approaches
├── execution_history/               # Historical executions (JSONL)
│   └── YYYY-MM/records_*.jsonl      # Monthly execution logs
├── patterns/                        # Discovered patterns
│   └── discovered_patterns.json
└── stigmergy/                       # Signal board state
    └── signals.json (or individual files)
```

### Monitoring Commands

**Check System Status**
```bash
python scripts/generate_system_report.py
```

Shows:
- Active approaches count
- Quality metrics
- Pattern discovery status
- Recent executions

**View Discovered Patterns**
```bash
cat data/patterns/discovered_patterns.json
```

**View Approach Definitions**
```bash
ls data/approaches/
cat data/approaches/approach_coding_explain_bulleted.json
```

**View Execution History**
```bash
ls data/execution_history/2025-10/
cat data/execution_history/2025-10/records_20251022.jsonl | tail -n 5
```

**View Specialists**
```bash
ls data/specialists/
cat data/specialists/specialist_*.json
```

**View Signal Board**
```bash
cat data/stigmergy/signals.json
```

## Demo vs Production Modes

### Demo Mode (hybrid_interface.py)
- Uses template-based answers (simulated)
- Good for testing coordination logic
- No real LLM required
- Fast for development/testing

```bash
python hybrid_interface.py "Test question"
python hybrid_interface.py --interactive
```

### Production Mode (@hybrid-swarm agent)
- Uses real Claude LLM for content generation
- Full coordination intelligence + execution capability
- Reports actual quality back to system
- Enables pattern discovery and evolution

```
@hybrid-swarm Your real question here
```

**Recommendation**: Use `@hybrid-swarm` for actual work, `hybrid_interface.py` for testing.

## Integration with Other Agents

Chain with other agents for powerful workflows:

### Research → Hybrid Swarm → Write
```
@researcher Gather information on async patterns
@hybrid-swarm "Create tutorial from: artifacts/research-output.md"
@writer Polish for blog publication
```

### Hybrid Swarm → Critic → Refine
```
@hybrid-swarm "Write technical guide on Docker"
@critic-reviewer Validate technical accuracy
@hybrid-swarm "Refine based on: artifacts/feedback.md"
```

### Parallel Perspectives
```
@hybrid-swarm "Research perspective on AI safety"
@hybrid-swarm "Technical perspective on AI safety"
@hybrid-swarm "Policy perspective on AI safety"
@writer "Synthesize all three perspectives"
```

## Configuration

### Adjust Vigilance (Specialist Creation)
- Higher (0.8-0.9): More specialists, highly specialized
- Medium (0.7-0.8): Balanced (default)
- Lower (0.5-0.7): Fewer specialists, more generalized

### Adjust Signal Decay
- Fast (900s): Recent experiences dominate
- Medium (1800s): Balanced memory (default)
- Slow (3600s): Long-term patterns

Edit in `src/hybrid_swarm.py` or pass parameters programmatically.

## What Makes This Different

### Traditional AI Systems
- Hardcoded routing rules
- Fixed response templates
- Manual configuration required
- No adaptation over time

### Hybrid Swarm
- ✅ Self-organizing (specialists emerge)
- ✅ Pattern-based (approaches discovered)
- ✅ Continuously learning (quality improves)
- ✅ Collective intelligence (swarm wisdom)
- ✅ Natural selection (poor approaches pruned)
- ✅ Full transparency (see all decisions)

## Frequently Asked Questions

**Q: Why is the same approach always selected?**  
A: If it's performing well (high avg_quality), the system will continue using it. This is correct behavior! Check the approach metrics to verify.

**Q: When will new approaches be discovered?**  
A: Pattern discovery runs every 50 executions. Ensure you have diverse tasks and quality scores >0.7 for clustering.

**Q: How do I see what the system has learned?**  
A: Run `python scripts/generate_system_report.py` for a comprehensive overview.

**Q: Can I manually add approaches?**  
A: Yes, but it's better to let the system discover them from successful executions. Manual approaches go in `data/approaches/`.

**Q: What if an approach gives poor results?**  
A: Report the actual quality score (even if low). The system learns from failures and will attenuate/prune poor approaches.

**Q: How long until the system is "trained"?**  
A: Week 1-2: Exploration, Week 3-4: First discoveries, Week 5-8: Evolution, Week 9+: Mature system with diverse specialized approaches.

## Advanced Usage

### Programmatic Access

```python
from agent_tools.agent_helper import CoordinationClient

client = CoordinationClient()

# Get coordination
coord = client.get_coordination("How do I use async/await?")
print(f"Approach: {coord['approach_id']}")
print(f"Pattern: {coord['approach_metadata']['style_characteristics']}")

# Generate content (using your LLM)
answer = your_llm_function(
    prompt=coord['task_context']['description'],
    **coord['approach_metadata']['style_characteristics']
)

# Report results
client.report_result(
    task_id=coord['task_id'],
    specialist_id=coord['specialist_id'],
    approach_id=coord['approach_id'],
    quality=0.88
)
```

### Custom Approach Creation

While the system discovers approaches automatically, you can seed custom approaches:

```json
{
  "id": "approach_custom_security",
  "name": "Security-Focused Analysis",
  "pattern_signature": {
    "domain_weights": {"coding": 0.9, "security": 0.95},
    "complexity_range": [0.6, 1.0],
    "keywords": ["security", "vulnerability", "authentication"],
    "output_type": "analysis"
  },
  "style_characteristics": {
    "structure": "hierarchical",
    "tone": "technical",
    "depth": "comprehensive",
    "code_requirements": "high",
    "example_density": "high"
  }
}
```

Save to `data/approaches/` and update `manifest.json`.

## Summary

The hybrid swarm agent provides:
- **Three-level coordination**: Specialists + Dynamic Approaches + Swarm Signals
- **Emergent intelligence**: No hardcoded rules, patterns discovered from success
- **Continuous learning**: Quality improves with every execution
- **Pattern discovery**: New approaches emerge automatically
- **Natural selection**: Poor approaches pruned, successful ones amplified
- **Full transparency**: See all coordination decisions and learning

Just use `@hybrid-swarm` followed by your question, and the system handles the rest!

---

**For detailed technical documentation:**
- [AGENT_WORKFLOW.md](AGENT_WORKFLOW.md) - Complete agent workflow guide
- [AGENT-INTEGRATION-GUIDE.md](AGENT-INTEGRATION-GUIDE.md) - Multi-agent integration patterns
- [DYNAMIC_APPROACHES_SPECIFICATION.md](DYNAMIC_APPROACHES_SPECIFICATION.md) - System architecture
