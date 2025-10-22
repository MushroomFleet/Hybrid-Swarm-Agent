"""
Phase 2: Pattern Analysis - Integration Demo
Demonstrates the complete pattern discovery workflow
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.execution_history import ExecutionHistory
from src.content_analyzer import ContentAnalyzer
from src.pattern_analyzer import PatternAnalyzer, PatternCluster
from src.approach_patterns import (
    ExecutionRecord, TaskContext, ContentFeatures,
    ApproachPattern, PerformanceMetrics
)
from src.dynamic_approach_manager import DynamicApproachManager


def generate_synthetic_records(count: int = 50) -> list:
    """
    Generate synthetic execution records for testing
    Creates clusters of similar tasks for pattern discovery
    """
    records = []
    
    # Cluster 1: Tutorial-style content (20 records)
    print(f"Generating {count} synthetic records...")
    for i in range(20):
        record = ExecutionRecord(
            record_id=f"tutorial_{i}",
            timestamp=datetime.now() - timedelta(days=random.randint(1, 30)),
            task_context=TaskContext(
                prompt=f"Write a tutorial on {random.choice(['Python', 'JavaScript', 'SQL'])}",
                domain_weights={'writing': 0.8, 'coding': 0.6},
                complexity=random.uniform(0.4, 0.7),
                keywords=['tutorial', 'guide', 'learn', random.choice(['beginner', 'intermediate'])],
                output_type='tutorial',
                estimated_duration=2.0
            ),
            specialist_id="specialist_tutorial",
            approach_id="legacy_approach_b_tutorial",
            quality_target=0.8,
            actual_quality=random.uniform(0.80, 0.95),
            success=True,
            execution_time_ms=random.randint(1000, 3000),
            content_features=ContentFeatures(
                section_count=random.randint(4, 7),
                has_code_blocks=True,
                code_block_count=random.randint(2, 5),
                has_numbered_list=True,
                has_bullets=False,
                has_tables=False,
                total_length=random.randint(2000, 4000),
                avg_section_length=500,
                detected_tone="educational",
                formality_score=0.6,
                explanation_ratio=0.6,
                example_ratio=0.3,
                code_ratio=0.1
            )
        )
        records.append(record)
    
    # Cluster 2: Code explanation content (15 records)
    for i in range(15):
        record = ExecutionRecord(
            record_id=f"code_explain_{i}",
            timestamp=datetime.now() - timedelta(days=random.randint(1, 30)),
            task_context=TaskContext(
                prompt=f"Explain how {random.choice(['sorting', 'recursion', 'async'])} works",
                domain_weights={'coding': 0.9, 'writing': 0.5},
                complexity=random.uniform(0.5, 0.8),
                keywords=['explain', 'code', 'algorithm', 'implementation'],
                output_type='explanation',
                estimated_duration=1.5
            ),
            specialist_id="specialist_code",
            approach_id="legacy_approach_a_comprehensive",
            quality_target=0.8,
            actual_quality=random.uniform(0.82, 0.93),
            success=True,
            execution_time_ms=random.randint(800, 2000),
            content_features=ContentFeatures(
                section_count=random.randint(3, 5),
                has_code_blocks=True,
                code_block_count=random.randint(4, 8),
                has_numbered_list=False,
                has_bullets=True,
                has_tables=False,
                total_length=random.randint(1500, 3000),
                avg_section_length=600,
                detected_tone="technical",
                formality_score=0.8,
                explanation_ratio=0.5,
                example_ratio=0.2,
                code_ratio=0.3
            )
        )
        records.append(record)
    
    # Cluster 3: Comparison/analysis content (15 records)
    for i in range(15):
        record = ExecutionRecord(
            record_id=f"comparison_{i}",
            timestamp=datetime.now() - timedelta(days=random.randint(1, 30)),
            task_context=TaskContext(
                prompt=f"Compare {random.choice(['React vs Vue', 'SQL vs NoSQL', 'Python vs JavaScript'])}",
                domain_weights={'analysis': 0.8, 'writing': 0.7, 'coding': 0.4},
                complexity=random.uniform(0.6, 0.9),
                keywords=['compare', 'vs', 'difference', 'pros', 'cons'],
                output_type='comparison',
                estimated_duration=3.0
            ),
            specialist_id="specialist_analysis",
            approach_id="legacy_approach_a_comprehensive",
            quality_target=0.8,
            actual_quality=random.uniform(0.81, 0.92),
            success=True,
            execution_time_ms=random.randint(1500, 3500),
            content_features=ContentFeatures(
                section_count=random.randint(5, 8),
                has_code_blocks=False,
                code_block_count=0,
                has_numbered_list=False,
                has_bullets=True,
                has_tables=True,
                total_length=random.randint(3000, 5000),
                avg_section_length=700,
                detected_tone="neutral",
                formality_score=0.7,
                explanation_ratio=0.7,
                example_ratio=0.2,
                code_ratio=0.1
            )
        )
        records.append(record)
    
    print(f"✓ Generated {len(records)} synthetic records in 3 clusters")
    return records


def demo_execution_history():
    """Demo: Recording and querying execution history"""
    print("\n" + "=" * 70)
    print("DEMO 1: Execution History")
    print("=" * 70)
    
    history = ExecutionHistory("data/execution_history")
    
    # Generate and record synthetic data
    records = generate_synthetic_records(50)
    
    print("\nRecording executions to history...")
    for record in records:
        success = history.record_execution(record)
        if not success:
            print(f"  Failed to record: {record.record_id}")
    
    print("✓ All records saved to JSONL files")
    
    # Query history
    print("\nQuerying history:")
    
    # Get high-quality records
    high_quality = history.get_records(min_quality=0.85)
    print(f"  High quality (≥0.85): {len(high_quality)} records")
    
    # Get recent records
    recent = history.get_recent_records(days=7)
    print(f"  Recent (7 days): {len(recent)} records")
    
    # Get statistics
    stats = history.get_statistics()
    print(f"\nHistory Statistics:")
    print(f"  Total records: {stats['total_records']}")
    print(f"  Total files: {stats['total_files']}")
    print(f"  Storage size: {stats['total_size_bytes']} bytes")
    
    return history


def demo_content_analysis():
    """Demo: Content feature extraction"""
    print("\n" + "=" * 70)
    print("DEMO 2: Content Analysis")
    print("=" * 70)
    
    analyzer = ContentAnalyzer()
    
    # Sample content
    sample = """
# Python List Comprehensions Tutorial

## Introduction

List comprehensions provide a concise way to create lists. Let's learn how!

## Basic Syntax

1. Start with square brackets
2. Add an expression
3. Include a for clause
4. Optionally add conditions

### Example

```python
# Create squares of numbers 1-10
squares = [x**2 for x in range(1, 11)]
print(squares)
```

## Key Benefits

- More readable than loops
- Faster execution
- Pythonic style

## Summary

You now understand list comprehensions! Try them in your code.
"""
    
    print("\nAnalyzing sample content...")
    features = analyzer.analyze_content(sample)
    
    print(f"\nExtracted Features:")
    print(f"  Sections: {features.section_count}")
    print(f"  Code blocks: {features.code_block_count}")
    print(f"  Numbered list: {features.has_numbered_list}")
    print(f"  Bullets: {features.has_bullets}")
    print(f"  Detected tone: {features.detected_tone}")
    print(f"  Formality: {features.formality_score:.2f}")
    print(f"  Code ratio: {features.code_ratio:.2f}")
    print(f"  Explanation ratio: {features.explanation_ratio:.2f}")
    
    structure = analyzer.analyze_structure_type(sample)
    print(f"  Structure type: {structure}")
    
    print("\n✓ Content analysis complete")


def demo_pattern_discovery(history: ExecutionHistory):
    """Demo: Pattern discovery and signature extraction"""
    print("\n" + "=" * 70)
    print("DEMO 3: Pattern Discovery")
    print("=" * 70)
    
    analyzer = PatternAnalyzer(history=history)
    
    print("\nDiscovering patterns in execution history...")
    clusters = analyzer.discover_patterns(
        min_cluster_size=10,
        min_quality=0.8,
        similarity_threshold=0.65
    )
    
    if not clusters:
        print("No patterns discovered (need more data)")
        return []
    
    print(f"\n✓ Discovered {len(clusters)} patterns")
    
    # Analyze each cluster
    for i, cluster in enumerate(clusters, 1):
        print(f"\n--- Pattern {i} ---")
        print(f"Records: {len(cluster.records)}")
        print(f"Avg Quality: {cluster.avg_quality:.2f}")
        print(f"Consistent: {cluster.is_consistent}")
        
        # Extract signature
        signature = analyzer.extract_pattern_signature(cluster)
        print(f"\nPattern Signature:")
        print(f"  Domains: {signature.domain_weights}")
        print(f"  Complexity: {signature.complexity_min:.2f} - {signature.complexity_max:.2f}")
        print(f"  Keywords: {signature.keyword_patterns[:5]}")
        print(f"  Output types: {signature.output_types}")
        print(f"  Requires code: {signature.requires_code}")
        
        # Extract style
        style = analyzer.extract_style_characteristics(cluster)
        print(f"\nStyle Characteristics:")
        print(f"  Structure: {style.structure_type}")
        print(f"  Sections: {style.section_count}")
        print(f"  Tone: {style.tone}")
        print(f"  Depth: {style.depth_level}")
        print(f"  Example density: {style.example_density}")
    
    return clusters


def demo_novelty_check(clusters: list):
    """Demo: Check if patterns are novel"""
    print("\n" + "=" * 70)
    print("DEMO 4: Novelty Checking")
    print("=" * 70)
    
    if not clusters:
        print("No clusters to check (need pattern discovery first)")
        return
    
    # Load existing approaches
    manager = DynamicApproachManager("data/approaches")
    existing_approaches = manager.list_approaches()
    
    print(f"\nChecking {len(clusters)} clusters against {len(existing_approaches)} existing approaches...")
    
    analyzer = PatternAnalyzer()
    
    novel_clusters = []
    for i, cluster in enumerate(clusters, 1):
        is_novel = analyzer.check_novelty(cluster, existing_approaches, threshold=0.85)
        print(f"  Cluster {i}: {'NOVEL ✓' if is_novel else 'Similar to existing'}")
        
        if is_novel:
            novel_clusters.append(cluster)
    
    print(f"\n✓ Found {len(novel_clusters)} novel patterns")
    
    if novel_clusters:
        print("\nThese patterns could be used to create new approaches!")


def main():
    """Run complete Phase 2 demo"""
    print("\n" + "=" * 70)
    print("PHASE 2: Pattern Analysis - Integration Demo")
    print("=" * 70)
    print("\nThis demo shows the complete pattern discovery workflow:")
    print("1. Recording execution history")
    print("2. Analyzing content features")
    print("3. Discovering patterns through clustering")
    print("4. Checking for novel patterns")
    
    try:
        # Demo 1: Execution history
        history = demo_execution_history()
        
        # Demo 2: Content analysis
        demo_content_analysis()
        
        # Demo 3: Pattern discovery
        clusters = demo_pattern_discovery(history)
        
        # Demo 4: Novelty checking
        demo_novelty_check(clusters)
        
        print("\n" + "=" * 70)
        print("✓ PHASE 2 DEMO COMPLETE")
        print("=" * 70)
        print("\nAll Phase 2 components are working correctly:")
        print("  ✓ ExecutionHistory - Recording and querying")
        print("  ✓ ContentAnalyzer - Feature extraction")
        print("  ✓ PatternAnalyzer - Pattern discovery")
        print("  ✓ Signature/Style extraction")
        print("  ✓ Novelty checking")
        print("\nNext steps:")
        print("  - Phase 3: Approach Evolution (creating approaches from patterns)")
        print("  - Phase 4: Integration with HybridSwarmOrchestrator")
        print("  - Phase 5: Production deployment")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
