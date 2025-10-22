"""
Approach Storage Layer
File-based storage for dynamic approach patterns
"""

import json
import threading
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime
from src.approach_patterns import ApproachPattern
from src.input_sanitization import sanitize_filename, sanitize_identifier


class ApproachStorage:
    """
    Manages persistent storage of approach patterns
    Uses JSON files with manifest for indexing
    """
    
    def __init__(self, storage_path: str = "data/approaches"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.manifest_path = self.storage_path / "manifest.json"
        self.lock = threading.RLock()  # Reentrant lock to prevent deadlock
        
        # Initialize or load manifest
        self.manifest = self._load_or_create_manifest()
    
    def _load_or_create_manifest(self) -> Dict:
        """Load existing manifest or create new one"""
        if self.manifest_path.exists():
            try:
                with open(self.manifest_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading manifest: {e}, creating new")
        
        # Create new manifest
        manifest = {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "total_approaches": 0,
            "active_approaches": 0,
            "deprecated_approaches": 0,
            "approaches": []
        }
        
        self._save_manifest(manifest)
        return manifest
    
    def _save_manifest(self, manifest: Dict):
        """Save manifest to file"""
        manifest['last_updated'] = datetime.now().isoformat()
        
        # Atomic write (write to temp, then rename)
        temp_path = self.manifest_path.with_suffix('.tmp')
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)
        
        # Rename to actual file (atomic on most systems)
        temp_path.replace(self.manifest_path)
    
    def _get_approach_path(self, approach_id: str) -> Path:
        """Get file path for an approach"""
        # Sanitize ID for safe filename
        safe_id = sanitize_identifier(approach_id)
        filename = sanitize_filename(f"{safe_id}.json")
        return self.storage_path / filename
    
    def save_approach(self, approach: ApproachPattern) -> bool:
        """
        Save approach to storage
        
        Args:
            approach: Approach to save
            
        Returns:
            True if successful
        """
        with self.lock:
            try:
                # Save approach to file
                filepath = self._get_approach_path(approach.id)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(approach.to_json())
                
                # Update manifest
                self._update_manifest_for_save(approach)
                
                return True
                
            except Exception as e:
                print(f"Error saving approach {approach.id}: {e}")
                return False
    
    def load_approach(self, approach_id: str) -> Optional[ApproachPattern]:
        """
        Load approach from storage
        
        Args:
            approach_id: ID of approach to load
            
        Returns:
            ApproachPattern if found, None otherwise
        """
        with self.lock:
            try:
                filepath = self._get_approach_path(approach_id)
                
                if not filepath.exists():
                    return None
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    json_data = f.read()
                
                return ApproachPattern.from_json(json_data)
                
            except Exception as e:
                print(f"Error loading approach {approach_id}: {e}")
                return None
    
    def delete_approach(self, approach_id: str) -> bool:
        """
        Soft delete approach (mark as inactive in manifest)
        
        Args:
            approach_id: ID of approach to delete
            
        Returns:
            True if successful
        """
        with self.lock:
            try:
                # Load approach
                approach = self.load_approach(approach_id)
                if not approach:
                    return False
                
                # Mark inactive
                approach.active = False
                approach.last_updated = datetime.now()
                
                # Save back
                self.save_approach(approach)
                
                return True
                
            except Exception as e:
                print(f"Error deleting approach {approach_id}: {e}")
                return False
    
    def list_approaches(
        self,
        active_only: bool = True,
        min_quality: float = 0.0
    ) -> List[str]:
        """
        List approach IDs matching criteria
        
        Args:
            active_only: Only include active approaches
            min_quality: Minimum average quality
            
        Returns:
            List of approach IDs
        """
        with self.lock:
            approach_ids = []
            
            for entry in self.manifest['approaches']:
                if active_only and not entry.get('active', True):
                    continue
                
                if entry.get('avg_quality', 0.0) < min_quality:
                    continue
                
                approach_ids.append(entry['id'])
            
            return approach_ids
    
    def get_statistics(self) -> Dict:
        """Get storage statistics"""
        with self.lock:
            return {
                'total_approaches': self.manifest['total_approaches'],
                'active_approaches': self.manifest['active_approaches'],
                'deprecated_approaches': self.manifest['deprecated_approaches'],
                'storage_path': str(self.storage_path),
                'manifest_size': self.manifest_path.stat().st_size if self.manifest_path.exists() else 0
            }
    
    def _update_manifest_for_save(self, approach: ApproachPattern):
        """Update manifest when saving an approach"""
        # Find existing entry
        existing_idx = None
        for idx, entry in enumerate(self.manifest['approaches']):
            if entry['id'] == approach.id:
                existing_idx = idx
                break
        
        # Create entry
        entry = {
            'id': approach.id,
            'name': approach.name,
            'file': self._get_approach_path(approach.id).name,
            'active': approach.active,
            'usage_count': approach.performance_metrics.usage_count,
            'avg_quality': approach.performance_metrics.avg_quality,
            'last_updated': approach.last_updated.isoformat()
        }
        
        if existing_idx is not None:
            # Update existing
            self.manifest['approaches'][existing_idx] = entry
        else:
            # Add new
            self.manifest['approaches'].append(entry)
            self.manifest['total_approaches'] += 1
        
        # Update counts
        active_count = sum(1 for e in self.manifest['approaches'] if e.get('active', True))
        self.manifest['active_approaches'] = active_count
        self.manifest['deprecated_approaches'] = self.manifest['total_approaches'] - active_count
        
        # Save manifest
        self._save_manifest(self.manifest)


if __name__ == "__main__":
    # Demo usage
    print("Approach Storage Demo")
    print("=" * 70)
    
    from src.approach_patterns import ApproachPattern, PatternSignature, StyleCharacteristics, PerformanceMetrics
    
    # Create test storage
    storage = ApproachStorage("data/approaches")
    
    # Create test approach
    approach = ApproachPattern(
        id="test_storage_approach",
        name="Test Storage Approach",
        version=1,
        created_at=datetime.now(),
        last_updated=datetime.now(),
        pattern_signature=PatternSignature(
            domain_weights={'writing': 0.9},
            complexity_min=0.3,
            complexity_max=0.8,
            keyword_patterns=['test'],
            keyword_weights={'test': 0.9},
            output_types=['test'],
            requires_code=False,
            requires_examples=True,
            requires_theory=False
        ),
        style_characteristics=StyleCharacteristics(
            structure_type="test",
            section_count=(2, 5),
            tone="casual",
            voice="first_person",
            depth_level="concise",
            explanation_style="practical",
            example_density="low",
            code_style=None,
            use_headers=True,
            use_bullets=True,
            use_numbered_lists=False,
            use_tables=False,
            include_summary=True,
            include_tldr=False,
            include_prerequisites=False,
            include_next_steps=False
        ),
        performance_metrics=PerformanceMetrics(
            usage_count=5,
            first_used=datetime.now(),
            last_used=datetime.now(),
            avg_quality=0.85,
            min_quality=0.75,
            max_quality=0.95,
            quality_std_dev=0.08,
            success_count=5,
            failure_count=0,
            success_rate=1.0,
            vs_alternatives={},
            recent_quality_trend="stable",
            quality_history=[]
        ),
        generation=0,
        tags=["test", "demo"]
    )
    
    # Test save
    print("\n1. Saving Approach:")
    success = storage.save_approach(approach)
    print(f"   Save successful: {success}")
    
    # Test load
    print("\n2. Loading Approach:")
    loaded = storage.load_approach(approach.id)
    print(f"   Load successful: {loaded is not None}")
    if loaded:
        print(f"   Loaded ID: {loaded.id}")
        print(f"   Loaded name: {loaded.name}")
        print(f"   Quality: {loaded.performance_metrics.avg_quality:.2f}")
    
    # Test list
    print("\n3. Listing Approaches:")
    approaches = storage.list_approaches()
    print(f"   Found {len(approaches)} approaches")
    for aid in approaches:
        print(f"   - {aid}")
    
    # Test statistics
    print("\n4. Storage Statistics:")
    stats = storage.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Test soft delete
    print("\n5. Soft Delete:")
    success = storage.delete_approach(approach.id)
    print(f"   Delete successful: {success}")
    
    active = storage.list_approaches(active_only=True)
    print(f"   Active approaches: {len(active)}")
    
    all_approaches = storage.list_approaches(active_only=False)
    print(f"   All approaches (including inactive): {len(all_approaches)}")
    
    print("\n" + "=" * 70)
    print("✓ Storage layer working correctly!")
