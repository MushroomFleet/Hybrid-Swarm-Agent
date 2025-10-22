"""
Dynamic Approach Pattern Data Models
Defines structures for emergent approach patterns
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import json


@dataclass
class PatternSignature:
    """
    Defines what tasks an approach is suited for
    Used for matching tasks to appropriate approaches
    """
    # Domain matching (multi-label with weights)
    domain_weights: Dict[str, float]  # {"writing": 0.9, "coding": 0.6}
    
    # Complexity range this approach handles well
    complexity_min: float  # 0.0 - 1.0
    complexity_max: float  # 0.0 - 1.0
    
    # Keyword patterns that indicate this approach
    keyword_patterns: List[str]  # ["tutorial", "how to", "step"]
    keyword_weights: Dict[str, float]  # {"tutorial": 0.9, "guide": 0.7}
    
    # Output types this approach is good for
    output_types: List[str]  # ["tutorial", "guide", "walkthrough"]
    
    # Task characteristic requirements
    requires_code: bool
    requires_examples: bool
    requires_theory: bool
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PatternSignature':
        """Create from dictionary"""
        return cls(**data)


@dataclass
class StyleCharacteristics:
    """
    Defines how content should be generated with this approach
    Provides guidance to LLM for content creation
    """
    # Structure
    structure_type: str  # "sequential_steps", "hierarchical", "prose", "bulleted"
    section_count: Tuple[int, int]  # (min, max) number of sections
    
    # Tone & Voice
    tone: str  # "formal", "casual", "technical", "educational"
    voice: str  # "second_person", "first_person", "third_person"
    
    # Content Depth
    depth_level: str  # "concise", "moderate", "comprehensive", "exhaustive"
    explanation_style: str  # "conceptual", "practical", "mixed"
    
    # Examples & Code
    example_density: str  # "low", "medium", "high"
    code_style: Optional[str]  # "minimal", "annotated", "production", None
    
    # Organization Elements
    use_headers: bool
    use_bullets: bool
    use_numbered_lists: bool
    use_tables: bool
    
    # Special Elements
    include_summary: bool
    include_tldr: bool
    include_prerequisites: bool
    include_next_steps: bool
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'StyleCharacteristics':
        """Create from dictionary"""
        return cls(**data)


@dataclass
class PerformanceMetrics:
    """
    Tracks approach effectiveness over time
    Used for evolution and pruning decisions
    """
    # Usage statistics
    usage_count: int
    first_used: datetime
    last_used: datetime
    
    # Quality metrics
    avg_quality: float  # 0.0 - 1.0
    min_quality: float
    max_quality: float
    quality_std_dev: float
    
    # Success metrics
    success_count: int  # Executions with quality >= 0.7
    failure_count: int  # Executions with quality < 0.7
    success_rate: float  # success_count / usage_count
    
    # Comparative metrics
    vs_alternatives: Dict[str, float]  # Comparison vs other approaches
    
    # Trend analysis
    recent_quality_trend: str  # "improving", "stable", "declining", "new"
    quality_history: List[Tuple[str, float]]  # List of (timestamp_iso, quality)
    
    def to_dict(self) -> dict:
        """Convert to dictionary with datetime serialization"""
        data = asdict(self)
        data['first_used'] = self.first_used.isoformat()
        data['last_used'] = self.last_used.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PerformanceMetrics':
        """Create from dictionary with datetime parsing"""
        data = data.copy()
        data['first_used'] = datetime.fromisoformat(data['first_used'])
        data['last_used'] = datetime.fromisoformat(data['last_used'])
        return cls(**data)
    
    def update_with_execution(self, quality: float, success: bool):
        """
        Update metrics after an execution
        
        Args:
            quality: Execution quality (0.0-1.0)
            success: Whether execution was successful
        """
        self.usage_count += 1
        self.last_used = datetime.now()
        
        # Update quality metrics
        if self.usage_count == 1:
            self.avg_quality = quality
            self.min_quality = quality
            self.max_quality = quality
            self.quality_std_dev = 0.0
        else:
            # Update running average (exponential moving average)
            alpha = 0.1  # Weight for new data
            self.avg_quality = (1 - alpha) * self.avg_quality + alpha * quality
            
            # Update min/max
            self.min_quality = min(self.min_quality, quality)
            self.max_quality = max(self.max_quality, quality)
            
            # Update std dev (simplified)
            variance = sum((q - self.avg_quality) ** 2 for _, q in self.quality_history[-100:]) / len(self.quality_history[-100:])
            self.quality_std_dev = variance ** 0.5
        
        # Update success metrics
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1
        
        self.success_rate = self.success_count / self.usage_count
        
        # Add to history (keep last 100)
        self.quality_history.append((datetime.now().isoformat(), quality))
        if len(self.quality_history) > 100:
            self.quality_history = self.quality_history[-100:]
        
        # Update trend
        self.recent_quality_trend = self._calculate_trend()
    
    def _calculate_trend(self) -> str:
        """Calculate recent quality trend"""
        if len(self.quality_history) < 10:
            return "new"
        
        # Compare last 10 vs previous 10
        recent_10 = [q for _, q in self.quality_history[-10:]]
        previous_10 = [q for _, q in self.quality_history[-20:-10]] if len(self.quality_history) >= 20 else recent_10
        
        recent_avg = sum(recent_10) / len(recent_10)
        previous_avg = sum(previous_10) / len(previous_10)
        
        diff = recent_avg - previous_avg
        
        if diff > 0.05:
            return "improving"
        elif diff < -0.05:
            return "declining"
        else:
            return "stable"


@dataclass
class ApproachPattern:
    """
    Complete definition of a dynamic approach
    Combines pattern signature, style characteristics, and performance metrics
    """
    # Identity
    id: str  # Unique identifier (e.g., "approach_tutorial_python_stepbystep")
    name: str  # Human-readable name
    version: int  # Incremented on evolution
    created_at: datetime
    last_updated: datetime
    
    # Pattern components
    pattern_signature: PatternSignature
    style_characteristics: StyleCharacteristics
    performance_metrics: PerformanceMetrics
    
    # Metadata
    parent_id: Optional[str] = None  # If evolved from another approach
    generation: int = 0  # 0 = seed, 1+ = evolved
    tags: List[str] = field(default_factory=list)
    active: bool = True  # For soft delete
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON storage"""
        return {
            'id': self.id,
            'name': self.name,
            'version': self.version,
            'created_at': self.created_at.isoformat(),
            'last_updated': self.last_updated.isoformat(),
            'pattern_signature': self.pattern_signature.to_dict(),
            'style_characteristics': self.style_characteristics.to_dict(),
            'performance_metrics': self.performance_metrics.to_dict(),
            'parent_id': self.parent_id,
            'generation': self.generation,
            'tags': self.tags,
            'active': self.active
        }
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ApproachPattern':
        """Create from dictionary"""
        data = data.copy()
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['last_updated'] = datetime.fromisoformat(data['last_updated'])
        data['pattern_signature'] = PatternSignature.from_dict(data['pattern_signature'])
        data['style_characteristics'] = StyleCharacteristics.from_dict(data['style_characteristics'])
        data['performance_metrics'] = PerformanceMetrics.from_dict(data['performance_metrics'])
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'ApproachPattern':
        """Create from JSON string"""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def match_task(self, task_context: 'TaskContext') -> float:
        """
        Calculate how well this approach matches a task
        
        Args:
            task_context: Task characteristics
            
        Returns:
            Match score (0.0 - 1.0)
        """
        from src.approach_matching import calculate_match_score
        return calculate_match_score(task_context, self.pattern_signature)


@dataclass
class TaskContext:
    """
    Task characteristics for matching
    """
    prompt: str
    domain_weights: Dict[str, float]
    complexity: float
    keywords: List[str]
    output_type: str
    estimated_duration: float
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'TaskContext':
        """Create from dictionary"""
        return cls(**data)


@dataclass
class ContentFeatures:
    """Extracted features from generated content"""
    
    # Structure analysis
    section_count: int
    has_code_blocks: bool
    code_block_count: int
    has_numbered_list: bool
    has_bullets: bool
    has_tables: bool
    
    # Length analysis
    total_length: int
    avg_section_length: int
    
    # Style analysis
    detected_tone: str  # Via simple heuristics or LLM
    formality_score: float  # 0.0 - 1.0
    
    # Content type
    explanation_ratio: float  # Portion that's explanatory
    example_ratio: float  # Portion that's examples
    code_ratio: float  # Portion that's code
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ContentFeatures':
        """Create from dictionary"""
        return cls(**data)


@dataclass
class ExecutionRecord:
    """
    Record of a single execution for pattern analysis
    """
    # Identity
    record_id: str
    timestamp: datetime
    
    # Task context
    task_context: TaskContext
    
    # Coordination decision
    specialist_id: str
    approach_id: str
    quality_target: float
    
    # Execution result
    actual_quality: float
    success: bool
    execution_time_ms: int
    
    # Content analysis (optional)
    content_features: Optional['ContentFeatures'] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'record_id': self.record_id,
            'timestamp': self.timestamp.isoformat(),
            'task_context': self.task_context.to_dict(),
            'specialist_id': self.specialist_id,
            'approach_id': self.approach_id,
            'quality_target': self.quality_target,
            'actual_quality': self.actual_quality,
            'success': self.success,
            'execution_time_ms': self.execution_time_ms,
            'content_features': self.content_features.to_dict() if self.content_features else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ExecutionRecord':
        """Create from dictionary"""
        data = data.copy()
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        data['task_context'] = TaskContext.from_dict(data['task_context'])
        if data.get('content_features'):
            data['content_features'] = ContentFeatures.from_dict(data['content_features'])
        return cls(**data)


if __name__ == "__main__":
    # Demo usage
    print("Approach Pattern Data Models Demo")
    print("=" * 70)
    
    # Create example approach pattern
    approach = ApproachPattern(
        id="example_tutorial_stepbystep",
        name="Step-by-Step Tutorial Example",
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
        tags=["tutorial", "step-by-step", "educational"]
    )
    
    print("\n1. Created ApproachPattern:")
    print(f"   ID: {approach.id}")
    print(f"   Name: {approach.name}")
    print(f"   Structure: {approach.style_characteristics.structure_type}")
    print(f"   Domains: {approach.pattern_signature.domain_weights}")
    
    # Test serialization
    print("\n2. Serialization Test:")
    json_str = approach.to_json()
    print(f"   JSON size: {len(json_str)} bytes")
    
    # Test deserialization
    loaded = ApproachPattern.from_json(json_str)
    print(f"   Deserialized ID: {loaded.id}")
    print(f"   Deserialized name: {loaded.name}")
    assert loaded.id == approach.id
    assert loaded.name == approach.name
    print("   ✓ Serialization working correctly")
    
    # Test metric updates
    print("\n3. Performance Metrics Update Test:")
    print(f"   Initial usage: {approach.performance_metrics.usage_count}")
    
    approach.performance_metrics.update_with_execution(0.85, True)
    print(f"   After execution 1: quality={approach.performance_metrics.avg_quality:.2f}, count={approach.performance_metrics.usage_count}")
    
    approach.performance_metrics.update_with_execution(0.90, True)
    print(f"   After execution 2: quality={approach.performance_metrics.avg_quality:.2f}, count={approach.performance_metrics.usage_count}")
    
    approach.performance_metrics.update_with_execution(0.75, True)
    print(f"   After execution 3: quality={approach.performance_metrics.avg_quality:.2f}, count={approach.performance_metrics.usage_count}")
    
    print(f"   Success rate: {approach.performance_metrics.success_rate:.1%}")
    print(f"   Trend: {approach.performance_metrics.recent_quality_trend}")
    
    print("\n" + "=" * 70)
    print("✓ All data models working correctly!")
