import chromadb
import os
import shutil

print(f"Current Working Directory: {os.getcwd()}")
print(f"Checking for chroma_db in current directory: {os.path.exists('./chroma_db')}")

try:
    print("Initializing ChromaDB PersistentClient...")
    client = chromadb.PersistentClient(path="./chroma_db")
    print(f"Client initialized. Settings path: {client._system.settings.persist_directory if hasattr(client, '_system') else 'Unknown'}")
    
    print(f"Checking for chroma_db again: {os.path.exists('./chroma_db')}")
    
    collection = client.get_or_create_collection(name="test_collection")
    print("Collection 'test_collection' obtained.")
    
    print("Attempting to add a test document...")
    collection.add(
        documents=["This is a test document"],
        metadatas=[{"source": "test"}],
        ids=["test_id_1"]
    )
    print("Document added successfully.")
    
except Exception as e:
    print(f"\nERROR: {e}")

# Check cache lock
cache_path = os.path.expanduser("~/.cache/chroma/onnx_models/all-MiniLM-L6-v2/onnx.tar.gz")
print(f"\nChecking lock on: {cache_path}")
if os.path.exists(cache_path):
    try:
        with open(cache_path, 'rb') as f:
            print("File is readable.")
        with open(cache_path, 'ab') as f:
            print("File is writable (no lock).")
    except Exception as e:
        print(f"LOCK DETECTED: {e}")
else:
    print("Cache file does not exist.")
