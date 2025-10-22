# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Hybrid-swarm** is a two-level self-organizing agent coordination system combining **Adaptive Resonance** (specialist selection) with **Stigmergic Coordination** (swarm intelligence) for emergent task routing and execution.

This is a standalone system extracted from the larger Cognition-9 project, focusing specifically on bio-inspired coordination patterns.

## Core Architecture

### Two-Level Coordination

**Level 1: Adaptive Resonance Layer** (`src/adaptive_resonance.py`)
- Dynamically creates specialist agents from task patterns
- Uses resonance matching (cosine similarity) to select specialists
- Specialists emerge organically without manual configuration
- Vigilance threshold controls specialization vs. generalization

**Level 2: Stigmergic Coordination Layer** (`src/stigmergic_coordination.py`)
- Specialists coordinate through shared signal board
- Signals amplify (reinforce) or attenuate based on collective feedback
- Enables swarm intelligence without direct agent communication
- Signal decay prevents stale patterns from dominating

**Integration** (`src/hybrid_swarm.py`)
- Combines both layers for dual learning
- Adaptive layer selects specialist → Specialist uses stigmergic signals for approach
- Both layers learn from execution outcomes

### Execution Flow

```
User Task
  ↓
[Hybrid Orchestrator]
  ↓ (extracts task signature)
[Adaptive Resonance Layer] → Match or create specialist
  ↓
[Selected Specialist]
  ↓ (reads signal board)
[Stigmergic Coordination] → Select approach based on signals
  ↓
Task Execution
  ↓
Update both layers with results
```

## Running the System

### Basic Usage

```bash
# Run the basic example
python examples/basic_usage.py

# Run the hybrid swarm orchestrator directly
python src/hybrid_swarm.py
```

### Interactive Q&A Interface

```bash
# Single question mode
python hybrid_interface.py "How do I use Python async/await?"

# Interactive chat mode
python hybrid_interface.py --interactive
python hybrid_interface.py -i

# On Windows (UTF-8 wrapper)
python run_hybrid_swarm.py --interactive
```

Interactive commands:
- Type questions to get answers
- `stats` - Show system statistics (specialists, signals, quality)
- `history` - Show recent interactions
- `quit` or `exit` - Save session and exit

### Running Individual Components

```bash
# Test adaptive resonance layer only
python src/adaptive_resonance.py

# Test stigmergic coordination only
python src/stigmergic_coordination.py
```

## Development

### Installing Dependencies

```bash
# Optional: numpy for vector operations (recommended)
pip install -r requirements.txt

# Or run without numpy (stdlib only, slightly less efficient)
# System will work but uses hash-based similarity instead
```

**Note**: Core system uses Python standard library only. Numpy is optional for optimized vector operations in adaptive resonance.

### Key Configuration Parameters

**Vigilance Threshold** (Adaptive Layer):
- Higher (0.8-0.9): More specialists, highly specialized
- Medium (0.7-0.8): Balanced (recommended for most tasks)
- Lower (0.5-0.7): Fewer specialists, more generalized

**Decay Rate** (Stigmergic Layer):
- Fast (900s / 15min): Recent experiences dominate
- Medium (1800s / 30min): Balanced memory (default)
- Slow (3600s / 60min): Long-term pattern retention

**Max Specialists**: Default 10. System prunes poor performers when limit reached.

### File Structure

```
src/
├── hybrid_swarm.py          # Main orchestrator (combines both layers)
├── adaptive_resonance.py    # Specialist creation and matching
├── stigmergic_coordination.py # Signal board and swarm coordination
└── __init__.py

examples/
└── basic_usage.py           # Complete working example

data/
├── specialists/             # Persistent specialist profiles (JSON)
└── stigmergy/              # Signal board state (JSON)

artifacts/
└── hybrid-sessions/        # Saved interaction sessions (JSON)

hybrid_interface.py          # Interactive Q&A system
run_hybrid_swarm.py         # Windows UTF-8 wrapper
```

## Key Data Structures

### Task Structure
```python
task = {
    "id": "task_001",
    "description": "Task description",
    "domain": "research",           # research, writing, coding, review, etc.
    "complexity": 0.7,              # 0.0 to 1.0
    "keywords": ["python", "async"],
    "input_type": "text",           # text, code, data
    "output_type": "report",        # report, tutorial, code, analysis
    "estimated_duration": 2.0       # hours
}
```

### Result Structure
```python
result = {
    "specialist_id": "specialist_91e31361",
    "approach": "approach_A",
    "quality": 0.84,                # 0.0 to 1.0
    "success": True
}
```

## Understanding the System

### First Task Execution
1. Task analyzed for characteristics (domain, complexity, keywords)
2. Adaptive layer searches for matching specialist (resonance < threshold)
3. No match → Create new specialist with task signature
4. Specialist reads signal board (empty on first run)
5. Explores randomly, selects approach
6. Executes, deposits signal with outcome
7. Both layers updated with results

### Subsequent Similar Tasks
1. Task analyzed
2. Adaptive layer finds matching specialist (resonance ≥ threshold)
3. Specialist reused and profile adapted
4. Reads signal board (signals present from prior work)
5. Selects approach weighted by signal strength
6. Executes, reinforces or attenuates signals
7. System learns: specialist profile AND signal board improve

### Learning Mechanisms

**Adaptive Layer**:
- Specialist profiles updated with task signatures (exponential moving average)
- Success rates tracked per specialist
- Quality scores maintained
- Poor performers pruned when max_specialists reached

**Stigmergic Layer**:
- Successful approaches amplified (signal strength increased by amplification_factor)
- Less successful approaches attenuated (strength reduced by attenuation_factor)
- Signals decay exponentially over time
- Multiple agents reinforce collective knowledge

## Persistent State

All state persists between sessions:

- **Specialists**: `data/specialists/specialist_*.json` - Profiles include task signatures, success rates, quality scores
- **Signals**: `data/stigmergy/signals.json` - Signal board with all deposited signals and timestamps
- **Sessions**: `artifacts/hybrid-sessions/session_*.json` - Interaction history from Q&A interface

To reset the system: delete files in `data/` directories (directories are preserved).

## Integration Points

The hybrid swarm can be:
- Used standalone via `HybridSwarmOrchestrator`
- Integrated into larger systems as a coordination mechanism
- Extended with real LLM integration (currently uses simulated answers)

To add real LLM integration: Modify `AnswerGenerator` class in `hybrid_interface.py:90-142` to call actual language models instead of using templates.

## Python Version

Requires Python 3.8+ for:
- `typing` module features (Dict, List, Any, Optional)
- Dataclasses
- pathlib
- f-strings

Tested with Python 3.12.

## Common Patterns

### Creating an orchestrator
```python
from src.hybrid_swarm import HybridSwarmOrchestrator

orchestrator = HybridSwarmOrchestrator(
    vigilance_threshold=0.75,
    decay_rate=1800.0,
    max_specialists=10
)
```

### Executing a task
```python
task = {
    "id": "unique_id",
    "description": "Task description",
    "domain": "research",
    "complexity": 0.7,
    "keywords": ["python", "async"],
    "estimated_duration": 2.0
}

result = orchestrator.execute_task(task)
# Returns: specialist_id, approach, quality, success
```

### Getting system statistics
```python
stats = orchestrator.get_system_stats()
# Returns adaptive_layer, stigmergic_layer, hybrid_metrics
```

### Visualizing coordination
```python
viz = orchestrator.visualize_coordination()
print(viz)  # Markdown-formatted system state
```

## Design Principles

**Self-Organization**: No manual routing or configuration. Specialists emerge from task patterns.

**Emergent Intelligence**: System intelligence emerges from interaction of simple coordination rules.

**Collective Learning**: Both vertical (specialist profiles) and horizontal (swarm signals) learning.

**Transparency**: Full visibility into coordination decisions via logging and statistics.

**Persistence**: State survives across sessions for continuous learning.

**Simplicity**: Minimal dependencies, clear separation of concerns, standard library focus.
