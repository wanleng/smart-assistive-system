import pyttsx3
import threading
import queue
import time

# Mock config
class Config:
    TTS_RATE = 200
    TTS_VOLUME = 1.0
config = Config()

class AudioFeedback:
    def __init__(self):
        self.q = queue.Queue()
        self.stopped = False
        
        # Start processing thread
        t = threading.Thread(target=self.worker)
        t.daemon = True
        t.start()

    def speak(self, text):
        self.q.put(text)

    def worker(self):
        print("Audio Worker Started")
        
        # Initialize engine in the worker thread
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', config.TTS_RATE)
        self.engine.setProperty('volume', config.TTS_VOLUME)
        
        while not self.stopped:
            try:
                text = self.q.get(timeout=1)
                print(f"[Audio] Saying: {text}")
                self.engine.say(text)
                self.engine.runAndWait()
                print(f"[Audio] Finished: {text}")
                self.q.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"[Audio] Error: {e}")

    def stop(self):
        self.stopped = True
        # self.engine.stop() # Calling stop on engine from another thread is risky

if __name__ == "__main__":
    audio = AudioFeedback()
    print("Queueing 'System Ready'")
    audio.speak("System Ready")
    
    time.sleep(2)
    
    long_text = "There is a person about 1 meter in front of you. Stop, and confirm verbally before proceeding."
    print(f"Queueing long text: {long_text}")
    audio.speak(long_text)
    
    time.sleep(5)
    print("Exiting")
    audio.stop()
