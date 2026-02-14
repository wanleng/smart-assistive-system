
import os
import shutil
import time
import chromadb
import logging

def reset_data():
    """
    Resets the application state by:
    1. Clearing all records from ChromaDB (keeping the DB structure/files).
    2. Deleting the 'detections.jsonl' log file.
    """
    CHROMA_DB_PATH = "./chroma_db"
    COLLECTION_NAME = "vision_events" # Matching vector_store.py
    LOG_FILE_PATH = "detections.jsonl"
    
    print("⚠️  WARNING: This will PERMANENTLY DELETE:")
    print(f"  - All records in ChromaDB collection '{COLLECTION_NAME}'")
    print(f"  - {LOG_FILE_PATH} (Detection Logs)")
    print("\nEnsure the 'assistive_vision_system' app is STOPPED before proceeding.")
    print("Waiting 3 seconds... (Ctrl+C to Cancel)")
    
    try:
        time.sleep(3)
    except KeyboardInterrupt:
        print("\n🚫 Aborted.")
        return

    print("\nStarting clean up...")

    # 1. Clear ChromaDB Records
    if os.path.exists(CHROMA_DB_PATH):
        try:
            print(f"Connecting to ChromaDB at {CHROMA_DB_PATH}...")
            client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
            
            try:
                # Try to get collection to see if it exists
                client.get_collection(COLLECTION_NAME)
                # If exists, delete it (fastest way to clear all data)
                client.delete_collection(COLLECTION_NAME)
                print(f"✅ Deleted collection '{COLLECTION_NAME}'")
                
                # Re-create it empty
                client.create_collection(COLLECTION_NAME)
                print(f"✅ Re-created empty collection '{COLLECTION_NAME}'")
                
            except ValueError:
                print(f"ℹ️  Collection '{COLLECTION_NAME}' did not exist (nothing to delete).")
                # Create it anyway to be ready
                client.create_collection(COLLECTION_NAME)
                print(f"✅ Created new collection '{COLLECTION_NAME}'")

        except Exception as e:
            print(f"❌ Failed to reset ChromaDB: {e}")
            # If chromadb fails (e.g. lock), warn user
            if "WinError 32" in str(e):
                print("   👉 The database is locked. Stop the main app/python processes.")
    else:
         print(f"ℹ️  ChromaDB directory not found at {CHROMA_DB_PATH}")

    # 2. Delete Log File (Existing logic, seemingly preserved)
    if os.path.exists(LOG_FILE_PATH):
        try:
            os.remove(LOG_FILE_PATH)
            print(f"✅ Deleted File: {LOG_FILE_PATH}")
        except PermissionError:
            print(f"❌ Permission Error: Could not delete {LOG_FILE_PATH}.")
            print("   👉 PLEASE STOP the running application/terminal and try again.")
        except Exception as e:
            print(f"❌ Failed to delete {LOG_FILE_PATH}: {e}")
    else:
        print(f"ℹ️  File not found (already clean): {LOG_FILE_PATH}")

    print("\n✨ Reset Complete.")

if __name__ == "__main__":
    reset_data()
