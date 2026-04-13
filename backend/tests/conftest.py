import sys
import os

# Ensure the backend directory is on the path so imports like
# `from models.schemas import ...` resolve to backend/models/schemas.py
# and not the root-level models.py
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Remove the project root from sys.path to avoid shadowing backend packages
# with root-level files like models.py, utils.py, etc.
project_root = os.path.dirname(backend_dir)
if project_root in sys.path:
    sys.path.remove(project_root)
