"""
Hybrid Adaptive-Stigmergic Orchestrator
Combines adaptive resonance (specialist selection) with stigmergic coordination (approach selection)

This creates a two-level self-organizing system:
- Level 1: Adaptive resonance selects specialists based on task patterns
- Level 2: Stigmergic coordination selects approaches based on collective signals
- Level 3: Dynamic approaches emerge from patterns and evolve over time

Result: Both vertical specialization AND horizontal swarm coordination with emergent approaches
"""

import time
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime
from src.adaptive_resonance import AdaptiveResonanceOrchestrator, TaskSignature
from src.stigmergic_coordination import StigmergicBoard, StigmergicAgent
from src.dynamic_approach_manager import DynamicApproachManager
from src.execution_history import ExecutionHistory
from src.approach_patterns import TaskContext, ExecutionRecord, ContentFeatures
from src.pattern_analyzer import PatternAnalyzer
from src.approach_evolution import ApproachEvolution


class HybridSwarmOrchestrator:
    """
    Combines adaptive resonance for specialist selection with 
    stigmergic coordination for approach selection, plus dynamic
    approach evolution
    """
    
    def __init__(
        self,
        vigilance_threshold: float = 0.7,
        decay_rate: float = 3600.0,
        max_specialists: int = 10,
        use_dynamic_approaches: bool = True,
        enable_pattern_discovery: bool = True
    ):
        # Adaptive resonance layer
        self.adaptive_layer = AdaptiveResonanceOrchestrator(
            vigilance_threshold=vigilance_threshold,
            max_specialists=max_specialists
        )
        
        # Stigmergic coordination layer
        self.stigmergic_board = StigmergicBoard(decay_rate=decay_rate)
        
        # Specialist agents (created dynamically)
        self.specialist_agents: Dict[str, StigmergicAgent] = {}
        
        # Dynamic approaches system (Phase 4 integration)
        self.use_dynamic_approaches = use_dynamic_approaches
        self.enable_pattern_discovery = enable_pattern_discovery
        
        if use_dynamic_approaches:
            self.approach_manager = DynamicApproachManager()
            self.execution_history = ExecutionHistory()
            self.pattern_analyzer = PatternAnalyzer(self.execution_history)
            self.approach_evolution = ApproachEvolution(self.approach_manager)
            self._execution_count = 0
            self._pattern_discovery_threshold = 50  # Run discovery every N executions
        else:
            self.approach_manager = None
            self.execution_history = None
    
    def get_coordination(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get coordination decision WITHOUT executing task.
        For agent integration - returns guidance for LLM execution.
        
        Returns:
            {
                "specialist_id": str,
                "approach_id": str,
                "approach_metadata": dict (if using dynamic approaches),
                "quality_target": float,
                "task_id": str,
                "task_context": dict
            }
        """
        # Phase 1: Adaptive Resonance - Select Specialist
        specialist_id = self.adaptive_layer.match_or_create_specialist(task)
        
        # Create specialist agent if new
        if specialist_id not in self.specialist_agents:
            agent = StigmergicAgent(specialist_id, self.stigmergic_board)
            self.specialist_agents[specialist_id] = agent
        
        agent = self.specialist_agents[specialist_id]
        task_id = task.get('id', 'unknown')
        
        # Phase 2: Dynamic Approach Selection (if enabled)
        if self.use_dynamic_approaches and self.approach_manager:
            # Create TaskContext for matching
            task_context = self._create_task_context(task, task_id)
            
            # Get matching approaches
            matches = self.approach_manager.match_approaches(
                task_context,
                threshold=0.3,
                limit=3
            )
            
            if matches:
                # Use stigmergic signals to choose among top matches
                approach_id = self._select_with_signals(matches, task_id, specialist_id)
                best_match = next(a for a, _ in matches if a.id == approach_id)
                
                # Get approach metadata for LLM guidance
                approach_metadata = {
                    'name': best_match.name,
                    'signature': {
                        'domains': best_match.pattern_signature.domain_weights,
                        'complexity_range': (best_match.pattern_signature.complexity_min,
                                           best_match.pattern_signature.complexity_max),
                        'keywords': best_match.pattern_signature.keyword_patterns[:5],
                        'output_types': best_match.pattern_signature.output_types
                    },
                    'style': {
                        'structure': best_match.style_characteristics.structure_type,
                        'tone': best_match.style_characteristics.tone,
                        'voice': best_match.style_characteristics.voice,
                        'depth': best_match.style_characteristics.depth_level,
                        'use_code': best_match.pattern_signature.requires_code,
                        'use_examples': best_match.pattern_signature.requires_examples
                    },
                    'expected_quality': best_match.performance_metrics.avg_quality
                }
                
                quality_target = best_match.performance_metrics.avg_quality or 0.8
            else:
                # Fallback to legacy approach
                approach_id = agent.select_approach(task_id)
                approach_metadata = None
                quality_target = 0.7
        else:
            # Legacy stigmergic approach selection
            approach_id = agent.select_approach(task_id)
            approach_metadata = None
            
            # Get quality estimate from signal strength
            signals = self.stigmergic_board.read_signals(task_id, specialist_id)
            quality_target = max([s['strength'] / 100.0 for s in signals], default=0.5)
            quality_target = min(quality_target, 1.0)
        
        result = {
            "specialist_id": specialist_id,
            "approach_id": approach_id,
            "quality_target": quality_target,
            "task_id": task_id,
            "task_context": task
        }
        
        if approach_metadata:
            result["approach_metadata"] = approach_metadata
        
        return result
    
    def record_execution_result(
        self,
        specialist_id: str,
        approach_id: str,
        task_id: str,
        actual_quality: float,
        success: bool = True,
        task_context: Optional[Dict[str, Any]] = None,
        content_features: Optional[ContentFeatures] = None
    ):
        """
        Record actual execution results after LLM generates content.
        Updates both coordination layers for learning and records to execution history.
        
        Args:
            specialist_id: Specialist that handled the task
            approach_id: Approach that was used
            task_id: Task identifier
            actual_quality: Actual quality (0.0-1.0)
            success: Whether task was successful
            task_context: Optional task context dict
            content_features: Optional content features (auto-analyzed if None)
        """
        # Update adaptive layer (specialist learning)
        self.adaptive_layer.record_execution(specialist_id, success, actual_quality)
        
        # Update stigmergic layer (approach reinforcement)
        if specialist_id in self.specialist_agents:
            agent = self.specialist_agents[specialist_id]
            agent.board.deposit_signal(task_id, approach_id, actual_quality, specialist_id)
        
        # Update dynamic approaches system (if enabled)
        if self.use_dynamic_approaches and self.approach_manager:
            # Record to approach manager for performance tracking
            self.approach_manager.record_execution(approach_id, actual_quality, success)
            
            # Record to execution history for pattern analysis
            if task_context:
                # Create TaskContext object
                tc = self._create_task_context(task_context, task_id)
                
                # Create execution record
                record = ExecutionRecord(
                    record_id=f"exec_{task_id}_{int(time.time())}",
                    timestamp=datetime.now(),
                    task_context=tc,
                    specialist_id=specialist_id,
                    approach_id=approach_id,
                    quality_target=task_context.get('quality_target', 0.8),
                    actual_quality=actual_quality,
                    success=success,
                    execution_time_ms=0,  # Not tracked yet
                    content_features=content_features
                )
                
                self.execution_history.record_execution(record)
                self._execution_count += 1
                
                # Trigger pattern discovery if threshold met
                if self.enable_pattern_discovery and \
                   self._execution_count % self._pattern_discovery_threshold == 0:
                    self._trigger_pattern_discovery()
    
    def _create_task_context(self, task: Dict[str, Any], task_id: str) -> TaskContext:
        """Create TaskContext from task dict"""
        # Extract domain weights (support both single domain and multi-domain)
        domain = task.get('domain', 'general')
        if isinstance(domain, dict):
            domain_weights = domain
        else:
            # Convert single domain to weights
            domain_weights = {domain: 1.0}
        
        return TaskContext(
            prompt=task.get('description', task.get('prompt', '')),
            domain_weights=domain_weights,
            complexity=task.get('complexity', 0.5),
            keywords=task.get('keywords', []),
            output_type=task.get('output_type', 'explanation'),
            estimated_duration=task.get('estimated_duration', 1.0)
        )
    
    def _select_with_signals(
        self,
        matches: List[Tuple[Any, float]],
        task_id: str,
        specialist_id: str
    ) -> str:
        """
        Select approach from matches using stigmergic signals
        Blends match scores with signal strength for exploration/exploitation
        """
        # Get signals for this task/specialist
        signals = self.stigmergic_board.read_signals(task_id, specialist_id)
        signal_map = {s['approach']: s['strength'] for s in signals}
        
        # Calculate combined scores (70% match, 30% signal)
        scores = []
        for approach, match_score in matches:
            signal_strength = signal_map.get(approach.id, 0.0)
            combined = 0.7 * match_score + 0.3 * (signal_strength / 100.0)
            scores.append((approach.id, combined))
        
        # Select best combined score
        if scores:
            return max(scores, key=lambda x: x[1])[0]
        
        # Fallback to first match
        return matches[0][0].id
    
    def _trigger_pattern_discovery(self):
        """Trigger pattern discovery and approach creation"""
        print(f"\n🔍 Pattern Discovery: Analyzing {self._execution_count} executions...")
        
        try:
            # Discover patterns
            clusters = self.pattern_analyzer.discover_patterns(
                min_cluster_size=10,
                min_quality=0.8,
                similarity_threshold=0.65
            )
            
            if clusters:
                print(f"✓ Found {len(clusters)} patterns")
                
                # Create approaches from patterns
                for i, cluster in enumerate(clusters, 1):
                    signature = self.pattern_analyzer.extract_pattern_signature(cluster)
                    style = self.pattern_analyzer.extract_style_characteristics(cluster)
                    
                    approach = self.approach_evolution.create_approach_from_cluster(
                        cluster, signature, style
                    )
                    
                    if approach:
                        print(f"  ✓ Created: {approach.name}")
            else:
                print("  - No patterns found (need more diverse data)")
                
        except Exception as e:
            print(f"  ✗ Pattern discovery failed: {e}")
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute task using hybrid coordination (LEGACY - for demos with simulated answers).
        
        For real LLM integration, use:
        1. get_coordination() - Get guidance
        2. [Agent generates real content]
        3. record_execution_result() - Update system
        """
        
        # Phase 1: Adaptive Resonance - Select Specialist
        print(f"\n🎯 Phase 1: Specialist Selection (Adaptive Resonance)")
        specialist_id = self.adaptive_layer.match_or_create_specialist(task)
        
        # Create specialist agent if new
        if specialist_id not in self.specialist_agents:
            agent = StigmergicAgent(specialist_id, self.stigmergic_board)
            self.specialist_agents[specialist_id] = agent
            print(f"  → Created new stigmergic agent: {specialist_id}")
        
        agent = self.specialist_agents[specialist_id]
        
        # Phase 2: Stigmergic Coordination - Select Approach
        print(f"\n🐜 Phase 2: Approach Selection (Stigmergic Coordination)")
        task_id = task.get('id', 'unknown')
        approach, quality = agent.execute_and_report(task_id)
        
        # Phase 3: Update Both Systems
        print(f"\n📊 Phase 3: Dual Learning Update")
        
        # Update adaptive layer (specialist learning)
        success = quality > 0.7
        self.adaptive_layer.record_execution(specialist_id, success, quality)
        print(f"  ✓ Specialist profile updated (quality: {quality:.1%})")
        
        # Stigmergic layer automatically updated via deposit_signal in execute_and_report
        print(f"  ✓ Signal deposited on board (approach: {approach})")
        
        return {
            "specialist_id": specialist_id,
            "approach": approach,
            "quality": quality,
            "success": success
        }
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get statistics from both coordination layers"""
        
        # Adaptive layer stats
        adaptive_stats = self.adaptive_layer.get_specialist_stats()
        
        # Stigmergic layer stats  
        board_state = self.stigmergic_board.get_board_state()
        
        # Combined stats
        return {
            "adaptive_layer": {
                "total_specialists": adaptive_stats['total_specialists'],
                "specialists": adaptive_stats.get('specialists', [])
            },
            "stigmergic_layer": {
                "total_signals": board_state['total_signals'],
                "total_tasks": board_state['total_tasks'],
                "tasks": board_state['tasks']
            },
            "hybrid_metrics": {
                "specialist_agents": len(self.specialist_agents),
                "integration": "Specialists use stigmergic coordination for approach selection"
            }
        }
    
    def visualize_coordination(self) -> str:
        """Generate visualization of the hybrid system state"""
        stats = self.get_system_stats()
        
        lines = [
            "# Hybrid Swarm Coordination State",
            "",
            "## Adaptive Layer (Specialist Pool)",
            f"Total Specialists: {stats['adaptive_layer']['total_specialists']}",
            ""
        ]
        
        for spec in stats['adaptive_layer']['specialists']:
            lines.append(f"- {spec['id']}: {spec['executions']} tasks, "
                        f"{spec['average_quality']:.1%} quality")
        
        lines.extend([
            "",
            "## Stigmergic Layer (Signal Board)",
            f"Total Signals: {stats['stigmergic_layer']['total_signals']}",
            f"Active Tasks: {stats['stigmergic_layer']['total_tasks']}",
            ""
        ])
        
        for task_id, signals in stats['stigmergic_layer']['tasks'].items():
            lines.append(f"### {task_id}")
            for sig in signals[:3]:  # Top 3 signals
                lines.append(f"  - {sig['approach']}: strength {sig['strength']:.1f}")
        
        lines.extend([
            "",
            "## Hybrid Integration",
            "- Specialists emerge from task patterns (adaptive)",
            "- Each specialist coordinates via signals (stigmergic)",
            "- Dual learning: both layers improve over time",
            ""
        ])
        
        return "\n".join(lines)


# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("HYBRID ADAPTIVE-STIGMERGIC ORCHESTRATION DEMO")
    print("=" * 70)
    
    orchestrator = HybridSwarmOrchestrator(
        vigilance_threshold=0.75,
        decay_rate=1800.0
    )
    
    # Simulate diverse tasks
    tasks = [
        {
            "id": "task_001",
            "description": "Research Python async patterns",
            "domain": "research",
            "complexity": 0.7,
            "keywords": ["python", "async"],
            "estimated_duration": 2.0
        },
        {
            "id": "task_002",
            "description": "Research Python concurrency",
            "domain": "research",
            "complexity": 0.65,
            "keywords": ["python", "concurrency"],
            "estimated_duration": 1.8
        },
        {
            "id": "task_003",
            "description": "Write async tutorial",
            "domain": "writing",
            "complexity": 0.6,
            "keywords": ["tutorial", "async"],
            "estimated_duration": 3.0
        }
    ]
    
    print("\nExecuting tasks through hybrid system...\n")
    
    for i, task in enumerate(tasks, 1):
        print(f"\n{'=' * 70}")
        print(f"TASK {i}: {task['description']}")
        print('=' * 70)
        
        result = orchestrator.execute_task(task)
        
        print(f"\n✅ Task completed:")
        print(f"   Specialist: {result['specialist_id']}")
        print(f"   Approach: {result['approach']}")
        print(f"   Quality: {result['quality']:.1%}")
        
        time.sleep(0.5)
    
    print("\n" + "=" * 70)
    print("HYBRID SYSTEM VISUALIZATION")
    print("=" * 70)
    print(orchestrator.visualize_coordination())
