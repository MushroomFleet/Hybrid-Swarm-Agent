#!/usr/bin/env python3
"""
Agent Helper Utilities
Convenience functions for hybrid-swarm agent workflow
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional


class CoordinationClient:
    """Client for interacting with hybrid swarm coordination system"""
    
    def __init__(self, tools_dir: Optional[Path] = None):
        """
        Initialize coordination client
        
        Args:
            tools_dir: Path to agent_tools directory (auto-detected if not provided)
        """
        if tools_dir is None:
            tools_dir = Path(__file__).parent
        self.tools_dir = Path(tools_dir)
    
    def get_coordination(self, prompt: str, task_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get coordination decision for a prompt
        
        Args:
            prompt: User's question/prompt
            task_id: Optional task identifier
        
        Returns:
            dict with coordination decision
        """
        cmd = ['python', str(self.tools_dir / 'get_coordination.py'), prompt]
        if task_id:
            cmd.append(task_id)
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        return json.loads(result.stdout)
    
    def report_result(
        self,
        task_id: str,
        specialist_id: str,
        quality: float,
        success: bool = True
    ) -> Dict[str, Any]:
        """
        Report execution result back to coordination system
        
        Args:
            task_id: Task identifier from coordination
            specialist_id: Specialist that handled the task
            quality: Actual quality score (0.0-1.0)
            success: Whether task was successful
        
        Returns:
            dict with update confirmation
        """
        cmd = [
            'python',
            str(self.tools_dir / 'report_result.py'),
            '--task-id', task_id,
            '--specialist', specialist_id,
            '--quality', str(quality),
            '--json'
        ]
        
        if not success:
            cmd.append('--no-success')
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        return json.loads(result.stdout)


class ApproachGuide:
    """Guidelines for different approach styles"""
    
    APPROACH_STYLES = {
        'approach_A': {
            'name': 'Comprehensive Research',
            'description': 'Authoritative, multi-source analysis',
            'characteristics': [
                'Research from multiple sources',
                'Detailed, thorough coverage',
                'Include citations and references',
                'Multiple perspectives considered',
                'Evidence-based conclusions'
            ],
            'best_for': ['complex topics', 'research questions', 'in-depth analysis'],
            'structure': 'Introduction → Detailed Analysis → Supporting Evidence → Conclusion'
        },
        'approach_B': {
            'name': 'Step-by-Step Tutorial',
            'description': 'Practical, hands-on learning path',
            'characteristics': [
                'Clear sequential steps',
                'Practical "how-to" focus',
                'Hands-on examples',
                'Build from simple to complex',
                'Actionable instructions'
            ],
            'best_for': ['tutorials', 'guides', 'learning new skills'],
            'structure': 'Overview → Step 1 → Step 2 → ... → Practice/Summary'
        },
        'approach_C': {
            'name': 'Summary & Key Points',
            'description': 'Concise, organized reference',
            'characteristics': [
                'Executive summary first',
                'Bullet-point key findings',
                'Concise examples',
                'Quick reference format',
                'Organized by theme/topic'
            ],
            'best_for': ['quick answers', 'reference material', 'comparisons'],
            'structure': 'Summary → Key Points → Examples → Recommendations'
        }
    }
    
    @classmethod
    def get_approach_guide(cls, approach: str) -> Dict[str, Any]:
        """Get guidelines for an approach"""
        return cls.APPROACH_STYLES.get(approach, cls.APPROACH_STYLES['approach_B'])
    
    @classmethod
    def format_approach_guide(cls, approach: str) -> str:
        """Format approach guidelines as readable text"""
        guide = cls.get_approach_guide(approach)
        
        lines = [
            f"📋 Approach: {guide['name']}",
            f"   {guide['description']}",
            "",
            "Characteristics:",
        ]
        
        for char in guide['characteristics']:
            lines.append(f"  • {char}")
        
        lines.extend([
            "",
            f"Best for: {', '.join(guide['best_for'])}",
            f"Structure: {guide['structure']}"
        ])
        
        return "\n".join(lines)


class QualityAssessment:
    """Helper for assessing answer quality"""
    
    QUALITY_CRITERIA = {
        'accuracy': 'Information is correct and factual',
        'completeness': 'All aspects of question addressed',
        'clarity': 'Easy to understand and well-organized',
        'relevance': 'Directly answers the question',
        'examples': 'Includes helpful examples where appropriate',
        'structure': 'Well-organized with clear flow'
    }
    
    @classmethod
    def estimate_quality(
        cls,
        accuracy: float = 1.0,
        completeness: float = 1.0,
        clarity: float = 1.0,
        relevance: float = 1.0,
        examples: float = 1.0,
        structure: float = 1.0
    ) -> float:
        """
        Estimate overall quality from individual criteria
        
        Args:
            All args are 0.0-1.0 scores for each criterion
        
        Returns:
            Overall quality score (0.0-1.0)
        """
        scores = [accuracy, completeness, clarity, relevance, examples, structure]
        return sum(scores) / len(scores)
    
    @classmethod
    def quality_description(cls, quality: float) -> str:
        """Get human-readable quality description"""
        if quality >= 0.9:
            return "Excellent - comprehensive, accurate, well-structured"
        elif quality >= 0.8:
            return "Good - solid answer, meets requirements"
        elif quality >= 0.7:
            return "Adequate - acceptable but room for improvement"
        elif quality >= 0.5:
            return "Below expectations - incomplete or issues"
        else:
            return "Poor - significant problems"


def main():
    """Demo of agent helper utilities"""
    print("Agent Helper Utilities Demo")
    print("=" * 70)
    
    # Demo approach guide
    print("\nApproach Guides:")
    for approach in ['approach_A', 'approach_B', 'approach_C']:
        print(f"\n{approach}:")
        print(ApproachGuide.format_approach_guide(approach))
        print()
    
    # Demo quality assessment
    print("\nQuality Assessment:")
    quality = QualityAssessment.estimate_quality(
        accuracy=0.95,
        completeness=0.90,
        clarity=0.85,
        relevance=0.90,
        examples=0.80,
        structure=0.85
    )
    print(f"Estimated quality: {quality:.1%}")
    print(f"Description: {QualityAssessment.quality_description(quality)}")


if __name__ == '__main__':
    main()
