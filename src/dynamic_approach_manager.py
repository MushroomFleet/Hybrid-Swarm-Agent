"""
Dynamic Approach Manager
Central management of dynamic approach lifecycle
"""

from typing import List, Optional, Tuple, Dict
from datetime import datetime
from src.approach_patterns import ApproachPattern, TaskContext, PatternSignature, StyleCharacteristics, PerformanceMetrics
from src.approach_storage import ApproachStorage
from src.approach_matching import match_approaches as match_approaches_func
from src.input_sanitization import sanitize_identifier


class DynamicApproachManager:
    """
    Manages dynamic approach lifecycle:
    - CRUD operations
    - Matching tasks to approaches
    - Performance tracking
    - Evolution and pruning (future)
    """
    
    def __init__(self, storage_path: str = "data/approaches"):
        self.storage = ApproachStorage(storage_path)
        self._approach_cache = {}  # Simple in-memory cache
    
    # === CRUD Operations ===
    
    def create_approach(self, approach: ApproachPattern) -> bool:
        """
        Create a new approach
        
        Args:
            approach: Approach to create
            
        Returns:
            True if successful
            
        Raises:
            ValueError: If approach with this ID already exists
        """
        # Check if already exists
        existing = self.get_approach(approach.id)
        if existing is not None:
            raise ValueError(f"Approach with ID '{approach.id}' already exists")
        
        # Save
        success = self.storage.save_approach(approach)
        
        if success:
            # Add to cache
            self._approach_cache[approach.id] = approach
        
        return success
    
    def get_approach(self, approach_id: str) -> Optional[ApproachPattern]:
        """
        Get approach by ID
        
        Args:
            approach_id: Approach identifier
            
        Returns:
            ApproachPattern if found, None otherwise
        """
        # Sanitize ID
        approach_id = sanitize_identifier(approach_id)
        
        # Check cache first
        if approach_id in self._approach_cache:
            return self._approach_cache[approach_id]
        
        # Load from storage
        approach = self.storage.load_approach(approach_id)
        
        if approach:
            # Cache for next time
            self._approach_cache[approach_id] = approach
        
        return approach
    
    def update_approach(self, approach: ApproachPattern) -> bool:
        """
        Update existing approach
        
        Args:
            approach: Updated approach
            
        Returns:
            True if successful
        """
        # Update timestamp
        approach.last_updated = datetime.now()
        
        # Save
        success = self.storage.save_approach(approach)
        
        if success:
            # Update cache
            self._approach_cache[approach.id] = approach
        
        return success
    
    def delete_approach(self, approach_id: str) -> bool:
        """
        Soft delete approach (mark inactive)
        
        Args:
            approach_id: ID of approach to delete
            
        Returns:
            True if successful
        """
        success = self.storage.delete_approach(approach_id)
        
        if success:
            # Remove from cache
            if approach_id in self._approach_cache:
                del self._approach_cache[approach_id]
        
        return success
    
    def list_approaches(
        self,
        active_only: bool = True,
        min_quality: float = 0.0
    ) -> List[ApproachPattern]:
        """
        List all approaches matching criteria
        
        Args:
            active_only: Only include active approaches
            min_quality: Minimum average quality
            
        Returns:
            List of ApproachPattern objects
        """
        approach_ids = self.storage.list_approaches(active_only, min_quality)
        
        approaches = []
        for aid in approach_ids:
            approach = self.get_approach(aid)
            if approach:
                approaches.append(approach)
        
        return approaches
    
    # === Matching Operations ===
    
    def match_approaches(
        self,
        task_context: TaskContext,
        threshold: float = 0.5,
        limit: int = 10
    ) -> List[Tuple[ApproachPattern, float]]:
        """
        Find approaches matching a task
        
        Args:
            task_context: Task characteristics
            threshold: Minimum match score
            limit: Maximum number of matches
            
        Returns:
            List of (approach, match_score) tuples, sorted by score
        """
        # Get all active approaches
        active_approaches = self.list_approaches(active_only=True)
        
        # Match using algorithm
        matches = match_approaches_func(task_context, active_approaches, threshold, limit)
        
        return matches
    
    def get_best_match(self, task_context: TaskContext) -> Optional[Tuple[ApproachPattern, float]]:
        """
        Get single best matching approach
        
        Args:
            task_context: Task characteristics
            
        Returns:
            (approach, score) tuple or None if no matches
        """
        matches = self.match_approaches(task_context, threshold=0.3, limit=1)
        
        if matches:
            return matches[0]
        return None
    
    # === Performance Tracking ===
    
    def record_execution(
        self,
        approach_id: str,
        quality: float,
        success: bool
    ) -> bool:
        """
        Record an execution result for an approach
        
        Args:
            approach_id: Approach that was used
            quality: Execution quality (0.0-1.0)
            success: Whether execution was successful
            
        Returns:
            True if successful
        """
        # Load approach
        approach = self.get_approach(approach_id)
        if not approach:
            return False
        
        # Update metrics
        approach.performance_metrics.update_with_execution(quality, success)
        approach.last_updated = datetime.now()
        
        # Save updated approach
        return self.update_approach(approach)
    
    # === Statistics ===
    
    def get_statistics(self) -> Dict:
        """Get manager statistics"""
        storage_stats = self.storage.get_statistics()
        
        approaches = self.list_approaches(active_only=False)
        
        # Calculate aggregate stats
        total_quality = sum(a.performance_metrics.avg_quality for a in approaches if a.performance_metrics.usage_count > 0)
        approaches_with_usage = [a for a in approaches if a.performance_metrics.usage_count > 0]
        
        return {
            **storage_stats,
            'cached_approaches': len(self._approach_cache),
            'avg_quality': total_quality / len(approaches_with_usage) if approaches_with_usage else 0.0,
            'approaches_with_usage': len(approaches_with_usage)
        }
    
    def get_approach_performance(
        self,
        approach_id: str
    ) -> Optional[Dict]:
        """
        Get detailed performance metrics for an approach
        
        Args:
            approach_id: Approach identifier
            
        Returns:
            Performance metrics dict or None
        """
        approach = self.get_approach(approach_id)
        if not approach:
            return None
        
        metrics = approach.performance_metrics
        
        return {
            'id': approach.id,
            'name': approach.name,
            'usage_count': metrics.usage_count,
            'avg_quality': metrics.avg_quality,
            'min_quality': metrics.min_quality,
            'max_quality': metrics.max_quality,
            'quality_std_dev': metrics.quality_std_dev,
            'success_rate': metrics.success_rate,
            'recent_trend': metrics.recent_quality_trend,
            'version': approach.version,
            'generation': approach.generation,
            'active': approach.active
        }
    
    # === Utility Methods ===
    
    def create_from_pattern(
        self,
        cluster: 'PatternCluster',
        signature: 'PatternSignature',
        style: 'StyleCharacteristics'
    ) -> Optional['ApproachPattern']:
        """
        Create approach from discovered pattern (convenience method)
        
        Args:
            cluster: PatternCluster with execution data
            signature: Extracted pattern signature
            style: Extracted style characteristics
            
        Returns:
            Created ApproachPattern or None
        """
        from src.approach_evolution import ApproachEvolution
        
        evolution = ApproachEvolution(manager=self)
        return evolution.create_approach_from_cluster(cluster, signature, style)
    
    def clear_cache(self):
        """Clear the approach cache"""
        self._approach_cache.clear()
    
    def reload_from_storage(self):
        """Reload all approaches from storage (clears cache)"""
        self.clear_cache()
        self.storage.manifest = self.storage._load_or_create_manifest()


if __name__ == "__main__":
    # Demo usage
    print("Dynamic Approach Manager Demo")
    print("=" * 70)
    
    # Create manager
    manager = DynamicApproachManager()
    
    # Create test approach
    test_approach = ApproachPattern(
        id="demo_tutorial_approach",
        name="Demo Tutorial Approach",
        version=1,
        created_at=datetime.now(),
        last_updated=datetime.now(),
        pattern_signature=PatternSignature(
            domain_weights={'writing': 0.9, 'coding': 0.7},
            complexity_min=0.3,
            complexity_max=0.8,
            keyword_patterns=['tutorial', 'guide', 'how to'],
            keyword_weights={'tutorial': 0.9, 'guide': 0.8, 'how to': 0.9},
            output_types=['tutorial', 'guide'],
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
        generation=0,
        tags=["demo", "tutorial"]
    )
    
    # Test 1: Create
    print("\n1. Creating Approach:")
    success = manager.create_approach(test_approach)
    print(f"   Create successful: {success}")
    
    # Test 2: Get
    print("\n2. Getting Approach:")
    loaded = manager.get_approach(test_approach.id)
    print(f"   Get successful: {loaded is not None}")
    if loaded:
        print(f"   Name: {loaded.name}")
    
    # Test 3: Record executions
    print("\n3. Recording Executions:")
    for i, quality in enumerate([0.85, 0.90, 0.88], 1):
        success = manager.record_execution(test_approach.id, quality, True)
        print(f"   Execution {i}: quality={quality}, recorded={success}")
    
    # Check updated metrics
    updated = manager.get_approach(test_approach.id)
    print(f"   Updated usage: {updated.performance_metrics.usage_count}")
    print(f"   Updated avg quality: {updated.performance_metrics.avg_quality:.2f}")
    
    # Test 4: Matching
    print("\n4. Matching Task to Approaches:")
    task = TaskContext(
        prompt="Write a Python tutorial",
        domain_weights={'writing': 0.8, 'coding': 0.5},
        complexity=0.6,
        keywords=['tutorial', 'python'],
        output_type='tutorial',
        estimated_duration=2.0
    )
    
    matches = manager.match_approaches(task, threshold=0.5)
    print(f"   Found {len(matches)} matches")
    for approach, score in matches:
        print(f"   - {approach.name}: {score:.2f}")
    
    # Test 5: Get best match
    print("\n5. Getting Best Match:")
    best = manager.get_best_match(task)
    if best:
        approach, score = best
        print(f"   Best match: {approach.name} (score: {score:.2f})")
    
    # Test 6: Statistics
    print("\n6. Manager Statistics:")
    stats = manager.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Test 7: Performance metrics
    print("\n7. Approach Performance:")
    perf = manager.get_approach_performance(test_approach.id)
    if perf:
        print(f"   Usage: {perf['usage_count']}")
        print(f"   Avg Quality: {perf['avg_quality']:.2f}")
        print(f"   Success Rate: {perf['success_rate']:.1%}")
        print(f"   Trend: {perf['recent_trend']}")
    
    print("\n" + "=" * 70)
    print("✓ DynamicApproachManager working correctly!")
