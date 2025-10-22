"""
Basic Usage Example for Hybrid Swarm Orchestration System
==========================================================

This example demonstrates:
1. Creating a hybrid swarm orchestrator
2. Defining and executing tasks
3. Viewing system statistics
4. Understanding specialist selection and signal coordination
"""

import sys
import os
import time

# Add parent directory to path to import src modules
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.hybrid_swarm import HybridSwarmOrchestrator


def print_header(text, char="="):
    """Print formatted header"""
    width = 70
    print(f"\n{char * width}")
    print(f"{text:^{width}}")
    print(f"{char * width}\n")


def main():
    print_header("HYBRID SWARM BASIC USAGE EXAMPLE")
    
    # Step 1: Create the orchestrator
    print("Step 1: Creating Hybrid Swarm Orchestrator")
    print("-" * 70)
    
    orchestrator = HybridSwarmOrchestrator(
        vigilance_threshold=0.75,  # Balanced specialist creation
        decay_rate=1800.0,         # 30-minute signal decay
        max_specialists=10         # Maximum number of specialists
    )
    
    print("✓ Orchestrator created with:")
    print(f"  - Vigilance threshold: 0.75 (balanced specialization)")
    print(f"  - Signal decay rate: 1800s (30 minutes)")
    print(f"  - Max specialists: 10")
    
    # Step 2: Define sample tasks
    print("\n\nStep 2: Defining Sample Tasks")
    print("-" * 70)
    
    tasks = [
        {
            "id": "task_001",
            "description": "Research Python async/await patterns",
            "domain": "research",
            "complexity": 0.7,
            "keywords": ["python", "async", "patterns"],
            "input_type": "text",
            "output_type": "report",
            "estimated_duration": 2.0
        },
        {
            "id": "task_002",
            "description": "Research Python concurrency models",
            "domain": "research",
            "complexity": 0.65,
            "keywords": ["python", "concurrency", "threading"],
            "input_type": "text",
            "output_type": "report",
            "estimated_duration": 2.5
        },
        {
            "id": "task_003",
            "description": "Write async programming tutorial",
            "domain": "writing",
            "complexity": 0.6,
            "keywords": ["tutorial", "async", "beginner"],
            "input_type": "text",
            "output_type": "tutorial",
            "estimated_duration": 3.0
        },
        {
            "id": "task_004",
            "description": "Deep dive into asyncio internals",
            "domain": "research",
            "complexity": 0.8,
            "keywords": ["python", "asyncio", "advanced"],
            "input_type": "text",
            "output_type": "analysis",
            "estimated_duration": 3.5
        }
    ]
    
    print(f"✓ Defined {len(tasks)} sample tasks:")
    for task in tasks:
        print(f"  - {task['id']}: {task['description']} ({task['domain']}, {task['complexity']:.1f})")
    
    # Step 3: Execute tasks through hybrid system
    print("\n\nStep 3: Executing Tasks Through Hybrid System")
    print("-" * 70)
    
    results = []
    
    for i, task in enumerate(tasks, 1):
        print(f"\n{'─' * 70}")
        print(f"Task {i}/{len(tasks)}: {task['description']}")
        print(f"{'─' * 70}")
        
        result = orchestrator.execute_task(task)
        results.append(result)
        
        print(f"\n✓ Execution Complete:")
        print(f"  Specialist: {result['specialist_id']}")
        print(f"  Approach: {result['approach']}")
        print(f"  Quality: {result['quality']:.1%}")
        print(f"  Success: {'Yes' if result['success'] else 'No'}")
        
        time.sleep(0.5)  # Brief pause for readability
    
    # Step 4: View system statistics
    print("\n\nStep 4: System Statistics")
    print("-" * 70)
    
    stats = orchestrator.get_system_stats()
    
    print("\nAdaptive Layer (Specialists):")
    print(f"  Total specialists created: {stats['adaptive_layer']['total_specialists']}")
    
    for specialist in stats['adaptive_layer']['specialists']:
        print(f"\n  Specialist: {specialist['id']}")
        print(f"    - Tasks executed: {specialist['executions']}")
        print(f"    - Average quality: {specialist['average_quality']:.1%}")
    
    print("\n\nStigmergic Layer (Signal Board):")
    print(f"  Total signals on board: {stats['stigmergic_layer']['total_signals']}")
    print(f"  Active task patterns: {stats['stigmergic_layer']['total_tasks']}")
    
    if stats['stigmergic_layer']['tasks']:
        print("\n  Signal Patterns:")
        for task_id, signals in stats['stigmergic_layer']['tasks'].items():
            print(f"\n    {task_id}:")
            for sig in signals[:3]:  # Top 3 signals
                print(f"      - {sig['approach']}: strength {sig['strength']:.2f}")
    
    # Step 5: Visualize coordination
    print("\n\nStep 5: Coordination Visualization")
    print("-" * 70)
    
    visualization = orchestrator.visualize_coordination()
    print("\n" + visualization)
    
    # Summary
    print_header("SUMMARY")
    
    avg_quality = sum(r['quality'] for r in results) / len(results)
    success_count = sum(1 for r in results if r['success'])
    
    print(f"Tasks Executed: {len(results)}")
    print(f"Success Rate: {success_count}/{len(results)} ({success_count/len(results):.1%})")
    print(f"Average Quality: {avg_quality:.1%}")
    print(f"Specialists Created: {stats['adaptive_layer']['total_specialists']}")
    print(f"Signals on Board: {stats['stigmergic_layer']['total_signals']}")
    
    print("\n" + "=" * 70)
    print("Key Observations:")
    print("=" * 70)
    print("1. Similar tasks (research on Python) matched to same specialist")
    print("2. Different domain (writing) triggered new specialist creation")
    print("3. Signals accumulated on board, guiding approach selection")
    print("4. Both layers learned and adapted from task outcomes")
    print("\nTry running this example multiple times to see learning over time!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
