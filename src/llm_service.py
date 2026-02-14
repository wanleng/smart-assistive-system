import json
import time
import logging
import threading
import config
from src.data_logger import DataLogger
from src.vector_store import VectorStore
try:
    from google import genai
except ImportError:
    genai = None

class LLMService:
    def __init__(self):
        self.session_data = {
            "objects_seen": {},
            "dangerous_events": 0,
            "start_time": time.time()
        }
        self.logger = DataLogger()
        
        # Configure Gemini (New SDK)
        self.client = None
        if genai and config.GOOGLE_API_KEY:
            try:
                self.client = genai.Client(api_key=config.GOOGLE_API_KEY)
                # We don't need to "configure" or create a "model" object like before
                # We just hold the client and specify model name during generation
                self.model_name = 'gemini-2.0-flash' 
            except Exception as e:
                logging.error(f"Failed to init Gemini Client: {e}")
                self.client = None
        elif not genai:
            logging.warning("google-genai library not installed. LLM features disabled.")
            print("⚠️ google-genai library not installed.")
        else:
            logging.warning("No Google API Key found. LLM features disabled.")

        # Initialize VectorStore in background to not block startup if slow
        self.vector_store = None
        threading.Thread(target=self._init_vector_store, daemon=True).start()

    def _init_vector_store(self):
        try:
            self.vector_store = VectorStore()
            logging.info("VectorStore initialized.")
        except Exception as e:
            logging.error(f"VectorStore init failed: {e}")

    def generate_response(self, metadata_json, target_language=config.TARGET_LANGUAGE):
        """
        Generates a spoken response from the LLM based on metadata using Google Gemini.
        """
        data = json.loads(metadata_json)
        objects = data.get("objects", [])
        timestamp = data.get("timestamp")
        
        if not objects:
            return None

        # Log & Embed for Session summary and RAG
        for obj in objects:
            label = obj['label']
            
            # Session Tracking
            self.session_data["objects_seen"][label] = self.session_data["objects_seen"].get(label, 0) + 1
            if obj['is_dangerous']:
                self.session_data["dangerous_events"] += 1
            
            # Persistent Logging
            self.logger.log({
                "timestamp": timestamp,
                "type": "detection",
                "label": label,
                "metadata": obj
            })
            
            # Vector Store Embedding (Async)
            if self.vector_store:
                desc = f"A {obj['distance']} {label} at {obj['position']}."
                threading.Thread(target=self.vector_store.add, args=(desc, {"label": label, "timestamp": timestamp}), daemon=True).start()

        # Construct Prompt
        object_descriptions = []
        for obj in objects:
            desc = f"- {obj['label']} at {obj['position']} (distance: {obj['distance']})"
            if obj['is_dangerous']:
                desc += " [DANGEROUS]"
            object_descriptions.append(desc)
        
        prompt = (
            f"You are an assistive vision assistant for a visually impaired user. "
            f"Here is a list of detected objects with their position (left/center/right) and distance (near/medium/far): \n"
            f"{chr(10).join(object_descriptions)}\n\n"
            f"Provide a spoken notification to the user in {target_language}. "
            f"Strictly follow this format: "
            f"'There is a [object] about [distance representation] from here. [Navigational guidance]'. "
            f"Example: 'There is a chair about 2 meters in front of you. Walk forward but stay slightly left.' "
            f"Map qualitative distances: near -> '1 meter', medium -> '3 meters', far -> '5+ meters'. "
            f"Give clear directional advice. Prioritize safety. "
            f"IMPORTANT: Output ONLY the spoken notification. Do NOT include phrases like 'Okay', 'Here is', or 'Spoken notification:'. "
            f"Keep it concise, under 2 sentences."
        )

        # Call Gemini (New SDK)
        if self.client:
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                return response.text
            except Exception as e:
                logging.error(f"Gemini API Error: {e}")
                print(f"⚠️ Gemini API Error (Using Fallback): {e}")
                # Fallback to heuristic if API fails
                return self._fallback_heuristic(objects)
        else:
            if not self.client:
                # We check client logic above, if it's None here it means init failed or key missing
                pass 
            return self._fallback_heuristic(objects)

    def _fallback_heuristic(self, objects):
        """Fallback if LLM is unavailable"""
        objects.sort(key=lambda x: (not x['is_dangerous'], x['distance'] != 'near'))
        parts = []
        for obj in objects[:3]: 
            label = obj['label']
            pos = obj['position']
            dist = obj['distance']
            desc = f"{label} on {pos}"
            if obj['is_dangerous']: 
                desc += f", {dist}"
            parts.append(desc)
        return ". ".join(parts)

    def summarize_session(self):
        """
        Returns a session summary string.
        """
        duration = int(time.time() - self.session_data["start_time"])
        top_objects = sorted(self.session_data["objects_seen"].items(), key=lambda x: x[1], reverse=True)[:5]
        top_str = ", ".join([f"{k} ({v})" for k, v in top_objects])
        
        return (f"Session ended. Duration: {duration} seconds. "
                f"Dangerous events: {self.session_data['dangerous_events']}. "
                f"Common objects: {top_str}.")
