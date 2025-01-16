import subprocess
import os
import fcntl
import time

def bash_like_shell():
    # Start a single Bash instance
    process = subprocess.Popen(
        "bash",
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    fcntl.fcntl(process.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

    try:
        while True:
            command = input("mysh> ")
            if command.strip().lower() == "exit":
                break

            # Send command to the shell instance
            process.stdin.write(command + "\n")
            process.stdin.flush()  # Ensure command is sent
            
            # Give the process time to execute
            time.sleep(0.1)
            
            while True:
                try:
                    chunk = process.stdout.read()
                    if chunk is None:
                        break
                    print(chunk, end="")
                except (IOError, TypeError):
                    break
            
    except KeyboardInterrupt:
        pass
    finally:
        process.terminate()
        
if __name__ == "__main__":
    bash_like_shell()