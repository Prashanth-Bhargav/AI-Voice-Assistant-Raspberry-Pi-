# main.py
import time
from ears import listen_and_transcribe
from advanced_brain import get_jarvis_response
from mouth import speak, cleanup

if __name__ == "__main__":
    try:
        print("\n" + "="*40)
        print(">>> JARVIS SYSTEM FULLY ONLINE <<<")
        print("="*40)
        speak("System initialization complete. I am online and ready, sir.")
        
        while True:
            print("\n[?? MIC OPEN] -> Waiting for audio...")
            
            # 1. LISTEN (Local Pi via ears.py)
            user_input = listen_and_transcribe(duration=5)
            
            if user_input:
                print(f"\nUser: '{user_input}'")
                
                # --- IMMEDIATE ACKNOWLEDGMENT ---
                speak("Okay.") 
                
                # 2. THINK (Cloudflare GPU via advanced_brain.py)
                ai_response = get_jarvis_response(user_input)
                
                # 3. SPEAK FINAL ANSWER (Local Pi via mouth.py)
                speak(ai_response)
            else:
                print("... silence ...")
                
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nInitiating shutdown sequence...")
        speak("Powering down. Goodbye, sir.")
    finally:
        cleanup()
        print("System Offline.")