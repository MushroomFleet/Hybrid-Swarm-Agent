"""
Hybrid Swarm Orchestration System
==================================

A two-level self-organizing agent coordination system combining:
- Adaptive Resonance: Dynamic specialist creation and selection
- Stigmergic Coordination: Swarm-based approach selection via signals

Main Components:
- HybridSwarmOrchestrator: Main orchestrator combining both layers
- AdaptiveResonanceOrchestrator: Specialist management layer
- StigmergicBoard: Signal coordination board
- StigmergicAgent: Swarm agent using signals for coordination
"""

from src.hybrid_swarm import HybridSwarmOrchestrator
from src.adaptive_resonance import (
    AdaptiveResonanceOrchestrator,
    TaskSignature,
    SpecialistProfile
)
from src.stigmergic_coordination import (
    StigmergicBoard,
    StigmergicAgent,
    Signal
)

__version__ = "1.0.0"
__all__ = [
    "HybridSwarmOrchestrator",
    "AdaptiveResonanceOrchestrator",
    "TaskSignature",
    "SpecialistProfile",
    "StigmergicBoard",
    "StigmergicAgent",
    "Signal"
]
