"""
Pattern Analyzer
Discovers patterns in execution history for creating new approaches
"""

import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
from collections import Counter
from src.approach_patterns import (
    ExecutionRecord, PatternSignature, StyleCharacteristics,
    ApproachPattern, PerformanceMetrics
)
from src.execution_history import ExecutionHistory
from src.content_analyzer import ContentAnalyzer


@dataclass
class PatternCluster:
    """Represents a discovered pattern from clustered executions"""
    cluster_id: str
    records: List[ExecutionRecord]
    avg_quality: float
    feature_centroid: Dict[str, float]
    is_novel: bool = True
    is_consistent: bool = True
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'cluster_id': self.cluster_id,
            'record_count': len(self.records),
            'avg_quality': self.avg_quality,
            'feature_centroid': self.feature_centroid,
            'is_novel': self.is_novel,
            'is_consistent': self.is_consistent
        }


class PatternAnalyzer:
    """
    Discovers patterns in execution history using clustering
    """
    
    def __init__(
        self,
        history: Optional[ExecutionHistory] = None,
        patterns_path: str = "data/patterns"
    ):
        self.history = history or ExecutionHistory()
        self.content_analyzer = ContentAnalyzer()
        self.patterns_path = Path(patterns_path)
        self.patterns_path.mkdir(parents=True, exist_ok=True)
    
    def discover_patterns(
        self,
        min_cluster_size: int = 10,
        min_quality: float = 0.8,
        similarity_threshold: float = 0.7
    ) -> List[PatternCluster]:
        """
        Discover patterns in successful executions using simple clustering
        
        Args:
            min_cluster_size: Minimum records to form a cluster
            min_quality: Minimum quality for successful executions
            similarity_threshold: Threshold for considering records similar (0-1)
            
        Returns:
            List of PatternCluster objects
        """
        # Get successful executions
        successful = self.history.get_records(min_quality=min_quality)
        
        if len(successful) < min_cluster_size:
            print(f"Not enough successful executions: {len(successful)} < {min_cluster_size}")
            return []
        
        print(f"Analyzing {len(successful)} successful executions...")
        
        # Extract feature vectors
        feature_vectors = []
        for record in successful:
            features = self.extract_feature_vector(record)
            feature_vectors.append(features)
        
        # Simple threshold-based clustering
        clusters = self._cluster_by_similarity(
            successful,
            feature_vectors,
            similarity_threshold,
            min_cluster_size
        )
        
        print(f"Found {len(clusters)} clusters")
        
        # Analyze each cluster
        pattern_clusters = []
        for i, (cluster_records, cluster_features) in enumerate(clusters):
            cluster = self._analyze_cluster(
                f"cluster_{i}",
                cluster_records,
                cluster_features
            )
            pattern_clusters.append(cluster)
        
        # Save discovered patterns
        self._save_patterns(pattern_clusters)
        
        return pattern_clusters
    
    def extract_feature_vector(self, record: ExecutionRecord) -> Dict[str, float]:
        """
        Convert execution record to feature dictionary for clustering
        
        Features include:
        - Domain weights
        - Complexity
        - Output type
        - Content characteristics
        """
        features = {}
        
        # Domain features (normalized)
        domain_names = ['research', 'writing', 'coding', 'review', 'comparison', 'analysis']
        for domain in domain_names:
            features[f'domain_{domain}'] = record.task_context.domain_weights.get(domain, 0.0)
        
        # Complexity
        features['complexity'] = record.task_context.complexity
        
        # Output type (one-hot encoding)
        output_types = ['tutorial', 'code', 'explanation', 'list', 'comparison', 'report']
        for otype in output_types:
            features[f'output_{otype}'] = 1.0 if record.task_context.output_type == otype else 0.0
        
        # Content features (if available)
        if record.content_features:
            cf = record.content_features
            features['has_code'] = 1.0 if cf.has_code_blocks else 0.0
            features['has_numbered_list'] = 1.0 if cf.has_numbered_list else 0.0
            features['has_bullets'] = 1.0 if cf.has_bullets else 0.0
            features['section_count'] = min(1.0, cf.section_count / 10.0)  # Normalize
            features['code_ratio'] = cf.code_ratio
            features['explanation_ratio'] = cf.explanation_ratio
            features['example_ratio'] = cf.example_ratio
            features['formality'] = cf.formality_score
        
        return features
    
    def _cluster_by_similarity(
        self,
        records: List[ExecutionRecord],
        feature_vectors: List[Dict[str, float]],
        threshold: float,
        min_size: int
    ) -> List[Tuple[List[ExecutionRecord], List[Dict[str, float]]]]:
        """
        Simple threshold-based clustering
        Groups records that are similar above threshold
        """
        clusters = []
        used = set()
        
        for i, (record, features) in enumerate(zip(records, feature_vectors)):
            if i in used:
                continue
            
            # Start new cluster with this record
            cluster_records = [record]
            cluster_features = [features]
            used.add(i)
            
            # Find similar records
            for j, (other_record, other_features) in enumerate(zip(records, feature_vectors)):
                if j in used or j == i:
                    continue
                
                # Calculate similarity
                similarity = self._calculate_similarity(features, other_features)
                
                if similarity >= threshold:
                    cluster_records.append(other_record)
                    cluster_features.append(other_features)
                    used.add(j)
            
            # Only keep clusters above minimum size
            if len(cluster_records) >= min_size:
                clusters.append((cluster_records, cluster_features))
        
        return clusters
    
    def _calculate_similarity(
        self,
        features1: Dict[str, float],
        features2: Dict[str, float]
    ) -> float:
        """
        Calculate cosine similarity between two feature vectors
        """
        # Get common keys
        keys = set(features1.keys()) & set(features2.keys())
        
        if not keys:
            return 0.0
        
        # Calculate dot product and magnitudes
        dot_product = sum(features1[k] * features2[k] for k in keys)
        mag1 = sum(features1[k] ** 2 for k in keys) ** 0.5
        mag2 = sum(features2[k] ** 2 for k in keys) ** 0.5
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
        
        # Cosine similarity
        return dot_product / (mag1 * mag2)
    
    def _analyze_cluster(
        self,
        cluster_id: str,
        records: List[ExecutionRecord],
        feature_vectors: List[Dict[str, float]]
    ) -> PatternCluster:
        """
        Analyze a cluster to determine its characteristics
        """
        # Calculate average quality
        avg_quality = sum(r.actual_quality for r in records) / len(records)
        
        # Calculate feature centroid (average of all features)
        centroid = {}
        all_keys = set()
        for features in feature_vectors:
            all_keys.update(features.keys())
        
        for key in all_keys:
            values = [f.get(key, 0.0) for f in feature_vectors]
            centroid[key] = sum(values) / len(values)
        
        # Check consistency (quality variance)
        quality_std = (sum((r.actual_quality - avg_quality) ** 2 for r in records) / len(records)) ** 0.5
        is_consistent = quality_std < 0.15  # Low variance = consistent
        
        return PatternCluster(
            cluster_id=cluster_id,
            records=records,
            avg_quality=avg_quality,
            feature_centroid=centroid,
            is_novel=True,  # Will be checked against existing approaches
            is_consistent=is_consistent
        )
    
    def extract_pattern_signature(self, cluster: PatternCluster) -> PatternSignature:
        """
        Extract pattern signature from cluster
        """
        records = cluster.records
        
        # Aggregate domain weights
        domain_weights = {}
        for record in records:
            for domain, weight in record.task_context.domain_weights.items():
                domain_weights[domain] = domain_weights.get(domain, 0.0) + weight * record.actual_quality
        
        # Normalize
        total = sum(domain_weights.values())
        if total > 0:
            domain_weights = {d: w/total for d, w in domain_weights.items()}
        
        # Complexity range
        complexities = [r.task_context.complexity for r in records]
        complexity_min = min(complexities)
        complexity_max = max(complexities)
        
        # Expand range slightly (10% on each side)
        range_span = complexity_max - complexity_min
        complexity_min = max(0.0, complexity_min - range_span * 0.1)
        complexity_max = min(1.0, complexity_max + range_span * 0.1)
        
        # Common keywords
        keyword_counts = Counter()
        for record in records:
            keyword_counts.update(record.task_context.keywords)
        
        top_keywords = [k for k, _ in keyword_counts.most_common(10)]
        keyword_weights = {
            k: count / len(records)
            for k, count in keyword_counts.items()
            if k in top_keywords
        }
        
        # Common output types
        output_types = [r.task_context.output_type for r in records]
        common_outputs = [ot for ot, _ in Counter(output_types).most_common(3)]
        
        # Boolean characteristics (>50% of records)
        has_code = sum(1 for r in records if r.content_features and r.content_features.has_code_blocks) / len(records) > 0.5
        has_examples = sum(1 for r in records if r.content_features and r.content_features.example_ratio > 0.3) / len(records) > 0.5
        has_theory = sum(1 for r in records if r.content_features and r.content_features.explanation_ratio > 0.4) / len(records) > 0.5
        
        return PatternSignature(
            domain_weights=domain_weights,
            complexity_min=complexity_min,
            complexity_max=complexity_max,
            keyword_patterns=top_keywords,
            keyword_weights=keyword_weights,
            output_types=common_outputs,
            requires_code=has_code,
            requires_examples=has_examples,
            requires_theory=has_theory
        )
    
    def extract_style_characteristics(self, cluster: PatternCluster) -> StyleCharacteristics:
        """
        Extract style characteristics from cluster
        """
        records = cluster.records
        
        # Filter records with content features
        records_with_features = [r for r in records if r.content_features]
        if not records_with_features:
            # Return default style
            return self._default_style()
        
        # Structure type (most common)
        structure_types = []
        for record in records_with_features:
            structure = self.content_analyzer.analyze_structure_type("")
            # Infer from features
            if record.content_features.has_numbered_list:
                structure_types.append("sequential_steps")
            elif record.content_features.has_bullets:
                structure_types.append("bulleted")
            elif record.content_features.section_count >= 4:
                structure_types.append("hierarchical")
            else:
                structure_types.append("prose")
        
        structure_type = Counter(structure_types).most_common(1)[0][0] if structure_types else "prose"
        
        # Section count range
        section_counts = [r.content_features.section_count for r in records_with_features]
        section_min = int(min(section_counts))
        section_max = int(max(section_counts))
        
        # Tone (most common detected tone)
        tones = [r.content_features.detected_tone for r in records_with_features]
        tone = Counter(tones).most_common(1)[0][0]
        
        # Voice (heuristic based on formality)
        avg_formality = sum(r.content_features.formality_score for r in records_with_features) / len(records_with_features)
        if avg_formality > 0.7:
            voice = "third_person"
        elif avg_formality < 0.3:
            voice = "first_person"
        else:
            voice = "second_person"
        
        # Depth level
        avg_length = sum(r.content_features.total_length for r in records_with_features) / len(records_with_features)
        if avg_length < 1000:
            depth_level = "concise"
        elif avg_length < 3000:
            depth_level = "moderate"
        elif avg_length < 5000:
            depth_level = "comprehensive"
        else:
            depth_level = "exhaustive"
        
        # Explanation style
        avg_explanation = sum(r.content_features.explanation_ratio for r in records_with_features) / len(records_with_features)
        avg_example = sum(r.content_features.example_ratio for r in records_with_features) / len(records_with_features)
        
        if avg_explanation > 0.6:
            explanation_style = "conceptual"
        elif avg_example > 0.4:
            explanation_style = "practical"
        else:
            explanation_style = "mixed"
        
        # Example density
        if avg_example < 0.2:
            example_density = "low"
        elif avg_example < 0.4:
            example_density = "medium"
        else:
            example_density = "high"
        
        # Code style
        avg_code = sum(r.content_features.code_ratio for r in records_with_features) / len(records_with_features)
        if avg_code < 0.05:
            code_style = None
        elif avg_code < 0.2:
            code_style = "minimal"
        elif avg_code < 0.4:
            code_style = "annotated"
        else:
            code_style = "production"
        
        # Organization elements (>50% have feature)
        use_headers = sum(1 for r in records_with_features if r.content_features.section_count > 1) / len(records_with_features) > 0.5
        use_bullets = sum(1 for r in records_with_features if r.content_features.has_bullets) / len(records_with_features) > 0.5
        use_numbered_lists = sum(1 for r in records_with_features if r.content_features.has_numbered_list) / len(records_with_features) > 0.5
        use_tables = sum(1 for r in records_with_features if r.content_features.has_tables) / len(records_with_features) > 0.5
        
        return StyleCharacteristics(
            structure_type=structure_type,
            section_count=(section_min, section_max),
            tone=tone,
            voice=voice,
            depth_level=depth_level,
            explanation_style=explanation_style,
            example_density=example_density,
            code_style=code_style,
            use_headers=use_headers,
            use_bullets=use_bullets,
            use_numbered_lists=use_numbered_lists,
            use_tables=use_tables,
            include_summary=True,  # Default
            include_tldr=False,
            include_prerequisites=tone == "educational",
            include_next_steps=structure_type == "sequential_steps"
        )
    
    def _default_style(self) -> StyleCharacteristics:
        """Return default style characteristics"""
        return StyleCharacteristics(
            structure_type="prose",
            section_count=(2, 5),
            tone="neutral",
            voice="third_person",
            depth_level="moderate",
            explanation_style="mixed",
            example_density="medium",
            code_style=None,
            use_headers=True,
            use_bullets=False,
            use_numbered_lists=False,
            use_tables=False,
            include_summary=False,
            include_tldr=False,
            include_prerequisites=False,
            include_next_steps=False
        )
    
    def _save_patterns(self, clusters: List[PatternCluster]):
        """Save discovered patterns to file"""
        patterns_file = self.patterns_path / "discovered_patterns.json"
        
        data = {
            'discovered_at': datetime.now().isoformat(),
            'cluster_count': len(clusters),
            'clusters': [c.to_dict() for c in clusters]
        }
        
        with open(patterns_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def check_novelty(
        self,
        cluster: PatternCluster,
        existing_approaches: List[ApproachPattern],
        threshold: float = 0.85
    ) -> bool:
        """
        Check if cluster represents a novel pattern
        Returns True if novel (not too similar to existing approaches)
        """
        cluster_signature = self.extract_pattern_signature(cluster)
        
        for approach in existing_approaches:
            similarity = self._calculate_signature_similarity(
                cluster_signature,
                approach.pattern_signature
            )
            
            if similarity > threshold:
                return False  # Too similar to existing
        
        return True  # Novel pattern
    
    def _calculate_signature_similarity(
        self,
        sig1: PatternSignature,
        sig2: PatternSignature
    ) -> float:
        """Calculate similarity between two pattern signatures"""
        scores = []
        
        # Domain overlap
        domain_sim = 0.0
        for domain in sig1.domain_weights:
            w1 = sig1.domain_weights.get(domain, 0.0)
            w2 = sig2.domain_weights.get(domain, 0.0)
            domain_sim += min(w1, w2)
        scores.append(domain_sim)
        
        # Complexity overlap
        range1 = (sig1.complexity_min, sig1.complexity_max)
        range2 = (sig2.complexity_min, sig2.complexity_max)
        overlap = max(0, min(range1[1], range2[1]) - max(range1[0], range2[0]))
        union = max(range1[1], range2[1]) - min(range1[0], range2[0])
        complexity_sim = overlap / union if union > 0 else 0
        scores.append(complexity_sim)
        
        # Keyword overlap
        keywords1 = set(sig1.keyword_patterns)
        keywords2 = set(sig2.keyword_patterns)
        if keywords1 or keywords2:
            keyword_sim = len(keywords1 & keywords2) / len(keywords1 | keywords2)
            scores.append(keyword_sim)
        
        # Output type overlap
        outputs1 = set(sig1.output_types)
        outputs2 = set(sig2.output_types)
        if outputs1 or outputs2:
            output_sim = len(outputs1 & outputs2) / len(outputs1 | outputs2)
            scores.append(output_sim)
        
        # Average similarity
        return sum(scores) / len(scores) if scores else 0.0


if __name__ == "__main__":
    # Demo usage
    print("Pattern Analyzer Demo")
    print("=" * 70)
    
    # Note: This demo requires execution history data
    # For real usage, run after collecting execution records
    
    analyzer = PatternAnalyzer()
    
    print("\nPattern Analyzer initialized")
    print("To discover patterns, first collect execution records")
    print("Then run: analyzer.discover_patterns()")
    
    print("\n" + "=" * 70)
    print("✓ PatternAnalyzer ready for use!")
