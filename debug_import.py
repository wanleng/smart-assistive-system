import sys
import traceback
import sqlite3

print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"SQLite version: {sqlite3.sqlite_version}")

sys.stdout.flush()

try:
    print("Attempting to import chromadb...")
    import chromadb
    print(f"Success! chromadb version: {chromadb.__version__}")
except BaseException as e:
    print(f"\nCaught Exception: {type(e).__name__}: {e}")
    traceback.print_exc(file=sys.stdout)
    sys.stdout.flush()
