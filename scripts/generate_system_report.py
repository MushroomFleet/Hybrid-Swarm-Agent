#!/usr/bin/env python3
"""
System Monitoring Report Generator
Generates comprehensive system status and metrics report
"""

import sys
import os
from pathlib import Path
from datetime import datetime
from collections import Counter

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.dynamic_approach_manager import DynamicApproachManager
from src.execution_history import ExecutionHistory
from src.hybrid_swarm import HybridSwarmOrchestrator


def generate_report():
    """Generate comprehensive system report"""
    
    print("=" * 70)
    print("DYNAMIC APPROACHES SYSTEM - STATUS REPORT")
    print("=" * 70)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Initialize components
    manager = DynamicApproachManager()
    history = ExecutionHistory()
    orchestrator = HybridSwarmOrchestrator()
    
    # 1. System Overview
    print("1. SYSTEM OVERVIEW")
    print("-" * 70)
    
    approaches = manager.list_approaches(active_only=False)
    active_approaches = [a for a in approaches if a.active]
    used_approaches = [a for a in approaches if a.performance_metrics.usage_count > 0]
    
    print(f"Total Approaches: {len(approaches)}")
    print(f"  Active: {len(active_approaches)}")
    print(f"  Inactive: {len(approaches) - len(active_approaches)}")
    print(f"  Used: {len(used_approaches)}")
    print(f"  Unused: {len(approaches) - len(used_approaches)}")
    print()
    
    # 2. Execution Statistics
    print("2. EXECUTION STATISTICS")
    print("-" * 70)
    
    hist_stats = history.get_statistics()
    print(f"Total Executions: {hist_stats['total_records']}")
    print(f"Storage Files: {hist_stats['total_files']}")
    print(f"Storage Size: {hist_stats['total_size_bytes'] / 1024:.1f} KB")
    
    if hist_stats.get('oldest_record'):
        print(f"Date Range: {hist_stats['oldest_record']} to {hist_stats['newest_record']}")
    print()
    
    # 3. Quality Metrics
    print("3. QUALITY METRICS")
    print("-" * 70)
    
    if used_approaches:
        qualities = [a.performance_metrics.avg_quality for a in used_approaches]
        total_usage = sum(a.performance_metrics.usage_count for a in used_approaches)
        
        avg_quality = sum(qualities) / len(qualities)
        min_quality = min(qualities)
        max_quality = max(qualities)
        
        print(f"Average Quality: {avg_quality:.3f}")
        print(f"Quality Range: {min_quality:.3f} - {max_quality:.3f}")
        print(f"Total Usage Count: {total_usage}")
        
        # Quality distribution
        recent_records = history.get_recent_records(days=7)
        if recent_records:
            qualities_dist = [r.actual_quality for r in recent_records]
            excellent = sum(1 for q in qualities_dist if q >= 0.9)
            good = sum(1 for q in qualities_dist if 0.8 <= q < 0.9)
            adequate = sum(1 for q in qualities_dist if 0.7 <= q < 0.8)
            below = sum(1 for q in qualities_dist if q < 0.7)
            
            print(f"\nQuality Distribution (last 7 days, {len(recent_records)} executions):")
            print(f"  Excellent (≥0.9): {excellent} ({excellent/len(recent_records)*100:.1f}%)")
            print(f"  Good (0.8-0.9): {good} ({good/len(recent_records)*100:.1f}%)")
            print(f"  Adequate (0.7-0.8): {adequate} ({adequate/len(recent_records)*100:.1f}%)")
            print(f"  Below (<0.7): {below} ({below/len(recent_records)*100:.1f}%)")
    print()
    
    # 4. Approach Performance
    print("4. TOP PERFORMING APPROACHES")
    print("-" * 70)
    
    if used_approaches:
        top_approaches = sorted(
            used_approaches,
            key=lambda a: a.performance_metrics.avg_quality,
            reverse=True
        )[:5]
        
        for i, approach in enumerate(top_approaches, 1):
            metrics = approach.performance_metrics
            print(f"{i}. {approach.name}")
            print(f"   Quality: {metrics.avg_quality:.3f}, Usage: {metrics.usage_count}, Trend: {metrics.recent_quality_trend}")
    print()
    
    # 5. Approach Usage Distribution
    print("5. APPROACH USAGE DISTRIBUTION")
    print("-" * 70)
    
    recent_records = history.get_recent_records(days=7)
    if recent_records:
        usage_counts = Counter(r.approach_id for r in recent_records)
        total = len(recent_records)
        
        for approach_id, count in usage_counts.most_common():
            percentage = (count / total) * 100
            approach = manager.get_approach(approach_id)
            name = approach.name if approach else approach_id
            bar = "█" * int(percentage / 2)
            print(f"  {name[:40]:40s} {bar} {percentage:5.1f}% ({count})")
    print()
    
    # 6. Generation Breakdown
    print("6. APPROACH GENERATIONS")
    print("-" * 70)
    
    gen_counts = Counter(a.generation for a in approaches)
    for gen in sorted(gen_counts.keys()):
        print(f"  Generation {gen}: {gen_counts[gen]} approaches")
    print()
    
    # 7. Pattern Discovery Status
    print("7. PATTERN DISCOVERY STATUS")
    print("-" * 70)
    
    patterns_file = Path('data/patterns/discovered_patterns.json')
    if patterns_file.exists():
        import json
        with open(patterns_file) as f:
            patterns_data = json.load(f)
        
        print(f"Last Discovery: {patterns_data.get('discovered_at', 'Unknown')}")
        print(f"Patterns Found: {patterns_data.get('cluster_count', 0)}")
        
        clusters = patterns_data.get('clusters', [])
        for i, cluster in enumerate(clusters, 1):
            print(f"\n  Pattern {i}:")
            print(f"    Records: {cluster.get('record_count', 0)}")
            print(f"    Avg Quality: {cluster.get('avg_quality', 0):.3f}")
            print(f"    Novel: {cluster.get('is_novel', False)}")
    else:
        print("  No patterns discovered yet")
    print()
    
    # 8. System Health
    print("8. SYSTEM HEALTH")
    print("-" * 70)
    
    coord_stats = orchestrator.get_system_stats()
    print(f"Specialists: {coord_stats['adaptive_layer']['total_specialists']}")
    print(f"Stigmergic Signals: {coord_stats['stigmergic_layer']['total_signals']}")
    print(f"Specialist Agents: {coord_stats['hybrid_metrics']['specialist_agents']}")
    print()
    
    # 9. Recommendations
    print("9. RECOMMENDATIONS")
    print("-" * 70)
    
    recommendations = []
    
    # Check if pattern discovery should run
    if hist_stats['total_records'] >= 100 and hist_stats['total_records'] % 50 < 10:
        recommendations.append("Pattern discovery threshold reached - will run on next execution")
    
    # Check approach usage
    if used_approaches:
        max_usage = max(a.performance_metrics.usage_count for a in used_approaches)
        total_usage = sum(a.performance_metrics.usage_count for a in used_approaches)
        if max_usage / total_usage > 0.5:
            recommendations.append("Single approach dominance detected - consider diversification")
    
    # Check for unused approaches
    unused = [a for a in approaches if a.active and a.performance_metrics.usage_count == 0]
    if len(unused) > 3:
        recommendations.append(f"{len(unused)} approaches unused - review signatures or consider pruning")
    
    if recommendations:
        for rec in recommendations:
            print(f"  • {rec}")
    else:
        print("  ✓ No issues detected - system operating optimally")
    print()
    
    print("=" * 70)
    print("END OF REPORT")
    print("=" * 70)


if __name__ == "__main__":
    generate_report()
