import sys
import os

# Base directory for the project
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)

from backend.app import app

# Vercel WSGI compatibility
handler = app
app = app
