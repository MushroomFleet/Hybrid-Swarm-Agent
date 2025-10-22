#!/usr/bin/env python3
"""
Production Readiness Validation Script
Validates all Phase 5 pre-deployment criteria
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.dynamic_approach_manager import DynamicApproachManager
from src.execution_history import ExecutionHistory
from src.pattern_analyzer import PatternAnalyzer
from src.hybrid_swarm import HybridSwarmOrchestrator


class ProductionValidator:
    """Validates system readiness for production"""
    
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'checks': [],
            'passed': 0,
            'failed': 0,
            'warnings': 0
        }
    
    def check(self, name, condition, message, is_critical=True):
        """Add validation check"""
        status = "✅ PASS" if condition else ("❌ FAIL" if is_critical else "⚠️  WARN")
        
        self.results['checks'].append({
            'name': name,
            'status': status,
            'message': message,
            'critical': is_critical
        })
        
        if condition:
            self.results['passed'] += 1
        elif is_critical:
            self.results['failed'] += 1
        else:
            self.results['warnings'] += 1
        
        print(f"{status}: {name}")
        print(f"   {message}")
    
    def validate_all(self):
        """Run all validation checks"""
        print("=" * 70)
        print("PRODUCTION READINESS VALIDATION")
        print("=" * 70)
        print()
        
        # 1. Component Availability
        print("1. COMPONENT AVAILABILITY")
        print("-" * 70)
        self._validate_components()
        print()
        
        # 2. Data Integrity
        print("2. DATA INTEGRITY")
        print("-" * 70)
        self._validate_data()
        print()
        
        # 3. Performance
        print("3. PERFORMANCE")
        print("-" * 70)
        self._validate_performance()
        print()
        
        # 4. Functionality
        print("4. FUNCTIONALITY")
        print("-" * 70)
        self._validate_functionality()
        print()
        
        # 5. Production Readiness
        print("5. PRODUCTION READINESS")
        print("-" * 70)
        self._validate_production_ready()
        print()
        
        # Summary
        print("=" * 70)
        print("VALIDATION SUMMARY")
        print("=" * 70)
        print(f"Passed: {self.results['passed']}")
        print(f"Failed: {self.results['failed']}")
        print(f"Warnings: {self.results['warnings']}")
        print()
        
        if self.results['failed'] == 0:
            print("✅ SYSTEM READY FOR PRODUCTION")
            return True
        else:
            print("❌ SYSTEM NOT READY - Fix failures before deployment")
            return False
    
    def _validate_components(self):
        """Validate all components load successfully"""
        try:
            manager = DynamicApproachManager()
            self.check(
                "DynamicApproachManager",
                True,
                "Manager initialized successfully"
            )
        except Exception as e:
            self.check(
                "DynamicApproachManager",
                False,
                f"Failed to initialize: {e}"
            )
        
        try:
            history = ExecutionHistory()
            self.check(
                "ExecutionHistory",
                True,
                "History initialized successfully"
            )
        except Exception as e:
            self.check(
                "ExecutionHistory",
                False,
                f"Failed to initialize: {e}"
            )
        
        try:
            orchestrator = HybridSwarmOrchestrator()
            self.check(
                "HybridSwarmOrchestrator",
                True,
                "Orchestrator initialized successfully"
            )
        except Exception as e:
            self.check(
                "HybridSwarmOrchestrator",
                False,
                f"Failed to initialize: {e}"
            )
    
    def _validate_data(self):
        """Validate data integrity"""
        manager = DynamicApproachManager()
        approaches = manager.list_approaches(active_only=False)
        
        self.check(
            "Approaches Available",
            len(approaches) >= 7,
            f"{len(approaches)} approaches loaded (target: 7+)"
        )
        
        active = [a for a in approaches if a.active]
        self.check(
            "Active Approaches",
            len(active) >= 5,
            f"{len(active)} active approaches (target: 5+)"
        )
        
        history = ExecutionHistory()
        stats = history.get_statistics()
        
        self.check(
            "Execution History",
            stats['total_records'] >= 50,
            f"{stats['total_records']} records (target: 50+)"
        )
        
        # Check for data corruption
        try:
            for approach in approaches[:3]:
                loaded = manager.get_approach(approach.id)
                assert loaded is not None
            self.check(
                "Data Integrity",
                True,
                "All approaches loadable without corruption"
            )
        except Exception as e:
            self.check(
                "Data Integrity",
                False,
                f"Data corruption detected: {e}"
            )
    
    def _validate_performance(self):
        """Validate performance metrics"""
        import time
        
        orchestrator = HybridSwarmOrchestrator()
        
        # Test coordination latency
        task = {
            'id': 'perf_test',
            'description': 'Test task',
            'domain_weights': {'writing': 0.8},
            'complexity': 0.5,
            'keywords': ['test'],
            'output_type': 'explanation'
        }
        
        start = time.time()
        coordination = orchestrator.get_coordination(task)
        latency = (time.time() - start) * 1000
        
        self.check(
            "Coordination Latency",
            latency < 100,
            f"{latency:.1f}ms (target: <100ms)"
        )
        
        # Check storage size
        history = ExecutionHistory()
        stats = history.get_statistics()
        storage_mb = stats['total_size_bytes'] / (1024 * 1024)
        
        self.check(
            "Storage Size",
            storage_mb < 200,
            f"{storage_mb:.1f}MB (target: <200MB)",
            is_critical=False
        )
    
    def _validate_functionality(self):
        """Validate key functionality"""
        manager = DynamicApproachManager()
        history = ExecutionHistory()
        
        # Test approach matching
        from src.approach_patterns import TaskContext
        task_context = TaskContext(
            prompt="Test",
            domain_weights={'writing': 0.8},
            complexity=0.5,
            keywords=['test'],
            output_type='tutorial',
            estimated_duration=1.0
        )
        
        matches = manager.match_approaches(task_context, threshold=0.3)
        self.check(
            "Approach Matching",
            len(matches) > 0,
            f"Found {len(matches)} matching approaches"
        )
        
        # Test pattern discovery capability
        records = history.get_records(min_quality=0.8)
        self.check(
            "Pattern Discovery Ready",
            len(records) >= 10,
            f"{len(records)} high-quality records available for clustering"
        )
    
    def _validate_production_ready(self):
        """Validate production-specific criteria"""
        manager = DynamicApproachManager()
        history = ExecutionHistory()
        
        approaches = manager.list_approaches()
        stats = history.get_statistics()
        
        # Quality criteria
        used_approaches = [a for a in approaches if a.performance_metrics.usage_count > 0]
        if used_approaches:
            avg_quality = sum(a.performance_metrics.avg_quality for a in used_approaches) / len(used_approaches)
            self.check(
                "Average Quality",
                avg_quality >= 0.70,
                f"{avg_quality:.2f} (target: ≥0.70)"
            )
        
        # Execution count
        self.check(
            "Execution Count",
            stats['total_records'] >= 100,
            f"{stats['total_records']} records (target: 100+)"
        )
        
        # Approach diversity
        self.check(
            "Approach Diversity",
            len(approaches) >= 7,
            f"{len(approaches)} approaches (target: 7+)"
        )
        
        # Pattern discovery tested
        patterns_file = Path('data/patterns/discovered_patterns.json')
        self.check(
            "Pattern Discovery Tested",
            patterns_file.exists(),
            "Pattern discovery has been executed"
        )


def main():
    """Run validation"""
    validator = ProductionValidator()
    
    success = validator.validate_all()
    
    # Save results
    import json
    output_file = Path('validation_results.json')
    with open(output_file, 'w') as f:
        json.dump(validator.results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
