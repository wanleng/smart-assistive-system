import time
import subprocess
import sys

# This test tries to run the main app for 5 seconds and checks output.
# It can't strictly verify the GUI appearing in headless, but we can check if it output "Camera Started" quickly.

def test_startup():
    start_time = time.time()
    
    # Needs Python 3.11 as discovered before
    python_exe = r"C:\Users\Sai Swam Wan Hline\AppData\Local\Programs\Python\Python311\python.exe"
    
    print("Launching app...")
    process = subprocess.Popen(
        [python_exe, "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=r"C:\Users\Sai Swam Wan Hline\.gemini\antigravity\scratch\assistive_vision_system"
    )

    camera_started = False
    
    try:
        # Read output line by line
        while True:
            if process.poll() is not None:
                break
            
            # Non-blocking read trick (simplistic)
            line = process.stdout.readline()
            if line:
                print(f"APP STDOUT: {line.strip()}")
                if "Camera Started" in line:
                    camera_started = True
                    elapsed = time.time() - start_time
                    print(f"SUCCESS: Camera started in {elapsed:.2f} seconds.")
                    break
            
            if time.time() - start_time > 10:
                print("TIMEOUT: Camera did not start in time.")
                break
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        process.kill()
        
    if camera_started:
        print("Test Passed.")
    else:
        print("Test Failed.")
        sys.exit(1)

if __name__ == "__main__":
    test_startup()
