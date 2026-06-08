import subprocess
import os
import sys
import shutil

def get_npx_path():
    # Try to find npx automatically
    path = shutil.which("npx")
    if path:
        return f'"{path}"'
    
    # Fallback for Windows if not in PATH
    windows_path = r"C:\Program Files\nodejs\npx.cmd"
    if os.path.exists(windows_path):
        return f'"{windows_path}"'
    
    return "npx" # Last resort

def get_git_path():
    path = shutil.which("git")
    if path:
        return path
    
    # Fallback for Windows
    windows_path = r"C:\Program Files\Git\bin\git.exe"
    if os.path.exists(windows_path):
        return windows_path
    
    return "git"

def run_command(cmd):
    try:
        # Use shell=True to handle complex commands and different OS behaviors
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', shell=True, check=False)
        if result.returncode != 0:
            error_msg = result.stderr.strip() if result.stderr else "Unknown error"
            return f"Assistant: I encountered an issue. ({error_msg})"
        return result.stdout.strip()
    except Exception as e:
        return f"Assistant: System error. ({str(e)})"

def git_sync(action):
    git_path = get_git_path()
    devnull = subprocess.DEVNULL
    
    try:
        if action == "pull":
            print("Syncing...")
            subprocess.run([git_path, "pull", "origin", "master"], check=False, stdout=devnull, stderr=devnull)
        elif action == "push":
            subprocess.run([git_path, "add", "manee_terminal.py", "CHAT_LOG.md"], check=False, stdout=devnull, stderr=devnull)
            subprocess.run([git_path, "commit", "-m", "update"], check=False, stdout=devnull, stderr=devnull)
            subprocess.run([git_path, "push", "origin", "master"], check=False, stdout=devnull, stderr=devnull)
    except:
        pass

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("========================================")
    print("   Terminal Assistant System v1.3")
    print("========================================")
    print(" (Type 'exit' or 'quit' to close) \n")
    
    git_sync("pull")
    
    history_file = "CHAT_LOG.md"
    npx_cmd = get_npx_path()

    while True:
        try:
            user_input = input("\nUser > ")
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye.")
                break
            
            if not user_input.strip():
                continue

            print("Thinking...")
            
            # Cross-platform command execution
            cmd = f'{npx_cmd} @google/gemini-cli "{user_input}"'
            response = run_command(cmd)
            
            print(f"\nAssistant: {response}\n")

            with open(history_file, "a", encoding="utf-8") as f:
                f.write(f"\nUser: {user_input}\nAssistant: {response}\n")
            
            git_sync("push")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
