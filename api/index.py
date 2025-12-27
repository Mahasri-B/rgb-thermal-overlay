# Vercel serverless function wrapper
# Note: OpenCV may have limitations on Vercel due to binary size
# Consider using Render for full OpenCV support

from flask import Flask
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Export the Flask app for Vercel
handler = app

