import sys
import os

# Robust path handling for Vercel
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from backend.app import app

# Handler for Vercel
app = app
