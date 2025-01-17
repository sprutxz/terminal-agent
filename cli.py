import os
import dotenv

from src.agent import TerminalAgent
from src.query import natural_language_query, command_line_query

def main():
    dotenv.load_dotenv()
    api_key = os.getenv("DS_API_KEY")
    
    if not api_key:
        raise ValueError("DS_API_KEY environment variable not set")
    
    agent = TerminalAgent(api_key=api_key)
    
    print("Terminal Agent CLI (type exit to quit)")
    print("-" * 40)
    
    while True:
        try:
            cwd = os.readlink(f"/proc/{agent.shell_pid}/cwd")
            prompt = input(f"{cwd}$ ")
            
            if prompt == "exit":
                break
            
            # if the prompt does not start with "!", it is a command
            if not prompt.startswith("!"):
                command = prompt
                command_line_query(agent, command)
            
            # if the prompt starts with "!", it is a natural language query
            else:
                command = prompt[1:]
                natural_language_query(agent, command)
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
