import logging
import sys

# Configure logging to stderr so we see it immediately
logging.basicConfig(stream=sys.stderr, level=logging.ERROR)

print(f"Python Executable: {sys.executable}")
import sys
print(f"sys.path: {sys.path}")



print("Attempting to import src.vector_store...")
try:
    from src.vector_store import VectorStore
    print("Import successful (unexpected if error persists).")
except Exception as e:
    print(f"Caught top-level exception: {e}")
