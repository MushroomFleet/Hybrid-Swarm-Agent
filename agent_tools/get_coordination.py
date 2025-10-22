#!/usr/bin/env python3
"""
Agent Coordination Tool
Analyzes user prompt and returns coordination decision from hybrid swarm system
Returns JSON with specialist, approach, and task context for agent to use
"""

import sys
import os
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.hybrid_swarm import HybridSwarmOrchestrator

class PromptAnalyzer:
    """Analyzes user prompts to determine task characteristics"""
    
    DOMAIN_KEYWORDS = {
        'research': ['research', 'investigate', 'analyze', 'study', 'explore', 'what is', 'explain', 'tell me about'],
        'writing': ['write', 'create', 'draft', 'compose', 'tutorial', 'guide', 'how to', 'make a'],
        'review': ['review', 'check', 'evaluate', 'critique', 'assess', 'improve', 'feedback'],
        'coding': ['code', 'implement', 'build', 'develop', 'program', 'function', 'script', 'debug'],
        'comparison': ['compare', 'vs', 'versus', 'difference', 'better', 'which', 'between'],
        'analysis': ['analyze', 'analysis', 'examine', 'dissect', 'breakdown']
    }
    
    def analyze(self, prompt: str) -> dict:
        """Analyze prompt and return task characteristics with domain weights"""
        import re
        prompt_lower = prompt.lower()
        
        # Calculate domain weights (multi-label classification)
        domain_weights = {}
        for dom, keywords in self.DOMAIN_KEYWORDS.items():
            # Count matching keywords
            matches = sum(1 for kw in keywords if kw in prompt_lower)
            if matches > 0:
                # Normalize by keyword count
                domain_weights[dom] = min(1.0, matches / 3.0)
        
        # If no domains detected, use general
        if not domain_weights:
            domain_weights = {'general': 1.0}
        
        # For backward compatibility, also provide primary domain
        primary_domain = max(domain_weights.items(), key=lambda x: x[1])[0]
        
        # Estimate complexity
        word_count = len(prompt.split())
        has_multiple_questions = prompt.count('?') > 1 or ' and ' in prompt_lower
        
        if word_count > 50 or has_multiple_questions:
            complexity = 0.8
        elif word_count > 20:
            complexity = 0.6
        else:
            complexity = 0.4
        
        # Extract keywords (words longer than 4 chars, excluding common words)
        words = re.findall(r'\b\w+\b', prompt_lower)
        stopwords = {'what', 'when', 'where', 'which', 'would', 'should', 'could', 'about', 'that', 'this', 'with', 'from', 'they', 'have', 'been'}
        keywords = [w for w in words if len(w) > 4 and w not in stopwords][:5]
        
        # Determine output type
        if 'tutorial' in prompt_lower or 'guide' in prompt_lower or 'how to' in prompt_lower:
            output_type = 'tutorial'
        elif 'code' in prompt_lower or 'example' in prompt_lower or 'implement' in prompt_lower:
            output_type = 'code'
        elif 'list' in prompt_lower or 'comparison' in prompt_lower or 'compare' in prompt_lower:
            output_type = 'list'
        else:
            output_type = 'explanation'
        
        return {
            'domain': primary_domain,  # For backward compatibility
            'domain_weights': domain_weights,  # For dynamic approaches
            'complexity': complexity,
            'keywords': keywords,
            'output_type': output_type,
            'estimated_duration': complexity * 3.0
        }


def get_coordination(prompt: str, task_id: str = None) -> dict:
    """
    Get coordination decision from hybrid swarm system
    
    Args:
        prompt: User's question/prompt
        task_id: Optional task identifier (auto-generated if not provided)
    
    Returns:
        dict with coordination decision and task context
    """
    # Create orchestrator
    orchestrator = HybridSwarmOrchestrator(
        vigilance_threshold=0.75,
        decay_rate=1800.0
    )
    
    # Analyze prompt
    analyzer = PromptAnalyzer()
    analysis = analyzer.analyze(prompt)
    
    # Generate task ID if not provided
    if task_id is None:
        import time
        task_id = f"task_{int(time.time())}"
    
    # Create task structure
    task = {
        'id': task_id,
        'description': prompt[:100] + "..." if len(prompt) > 100 else prompt,
        **analysis
    }
    
    # Get coordination decision (NO execution - pure coordination)
    coordination = orchestrator.get_coordination(task)
    
    # Return coordination decision with context
    result = {
        'task_id': coordination['task_id'],
        'specialist_id': coordination['specialist_id'],
        'approach_id': coordination['approach_id'],
        'quality_target': coordination['quality_target'],
        'task_context': {
            'domain': analysis['domain'],
            'domain_weights': analysis['domain_weights'],
            'complexity': analysis['complexity'],
            'keywords': analysis['keywords'],
            'output_type': analysis['output_type']
        },
        'prompt': prompt
    }
    
    # Include approach metadata if available (from dynamic approaches)
    if 'approach_metadata' in coordination:
        result['approach_metadata'] = coordination['approach_metadata']
    
    return result


def main():
    """CLI entry point"""
    if len(sys.argv) < 2 or '--help' in sys.argv or '-h' in sys.argv:
        print("""
Agent Coordination Tool
Usage: python get_coordination.py "<prompt>" [task_id]

Returns JSON with coordination decision from hybrid swarm system.

Arguments:
  prompt     User's question or prompt (required)
  task_id    Optional task identifier (auto-generated if not provided)

Example:
  python get_coordination.py "How do I use Python async/await?"
  python get_coordination.py "Write a tutorial on asyncio" "my_task_001"

Output:
  JSON with specialist_id, approach, quality_target, and task_context
        """)
        sys.exit(0 if '--help' in sys.argv or '-h' in sys.argv else 1)
    
    # Get prompt from arguments
    prompt = sys.argv[1]
    task_id = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        # Get coordination decision
        result = get_coordination(prompt, task_id)
        
        # Output as JSON
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(json.dumps({
            'error': str(e),
            'type': type(e).__name__
        }, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
