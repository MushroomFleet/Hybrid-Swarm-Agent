"""
Execution History Management
Tracks execution records for pattern analysis
"""

import json
import threading
from pathlib import Path
from typing import List, Optional, Dict, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from src.approach_patterns import ExecutionRecord, TaskContext, ContentFeatures
from src.input_sanitization import sanitize_identifier


class ExecutionHistory:
    """
    Manages persistent storage of execution records
    Uses daily JSONL files for efficient append and streaming
    """
    
    def __init__(self, history_path: str = "data/execution_history"):
        self.history_path = Path(history_path)
        self.history_path.mkdir(parents=True, exist_ok=True)
        
        self.lock = threading.RLock()
        self.current_date = None
        self.current_file = None
        
        # Create index file if needed
        self.index_path = self.history_path / "index.json"
        self.index = self._load_or_create_index()
    
    def _load_or_create_index(self) -> Dict:
        """Load or create index file"""
        if self.index_path.exists():
            try:
                with open(self.index_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading index: {e}, creating new")
        
        index = {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "total_records": 0,
            "date_ranges": {},  # {"2025-10": {"min": "2025-10-01", "max": "2025-10-31", "count": 150}}
            "files": []  # List of JSONL files
        }
        
        self._save_index(index)
        return index
    
    def _save_index(self, index: Dict):
        """Save index to file"""
        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)
    
    def _get_daily_file_path(self, date: datetime) -> Path:
        """Get file path for a specific date"""
        year_month = date.strftime("%Y-%m")
        month_dir = self.history_path / year_month
        month_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"records_{date.strftime('%Y%m%d')}.jsonl"
        return month_dir / filename
    
    def record_execution(self, record: ExecutionRecord) -> bool:
        """
        Add execution record to history
        
        Args:
            record: ExecutionRecord to store
            
        Returns:
            True if successful
        """
        with self.lock:
            try:
                # Get file for today
                today = datetime.now()
                filepath = self._get_daily_file_path(today)
                
                # Append record (JSONL format: one JSON per line)
                with open(filepath, 'a', encoding='utf-8') as f:
                    json_line = json.dumps(record.to_dict())
                    f.write(json_line + '\n')
                
                # Update index
                self._update_index_for_record(record, filepath.name, today)
                
                return True
                
            except Exception as e:
                print(f"Error recording execution: {e}")
                return False
    
    def _update_index_for_record(self, record: ExecutionRecord, filename: str, date: datetime):
        """Update index after adding record"""
        self.index['total_records'] += 1
        
        # Update date range
        year_month = date.strftime("%Y-%m")
        if year_month not in self.index['date_ranges']:
            self.index['date_ranges'][year_month] = {
                'min': date.date().isoformat(),
                'max': date.date().isoformat(),
                'count': 0
            }
        
        date_range = self.index['date_ranges'][year_month]
        date_range['count'] += 1
        date_range['max'] = max(date_range['max'], date.date().isoformat())
        
        # Track files
        if filename not in self.index['files']:
            self.index['files'].append(filename)
        
        self._save_index(self.index)
    
    def get_records(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        min_quality: Optional[float] = None,
        approach_id: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[ExecutionRecord]:
        """
        Query execution records with filters
        
        Args:
            start_date: Minimum date (inclusive)
            end_date: Maximum date (inclusive)
            min_quality: Minimum quality threshold
            approach_id: Filter by approach
            limit: Maximum records to return
            
        Returns:
            List of ExecutionRecord objects
        """
        with self.lock:
            records = []
            
            # Determine date range to scan
            if start_date is None:
                start_date = datetime.now() - timedelta(days=365)  # Last year
            if end_date is None:
                end_date = datetime.now()
            
            # Iterate through dates
            current = start_date.date()
            end = end_date.date()
            
            while current <= end:
                filepath = self._get_daily_file_path(datetime.combine(current, datetime.min.time()))
                
                if filepath.exists():
                    # Read JSONL file
                    daily_records = self._read_jsonl_file(filepath)
                    
                    # Apply filters
                    for record in daily_records:
                        # Quality filter
                        if min_quality is not None and record.actual_quality < min_quality:
                            continue
                        
                        # Approach filter
                        if approach_id is not None and record.approach_id != approach_id:
                            continue
                        
                        records.append(record)
                        
                        # Limit check
                        if limit is not None and len(records) >= limit:
                            return records
                
                # Next day
                current += timedelta(days=1)
            
            return records
    
    def _read_jsonl_file(self, filepath: Path) -> List[ExecutionRecord]:
        """Read all records from a JSONL file"""
        records = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    data = json.loads(line)
                    record = ExecutionRecord.from_dict(data)
                    records.append(record)
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
        
        return records
    
    def get_recent_records(
        self,
        days: int = 7,
        min_quality: Optional[float] = None
    ) -> List[ExecutionRecord]:
        """
        Get records from recent days
        
        Args:
            days: Number of days to look back
            min_quality: Minimum quality threshold
            
        Returns:
            List of ExecutionRecord objects
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        return self.get_records(
            start_date=start_date,
            end_date=end_date,
            min_quality=min_quality
        )
    
    def get_approach_history(
        self,
        approach_id: str,
        days: Optional[int] = None
    ) -> List[ExecutionRecord]:
        """
        Get all records for a specific approach
        
        Args:
            approach_id: Approach identifier
            days: Optional number of days to look back
            
        Returns:
            List of ExecutionRecord objects
        """
        start_date = None
        if days is not None:
            start_date = datetime.now() - timedelta(days=days)
        
        return self.get_records(
            start_date=start_date,
            approach_id=approach_id
        )
    
    def get_statistics(self) -> Dict:
        """Get history statistics"""
        with self.lock:
            # Count files
            file_count = 0
            total_size = 0
            
            for year_month_dir in self.history_path.iterdir():
                if year_month_dir.is_dir() and year_month_dir.name != '.':
                    for file in year_month_dir.glob('*.jsonl'):
                        file_count += 1
                        total_size += file.stat().st_size
            
            return {
                'total_records': self.index['total_records'],
                'total_files': file_count,
                'total_size_bytes': total_size,
                'date_ranges': len(self.index['date_ranges']),
                'oldest_record': min(self.index['date_ranges'].values(), key=lambda x: x['min'])['min'] if self.index['date_ranges'] else None,
                'newest_record': max(self.index['date_ranges'].values(), key=lambda x: x['max'])['max'] if self.index['date_ranges'] else None
            }
    
    def compact_old_records(self, days_to_keep: int = 90) -> int:
        """
        Archive old records (compress or move to archive)
        
        Args:
            days_to_keep: Keep records newer than this
            
        Returns:
            Number of files archived
        """
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        archived_count = 0
        
        # TODO: Implement compression/archival
        # For now, just report what would be archived
        
        return archived_count


if __name__ == "__main__":
    # Demo usage
    print("Execution History Demo")
    print("=" * 70)
    
    from src.approach_patterns import TaskContext, ContentFeatures
    
    # Create history manager
    history = ExecutionHistory("data/execution_history")
    
    # Create sample record
    record = ExecutionRecord(
        record_id="test_exec_001",
        timestamp=datetime.now(),
        task_context=TaskContext(
            prompt="Write a tutorial on Python functions",
            domain_weights={'writing': 0.8, 'coding': 0.6},
            complexity=0.5,
            keywords=['tutorial', 'python', 'functions'],
            output_type='tutorial',
            estimated_duration=2.0
        ),
        specialist_id="specialist_001",
        approach_id="legacy_approach_b_tutorial",
        quality_target=0.8,
        actual_quality=0.85,
        success=True,
        execution_time_ms=1500,
        content_features=ContentFeatures(
            section_count=5,
            has_code_blocks=True,
            code_block_count=3,
            has_numbered_list=True,
            has_bullets=False,
            has_tables=False,
            total_length=2500,
            avg_section_length=500,
            detected_tone="educational",
            formality_score=0.7,
            explanation_ratio=0.6,
            example_ratio=0.3,
            code_ratio=0.1
        )
    )
    
    # Test 1: Record execution
    print("\n1. Recording Execution:")
    success = history.record_execution(record)
    print(f"   Record successful: {success}")
    
    # Test 2: Get recent records
    print("\n2. Getting Recent Records:")
    recent = history.get_recent_records(days=7)
    print(f"   Found {len(recent)} recent records")
    
    # Test 3: Query with filters
    print("\n3. Querying with Filters:")
    high_quality = history.get_records(min_quality=0.8)
    print(f"   Found {len(high_quality)} high-quality records")
    
    # Test 4: Get approach history
    print("\n4. Getting Approach History:")
    approach_records = history.get_approach_history("legacy_approach_b_tutorial")
    print(f"   Found {len(approach_records)} records for approach")
    
    # Test 5: Statistics
    print("\n5. History Statistics:")
    stats = history.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n" + "=" * 70)
    print("✓ ExecutionHistory working correctly!")
