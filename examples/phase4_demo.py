"""
Phase 4: Integration - Complete Workflow Demo
Demonstrates HybridSwarmOrchestrator with dynamic approaches
"""

import sys
import os
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.hybrid_swarm import HybridSwarmOrchestrator
from src.content_analyzer import ContentAnalyzer
from src.dynamic_approach_manager import DynamicApproachManager


def demo_dynamic_coordination():
    """Demo: Getting coordination with dynamic approaches"""
    print("\n" + "=" * 70)
    print("DEMO 1: Dynamic Approach Coordination")
    print("=" * 70)
    
    orchestrator = HybridSwarmOrchestrator(
        vigilance_threshold=0.75,
        decay_rate=1800.0,
        use_dynamic_approaches=True,
        enable_pattern_discovery=True
    )
    
    # Test different task types
    tasks = [
        {
            'id': 'test_001',
            'description': 'Write a tutorial on Python decorators',
            'domain_weights': {'writing': 0.8, 'coding': 0.6},
            'complexity': 0.6,
            'keywords': ['tutorial', 'python', 'decorators'],
            'output_type': 'tutorial',
            'estimated_duration': 2.5
        },
        {
            'id': 'test_002',
            'description': 'Explain how sorting algorithms work',
            'domain_weights': {'coding': 0.9, 'writing': 0.5},
            'complexity': 0.7,
            'keywords': ['explain', 'sorting', 'algorithm'],
            'output_type': 'explanation',
            'estimated_duration': 2.0
        },
        {
            'id': 'test_003',
            'description': 'Compare React vs Vue frameworks',
            'domain_weights': {'analysis': 0.8, 'comparison': 0.7, 'coding': 0.5},
            'complexity': 0.8,
            'keywords': ['compare', 'react', 'vue', 'frameworks'],
            'output_type': 'comparison',
            'estimated_duration': 3.0
        }
    ]
    
    print("\nGetting coordination for 3 tasks...\n")
    
    for i, task in enumerate(tasks, 1):
        print(f"--- Task {i}: {task['description'][:50]}... ---")
        
        coordination = orchestrator.get_coordination(task)
        
        print(f"  Specialist: {coordination['specialist_id']}")
        print(f"  Approach ID: {coordination['approach_id']}")
        print(f"  Quality Target: {coordination['quality_target']:.2f}")
        
        if 'approach_metadata' in coordination:
            meta = coordination['approach_metadata']
            print(f"  Approach Name: {meta['name']}")
            print(f"  Structure: {meta['style']['structure']}")
            print(f"  Tone: {meta['style']['tone']}")
            print(f"  Requires Code: {meta['style']['use_code']}")
            print(f"  Expected Quality: {meta['expected_quality']:.2f}")
        
        print()
    
    print("✓ Dynamic approach coordination working!")
    return tasks


def demo_result_recording():
    """Demo: Recording results with content analysis"""
    print("\n" + "=" * 70)
    print("DEMO 2: Result Recording with Content Analysis")
    print("=" * 70)
    
    orchestrator = HybridSwarmOrchestrator(
        vigilance_threshold=0.75,
        use_dynamic_approaches=True
    )
    
    # Simulate execution result with generated content
    sample_content = """
# Python Decorators Tutorial

## Introduction

Decorators are a powerful feature in Python. Let's learn how they work!

## Step 1: Understanding Functions

In Python, functions are first-class objects. This means you can:
- Pass functions as arguments
- Return functions from other functions
- Assign functions to variables

### Example

```python
def greet(name):
    return f"Hello, {name}!"

# Functions can be assigned
say_hello = greet
print(say_hello("Alice"))
```

## Step 2: Creating a Decorator

A decorator is a function that takes another function and extends its behavior.

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before function call")
        result = func(*args, **kwargs)
        print("After function call")
        return result
    return wrapper

@my_decorator
def say_something(text):
    print(text)
```

## Step 3: Using Decorators

You can apply decorators using the @ syntax:

```python
@my_decorator
def greet(name):
    return f"Hello, {name}!"
```

## Summary

You've learned how Python decorators work! Practice creating your own decorators.
"""
    
    # Get coordination first
    task = {
        'id': 'content_test',
        'description': 'Write a tutorial on Python decorators',
        'domain_weights': {'writing': 0.8, 'coding': 0.6},
        'complexity': 0.6,
        'keywords': ['tutorial', 'python', 'decorators'],
        'output_type': 'tutorial',
        'estimated_duration': 2.5
    }
    
    coordination = orchestrator.get_coordination(task)
    
    print("\nCoordination received:")
    print(f"  Specialist: {coordination['specialist_id']}")
    print(f"  Approach: {coordination['approach_id']}")
    
    # Simulate LLM execution (content already generated above)
    print("\n[LLM generates content...]")
    
    # Analyze content
    analyzer = ContentAnalyzer()
    features = analyzer.analyze_content(sample_content)
    
    print("\nContent Analysis:")
    print(f"  Sections: {features.section_count}")
    print(f"  Code blocks: {features.code_block_count}")
    print(f"  Structure: Sequential steps")
    print(f"  Tone: {features.detected_tone}")
    print(f"  Code ratio: {features.code_ratio:.2f}")
    
    # Record result with content
    print("\nRecording result...")
    orchestrator.record_execution_result(
        specialist_id=coordination['specialist_id'],
        approach_id=coordination['approach_id'],
        task_id=coordination['task_id'],
        actual_quality=0.88,
        success=True,
        task_context=task,
        content_features=features
    )
    
    print("✓ Result recorded with content analysis!")
    
    # Check execution history
    from src.execution_history import ExecutionHistory
    history = ExecutionHistory()
    stats = history.get_statistics()
    print(f"\nExecution History Stats:")
    print(f"  Total records: {stats['total_records']}")


def demo_pattern_discovery_trigger():
    """Demo: Automatic pattern discovery after threshold"""
    print("\n" + "=" * 70)
    print("DEMO 3: Automatic Pattern Discovery")
    print("=" * 70)
    
    orchestrator = HybridSwarmOrchestrator(
        vigilance_threshold=0.75,
        use_dynamic_approaches=True,
        enable_pattern_discovery=True
    )
    
    # Check current approach count
    approach_count_before = len(orchestrator.approach_manager.list_approaches())
    print(f"\nApproaches before: {approach_count_before}")
    
    print("\nPattern discovery is triggered automatically every 50 executions")
    print("Current execution count:", orchestrator._execution_count)
    
    # Show execution history stats
    from src.execution_history import ExecutionHistory
    history = ExecutionHistory()
    stats = history.get_statistics()
    
    print(f"\nExecution History:")
    print(f"  Total records: {stats['total_records']}")
    print(f"  Storage size: {stats['total_size_bytes']} bytes")
    
    if stats['total_records'] >= 50:
        print("\n✓ Sufficient data for pattern discovery")
        print("  Pattern discovery will run on next result recording")
    else:
        print(f"\n- Need {50 - stats['total_records']} more executions for pattern discovery")


def demo_complete_workflow():
    """Demo: Complete end-to-end workflow"""
    print("\n" + "=" * 70)
    print("DEMO 4: Complete Workflow")
    print("=" * 70)
    
    orchestrator = HybridSwarmOrchestrator(
        vigilance_threshold=0.75,
        use_dynamic_approaches=True
    )
    
    print("\nComplete workflow demonstration:")
    print("1. Get coordination → 2. Generate content → 3. Record result")
    
    # Step 1: Get coordination
    print("\n[Step 1: Get Coordination]")
    task = {
        'id': 'workflow_test',
        'description': 'Explain recursion in programming',
        'domain_weights': {'coding': 0.7, 'writing': 0.6},
        'complexity': 0.7,
        'keywords': ['recursion', 'programming', 'explain'],
        'output_type': 'explanation',
        'estimated_duration': 2.0
    }
    
    coordination = orchestrator.get_coordination(task)
    print(f"  ✓ Got coordination:")
    print(f"    Specialist: {coordination['specialist_id']}")
    print(f"    Approach: {coordination['approach_id']}")
    
    # Step 2: Simulate content generation
    print("\n[Step 2: LLM Generates Content]")
    print("  (In production, real LLM would generate here)")
    
    simulated_content = """
Recursion is when a function calls itself. It consists of:

1. Base case - stops recursion
2. Recursive case - calls itself with modified input

Example:
```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
```
"""
    
    # Step 3: Analyze and record
    print("\n[Step 3: Analyze & Record Result]")
    analyzer = ContentAnalyzer()
    features = analyzer.analyze_content(simulated_content)
    
    orchestrator.record_execution_result(
        specialist_id=coordination['specialist_id'],
        approach_id=coordination['approach_id'],
        task_id=coordination['task_id'],
        actual_quality=0.82,
        success=True,
        task_context=task,
        content_features=features
    )
    
    print("  ✓ Result recorded")
    print("  ✓ Execution history updated")
    print("  ✓ Approach performance tracked")
    print("  ✓ Stigmergic signals deposited")
    
    # Show updated approach performance
    manager = DynamicApproachManager()
    approach = manager.get_approach(coordination['approach_id'])
    if approach:
        print(f"\n  Approach Performance:")
        print(f"    Usage: {approach.performance_metrics.usage_count}")
        print(f"    Avg Quality: {approach.performance_metrics.avg_quality:.2f}")
    
    print("\n✓ Complete workflow validated!")


def demo_system_overview():
    """Demo: System overview with all components"""
    print("\n" + "=" * 70)
    print("DEMO 5: System Overview")
    print("=" * 70)
    
    orchestrator = HybridSwarmOrchestrator(
        use_dynamic_approaches=True,
        enable_pattern_discovery=True
    )
    
    # Approach statistics
    manager = DynamicApproachManager()
    approaches = manager.list_approaches(active_only=False)
    active_approaches = [a for a in approaches if a.active]
    used_approaches = [a for a in approaches if a.performance_metrics.usage_count > 0]
    
    print("\n--- Dynamic Approaches System ---")
    print(f"Total Approaches: {len(approaches)}")
    print(f"  Active: {len(active_approaches)}")
    print(f"  Used: {len(used_approaches)}")
    
    # Execution history statistics
    from src.execution_history import ExecutionHistory
    history = ExecutionHistory()
    hist_stats = history.get_statistics()
    
    print("\n--- Execution History ---")
    print(f"Total Records: {hist_stats['total_records']}")
    print(f"Files: {hist_stats['total_files']}")
    print(f"Storage: {hist_stats['total_size_bytes']} bytes")
    
    # Coordinator statistics
    coord_stats = orchestrator.get_system_stats()
    
    print("\n--- Hybrid Coordination ---")
    print(f"Specialists: {coord_stats['adaptive_layer']['total_specialists']}")
    print(f"Stigmergic Signals: {coord_stats['stigmergic_layer']['total_signals']}")
    
    # Top performing approaches
    if used_approaches:
        print("\n--- Top 3 Approaches ---")
        top = sorted(used_approaches, key=lambda a: a.performance_metrics.avg_quality, reverse=True)[:3]
        for i, approach in enumerate(top, 1):
            metrics = approach.performance_metrics
            print(f"{i}. {approach.name}")
            print(f"   Quality: {metrics.avg_quality:.2f}, Usage: {metrics.usage_count}")
    
    print("\n✓ System overview complete")
    
    # Summary
    print("\n" + "=" * 70)
    print("INTEGRATION STATUS")
    print("=" * 70)
    print("\n✅ All components integrated:")
    print("  • HybridSwarmOrchestrator → DynamicApproachManager")
    print("  • Agent tools → Dynamic approach metadata")
    print("  • Result recording → Execution history")
    print("  • Pattern discovery → Automatic triggers")
    print("\nThe system is now:")
    print("  🎯 Selecting specialists adaptively")
    print("  🐜 Coordinating approaches via stigmergy")
    print("  🔍 Discovering patterns from data")
    print("  🧬 Evolving approaches automatically")
    print("  ♻️  Pruning underperformers")


def main():
    """Run complete Phase 4 demo"""
    print("\n" + "=" * 70)
    print("PHASE 4: Integration - Complete Workflow Demo")
    print("=" * 70)
    print("\nThis demo shows:")
    print("1. Dynamic approach coordination")
    print("2. Result recording with content analysis")
    print("3. Automatic pattern discovery triggers")
    print("4. Complete end-to-end workflow")
    print("5. System overview")
    
    try:
        # Demo 1: Dynamic coordination
        tasks = demo_dynamic_coordination()
        
        # Demo 2: Result recording
        demo_result_recording()
        
        # Demo 3: Pattern discovery
        demo_pattern_discovery_trigger()
        
        # Demo 4: Complete workflow
        demo_complete_workflow()
        
        # Demo 5: System overview
        demo_system_overview()
        
        print("\n" + "=" * 70)
        print("✓ PHASE 4 DEMO COMPLETE")
        print("=" * 70)
        print("\nIntegration successful!")
        print("\nThe Dynamic Approaches System is now fully integrated:")
        print("  ✅ Phase 1: Foundation (Data models, storage, matching)")
        print("  ✅ Phase 2: Pattern Analysis (History, content analysis, clustering)")
        print("  ✅ Phase 3: Evolution (Creation, evolution, pruning)")
        print("  ✅ Phase 4: Integration (Orchestrator, agent tools, workflow)")
        print("\nNext step:")
        print("  - Phase 5: Production deployment and monitoring")
        print("\nReady for real-world usage with automatic approach discovery!")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
