"""
Convert Legacy Approaches A/B/C to Dynamic Format
Migrates hardcoded approaches to dynamic approach patterns
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.approach_patterns import ApproachPattern, PatternSignature, StyleCharacteristics, PerformanceMetrics
from src.dynamic_approach_manager import DynamicApproachManager


def create_legacy_approach_A() -> ApproachPattern:
    """
    Convert approach_A (Comprehensive Research) to dynamic format
    
    Original characteristics:
    - Multi-source research template with citations
    - Structured guide with introduction, body, examples
    - Formal, comprehensive approach
    """
    return ApproachPattern(
        id="legacy_approach_A_comprehensive",
        name="Comprehensive Research (Legacy A)",
        version=1,
        created_at=datetime.now(),
        last_updated=datetime.now(),
        
        pattern_signature=PatternSignature(
            domain_weights={
                'research': 0.9,
                'writing': 0.6,
                'comparison': 0.7,
                'review': 0.5
            },
            complexity_min=0.5,
            complexity_max=1.0,
            keyword_patterns=['research', 'investigate', 'analyze', 'study', 'explore', 'comprehensive'],
            keyword_weights={
                'research': 0.9,
                'investigate': 0.8,
                'analyze': 0.8,
                'study': 0.7,
                'explore': 0.7,
                'comprehensive': 0.8
            },
            output_types=['explanation', 'analysis', 'research', 'comparison'],
            requires_code=False,
            requires_examples=True,
            requires_theory=True
        ),
        
        style_characteristics=StyleCharacteristics(
            structure_type="hierarchical",
            section_count=(4, 8),
            tone="formal",
            voice="third_person",
            depth_level="comprehensive",
            explanation_style="conceptual",
            example_density="medium",
            code_style=None,
            use_headers=True,
            use_bullets=True,
            use_numbered_lists=False,
            use_tables=True,
            include_summary=True,
            include_tldr=False,
            include_prerequisites=False,
            include_next_steps=True
        ),
        
        performance_metrics=PerformanceMetrics(
            usage_count=0,
            first_used=datetime.now(),
            last_used=datetime.now(),
            avg_quality=0.0,
            min_quality=0.0,
            max_quality=0.0,
            quality_std_dev=0.0,
            success_count=0,
            failure_count=0,
            success_rate=0.0,
            vs_alternatives={},
            recent_quality_trend="new",
            quality_history=[]
        ),
        
        parent_id=None,
        generation=0,
        tags=["legacy", "research", "comprehensive", "formal", "analysis"],
        active=True
    )


def create_legacy_approach_B() -> ApproachPattern:
    """
    Convert approach_B (Step-by-Step Tutorial) to dynamic format
    
    Original characteristics:
    - Step-by-step tutorial format
    - Practical examples with code
    - Educational, hands-on approach
    """
    return ApproachPattern(
        id="legacy_approach_B_tutorial",
        name="Step-by-Step Tutorial (Legacy B)",
        version=1,
        created_at=datetime.now(),
        last_updated=datetime.now(),
        
        pattern_signature=PatternSignature(
            domain_weights={
                'writing': 0.9,
                'coding': 0.7,
                'research': 0.3
            },
            complexity_min=0.3,
            complexity_max=0.8,
            keyword_patterns=['tutorial', 'guide', 'how to', 'step', 'learn'],
            keyword_weights={
                'tutorial': 0.9,
                'guide': 0.8,
                'how to': 0.9,
                'step': 0.8,
                'learn': 0.7
            },
            output_types=['tutorial', 'guide', 'walkthrough', 'explanation'],
            requires_code=True,
            requires_examples=True,
            requires_theory=False
        ),
        
        style_characteristics=StyleCharacteristics(
            structure_type="sequential_steps",
            section_count=(3, 7),
            tone="educational",
            voice="second_person",
            depth_level="moderate",
            explanation_style="practical",
            example_density="high",
            code_style="annotated",
            use_headers=True,
            use_bullets=False,
            use_numbered_lists=True,
            use_tables=False,
            include_summary=True,
            include_tldr=False,
            include_prerequisites=True,
            include_next_steps=True
        ),
        
        performance_metrics=PerformanceMetrics(
            usage_count=0,
            first_used=datetime.now(),
            last_used=datetime.now(),
            avg_quality=0.0,
            min_quality=0.0,
            max_quality=0.0,
            quality_std_dev=0.0,
            success_count=0,
            failure_count=0,
            success_rate=0.0,
            vs_alternatives={},
            recent_quality_trend="new",
            quality_history=[]
        ),
        
        parent_id=None,
        generation=0,
        tags=["legacy", "tutorial", "step-by-step", "educational", "practical"],
        active=True
    )


def create_legacy_approach_C() -> ApproachPattern:
    """
    Convert approach_C (Summary & Key Points) to dynamic format
    
    Original characteristics:
    - Summary with detailed analysis
    - Bullet points and concise format
    - Quick reference style
    """
    return ApproachPattern(
        id="legacy_approach_C_summary",
        name="Summary & Key Points (Legacy C)",
        version=1,
        created_at=datetime.now(),
        last_updated=datetime.now(),
        
        pattern_signature=PatternSignature(
            domain_weights={
                'writing': 0.7,
                'research': 0.6,
                'review': 0.8,
                'comparison': 0.6
            },
            complexity_min=0.2,
            complexity_max=0.6,
            keyword_patterns=['summary', 'list', 'quick', 'overview', 'key points'],
            keyword_weights={
                'summary': 0.9,
                'list': 0.7,
                'quick': 0.8,
                'overview': 0.8,
                'key points': 0.9
            },
            output_types=['list', 'summary', 'overview', 'explanation'],
            requires_code=False,
            requires_examples=True,
            requires_theory=False
        ),
        
        style_characteristics=StyleCharacteristics(
            structure_type="bulleted",
            section_count=(2, 5),
            tone="casual",
            voice="second_person",
            depth_level="concise",
            explanation_style="practical",
            example_density="low",
            code_style="minimal",
            use_headers=True,
            use_bullets=True,
            use_numbered_lists=False,
            use_tables=True,
            include_summary=True,
            include_tldr=True,
            include_prerequisites=False,
            include_next_steps=False
        ),
        
        performance_metrics=PerformanceMetrics(
            usage_count=0,
            first_used=datetime.now(),
            last_used=datetime.now(),
            avg_quality=0.0,
            min_quality=0.0,
            max_quality=0.0,
            quality_std_dev=0.0,
            success_count=0,
            failure_count=0,
            success_rate=0.0,
            vs_alternatives={},
            recent_quality_trend="new",
            quality_history=[]
        ),
        
        parent_id=None,
        generation=0,
        tags=["legacy", "summary", "concise", "quick-reference", "bullets"],
        active=True
    )


def main():
    """Convert legacy approaches A/B/C to dynamic format"""
    print("=" * 70)
    print("Converting Legacy Approaches A/B/C to Dynamic Format")
    print("=" * 70)
    
    # Create manager
    manager = DynamicApproachManager()
    
    # Create legacy approaches in dynamic format
    print("\nCreating dynamic versions of legacy approaches...")
    
    approaches = [
        ("A", create_legacy_approach_A()),
        ("B", create_legacy_approach_B()),
        ("C", create_legacy_approach_C())
    ]
    
    created = []
    for legacy_id, approach in approaches:
        print(f"\n{legacy_id}. Converting approach_{legacy_id}:")
        print(f"   ID: {approach.id}")
        print(f"   Name: {approach.name}")
        print(f"   Domains: {list(approach.pattern_signature.domain_weights.keys())}")
        print(f"   Structure: {approach.style_characteristics.structure_type}")
        
        try:
            success = manager.create_approach(approach)
            if success:
                print(f"   ✓ Created successfully")
                created.append(approach.id)
            else:
                print(f"   ✗ Failed to create")
        except ValueError as e:
            # Already exists - update instead
            print(f"   ⚠ Already exists, updating...")
            success = manager.update_approach(approach)
            if success:
                print(f"   ✓ Updated successfully")
                created.append(approach.id)
            else:
                print(f"   ✗ Failed to update")
    
    # Validate conversions
    print("\n" + "=" * 70)
    print("Validating Conversions")
    print("=" * 70)
    
    validation_passed = True
    for approach_id in created:
        loaded = manager.get_approach(approach_id)
        if loaded and loaded.id == approach_id:
            print(f"✓ {approach_id}: Valid")
        else:
            print(f"✗ {approach_id}: FAILED")
            validation_passed = False
    
    # Test matching
    print("\n" + "=" * 70)
    print("Testing Approach Selection")
    print("=" * 70)
    
    from src.approach_patterns import TaskContext
    
    test_tasks = [
        ("Tutorial task", TaskContext(
            prompt="Write a tutorial on Python",
            domain_weights={'writing': 0.8, 'coding': 0.5},
            complexity=0.6,
            keywords=['tutorial', 'python'],
            output_type='tutorial',
            estimated_duration=2.0
        )),
        ("Research task", TaskContext(
            prompt="Research quantum computing",
            domain_weights={'research': 0.9},
            complexity=0.8,
            keywords=['research', 'quantum'],
            output_type='research',
            estimated_duration=5.0
        )),
        ("Summary task", TaskContext(
            prompt="Quick summary of async patterns",
            domain_weights={'writing': 0.6},
            complexity=0.4,
            keywords=['summary', 'quick'],
            output_type='summary',
            estimated_duration=1.0
        ))
    ]
    
    for task_name, task in test_tasks:
        print(f"\n{task_name}:")
        matches = manager.match_approaches(task, threshold=0.3, limit=3)
        for approach, score in matches:
            print(f"   {approach.name}: {score:.2f}")
    
    # Summary
    print("\n" + "=" * 70)
    print("Conversion Summary")
    print("=" * 70)
    
    stats = manager.get_statistics()
    print(f"\nTotal approaches: {stats['total_approaches']}")
    print(f"Active approaches: {stats['active_approaches']}")
    print(f"Legacy approaches converted: {len(created)}")
    
    if validation_passed:
        print("\n✅ All conversions successful!")
        print("\nLegacy approaches now available in dynamic format:")
        for approach_id in created:
            approach = manager.get_approach(approach_id)
            print(f"  - {approach.name} ({approach_id})")
        
        print("\n✅ Migration complete! Ready for Phase 2.")
    else:
        print("\n✗ Some conversions failed. Please review errors above.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
