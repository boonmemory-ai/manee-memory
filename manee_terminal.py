import subprocess
import os
import sys

def run_command(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', check=False)
        return result.stdout.strip()
    except Exception:
        return ""

def git_sync_pull():
    git_path = r"C:\Program Files\Git\bin\git.exe"
    if os.path.exists(git_path):
        subprocess.run([git_path, "pull", "origin", "master"], check=False, capture_output=True)

def git_sync_push(log_entry):
    git_path = r"C:\Program Files\Git\bin\git.exe"
    if os.path.exists(git_path):
        subprocess.run([git_path, "add", "."], check=False, capture_output=True)
        subprocess.run([git_path, "commit", "-m", "update history"], check=False, capture_output=True)
        subprocess.run([git_path, "push", "origin", "master"], check=False, capture_output=True)

def main():
    print("--- Terminal Assistant System ---")
    print(" (Enter 'exit' to quit) \n")
    
    # Sync before starting
    git_sync_pull()
    
    history_file = "CHAT_LOG.md"

    while True:
        user_input = input("> ")
        if user_input.lower() in ['exit', 'quit']:
            break
        
        if not user_input.strip():
            continue

        # Get response using the system's CLI
        cmd = ["npx", "@google/gemini-cli", user_input]
        response = run_command(cmd)
        
        if not response:
            response = "System: Unable to process request."

        print(f"\nAssistant: {response}\n")

        # Log history
        try:
            with open(history_file, "a", encoding="utf-8") as f:
                f.write(f"\nUser: {user_input}\nAssistant: {response}\n")
            
            # Sync after each interaction
            git_sync_push(user_input)
        except Exception:
            pass

if __name__ == "__main__":
    main()
