"""
Wrapper for hybrid-interface.py with proper UTF-8 encoding
"""
import sys
import os
import io

# Force UTF-8 encoding for stdout/stderr on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import and run the actual interface
if __name__ == "__main__":
    # Import here after path is set
    import importlib.util
    spec = importlib.util.spec_from_file_location("hybrid_interface", "hybrid_interface.py")
    hybrid_interface = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hybrid_interface)
    hybrid_interface.main()
