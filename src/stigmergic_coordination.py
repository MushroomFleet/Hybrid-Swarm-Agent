"""
Stigmergic Coordination System
Agents coordinate through shared environment modification
"""

import time
import json
import math
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
from collections import defaultdict
import threading

@dataclass
class Signal:
    """A signal deposited on the stigmergic board"""
    task_id: str
    approach: str  # Solution approach being signaled
    strength: float  # Signal strength (0.0 to 100.0)
    timestamp: float
    deposited_by: str  # Agent ID
    success_metric: float  # Quality/success of approach (0.0 to 1.0)
    
    def age(self) -> float:
        """Get signal age in seconds"""
        return time.time() - self.timestamp
    
    def decayed_strength(self, decay_rate: float) -> float:
        """Calculate current strength after decay"""
        age_seconds = self.age()
        decay_factor = math.exp(-age_seconds / decay_rate)
        return self.strength * decay_factor


class StigmergicBoard:
    """
    Shared coordination board where agents deposit and read signals
    """
    
    def __init__(
        self,
        decay_rate: float = 3600.0,  # Seconds for signal to decay to ~37%
        amplification_factor: float = 1.5,
        attenuation_factor: float = 0.7,
        storage_path: str = "data/stigmergy"
    ):
        self.decay_rate = decay_rate
        self.amplification_factor = amplification_factor
        self.attenuation_factor = attenuation_factor
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # task_id -> List[Signal]
        self.signals: Dict[str, List[Signal]] = defaultdict(list)
        self.lock = threading.Lock()
        
        self._load_signals()
        
        # Start decay background thread
        self._start_decay_thread()
    
    def deposit_signal(
        self,
        task_id: str,
        approach: str,
        success_metric: float,
        agent_id: str
    ):
        """
        Agent deposits a signal about an approach to a task
        
        Args:
            task_id: Identifier for the task
            approach: Description of solution approach
            success_metric: Quality/success measure (0.0 to 1.0)
            agent_id: ID of depositing agent
        """
        with self.lock:
            # Calculate initial signal strength from success
            initial_strength = success_metric * 100.0
            
            # Check for existing signals for this task/approach
            existing_signal = None
            for signal in self.signals[task_id]:
                if signal.approach == approach:
                    existing_signal = signal
                    break
            
            if existing_signal:
                # Same approach exists - reinforce or attenuate
                current_strength = existing_signal.decayed_strength(self.decay_rate)
                
                if existing_signal.deposited_by == agent_id or success_metric > 0.7:
                    # Reinforce: Same agent or high success
                    new_strength = current_strength + (initial_strength * self.amplification_factor)
                    print(f"  ✓ Amplifying signal for '{approach}': {current_strength:.1f} → {new_strength:.1f}")
                else:
                    # Attenuate: Different agent with modest success
                    new_strength = current_strength * self.attenuation_factor
                    print(f"  ✓ Attenuating signal for '{approach}': {current_strength:.1f} → {new_strength:.1f}")
                
                # Update existing signal
                existing_signal.strength = min(new_strength, 100.0)
                existing_signal.timestamp = time.time()
                existing_signal.success_metric = (
                    existing_signal.success_metric * 0.7 + success_metric * 0.3
                )
            else:
                # New approach - create signal
                signal = Signal(
                    task_id=task_id,
                    approach=approach,
                    strength=initial_strength,
                    timestamp=time.time(),
                    deposited_by=agent_id,
                    success_metric=success_metric
                )
                self.signals[task_id].append(signal)
                print(f"  ✓ New signal deposited for '{approach}': {initial_strength:.1f}")
            
            self._save_signals()
    
    def read_signals(self, task_id: str, agent_id: str) -> List[Dict[str, Any]]:
        """
        Agent reads signals for a task
        
        Returns:
            List of signals with current (decayed) strengths
        """
        with self.lock:
            if task_id not in self.signals:
                return []
            
            # Calculate current strengths after decay
            signal_data = []
            for signal in self.signals[task_id]:
                current_strength = signal.decayed_strength(self.decay_rate)
                if current_strength > 1.0:  # Only include non-negligible signals
                    signal_data.append({
                        "approach": signal.approach,
                        "strength": current_strength,
                        "success_metric": signal.success_metric,
                        "age_hours": signal.age() / 3600.0,
                        "from_self": signal.deposited_by == agent_id
                    })
            
            # Sort by strength
            signal_data.sort(key=lambda x: x['strength'], reverse=True)
            
            return signal_data
    
    def strongest_signal(self, task_id: str) -> Optional[str]:
        """Get approach with strongest signal for task"""
        signals = self.read_signals(task_id, "system")
        if not signals:
            return None
        return signals[0]['approach']
    
    def decay_signals(self):
        """Remove signals that have decayed to negligible strength"""
        with self.lock:
            for task_id in list(self.signals.keys()):
                # Filter out weak signals
                self.signals[task_id] = [
                    s for s in self.signals[task_id]
                    if s.decayed_strength(self.decay_rate) > 1.0
                ]
                
                # Remove empty task entries
                if not self.signals[task_id]:
                    del self.signals[task_id]
            
            self._save_signals()
    
    def get_board_state(self) -> Dict[str, Any]:
        """Get current state of the board"""
        with self.lock:
            return {
                "total_tasks": len(self.signals),
                "total_signals": sum(len(sigs) for sigs in self.signals.values()),
                "tasks": {
                    task_id: [
                        {
                            "approach": sig.approach,
                            "strength": sig.decayed_strength(self.decay_rate),
                            "age_hours": sig.age() / 3600.0
                        }
                        for sig in signals
                    ]
                    for task_id, signals in self.signals.items()
                }
            }
    
    def _start_decay_thread(self):
        """Start background thread for signal decay"""
        def decay_loop():
            while True:
                time.sleep(600)  # Every 10 minutes
                self.decay_signals()
        
        thread = threading.Thread(target=decay_loop, daemon=True)
        thread.start()
    
    def _save_signals(self):
        """Persist signals to storage"""
        filepath = self.storage_path / "signals.json"
        data = {
            task_id: [asdict(sig) for sig in signals]
            for task_id, signals in self.signals.items()
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_signals(self):
        """Load signals from storage"""
        filepath = self.storage_path / "signals.json"
        if not filepath.exists():
            return
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                for task_id, signal_list in data.items():
                    self.signals[task_id] = [
                        Signal(**sig_data) for sig_data in signal_list
                    ]
        except Exception as e:
            print(f"Error loading signals: {e}")


class StigmergicAgent:
    """
    Agent that coordinates via stigmergic board
    """
    
    def __init__(self, agent_id: str, board: StigmergicBoard):
        self.agent_id = agent_id
        self.board = board
    
    def select_approach(self, task_id: str) -> str:
        """Select approach based on board signals"""
        signals = self.board.read_signals(task_id, self.agent_id)
        
        if not signals:
            # No signals - explore randomly
            approaches = ["approach_A", "approach_B", "approach_C"]
            import random
            return random.choice(approaches)
        
        # Weight selection by signal strength
        total_strength = sum(s['strength'] for s in signals)
        
        import random
        rand = random.uniform(0, total_strength)
        cumulative = 0
        
        for signal in signals:
            cumulative += signal['strength']
            if rand <= cumulative:
                return signal['approach']
        
        # Fallback to strongest
        return signals[0]['approach']
    
    def execute_and_report(self, task_id: str):
        """Execute task and report results to board"""
        # Select approach based on signals
        approach = self.select_approach(task_id)
        print(f"\n{self.agent_id}: Selected '{approach}' for task '{task_id}'")
        
        # Simulate execution
        import random
        success_metric = random.uniform(0.5, 0.95)
        
        # Deposit signal
        print(f"{self.agent_id}: Execution complete (quality: {success_metric:.2f})")
        self.board.deposit_signal(task_id, approach, success_metric, self.agent_id)
        
        return approach, success_metric


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("STIGMERGIC COORDINATION DEMO")
    print("=" * 60)
    
    # Create shared board
    board = StigmergicBoard(decay_rate=1800.0)  # 30 min decay
    
    # Create agents
    agents = [
        StigmergicAgent(f"agent_{i}", board)
        for i in range(5)
    ]
    
    # Simulate work cycles
    task_id = "task_001"
    
    for cycle in range(3):
        print(f"\n--- Cycle {cycle + 1} ---")
        
        for agent in agents:
            agent.execute_and_report(task_id)
            time.sleep(0.1)  # Small delay for readability
        
        # Show board state
        print("\nBoard State:")
        state = board.get_board_state()
        if task_id in state['tasks']:
            for sig in state['tasks'][task_id]:
                print(f"  {sig['approach']}: strength={sig['strength']:.1f}, age={sig['age_hours']:.2f}h")
    
    print("\n" + "=" * 60)
    print("FINAL BOARD STATE")
    print("=" * 60)
    print(json.dumps(board.get_board_state(), indent=2))
