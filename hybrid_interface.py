"""
Hybrid Swarm Interactive Interface
==================================
Interactive test interface for the hybrid adaptive-stigmergic orchestrator

⚠️  NOTE: This interface uses SIMULATED answers for demo purposes.
    For real LLM integration with Claude Code agent, use the agent_tools/ scripts:
    - agent_tools/get_coordination.py - Get coordination decision
    - agent_tools/report_result.py - Report actual execution results
    See .claude/agents/hybrid-swarm.md for agent workflow

This demo interface:
- Accepts user prompts/questions
- Processes them through hybrid swarm system
- Shows specialist selection and coordination
- Generates template-based answers (SIMULATED for demo)
- Demonstrates the coordination system

Run: python hybrid_interface.py [prompt]
     python hybrid_interface.py --interactive
"""

import sys
import os
import time
from datetime import datetime
from pathlib import Path
import re
from typing import Dict, Any

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.hybrid_swarm import HybridSwarmOrchestrator

# Create session artifacts directory
SESSION_DIR = Path("artifacts/hybrid-sessions")
SESSION_DIR.mkdir(parents=True, exist_ok=True)

class PromptProcessor:
    """Converts user prompts into task structures for hybrid swarm"""
    
    DOMAIN_KEYWORDS = {
        'research': ['research', 'investigate', 'analyze', 'study', 'explore', 'what is', 'explain'],
        'writing': ['write', 'create', 'draft', 'compose', 'tutorial', 'guide', 'how to'],
        'review': ['review', 'check', 'evaluate', 'critique', 'assess', 'improve'],
        'coding': ['code', 'implement', 'build', 'develop', 'program', 'function'],
        'comparison': ['compare', 'vs', 'versus', 'difference', 'better', 'which']
    }
    
    def analyze_prompt(self, prompt: str) -> Dict[str, Any]:
        """Analyze prompt to determine task characteristics"""
        prompt_lower = prompt.lower()
        
        # Determine domain
        domain = 'general'
        for dom, keywords in self.DOMAIN_KEYWORDS.items():
            if any(kw in prompt_lower for kw in keywords):
                domain = dom
                break
        
        # Estimate complexity from prompt length and question complexity
        word_count = len(prompt.split())
        has_multiple_questions = prompt.count('?') > 1 or 'and' in prompt_lower
        
        if word_count > 50 or has_multiple_questions:
            complexity = 0.8
        elif word_count > 20:
            complexity = 0.6
        else:
            complexity = 0.4
        
        # Extract keywords
        words = re.findall(r'\b\w+\b', prompt_lower)
        keywords = [w for w in words if len(w) > 4 and w not in ['what', 'when', 'where', 'which', 'would', 'should', 'could']][:5]
        
        # Determine output type
        if 'tutorial' in prompt_lower or 'guide' in prompt_lower or 'how to' in prompt_lower:
            output_type = 'tutorial'
        elif 'code' in prompt_lower or 'example' in prompt_lower:
            output_type = 'code'
        elif 'list' in prompt_lower or 'comparison' in prompt_lower:
            output_type = 'list'
        else:
            output_type = 'explanation'
        
        return {
            'domain': domain,
            'complexity': complexity,
            'keywords': keywords,
            'output_type': output_type,
            'input_type': 'text',
            'estimated_duration': complexity * 3.0
        }

class AnswerGenerator:
    """Generates simulated answers based on task and approach"""
    
    ANSWER_TEMPLATES = {
        'approach_A': {
            'research': "Based on research from multiple sources:\n\n{content}\n\nKey findings: {keywords}",
            'writing': "Here's a comprehensive guide:\n\n1. Introduction\n2. {content}\n3. Examples\n4. Summary",
            'review': "Analysis:\n\n✓ Strengths: {content}\n✗ Issues found\n→ Recommendations",
            'coding': "```python\n# {content}\n{code}\n```\n\nExplanation: {keywords}",
        },
        'approach_B': {
            'research': "Let me break this down:\n\n• Point 1: {content}\n• Point 2: {keywords}\n• Conclusion",
            'writing': "Step-by-step tutorial:\n\nStep 1: {content}\nStep 2: Practice\nStep 3: Master it!",
            'review': "Quick review:\n{content}\n\nScore: {quality}/10\nNext steps: {keywords}",
            'coding': "# Solution\n{code}\n\n# Usage\n{content}\n\n# Best practices: {keywords}",
        },
        'approach_C': {
            'research': "Summary: {content}\n\nDetailed analysis:\n- {keywords}\n\nSources cited: 5",
            'writing': "{content}\n\nPractical examples:\n- Example 1\n- Example 2\n\nKey takeaways: {keywords}",
            'review': "Comprehensive review:\n\nQuality: {quality}\nDetails: {content}\nRecommended: {keywords}",
            'coding': "// Implementation\n{code}\n\n// Explanation\n{content}\n\n// Notes: {keywords}",
        }
    }
    
    def generate_answer(self, task: Dict[str, Any], approach: str, quality: float) -> str:
        """Generate a simulated answer based on task, approach, and quality"""
        domain = task.get('domain', 'general')
        keywords_str = ', '.join(task.get('keywords', ['example', 'demo'])[:3])
        
        # Get template for this approach and domain
        templates = self.ANSWER_TEMPLATES.get(approach, self.ANSWER_TEMPLATES['approach_A'])
        template = templates.get(domain, templates['research'])
        
        # Generate content based on quality
        if quality > 0.8:
            content = "High-quality detailed information with comprehensive coverage"
            code = "def high_quality_implementation():\n    return 'Well-structured solution'"
        elif quality > 0.6:
            content = "Good information with adequate detail"
            code = "def good_solution():\n    return 'Functional approach'"
        else:
            content = "Basic information"
            code = "def basic_solution():\n    pass"
        
        # Fill template
        answer = template.format(
            content=content,
            keywords=keywords_str,
            quality=int(quality * 10),
            code=code
        )
        
        return answer

class HybridInterface:
    """Interactive interface for hybrid swarm system"""
    
    def __init__(self):
        self.orchestrator = HybridSwarmOrchestrator(
            vigilance_threshold=0.75,
            decay_rate=1800.0
        )
        self.prompt_processor = PromptProcessor()
        self.answer_generator = AnswerGenerator()
        self.session_history = []
        self.interaction_count = 0
    
    def print_header(self, text, width=70, char="="):
        """Print formatted header"""
        print(f"\n{char * width}")
        print(f"{text:^{width}}")
        print(f"{char * width}")
    
    def print_section(self, text):
        """Print section divider"""
        print(f"\n{text}")
        print("-" * 70)
    
    def process_prompt(self, prompt: str, show_details: bool = True) -> Dict[str, Any]:
        """Process a user prompt through the hybrid swarm system"""
        
        self.interaction_count += 1
        task_id = f"prompt_{self.interaction_count:04d}"
        
        if show_details:
            self.print_header(f"PROCESSING PROMPT #{self.interaction_count}")
            print(f"\n💬 Your Question:")
            print(f"   \"{prompt}\"")
        
        # Step 1: Analyze prompt
        if show_details:
            self.print_section("🔍 Step 1: Analyzing Prompt")
        
        analysis = self.prompt_processor.analyze_prompt(prompt)
        
        if show_details:
            print(f"   Domain: {analysis['domain']}")
            print(f"   Complexity: {analysis['complexity']:.2f}")
            print(f"   Output Type: {analysis['output_type']}")
            print(f"   Keywords: {', '.join(analysis['keywords'][:3])}")
        
        # Step 2: Create task structure
        task = {
            'id': task_id,
            'description': prompt[:50] + "..." if len(prompt) > 50 else prompt,
            **analysis
        }
        
        # Step 3: Execute through hybrid swarm
        if show_details:
            self.print_section("🤖 Step 2: Hybrid Swarm Coordination")
        
        result = self.orchestrator.execute_task(task)
        
        # Step 4: Generate answer
        if show_details:
            self.print_section("📝 Step 3: Generating Answer")
        
        answer = self.answer_generator.generate_answer(task, result['approach'], result['quality'])
        
        # Record interaction
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'prompt': prompt,
            'task_id': task_id,
            'analysis': analysis,
            'specialist': result['specialist_id'],
            'approach': result['approach'],
            'quality': result['quality'],
            'answer': answer
        }
        
        self.session_history.append(interaction)
        
        if show_details:
            self.print_section("✅ Answer")
            print(f"\n{answer}\n")
            
            self.print_section("📊 Coordination Details")
            print(f"   Specialist: {result['specialist_id']}")
            print(f"   Approach: {result['approach']}")
            print(f"   Quality: {result['quality']:.1%}")
            print(f"   Processing time: ~{analysis['estimated_duration']:.1f}s (estimated)")
        
        return interaction
    
    def interactive_mode(self):
        """Run in interactive chat mode"""
        self.print_header("HYBRID SWARM INTERACTIVE INTERFACE", char="=")
        print("\n  Welcome to the Hybrid Swarm Q&A System!")
        print("  This system uses adaptive resonance + stigmergic coordination")
        print("  to intelligently route and answer your questions.\n")
        print("  Commands:")
        print("    • Type your question and press ENTER")
        print("    • 'stats' - Show system statistics")
        print("    • 'history' - Show interaction history")
        print("    • 'quit' or 'exit' - Exit interface")
        print("\n" + "=" * 70)
        
        while True:
            try:
                prompt = input("\n💬 You: ").strip()
                
                if not prompt:
                    continue
                
                if prompt.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye! Session saved.")
                    self.save_session()
                    break
                
                if prompt.lower() == 'stats':
                    self.show_stats()
                    continue
                
                if prompt.lower() == 'history':
                    self.show_history()
                    continue
                
                # Process prompt
                self.process_prompt(prompt, show_details=True)
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Session saved.")
                self.save_session()
                break
            except EOFError:
                print("\n\n👋 EOF. Session saved.")
                self.save_session()
                break
    
    def show_stats(self):
        """Display system statistics"""
        stats = self.orchestrator.get_system_stats()
        
        self.print_section("📊 System Statistics")
        
        print(f"\n  Session Info:")
        print(f"    Total interactions: {self.interaction_count}")
        print(f"    Average quality: {sum(i['quality'] for i in self.session_history) / len(self.session_history):.1%}" if self.session_history else "    No interactions yet")
        
        print(f"\n  Adaptive Layer:")
        print(f"    Specialists: {stats['adaptive_layer']['total_specialists']}")
        for spec in stats['adaptive_layer']['specialists']:
            print(f"      • {spec['id']}: {spec['executions']} tasks, {spec['average_quality']:.1%} quality")
        
        print(f"\n  Stigmergic Layer:")
        print(f"    Active signals: {stats['stigmergic_layer']['total_signals']}")
        print(f"    Tasks on board: {stats['stigmergic_layer']['total_tasks']}")
    
    def show_history(self):
        """Display interaction history"""
        self.print_section("📜 Interaction History")
        
        if not self.session_history:
            print("\n  No interactions yet.")
            return
        
        for i, interaction in enumerate(self.session_history[-5:], 1):  # Last 5
            print(f"\n  {i}. {interaction['prompt'][:60]}...")
            print(f"     Specialist: {interaction['specialist']}")
            print(f"     Quality: {interaction['quality']:.1%}")
            print(f"     Time: {interaction['timestamp'][11:19]}")
    
    def save_session(self):
        """Save session history"""
        if not self.session_history:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = SESSION_DIR / f"session_{timestamp}.json"
        
        import json
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'session_start': self.session_history[0]['timestamp'],
                'session_end': self.session_history[-1]['timestamp'],
                'total_interactions': len(self.session_history),
                'interactions': self.session_history
            }, f, indent=2)
        
        print(f"\n📁 Session saved: {filepath}")

def single_prompt_mode(prompt: str):
    """Process a single prompt and show result"""
    interface = HybridInterface()
    
    print("=" * 70)
    print(" " * 20 + "HYBRID SWARM Q&A SYSTEM")
    print("=" * 70)
    
    interface.process_prompt(prompt, show_details=True)
    
    print("\n" + "=" * 70)
    print("\n💡 Tip: Run with --interactive for chat mode!")
    print("=" * 70)

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        if sys.argv[1] == '--interactive' or sys.argv[1] == '-i':
            # Interactive mode
            interface = HybridInterface()
            interface.interactive_mode()
        elif sys.argv[1] in ['--help', '-h']:
            print("""
Hybrid Swarm Interactive Interface

Usage:
  python hybrid_interface.py "Your question here"    # Single prompt
  python hybrid_interface.py --interactive          # Chat mode
  python hybrid_interface.py --help                 # This help

Examples:
  python hybrid_interface.py "How do I use Python async/await?"
  python hybrid_interface.py "Write a tutorial on concurrency"
  python hybrid_interface.py --interactive

In interactive mode:
  - Type questions and get answers
  - Type 'stats' to see system statistics
  - Type 'history' to see past interactions
  - Type 'quit' to exit and save session
            """)
        else:
            # Single prompt mode
            prompt = ' '.join(sys.argv[1:])
            single_prompt_mode(prompt)
    else:
        # Default to interactive
        print("No prompt provided. Starting interactive mode...")
        print("(Use --help for usage information)\n")
        time.sleep(1)
        interface = HybridInterface()
        interface.interactive_mode()

if __name__ == "__main__":
    main()
