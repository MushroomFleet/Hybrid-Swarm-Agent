"""
Approach Evolution Module
Handles creation, evolution, and pruning of dynamic approaches
"""

import re
from datetime import datetime, timedelta
from typing import List, Optional, Tuple, Dict
from collections import Counter
from src.approach_patterns import (
    ApproachPattern, PatternSignature, StyleCharacteristics,
    PerformanceMetrics, ExecutionRecord
)
from src.pattern_analyzer import PatternCluster
from src.dynamic_approach_manager import DynamicApproachManager


class ApproachEvolution:
    """
    Manages the lifecycle of dynamic approaches:
    - Creation from discovered patterns
    - Evolution based on performance
    - Pruning of ineffective approaches
    """
    
    def __init__(self, manager: Optional[DynamicApproachManager] = None):
        self.manager = manager or DynamicApproachManager()
    
    def create_approach_from_cluster(
        self,
        cluster: PatternCluster,
        signature: PatternSignature,
        style: StyleCharacteristics
    ) -> Optional[ApproachPattern]:
        """
        Create a new approach from a discovered pattern cluster
        
        Args:
            cluster: PatternCluster with execution data
            signature: Extracted pattern signature
            style: Extracted style characteristics
            
        Returns:
            ApproachPattern if creation successful, None otherwise
        """
        # Check novelty
        existing_approaches = self.manager.list_approaches()
        if not self._is_novel(signature, existing_approaches):
            print(f"Pattern too similar to existing approaches")
            return None
        
        # Generate unique ID
        approach_id = self._generate_approach_id(signature, style)
        
        # Check if ID already exists
        if self.manager.get_approach(approach_id):
            # Add suffix to make unique
            approach_id = f"{approach_id}_{len(existing_approaches) + 1}"
        
        # Generate name
        name = self._generate_approach_name(signature, style)
        
        # Initialize performance metrics with expected quality from cluster
        metrics = PerformanceMetrics(
            usage_count=0,
            first_used=datetime.now(),
            last_used=datetime.now(),
            avg_quality=cluster.avg_quality,  # Expected quality
            min_quality=0.0,
            max_quality=0.0,
            quality_std_dev=0.0,
            success_count=0,
            failure_count=0,
            success_rate=0.0,
            vs_alternatives={},
            recent_quality_trend="new",
            quality_history=[]
        )
        
        # Extract tags
        tags = self._generate_tags(signature, style)
        
        # Create approach
        approach = ApproachPattern(
            id=approach_id,
            name=name,
            version=1,
            created_at=datetime.now(),
            last_updated=datetime.now(),
            pattern_signature=signature,
            style_characteristics=style,
            performance_metrics=metrics,
            parent_id=None,
            generation=0,
            tags=tags,
            active=True
        )
        
        # Validate
        if not self._validate_approach(approach):
            print(f"Created approach failed validation")
            return None
        
        # Save
        success = self.manager.create_approach(approach)
        if success:
            print(f"✓ Created new approach: {name} (ID: {approach_id})")
            return approach
        else:
            print(f"Failed to save approach: {name}")
            return None
    
    def _is_novel(
        self,
        signature: PatternSignature,
        existing_approaches: List[ApproachPattern],
        threshold: float = 0.85
    ) -> bool:
        """Check if pattern signature is sufficiently novel"""
        for approach in existing_approaches:
            similarity = self._calculate_signature_similarity(
                signature,
                approach.pattern_signature
            )
            if similarity > threshold:
                return False
        return True
    
    def _calculate_signature_similarity(
        self,
        sig1: PatternSignature,
        sig2: PatternSignature
    ) -> float:
        """Calculate similarity between two pattern signatures"""
        scores = []
        
        # Domain overlap
        domain_sim = 0.0
        all_domains = set(sig1.domain_weights.keys()) | set(sig2.domain_weights.keys())
        for domain in all_domains:
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
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def _generate_approach_id(
        self,
        signature: PatternSignature,
        style: StyleCharacteristics
    ) -> str:
        """Generate unique approach ID from signature and style"""
        # Get primary domain
        primary_domain = max(signature.domain_weights.items(), key=lambda x: x[1])[0] if signature.domain_weights else "general"
        
        # Get primary keyword
        primary_keyword = signature.keyword_patterns[0] if signature.keyword_patterns else "content"
        
        # Clean and format
        domain_clean = re.sub(r'[^a-z0-9]', '', primary_domain.lower())
        keyword_clean = re.sub(r'[^a-z0-9]', '', primary_keyword.lower())
        structure_clean = re.sub(r'[^a-z0-9]', '', style.structure_type.lower())
        
        return f"approach_{domain_clean}_{keyword_clean}_{structure_clean}"
    
    def _generate_approach_name(
        self,
        signature: PatternSignature,
        style: StyleCharacteristics
    ) -> str:
        """Generate human-readable name for approach"""
        # Get primary domain
        primary_domain = max(signature.domain_weights.items(), key=lambda x: x[1])[0] if signature.domain_weights else "General"
        
        # Get style descriptor
        style_desc = style.tone.capitalize()
        
        # Get structure descriptor
        structure_map = {
            "sequential_steps": "Step-by-Step",
            "hierarchical": "Structured",
            "prose": "Narrative",
            "bulleted": "List-Based"
        }
        structure_desc = structure_map.get(style.structure_type, style.structure_type.capitalize())
        
        # Get output type
        output_type = signature.output_types[0].capitalize() if signature.output_types else "Content"
        
        return f"{style_desc} {structure_desc} {output_type} ({primary_domain.capitalize()})"
    
    def _generate_tags(
        self,
        signature: PatternSignature,
        style: StyleCharacteristics
    ) -> List[str]:
        """Generate tags for approach"""
        tags = []
        
        # Add primary domains
        for domain, weight in sorted(signature.domain_weights.items(), key=lambda x: x[1], reverse=True)[:2]:
            if weight > 0.3:
                tags.append(domain)
        
        # Add style tags
        tags.append(style.tone)
        tags.append(style.structure_type)
        
        # Add content tags
        if signature.requires_code:
            tags.append("code")
        if signature.requires_examples:
            tags.append("examples")
        if signature.requires_theory:
            tags.append("theory")
        
        # Add depth tag
        tags.append(style.depth_level)
        
        return tags
    
    def _validate_approach(self, approach: ApproachPattern) -> bool:
        """Validate approach is well-formed"""
        # Check required fields
        if not approach.id or not approach.name:
            return False
        
        # Check signature has domains
        if not approach.pattern_signature.domain_weights:
            return False
        
        # Check complexity range is valid
        sig = approach.pattern_signature
        if sig.complexity_min < 0 or sig.complexity_max > 1 or sig.complexity_min > sig.complexity_max:
            return False
        
        # Check style section count is valid
        style = approach.style_characteristics
        if style.section_count[0] < 0 or style.section_count[1] < style.section_count[0]:
            return False
        
        return True
    
    def evolve_approach(
        self,
        approach_id: str,
        recent_executions: List[ExecutionRecord],
        min_executions: int = 20,
        min_quality_improvement: float = 0.05
    ) -> Optional[ApproachPattern]:
        """
        Evolve an approach based on recent performance
        
        Args:
            approach_id: ID of approach to evolve
            recent_executions: Recent execution records using this approach
            min_executions: Minimum executions before evolution
            min_quality_improvement: Minimum improvement to trigger evolution
            
        Returns:
            Evolved ApproachPattern if evolved, None otherwise
        """
        # Load current approach
        approach = self.manager.get_approach(approach_id)
        if not approach:
            print(f"Approach {approach_id} not found")
            return None
        
        # Check if enough executions
        if len(recent_executions) < min_executions:
            print(f"Not enough executions ({len(recent_executions)} < {min_executions})")
            return None
        
        # Calculate recent average quality
        recent_avg_quality = sum(e.actual_quality for e in recent_executions) / len(recent_executions)
        
        # Check if quality improved enough
        if recent_avg_quality <= approach.performance_metrics.avg_quality + min_quality_improvement:
            print(f"Quality not improved enough ({recent_avg_quality:.3f} vs {approach.performance_metrics.avg_quality:.3f})")
            return None
        
        # Check evolution frequency (don't evolve too often)
        if approach.last_updated and (datetime.now() - approach.last_updated).days < 7:
            print(f"Too soon since last update ({(datetime.now() - approach.last_updated).days} days)")
            return None
        
        print(f"Evolving approach {approach.name}...")
        
        # Create evolved version
        import copy
        evolved = copy.deepcopy(approach)
        evolved.version += 1
        evolved.last_updated = datetime.now()
        evolved.parent_id = approach.id
        evolved.generation = approach.generation + 1
        evolved.id = f"{approach.id}_v{evolved.version}"
        
        # Refine pattern signature based on high-quality executions
        high_quality_executions = [e for e in recent_executions if e.actual_quality >= 0.85]
        if high_quality_executions:
            evolved.pattern_signature = self._refine_signature(
                evolved.pattern_signature,
                high_quality_executions
            )
        
        # Refine style characteristics
        if high_quality_executions:
            evolved.style_characteristics = self._refine_style(
                evolved.style_characteristics,
                high_quality_executions
            )
        
        # Update performance metrics (inherit and boost)
        evolved.performance_metrics.avg_quality = recent_avg_quality
        
        # Save evolved approach
        success = self.manager.create_approach(evolved)
        if success:
            print(f"✓ Created evolved approach: {evolved.name} v{evolved.version}")
            return evolved
        else:
            print(f"Failed to save evolved approach")
            return None
    
    def _refine_signature(
        self,
        signature: PatternSignature,
        high_quality_executions: List[ExecutionRecord]
    ) -> PatternSignature:
        """Refine signature based on high-quality executions"""
        import copy
        refined = copy.deepcopy(signature)
        
        # Adjust domain weights toward successful executions (80% old, 20% new)
        new_domain_weights = {}
        for record in high_quality_executions:
            for domain, weight in record.task_context.domain_weights.items():
                new_domain_weights[domain] = new_domain_weights.get(domain, 0.0) + weight * record.actual_quality
        
        total = sum(new_domain_weights.values())
        if total > 0:
            new_domain_weights = {d: w/total for d, w in new_domain_weights.items()}
            
            # Blend with existing
            for domain in refined.domain_weights:
                old_weight = refined.domain_weights[domain]
                new_weight = new_domain_weights.get(domain, 0.0)
                refined.domain_weights[domain] = 0.8 * old_weight + 0.2 * new_weight
        
        # Refine complexity range
        complexities = [e.task_context.complexity for e in high_quality_executions]
        if complexities:
            refined.complexity_min = min(refined.complexity_min, min(complexities))
            refined.complexity_max = max(refined.complexity_max, max(complexities))
        
        return refined
    
    def _refine_style(
        self,
        style: StyleCharacteristics,
        high_quality_executions: List[ExecutionRecord]
    ) -> StyleCharacteristics:
        """Refine style based on high-quality executions"""
        import copy
        refined = copy.deepcopy(style)
        
        # Adjust section count range
        executions_with_features = [e for e in high_quality_executions if e.content_features]
        if executions_with_features:
            section_counts = [e.content_features.section_count for e in executions_with_features]
            refined.section_count = (
                min(refined.section_count[0], min(section_counts)),
                max(refined.section_count[1], max(section_counts))
            )
        
        return refined
    
    def prune_approaches(
        self,
        min_usage_for_evaluation: int = 20,
        max_age_no_traction_days: int = 30,
        min_quality_threshold: float = 0.6,
        min_success_rate: float = 0.5,
        dry_run: bool = True
    ) -> List[str]:
        """
        Identify and prune underperforming approaches
        
        Args:
            min_usage_for_evaluation: Minimum usage before quality evaluation
            max_age_no_traction_days: Max days with low usage before pruning
            min_quality_threshold: Minimum average quality to keep
            min_success_rate: Minimum success rate to keep
            dry_run: If True, only identify candidates without pruning
            
        Returns:
            List of pruned (or candidate) approach IDs
        """
        all_approaches = self.manager.list_approaches(active_only=True)
        pruned_ids = []
        current_time = datetime.now()
        
        for approach in all_approaches:
            age_days = (current_time - approach.created_at).days
            metrics = approach.performance_metrics
            
            should_prune = False
            reason = ""
            
            # Criterion 1: No traction after sufficient time
            if age_days > max_age_no_traction_days and metrics.usage_count < 5:
                should_prune = True
                reason = f"no traction ({metrics.usage_count} uses in {age_days} days)"
            
            # Criterion 2: Consistently poor quality
            elif metrics.usage_count >= min_usage_for_evaluation:
                if metrics.avg_quality < min_quality_threshold:
                    should_prune = True
                    reason = f"low quality ({metrics.avg_quality:.2f} < {min_quality_threshold})"
                
                elif metrics.success_rate < min_success_rate:
                    should_prune = True
                    reason = f"low success rate ({metrics.success_rate:.1%} < {min_success_rate:.1%})"
            
            # Criterion 3: Superseded by better alternatives
            if not should_prune and metrics.usage_count >= min_usage_for_evaluation:
                similar = self._find_similar_approaches(approach, all_approaches, threshold=0.7)
                for similar_approach in similar:
                    if similar_approach.id == approach.id:
                        continue
                    
                    similar_metrics = similar_approach.performance_metrics
                    if similar_metrics.usage_count < min_usage_for_evaluation:
                        continue
                    
                    # Compare performance
                    quality_diff = similar_metrics.avg_quality - metrics.avg_quality
                    usage_diff = similar_metrics.usage_count - metrics.usage_count
                    
                    if quality_diff > 0.15 and usage_diff > 50:
                        should_prune = True
                        reason = f"superseded by {similar_approach.name}"
                        break
            
            if should_prune:
                pruned_ids.append(approach.id)
                if dry_run:
                    print(f"Would prune: {approach.name} - {reason}")
                else:
                    success = self.manager.delete_approach(approach.id)
                    if success:
                        print(f"✓ Pruned: {approach.name} - {reason}")
                    else:
                        print(f"✗ Failed to prune: {approach.name}")
        
        if dry_run and pruned_ids:
            print(f"\nDry run complete: {len(pruned_ids)} candidates for pruning")
        elif not dry_run:
            print(f"\nPruning complete: {len(pruned_ids)} approaches pruned")
        
        return pruned_ids
    
    def _find_similar_approaches(
        self,
        approach: ApproachPattern,
        all_approaches: List[ApproachPattern],
        threshold: float = 0.7
    ) -> List[ApproachPattern]:
        """Find approaches similar to the given approach"""
        similar = []
        for other in all_approaches:
            if other.id == approach.id:
                continue
            
            similarity = self._calculate_signature_similarity(
                approach.pattern_signature,
                other.pattern_signature
            )
            
            if similarity >= threshold:
                similar.append(other)
        
        return similar


if __name__ == "__main__":
    # Demo usage
    print("Approach Evolution Demo")
    print("=" * 70)
    
    evolution = ApproachEvolution()
    
    print("\nApproachEvolution module initialized")
    print("Main capabilities:")
    print("  - create_approach_from_cluster() - Create from pattern")
    print("  - evolve_approach() - Refine based on performance")
    print("  - prune_approaches() - Remove underperformers")
    
    print("\n" + "=" * 70)
    print("✓ ApproachEvolution ready for use!")
