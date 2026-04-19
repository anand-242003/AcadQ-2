import sys
import os




backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)



project_root = os.path.dirname(backend_dir)
if project_root in sys.path:
    sys.path.remove(project_root)
