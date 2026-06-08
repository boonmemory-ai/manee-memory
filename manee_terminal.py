import subprocess
import os
import sys

# Specify the full path to npx.cmd
NPX_PATH = r"C:\Program Files\nodejs\npx.cmd"

def run_command(cmd):
    try:
        # Use shell=True for Windows command execution
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', shell=True, check=False)
        if result.returncode != 0:
            error_msg = result.stderr.strip() if result.stderr else "Unknown error"
            return f"Assistant: I encountered an issue processing that. ({error_msg})"
        return result.stdout.strip()
    except Exception as e:
        return f"Assistant: System error occurred. ({str(e)})"

def git_sync(action):
    git_path = r"C:\Program Files\Git\bin\git.exe"
    if not os.path.exists(git_path):
        return
    
    # Hide output to keep terminal clean
    devnull = subprocess.DEVNULL
    
    if action == "pull":
        print("Syncing with cloud...")
        subprocess.run([git_path, "pull", "origin", "master"], check=False, stdout=devnull, stderr=devnull)
    elif action == "push":
        subprocess.run([git_path, "add", "manee_terminal.py", "CHAT_LOG.md"], check=False, stdout=devnull, stderr=devnull)
        subprocess.run([git_path, "commit", "-m", "update"], check=False, stdout=devnull, stderr=devnull)
        subprocess.run([git_path, "push", "origin", "master"], check=False, stdout=devnull, stderr=devnull)

def main():
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    print("========================================")
    print("   Terminal Assistant System v1.2")
    print("========================================")
    print(" (Type 'exit' or 'quit' to close) \n")
    
    # Sync before starting
    git_sync("pull")
    
    history_file = "CHAT_LOG.md"

    while True:
        try:
            user_input = input("\nUser > ")
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye.")
                break
            
            if not user_input.strip():
                continue

            print("Thinking...")
            
            # Using the full path to npx
            cmd = f'"{NPX_PATH}" @google/gemini-cli "{user_input}"'
            response = run_command(cmd)
            
            print(f"\nAssistant: {response}\n")

            # Save history locally
            with open(history_file, "a", encoding="utf-8") as f:
                f.write(f"\nUser: {user_input}\nAssistant: {response}\n")
            
            # Auto sync after interaction
            git_sync("push")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
