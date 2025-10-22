# Hybrid Swarm Orchestration System

A three-level self-organizing agent coordination system that combines **Adaptive Resonance** (specialist selection), **Dynamic Approaches** (pattern-based approach evolution), and **Stigmergic Coordination** (swarm signals) for intelligent task routing and execution.

## Overview

The Hybrid Swarm system creates emergent intelligence through three complementary coordination layers:

### Level 1: Adaptive Resonance Layer
- Dynamically creates and manages specialist agents based on task patterns
- Specialists emerge organically from task characteristics
- Uses resonance matching to select appropriate specialists
- Learns and adapts specialist profiles over time

### Level 2: Dynamic Approaches Layer
- Approaches emerge from successful execution patterns (not hardcoded)
- Discovers effective patterns through clustering of execution history
- Approaches evolve based on performance feedback
- Natural selection: ineffective approaches are pruned automatically
- Specialized approaches for different task niches and styles

### Level 3: Stigmergic Coordination Layer
- Specialists coordinate through shared signal board
- Agents deposit signals about approach effectiveness
- Signals amplify (reinforce) or attenuate based on collective feedback
- Enables swarm intelligence without direct agent communication

**Result:** Vertical specialization (specialists) + horizontal diversity (approaches) + collective intelligence (swarm)!

## 🚀 Quick Start for Claude Code Users

**This is the intended use case** - The Hybrid Swarm system is designed as an intelligent coordination layer for Claude Code agents, enabling emergent specialization and collective learning.

### Setup the @Hybrid-swarm Agent

The agent is pre-configured in this repository. To use it in Claude Code:

1. **Open this project** in Claude Code (claude.ai/code)
2. **Type `@Hybrid-swarm`** in your chat to invoke the agent
3. **Ask your question** - The agent handles everything automatically

### Basic Usage

```
@Hybrid-swarm How do I implement async patterns in Python?
```

The agent will:
1. **Get coordination** - System selects specialist + dynamic approach + reads swarm signals
2. **Generate answer** - Agent creates real content following the coordinated approach style
3. **Report results** - System learns from the execution quality

### What Happens Behind the Scenes

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
Agent generates real answer
    ↓
agent_tools/report_result.py
    ↓
System learns and evolves
```

### Key Benefits

- **Zero configuration** - Agent is ready to use immediately
- **Emergent intelligence** - Specialists and approaches emerge automatically
- **Continuous learning** - System improves with every interaction
- **Style adaptation** - Answers adapt to question characteristics
- **Collective wisdom** - Benefits from all previous interactions

### Agent Files

- `.claude/agents/hybrid-swarm.md` - Agent configuration and instructions
- `agent_tools/get_coordination.py` - Coordination interface
- `agent_tools/report_result.py` - Results reporting
- `docs/AGENT_WORKFLOW.md` - Detailed workflow documentation

**💡 Pro Tip:** The more you use @Hybrid-swarm, the smarter it gets. The system discovers patterns, evolves approaches, and builds specialist expertise automatically!

## Architecture

```
User Task
    ↓
[Hybrid Orchestrator]
    ↓
┌─────────────────────────────────┐
│  Adaptive Resonance Layer       │
│  - Match task to specialists    │
│  - Create new if no good match  │
│  - Learn from outcomes          │
└──────────┬──────────────────────┘
           ↓
    Selected Specialist
           ↓
┌─────────────────────────────────┐
│  Dynamic Approaches Layer       │
│  - Pattern matching to task     │
│  - Select best-fit approach     │
│  - Discover new patterns        │
│  - Evolve approach signatures   │
└──────────┬──────────────────────┘
           ↓
    Matched Approach
           ↓
┌─────────────────────────────────┐
│  Stigmergic Coordination Layer  │
│  - Read signals from board      │
│  - Blend with pattern match     │
│  - Execute with approach style  │
│  - Deposit outcome signal       │
└─────────────────────────────────┘
           ↓
    Task Execution
           ↓
    Execution History
           ↓
    Pattern Discovery
```

## Quick Start

### Installation

```bash
# Clone or copy the Hybrid-swarm directory
cd Hybrid-swarm

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from src.hybrid_swarm import HybridSwarmOrchestrator

# Create orchestrator
orchestrator = HybridSwarmOrchestrator(
    vigilance_threshold=0.75,  # Higher = more specialized agents
    decay_rate=1800.0          # Signal decay time (seconds)
)

# Define a task
task = {
    "id": "task_001",
    "description": "Research Python async patterns",
    "domain": "research",
    "complexity": 0.7,
    "keywords": ["python", "async"],
    "estimated_duration": 2.0
}

# Execute through hybrid system
result = orchestrator.execute_task(task)

print(f"Specialist: {result['specialist_id']}")
print(f"Approach: {result['approach_id']}")
print(f"Quality: {result['quality']:.1%}")
```

### Interactive Q&A Interface

```bash
# Single question
python hybrid_interface.py "How do I use Python async/await?"

# Interactive chat mode
python hybrid_interface.py --interactive

# Using the wrapper (Windows UTF-8 support)
python run_hybrid_swarm.py --interactive
```

## Key Features

### Self-Organization
- **No manual configuration**: Specialists emerge from task patterns
- **Pattern discovery**: Approaches discovered from successful executions
- **Natural selection**: Poor performers automatically pruned
- **Continuous evolution**: Approaches refine themselves over time

### Emergent Intelligence
- **Specialist emergence**: Agents specialize in task domains
- **Approach emergence**: Execution patterns crystallize into approaches
- **Collective learning**: Swarm signals enable group knowledge
- **Adaptive coordination**: All layers learn and improve together

### Pattern-Based Coordination
- **Content analysis**: Extracts structure, tone, and style patterns
- **Similarity clustering**: Groups successful executions into patterns
- **Signature extraction**: Creates approach signatures from clusters
- **Style characteristics**: Defines how content should be generated

### Intelligent Matching
- **Hybrid selection**: 70% pattern matching + 30% stigmergic signals
- **Multi-factor scoring**: Domain, complexity, keywords, output types
- **Novelty detection**: Prevents duplicate approaches
- **Quality tracking**: Performance metrics guide evolution

### Transparency & Persistence
- **Full visibility**: Complete coordination decision trail
- **Execution history**: All executions recorded with quality metrics
- **Persistent learning**: Specialists, approaches, and signals saved between sessions
- **Pattern discovery**: Automatic triggers analyze execution history

## Real LLM Integration

The system now supports **real LLM execution** via Claude Code agent integration:

### Agent Tools
- `agent_tools/get_coordination.py` - Get coordination decisions for real execution
- `agent_tools/report_result.py` - Report actual execution results back to system
- `agent_tools/agent_helper.py` - Python utilities for programmatic access

### Agent Workflow
1. **Get Coordination**: Agent calls `get_coordination.py` to get specialist + approach
2. **Generate Answer**: Agent uses Claude LLM to generate real content following approach style
3. **Report Results**: Agent calls `report_result.py` to update system with actual quality
4. **System Learns**: All three layers improve from real execution feedback
5. **Pattern Discovery**: System automatically discovers new effective patterns
6. **Approach Evolution**: Approaches evolve based on performance data

### Documentation
- `docs/AGENT_WORKFLOW.md` - Complete agent workflow guide with examples
- `docs/AGENT-INTEGRATION-GUIDE.md` - Integration specifications
- `agent_tools/README.md` - Agent tools reference

### Demo vs Production
- `hybrid_interface.py` - Demo interface with simulated answers (for testing)
- `agent_tools/` - Production tools for real LLM execution (for Claude Code agent)

**Key Insight:** Python system provides three-level coordination intelligence, Claude agent provides execution capability!

## System Components

### Core Orchestration
- `src/hybrid_swarm.py` - Main orchestrator combining all three layers
- `src/adaptive_resonance.py` - Specialist creation and matching (Level 1)
- `src/stigmergic_coordination.py` - Signal board and swarm coordination (Level 3)

### Dynamic Approaches (Level 2)
- `src/dynamic_approach_manager.py` - Approach lifecycle management (CRUD, matching)
- `src/approach_patterns.py` - Data models for approaches, signatures, metrics
- `src/approach_storage.py` - Persistent storage and manifest management
- `src/approach_matching.py` - Pattern-based approach selection logic

### Pattern Discovery & Evolution
- `src/execution_history.py` - Historical execution tracking (JSONL format)
- `src/content_analyzer.py` - Content feature extraction and analysis
- `src/pattern_analyzer.py` - Pattern discovery via clustering, signature extraction
- `src/approach_evolution.py` - Approach creation, evolution, and pruning

### Security & Utilities
- `src/input_sanitization.py` - Input validation and security
- `src/approach_matching.py` - Matching utilities

### Agent Tools (Real LLM Integration)
- `agent_tools/get_coordination.py` - CLI tool to get coordination decisions
- `agent_tools/report_result.py` - CLI tool to report execution results
- `agent_tools/agent_helper.py` - Python utilities for programmatic access

### Interfaces
- `hybrid_interface.py` - Interactive Q&A system (demo with simulated answers)
- `run_hybrid_swarm.py` - UTF-8 wrapper for Windows

### Data Storage
- `data/specialists/` - Persistent specialist profiles
- `data/approaches/` - Dynamic approach definitions and manifest
- `data/execution_history/` - Historical execution records (JSONL by month)
- `data/patterns/` - Discovered patterns
- `data/stigmergy/` - Signal board state

## Configuration

### Vigilance Threshold (Adaptive Layer)
Controls specialist creation vs. reuse:
- **Higher (0.8-0.9)**: More specialists, highly specialized
- **Medium (0.7-0.8)**: Balanced specialization (recommended)
- **Lower (0.5-0.7)**: Fewer specialists, more generalized

### Decay Rate (Stigmergic Layer)
Controls signal persistence:
- **Fast (900s / 15min)**: Recent experiences dominate
- **Medium (1800s / 30min)**: Balanced memory (recommended)
- **Slow (3600s / 60min)**: Long-term pattern memory

### Hybrid Selection Strategy (Dynamic Approaches)
Blends pattern matching with stigmergic signals:
- **Pattern Weight (70%)**: Match based on task characteristics
- **Signal Weight (30%)**: Incorporate swarm intelligence
- Automatically triggers pattern discovery every 50 executions

## Examples

See `examples/basic_usage.py` for a complete working example.

See `examples/phase2_demo.py` for pattern discovery demonstration.

See `examples/phase3_demo.py` for approach evolution demonstration.

See `examples/phase4_demo.py` for complete integration demonstration.

## How It Works

### First Task Execution
1. Task analyzed for characteristics (domain, complexity, keywords)
2. **Adaptive layer** searches for matching specialist
3. No match found → Create new specialist
4. **Dynamic approach layer** matches task to approach patterns
5. **Stigmergic layer** reads signal board (initially empty)
6. Executes task with selected approach style
7. Records execution to history (quality, context, content)
8. Deposits signal about outcome to board
9. All three layers updated with results

### Subsequent Similar Tasks
1. Task analyzed
2. **Adaptive layer** finds matching specialist (resonance!)
3. **Dynamic approach layer** finds best-fit approach (pattern matching!)
4. **Stigmergic layer** reads signal board (signals present!)
5. Blends pattern match (70%) with signal strength (30%)
6. Executes task with approach guidance
7. Records to execution history
8. Reinforces or attenuates signals based on outcome
9. System learns: specialist profile + approach metrics + signal board

### Pattern Discovery & Evolution
1. Every 50 executions, system analyzes execution history
2. Clusters successful executions by similarity
3. Extracts pattern signatures from clusters:
   - Domain weights (e.g., writing: 0.9, coding: 0.6)
   - Complexity ranges (min/max)
   - Keyword patterns
   - Output type affinity
4. Extracts style characteristics from content:
   - Structure (sequential, hierarchical, bulleted)
   - Tone (formal, casual, technical)
   - Depth (concise, moderate, comprehensive)
   - Code requirements and example density
5. Creates new approaches from discovered patterns
6. Evolves existing approaches based on performance
7. Prunes ineffective approaches (soft delete)

### Learning Mechanisms

**Adaptive Layer:**
- Specialist profiles updated with task signatures
- Success rates tracked per specialist
- Quality scores maintained (exponential moving average)
- Poor performers pruned when limit reached

**Dynamic Approaches Layer:**
- Execution history analyzed for patterns
- Successful patterns crystallize into approaches
- Approaches evolve based on performance trends
- Natural selection removes underperformers
- Novelty checking prevents duplicates

**Stigmergic Layer:**
- Successful approaches amplified (signal strengthened)
- Less successful approaches attenuated (signal weakened)
- Signals decay over time (prevents stale patterns)
- Multiple agents reinforce collective knowledge

## Requirements

- Python 3.8+
- numpy (for adaptive resonance vector operations)
- scikit-learn (optional, for pattern clustering - fallback available)
- Standard library for core functionality

## License

[Include your license here]

## Related Projects

This is a standalone extraction from the Cognition-9 multi-agent orchestration system.

Original repository: https://github.com/MushroomFleet/Cognition-9

## Contributing

[Include contribution guidelines if applicable]

## Citation

If you use this system in your research or project, please cite:

```
Hybrid Swarm Orchestration System
Three-Level Emergent Intelligence
Adaptive Resonance + Dynamic Approaches + Stigmergic Coordination
https://github.com/[your-repo]/Hybrid-swarm
