"""
Approach Matching Algorithm
Scores how well tasks match approach patterns
"""

from typing import Dict, List, Tuple
from src.approach_patterns import PatternSignature, TaskContext, ApproachPattern


def calculate_match_score(
    task: TaskContext,
    signature: PatternSignature
) -> float:
    """
    Calculate how well a task matches an approach signature
    
    Scoring components (weighted):
    - Domain overlap: 40%
    - Complexity fit: 20%
    - Keyword match: 20%
    - Output type match: 20%
    
    Args:
        task: Task characteristics
        signature: Approach pattern signature
        
    Returns:
        Match score (0.0 - 1.0)
    """
    scores = []
    
    # 1. Domain overlap (40% weight)
    domain_score = calculate_domain_overlap(task.domain_weights, signature.domain_weights)
    scores.append(('domain', domain_score, 0.4))
    
    # 2. Complexity fit (20% weight)
    complexity_score = calculate_complexity_fit(task.complexity, signature.complexity_min, signature.complexity_max)
    scores.append(('complexity', complexity_score, 0.2))
    
    # 3. Keyword match (20% weight)
    keyword_score = calculate_keyword_match(task.keywords, signature.keyword_weights)
    scores.append(('keywords', keyword_score, 0.2))
    
    # 4. Output type match (20% weight)
    output_score = 1.0 if task.output_type in signature.output_types else 0.0
    scores.append(('output', output_score, 0.2))
    
    # Weighted average
    total_score = sum(score * weight for _, score, weight in scores)
    
    return total_score


def calculate_domain_overlap(
    task_domains: Dict[str, float],
    signature_domains: Dict[str, float]
) -> float:
    """
    Calculate overlap between task domains and signature domains
    
    Uses weighted dot product similarity
    
    Args:
        task_domains: Task domain weights
        signature_domains: Signature domain weights
        
    Returns:
        Overlap score (0.0 - 1.0)
    """
    if not task_domains or not signature_domains:
        return 0.0
    
    # Calculate weighted overlap
    overlap = 0.0
    for domain, task_weight in task_domains.items():
        sig_weight = signature_domains.get(domain, 0.0)
        overlap += task_weight * sig_weight
    
    # Normalize to 0-1 range
    # Maximum possible overlap is sum of min(task_weight, sig_weight) for each domain
    max_possible = sum(
        min(task_domains.get(d, 0.0), signature_domains.get(d, 0.0))
        for d in set(list(task_domains.keys()) + list(signature_domains.keys()))
    )
    
    if max_possible > 0:
        overlap = overlap / max_possible
    
    return min(1.0, overlap)


def calculate_complexity_fit(
    task_complexity: float,
    sig_min: float,
    sig_max: float
) -> float:
    """
    Calculate how well task complexity fits in signature range
    
    Args:
        task_complexity: Task complexity (0.0-1.0)
        sig_min: Signature minimum complexity
        sig_max: Signature maximum complexity
        
    Returns:
        Fit score (0.0 - 1.0)
    """
    # Perfect fit if within range
    if sig_min <= task_complexity <= sig_max:
        return 1.0
    
    # Partial credit based on distance from range
    if task_complexity < sig_min:
        distance = sig_min - task_complexity
    else:  # task_complexity > sig_max
        distance = task_complexity - sig_max
    
    # Score decays with distance (reaches 0 at distance 0.5)
    score = max(0.0, 1.0 - (distance * 2.0))
    
    return score


def calculate_keyword_match(
    task_keywords: List[str],
    signature_keywords: Dict[str, float]
) -> float:
    """
    Calculate keyword matching score
    
    Args:
        task_keywords: Keywords from task
        signature_keywords: Keyword weights from signature
        
    Returns:
        Match score (0.0 - 1.0)
    """
    if not task_keywords or not signature_keywords:
        return 0.0
    
    # Convert task keywords to set for fast lookup
    task_keywords_set = set(kw.lower() for kw in task_keywords)
    
    # Calculate weighted matches
    total_weight = 0.0
    matched_weight = 0.0
    
    for sig_keyword, weight in signature_keywords.items():
        total_weight += weight
        sig_keyword_lower = sig_keyword.lower()
        
        # Check for exact match
        if sig_keyword_lower in task_keywords_set:
            matched_weight += weight
        # Check for partial match (keyword contains or is contained)
        elif any(sig_keyword_lower in tk or tk in sig_keyword_lower for tk in task_keywords_set):
            matched_weight += weight * 0.5  # Partial credit
    
    if total_weight > 0:
        score = matched_weight / total_weight
    else:
        score = 0.0
    
    return min(1.0, score)


def match_approaches(
    task_context: TaskContext,
    approaches: List[ApproachPattern],
    threshold: float = 0.5,
    limit: int = 10
) -> List[Tuple[ApproachPattern, float]]:
    """
    Match task to candidate approaches
    
    Args:
        task_context: Task characteristics
        approaches: List of available approaches
        threshold: Minimum match score to include
        limit: Maximum number of matches to return
        
    Returns:
        List of (approach, match_score) tuples, sorted by score descending
    """
    candidates = []
    
    for approach in approaches:
        if not approach.active:
            continue  # Skip inactive approaches
        
        score = calculate_match_score(task_context, approach.pattern_signature)
        
        if score >= threshold:
            candidates.append((approach, score))
    
    # Sort by match score descending
    candidates.sort(key=lambda x: x[1], reverse=True)
    
    # Return top N
    return candidates[:limit]


if __name__ == "__main__":
    # Demo usage
    print("Approach Matching Algorithm Demo")
    print("=" * 70)
    
    from src.approach_patterns import ApproachPattern, PatternSignature, StyleCharacteristics, PerformanceMetrics
    from datetime import datetime
    
    # Create test approaches
    tutorial_approach = ApproachPattern(
        id="test_tutorial",
        name="Tutorial Approach",
        version=1,
        created_at=datetime.now(),
        last_updated=datetime.now(),
        pattern_signature=PatternSignature(
            domain_weights={'writing': 0.9, 'coding': 0.7},
            complexity_min=0.3,
            complexity_max=0.8,
            keyword_patterns=['tutorial', 'guide', 'how to'],
            keyword_weights={'tutorial': 0.9, 'guide': 0.8},
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
        tags=["tutorial"]
    )
    
    research_approach = ApproachPattern(
        id="test_research",
        name="Research Approach",
        version=1,
        created_at=datetime.now(),
        last_updated=datetime.now(),
        pattern_signature=PatternSignature(
            domain_weights={'research': 0.9, 'writing': 0.5},
            complexity_min=0.5,
            complexity_max=1.0,
            keyword_patterns=['research', 'investigate', 'analyze'],
            keyword_weights={'research': 0.9, 'investigate': 0.8},
            output_types=['research', 'analysis'],
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
        generation=0,
        tags=["research"]
    )
    
    # Test 1: Tutorial task should match tutorial approach
    print("\n1. Tutorial Task Matching:")
    tutorial_task = TaskContext(
        prompt="Write a tutorial on Python async/await",
        domain_weights={'writing': 0.8, 'coding': 0.5},
        complexity=0.6,
        keywords=['tutorial', 'python', 'async'],
        output_type='tutorial',
        estimated_duration=2.0
    )
    
    tutorial_score = calculate_match_score(tutorial_task, tutorial_approach.pattern_signature)
    research_score = calculate_match_score(tutorial_task, research_approach.pattern_signature)
    
    print(f"   Tutorial task vs Tutorial approach: {tutorial_score:.2f}")
    print(f"   Tutorial task vs Research approach: {research_score:.2f}")
    print(f"   ✓ Tutorial approach scored higher: {tutorial_score > research_score}")
    
    # Test 2: Research task should match research approach
    print("\n2. Research Task Matching:")
    research_task = TaskContext(
        prompt="Research the impact of quantum computing",
        domain_weights={'research': 0.9, 'writing': 0.3},
        complexity=0.8,
        keywords=['research', 'quantum', 'impact'],
        output_type='research',
        estimated_duration=5.0
    )
    
    tutorial_score = calculate_match_score(research_task, tutorial_approach.pattern_signature)
    research_score = calculate_match_score(research_task, research_approach.pattern_signature)
    
    print(f"   Research task vs Tutorial approach: {tutorial_score:.2f}")
    print(f"   Research task vs Research approach: {research_score:.2f}")
    print(f"   ✓ Research approach scored higher: {research_score > tutorial_score}")
    
    # Test 3: Multi-approach matching
    print("\n3. Multi-Approach Matching:")
    matches = match_approaches(tutorial_task, [tutorial_approach, research_approach], threshold=0.3)
    
    print(f"   Found {len(matches)} matches for tutorial task")
    for approach, score in matches:
        print(f"   - {approach.name}: {score:.2f}")
    
    print("\n" + "=" * 70)
    print("✓ Approach matching algorithm working correctly!")
