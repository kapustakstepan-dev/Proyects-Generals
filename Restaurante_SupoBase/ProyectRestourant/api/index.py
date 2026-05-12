import sys
import os

# Ensure the project root is in the python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.app import app

# Redundancy required by Vercel in some environments
app = app
