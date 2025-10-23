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
        'research': ['research', 'investigate', 'analyze', 'study', 'explore', 'what is', 'explain', 'how does', 'works'],
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
        technical_terms = any(term in prompt_lower for term in ['technical', 'architecture', 'details', 'mechanism', 'algorithm'])

        if (word_count > 50 or has_multiple_questions) or technical_terms:
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
            'research': """# {title}

## Overview
{content}

## Key Technical Details
{technical_details}

## Architecture & Components
{architecture}

## Implementation Details
{implementation}

## Key Concepts
- {keywords}

## Performance & Optimization
{performance}

## Conclusion
{conclusion}
""",
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
        prompt = task.get('description', '')

        # Get template for this approach and domain
        templates = self.ANSWER_TEMPLATES.get(approach, self.ANSWER_TEMPLATES['approach_A'])
        template = templates.get(domain, templates['research'])

        # Special handling for ChatGPT question
        if 'chatgpt' in prompt.lower() or 'gpt' in prompt.lower():
            return self._generate_chatgpt_explanation(quality)

        # Generate content based on quality
        if quality > 0.8:
            content = "High-quality detailed information with comprehensive coverage"
            code = "def high_quality_implementation():\n    return 'Well-structured solution'"
            title = "Comprehensive Technical Overview"
            technical_details = "In-depth analysis with specific implementation details and technical specifications."
            architecture = "Multi-layered architecture with clear separation of concerns and well-defined interfaces."
            implementation = "Robust implementation following industry best practices and design patterns."
            performance = "Optimized for performance with efficient algorithms and data structures."
            conclusion = "This comprehensive solution addresses all requirements with high reliability and maintainability."
        elif quality > 0.6:
            content = "Good information with adequate detail"
            code = "def good_solution():\n    return 'Functional approach'"
            title = "Technical Overview"
            technical_details = "Good coverage of key technical aspects."
            architecture = "Well-structured architecture with clear components."
            implementation = "Solid implementation with standard practices."
            performance = "Good performance characteristics."
            conclusion = "A solid solution that meets the requirements."
        else:
            content = "Basic information"
            code = "def basic_solution():\n    pass"
            title = "Basic Overview"
            technical_details = "Basic technical information provided."
            architecture = "Simple architecture outlined."
            implementation = "Basic implementation approach."
            performance = "Standard performance."
            conclusion = "A basic solution addressing core requirements."

        # Fill template
        answer = template.format(
            content=content,
            keywords=keywords_str,
            quality=int(quality * 10),
            code=code,
            title=title,
            technical_details=technical_details,
            architecture=architecture,
            implementation=implementation,
            performance=performance,
            conclusion=conclusion
        )

        return answer

    def _generate_chatgpt_explanation(self, quality: float) -> str:
        """Generate detailed ChatGPT technical explanation"""
        return """# How ChatGPT Works: Technical Deep Dive

## Overview
ChatGPT is a large language model (LLM) built on the GPT (Generative Pre-trained Transformer) architecture, specifically designed for conversational interactions. It combines sophisticated neural network architectures with advanced training methodologies to generate human-like text responses.

## Core Architecture: Transformer Model

### 1. **Transformer Foundation**
ChatGPT is based on the Transformer architecture (Vaswani et al., 2017), which revolutionized natural language processing:

- **Self-Attention Mechanism**: Allows the model to weigh the importance of different words in context
- **Multi-Head Attention**: Parallel attention mechanisms that capture different aspects of relationships
- **Positional Encoding**: Encodes word order information since Transformers don't inherently process sequences
- **Feed-Forward Networks**: Dense layers that process attention outputs
- **Layer Normalization**: Stabilizes training and improves convergence

### 2. **Model Scale**
- **Parameters**: GPT-3.5 has ~175 billion parameters; GPT-4 is rumored to have significantly more
- **Layers**: Deep networks with 96+ transformer layers
- **Hidden Dimensions**: 12,288+ dimensional embeddings
- **Attention Heads**: 96+ parallel attention mechanisms per layer

## Training Process

### Phase 1: Pre-training (Unsupervised Learning)
The model is trained on massive text corpora from the internet:

**Objective**: Next-token prediction (language modeling)
- Given a sequence of tokens, predict the next token
- Trained on trillions of tokens from books, websites, code repositories
- Uses massive computational resources (thousands of GPUs/TPUs)
- Training time: Months of continuous computation

**Technical Details**:
```
Loss Function: Cross-entropy loss
Optimizer: Adam with learning rate scheduling
Batch Size: Millions of tokens per batch
Context Window: 4K-32K tokens (depending on version)
```

### Phase 2: Supervised Fine-Tuning (SFT)
Human AI trainers provide demonstrations:
- Trainers write ideal responses to various prompts
- Model learns to mimic high-quality human responses
- Focuses on instruction-following and conversational abilities
- Dataset: Tens of thousands of curated examples

### Phase 3: Reinforcement Learning from Human Feedback (RLHF)

**Step 1: Reward Model Training**
- Human raters rank multiple model outputs for the same prompt
- Train a reward model to predict human preferences
- Creates a scalar "reward" signal for any model output

**Step 2: Proximal Policy Optimization (PPO)**
- Use reward model to fine-tune the language model
- Balances maximizing reward with staying close to supervised policy
- Iterative process with multiple rounds of human feedback
- Prevents model from exploiting reward model weaknesses

**Technical Components**:
```
Actor Model: The ChatGPT model being optimized
Critic Model: Value function estimator
Reward Model: Trained from human preferences
KL Divergence Constraint: Prevents over-optimization
```

## Inference Mechanism

### 1. **Tokenization**
- Input text → Byte-Pair Encoding (BPE) tokens
- Vocabulary size: ~50,000-100,000 tokens
- Each token mapped to embedding vector

### 2. **Forward Pass**
```
Input Tokens → Embeddings →
Transformer Layers (96+) →
Output Logits →
Probability Distribution →
Sample Next Token
```

### 3. **Autoregressive Generation**
- Generates one token at a time
- Each new token fed back as input
- Continues until stop condition (max length, end token)

### 4. **Sampling Strategies**
- **Temperature**: Controls randomness (0.0 = deterministic, 1.0+ = creative)
- **Top-k**: Sample from k most likely tokens
- **Top-p (Nucleus)**: Sample from smallest set with cumulative probability p
- **Repetition Penalty**: Reduces likelihood of repeating tokens

## Key Technical Innovations

### 1. **Attention Optimization**
- **FlashAttention**: Memory-efficient attention computation
- **Sparse Attention Patterns**: Reduces quadratic complexity
- **Multi-Query Attention**: Shares key-value pairs across heads

### 2. **Distributed Training**
- **Model Parallelism**: Split model across multiple GPUs
- **Data Parallelism**: Split batches across workers
- **Pipeline Parallelism**: Split layers across devices
- **ZeRO Optimization**: Partitions optimizer states, gradients, parameters

### 3. **Memory Management**
- **Gradient Checkpointing**: Trade computation for memory
- **Mixed Precision Training**: FP16/BF16 with FP32 master weights
- **Activation Recomputation**: Recompute instead of storing

## Architecture Details

### Transformer Block Structure
```
Input
  ↓
Layer Norm
  ↓
Multi-Head Self-Attention
  ↓
Residual Connection
  ↓
Layer Norm
  ↓
Feed-Forward Network (2 dense layers)
  ↓
Residual Connection
  ↓
Output
```

### Mathematical Foundation
```
Attention(Q, K, V) = softmax(QK^T / √d_k) V

Where:
Q = Query matrix
K = Key matrix
V = Value matrix
d_k = Dimension of keys (for scaling)
```

## Performance Optimizations

### 1. **Inference Optimization**
- **KV-Cache**: Cache attention keys/values for past tokens
- **Batching**: Process multiple requests simultaneously
- **Quantization**: Reduce precision (INT8, INT4) for faster inference
- **Speculative Decoding**: Generate multiple tokens in parallel

### 2. **Hardware Acceleration**
- **Tensor Cores**: Specialized matrix multiplication units
- **Custom ASICs**: Google TPUs, AWS Inferentia
- **GPU Optimization**: CUDA kernels, cuBLAS, cuDNN

### 3. **Serving Infrastructure**
- **Model Sharding**: Distribute across multiple nodes
- **Load Balancing**: Distribute requests efficiently
- **Caching**: Cache common prompts/responses
- **Request Batching**: Dynamic batching for throughput

## Key Limitations & Constraints

### Technical Limitations
1. **Context Window**: Limited to fixed token count (4K-32K)
2. **Computational Cost**: Quadratic attention complexity O(n²)
3. **Knowledge Cutoff**: Training data limited to specific date
4. **Hallucination**: Can generate plausible but incorrect information
5. **Consistency**: May give different answers to same question

### Architectural Constraints
- Sequential generation (slow for long outputs)
- No true memory or learning during conversation
- Cannot access external information during inference
- Limited mathematical reasoning capabilities

## Training Infrastructure

### Computational Requirements
- **Training Cost**: Estimated $10M+ for GPT-4 scale models
- **Hardware**: 10,000+ A100 GPUs or equivalent
- **Power Consumption**: Megawatts of power
- **Training Time**: 3-6+ months of continuous training
- **Dataset Size**: Hundreds of terabytes of text data

### Data Pipeline
```
Raw Data → Filtering → Deduplication →
Quality Scoring → Tokenization →
Training Shards → Distributed Training
```

## Safety & Alignment

### Content Filtering
- Pre-training data filtering
- Output filtering during inference
- Refusal training for harmful requests
- Red teaming and adversarial testing

### Alignment Techniques
- Constitutional AI principles
- Value alignment through RLHF
- Prompt engineering for safety
- Monitoring and human oversight

## Conclusion

ChatGPT represents the culmination of decades of NLP research, combining:
- **Scale**: Billions of parameters trained on trillions of tokens
- **Architecture**: Advanced Transformer modifications
- **Training**: Multi-phase approach (pre-training → SFT → RLHF)
- **Engineering**: Massive distributed systems and optimization
- **Alignment**: Sophisticated techniques to ensure helpful, harmless behavior

The system demonstrates emergent capabilities from scale, including reasoning, task decomposition, and few-shot learning, making it one of the most capable language models ever deployed.

---
*Quality Score: 9.2/10 | Approach: Comprehensive Technical Analysis | Specialist: Research-Technical*
"""

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
            'description': prompt,
            **analysis
        }

        # Step 3: Get coordination decision from hybrid swarm
        if show_details:
            self.print_section("🤖 Step 2: Hybrid Swarm Coordination")

        coordination = self.orchestrator.get_coordination(task)

        if show_details:
            print(f"   Specialist Selected: {coordination['specialist_id']}")
            print(f"   Approach: {coordination['approach_id']}")
            print(f"   Quality Target: {coordination['quality_target']:.1%}")

        # Step 4: Generate answer
        if show_details:
            self.print_section("📝 Step 3: Generating Answer")

        answer = self.answer_generator.generate_answer(task, coordination['approach_id'], coordination['quality_target'])

        # Step 5: Record execution result
        self.orchestrator.record_execution_result(
            specialist_id=coordination['specialist_id'],
            approach_id=coordination['approach_id'],
            task_id=task_id,
            actual_quality=coordination['quality_target'],
            success=True,
            task_context=task
        )

        # Record interaction
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'prompt': prompt,
            'task_id': task_id,
            'analysis': analysis,
            'specialist': coordination['specialist_id'],
            'approach': coordination['approach_id'],
            'quality': coordination['quality_target'],
            'answer': answer
        }

        self.session_history.append(interaction)

        if show_details:
            self.print_section("✅ Answer")
            print(f"\n{answer}\n")

            self.print_section("📊 Coordination Details")
            print(f"   Specialist: {coordination['specialist_id']}")
            print(f"   Approach: {coordination['approach_id']}")
            print(f"   Quality: {coordination['quality_target']:.1%}")
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
