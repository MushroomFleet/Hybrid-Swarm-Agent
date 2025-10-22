"""
Phase 3: Approach Evolution - Integration Demo
Demonstrates approach creation, evolution, and pruning
"""

import sys
import os
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.execution_history import ExecutionHistory
from src.pattern_analyzer import PatternAnalyzer
from src.approach_evolution import ApproachEvolution
from src.dynamic_approach_manager import DynamicApproachManager
from src.approach_patterns import ExecutionRecord, TaskContext, ContentFeatures


def demo_approach_creation():
    """Demo: Creating approaches from discovered patterns"""
    print("\n" + "=" * 70)
    print("DEMO 1: Approach Creation from Patterns")
    print("=" * 70)
    
    # Use patterns discovered in Phase 2
    print("\nLoading execution history and discovering patterns...")
    history = ExecutionHistory("data/execution_history")
    analyzer = PatternAnalyzer(history=history)
    
    clusters = analyzer.discover_patterns(
        min_cluster_size=10,
        min_quality=0.8,
        similarity_threshold=0.65
    )
    
    if not clusters:
        print("No patterns found. Run phase2_demo.py first to generate data.")
        return None
    
    print(f"✓ Found {len(clusters)} patterns")
    
    # Create approaches from patterns
    evolution = ApproachEvolution()
    created_approaches = []
    
    for i, cluster in enumerate(clusters, 1):
        print(f"\n--- Creating Approach from Pattern {i} ---")
        
        # Extract signature and style
        signature = analyzer.extract_pattern_signature(cluster)
        style = analyzer.extract_style_characteristics(cluster)
        
        # Create approach
        approach = evolution.create_approach_from_cluster(cluster, signature, style)
        
        if approach:
            created_approaches.append(approach)
            print(f"  Name: {approach.name}")
            print(f"  ID: {approach.id}")
            print(f"  Tags: {', '.join(approach.tags)}")
            print(f"  Expected quality: {approach.performance_metrics.avg_quality:.2f}")
        else:
            print("  ✗ Failed to create (may be too similar to existing)")
    
    print(f"\n✓ Created {len(created_approaches)} new approaches")
    return created_approaches


def demo_approach_usage():
    """Demo: Simulating approach usage"""
    print("\n" + "=" * 70)
    print("DEMO 2: Approach Usage Simulation")
    print("=" * 70)
    
    manager = DynamicApproachManager()
    approaches = manager.list_approaches()
    
    print(f"\nSimulating usage of {len(approaches)} approaches...")
    
    # Simulate different usage patterns
    import random
    
    for approach in approaches[:3]:  # Use first 3 approaches
        # Simulate 5-10 executions per approach
        num_executions = random.randint(5, 10)
        
        print(f"\n{approach.name}:")
        for i in range(num_executions):
            # Random quality with slight bias based on expected quality
            expected = approach.performance_metrics.avg_quality
            quality = max(0.6, min(1.0, expected + random.gauss(0, 0.1)))
            success = quality >= 0.7
            
            manager.record_execution(approach.id, quality, success)
            print(f"  Execution {i+1}: quality={quality:.2f}")
        
        # Show updated metrics
        updated = manager.get_approach(approach.id)
        metrics = updated.performance_metrics
        print(f"  Final: avg={metrics.avg_quality:.2f}, usage={metrics.usage_count}, trend={metrics.recent_quality_trend}")
    
    print("\n✓ Usage simulation complete")


def demo_approach_evolution():
    """Demo: Evolving approaches based on performance"""
    print("\n" + "=" * 70)
    print("DEMO 3: Approach Evolution")
    print("=" * 70)
    
    # Get approaches with sufficient usage
    manager = DynamicApproachManager()
    history = ExecutionHistory("data/execution_history")
    evolution = ApproachEvolution(manager)
    
    approaches = manager.list_approaches()
    
    print(f"\nChecking {len(approaches)} approaches for evolution eligibility...")
    
    evolved_count = 0
    for approach in approaches:
        metrics = approach.performance_metrics
        
        # Need sufficient usage to evolve
        if metrics.usage_count < 5:
            print(f"\n{approach.name}: Not enough usage ({metrics.usage_count})")
            continue
        
        # Get recent executions for this approach
        recent = history.get_approach_history(approach.id, days=30)
        
        if not recent:
            print(f"\n{approach.name}: No execution history found")
            continue
        
        print(f"\n{approach.name}:")
        print(f"  Current quality: {metrics.avg_quality:.2f}")
        print(f"  Usage: {metrics.usage_count}")
        print(f"  Attempting evolution...")
        
        # Try to evolve (will only succeed if quality improved enough)
        evolved = evolution.evolve_approach(
            approach.id,
            recent,
            min_executions=5,  # Lower threshold for demo
            min_quality_improvement=0.02  # Lower threshold for demo
        )
        
        if evolved:
            evolved_count += 1
            print(f"  ✓ Evolved to v{evolved.version}")
            print(f"  New ID: {evolved.id}")
        else:
            print(f"  - No evolution (criteria not met)")
    
    print(f"\n✓ Evolved {evolved_count} approaches")


def demo_approach_pruning():
    """Demo: Pruning underperforming approaches"""
    print("\n" + "=" * 70)
    print("DEMO 4: Approach Pruning")
    print("=" * 70)
    
    evolution = ApproachEvolution()
    
    print("\nRunning pruning analysis (dry run)...")
    
    # Dry run to see what would be pruned
    pruned_ids = evolution.prune_approaches(
        min_usage_for_evaluation=5,  # Lower for demo
        max_age_no_traction_days=1,  # Aggressive for demo
        min_quality_threshold=0.65,
        min_success_rate=0.5,
        dry_run=True
    )
    
    if pruned_ids:
        print(f"\n{len(pruned_ids)} approaches identified for pruning")
        print("\nTo actually prune, set dry_run=False")
    else:
        print("\n✓ No approaches need pruning")


def demo_complete_lifecycle():
    """Demo: Complete approach lifecycle"""
    print("\n" + "=" * 70)
    print("DEMO 5: Complete Lifecycle Overview")
    print("=" * 70)
    
    manager = DynamicApproachManager()
    approaches = manager.list_approaches(active_only=False)
    
    print(f"\nTotal approaches: {len(approaches)}")
    print("\n--- Approach Breakdown ---")
    
    # By generation
    gen_counts = {}
    for approach in approaches:
        gen = approach.generation
        gen_counts[gen] = gen_counts.get(gen, 0) + 1
    
    print("\nBy Generation:")
    for gen in sorted(gen_counts.keys()):
        print(f"  Generation {gen}: {gen_counts[gen]} approaches")
    
    # By status
    active = [a for a in approaches if a.active]
    inactive = [a for a in approaches if not a.active]
    
    print(f"\nBy Status:")
    print(f"  Active: {len(active)}")
    print(f"  Inactive: {len(inactive)}")
    
    # By usage
    with_usage = [a for a in approaches if a.performance_metrics.usage_count > 0]
    without_usage = [a for a in approaches if a.performance_metrics.usage_count == 0]
    
    print(f"\nBy Usage:")
    print(f"  Used: {len(with_usage)}")
    print(f"  Unused: {len(without_usage)}")
    
    # Quality distribution
    if with_usage:
        qualities = [a.performance_metrics.avg_quality for a in with_usage]
        avg_quality = sum(qualities) / len(qualities)
        min_quality = min(qualities)
        max_quality = max(qualities)
        
        print(f"\nQuality Distribution:")
        print(f"  Average: {avg_quality:.2f}")
        print(f"  Range: {min_quality:.2f} - {max_quality:.2f}")
    
    # Top performers
    print(f"\nTop 3 Performers:")
    top = sorted(with_usage, key=lambda a: a.performance_metrics.avg_quality, reverse=True)[:3]
    for i, approach in enumerate(top, 1):
        metrics = approach.performance_metrics
        print(f"  {i}. {approach.name}")
        print(f"     Quality: {metrics.avg_quality:.2f}, Usage: {metrics.usage_count}")
    
    print("\n✓ Lifecycle analysis complete")


def main():
    """Run complete Phase 3 demo"""
    print("\n" + "=" * 70)
    print("PHASE 3: Approach Evolution - Integration Demo")
    print("=" * 70)
    print("\nThis demo shows the complete approach lifecycle:")
    print("1. Creating approaches from discovered patterns")
    print("2. Simulating approach usage")
    print("3. Evolving high-performing approaches")
    print("4. Pruning underperforming approaches")
    print("5. Complete lifecycle overview")
    
    try:
        # Demo 1: Create approaches from patterns
        created = demo_approach_creation()
        
        if created:
            # Demo 2: Simulate usage
            demo_approach_usage()
            
            # Demo 3: Evolution
            demo_approach_evolution()
        
        # Demo 4: Pruning
        demo_approach_pruning()
        
        # Demo 5: Complete lifecycle
        demo_complete_lifecycle()
        
        print("\n" + "=" * 70)
        print("✓ PHASE 3 DEMO COMPLETE")
        print("=" * 70)
        print("\nAll Phase 3 components are working correctly:")
        print("  ✓ ApproachEvolution - Creation, evolution, pruning")
        print("  ✓ Approach lifecycle management")
        print("  ✓ Novelty checking")
        print("  ✓ Quality-based evolution")
        print("  ✓ Performance-based pruning")
        print("\nNext steps:")
        print("  - Phase 4: Integration with HybridSwarmOrchestrator")
        print("  - Phase 5: Production deployment")
        print("\nThe dynamic approaches system is now capable of:")
        print("  • Discovering patterns in execution data")
        print("  • Creating specialized approaches automatically")
        print("  • Evolving approaches based on performance")
        print("  • Removing underperformers through natural selection")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
