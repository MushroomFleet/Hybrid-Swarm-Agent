#!/usr/bin/env python3
"""
Result Reporting Tool
Reports actual execution results back to hybrid swarm coordination system
Enables learning from real LLM execution
"""

import sys
import os
import json
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.hybrid_swarm import HybridSwarmOrchestrator


def report_result(
    task_id: str,
    specialist_id: str,
    quality: float,
    approach_id: str = None,
    success: bool = True,
    task_context: dict = None,
    content: str = None
) -> dict:
    """
    Report execution result back to coordination system
    
    Args:
        task_id: Task identifier from coordination
        specialist_id: Specialist that handled the task
        quality: Actual quality score (0.0-1.0)
        approach_id: Approach that was used (required for dynamic approaches)
        success: Whether task was successful
        task_context: Optional task context dict from coordination
        content: Optional generated content for analysis
    
    Returns:
        dict with update confirmation
    """
    # Create orchestrator (will load existing state)
    orchestrator = HybridSwarmOrchestrator(
        vigilance_threshold=0.75,
        decay_rate=1800.0
    )
    
    # If approach not provided, default to legacy
    if approach_id is None:
        approach_id = 'legacy_approach_b_tutorial'
    
    # Analyze content if provided
    content_features = None
    if content and orchestrator.use_dynamic_approaches:
        from src.content_analyzer import ContentAnalyzer
        analyzer = ContentAnalyzer()
        content_features = analyzer.analyze_content(content)
    
    # Update coordination system with results
    orchestrator.record_execution_result(
        specialist_id=specialist_id,
        approach_id=approach_id,
        task_id=task_id,
        actual_quality=quality,
        success=success,
        task_context=task_context,
        content_features=content_features
    )
    
    return {
        'task_id': task_id,
        'specialist_id': specialist_id,
        'approach_id': approach_id,
        'quality': quality,
        'success': success,
        'content_analyzed': content_features is not None,
        'status': 'Coordination system updated with actual execution results'
    }


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Report execution results to hybrid swarm coordination system',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python report_result.py --task-id task_001 --specialist specialist_abc --quality 0.90
  python report_result.py --task-id task_002 --specialist specialist_xyz --quality 0.75 --no-success
  
Quality Scale:
  0.9-1.0 = Excellent (comprehensive, accurate, well-structured)
  0.8-0.9 = Good (solid answer, meets requirements)
  0.7-0.8 = Adequate (acceptable but room for improvement)
  0.5-0.7 = Below expectations (incomplete or issues)
  0.0-0.5 = Poor (significant problems)
        """
    )
    
    parser.add_argument(
        '--task-id',
        required=True,
        help='Task identifier from coordination'
    )
    
    parser.add_argument(
        '--specialist',
        required=True,
        help='Specialist ID that handled the task'
    )
    
    parser.add_argument(
        '--quality',
        type=float,
        required=True,
        help='Actual quality score (0.0-1.0)'
    )
    
    parser.add_argument(
        '--success',
        action='store_true',
        default=True,
        help='Task was successful (default: true)'
    )
    
    parser.add_argument(
        '--no-success',
        dest='success',
        action='store_false',
        help='Task was not successful'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output result as JSON'
    )
    
    args = parser.parse_args()
    
    # Validate quality score
    if not 0.0 <= args.quality <= 1.0:
        print("Error: Quality score must be between 0.0 and 1.0", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Report result to coordination system
        result = report_result(
            task_id=args.task_id,
            specialist_id=args.specialist,
            quality=args.quality,
            success=args.success
        )
        
        if args.json:
            # Output as JSON
            print(json.dumps(result, indent=2))
        else:
            # Human-readable output
            print(f"✓ Coordination system updated")
            print(f"  Task: {result['task_id']}")
            print(f"  Specialist: {result['specialist_id']}")
            print(f"  Quality: {result['quality']:.1%}")
            print(f"  Success: {result['success']}")
            print(f"\n  {result['status']}")
        
    except Exception as e:
        error_msg = {
            'error': str(e),
            'type': type(e).__name__
        }
        
        if args.json:
            print(json.dumps(error_msg, indent=2), file=sys.stderr)
        else:
            print(f"Error: {e}", file=sys.stderr)
        
        sys.exit(1)


if __name__ == '__main__':
    main()
