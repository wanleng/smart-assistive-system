try:
    import chromadb
except ImportError as e:
    import logging
    logging.error(f"Failed to import chromadb: {e}")
    chromadb = None
import uuid
import logging

class VectorStore:
    def __init__(self, collection_name="vision_events"):
        self.ready = False
        if chromadb is None:
            logging.warning("chromadb not installed. VectorStore disabled.")
            return

        try:
            # Persistent client saves to disk
            self.client = chromadb.PersistentClient(path="./chroma_db")
            self.collection = self.client.get_or_create_collection(name=collection_name)
            self.ready = True
        except Exception as e:
            logging.error(f"Failed to initialize VectorStore: {e}")

    def add(self, text, metadata):
        """
        Adds a text entry with metadata to the vector store.
        """
        if not self.ready:
            return

        try:
            # ID must be unique string
            doc_id = str(uuid.uuid4())
            self.collection.add(
                documents=[text],
                metadatas=[metadata],
                ids=[doc_id]
            )
        except Exception as e:
            logging.error(f"VectorStore add failed: {e}")

    def query(self, query_text, n_results=3):
        """
        Returns similar past events.
        """
        if not self.ready:
            return []
            
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            return results
        except Exception as e:
            logging.error(f"VectorStore query failed: {e}")
            return []
