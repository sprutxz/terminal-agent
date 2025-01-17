import fcntl
import os
import time
import subprocess
import json

from openai import OpenAI

from src.tools import tools

class TerminalAgent:
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com"):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.tools = tools
        with open("sysprompt.txt", "r") as f:
            self.sysprompt = f.read()
        self.messages = [{"role": "system", "content": self.sysprompt}]
        
        self.shell = subprocess.Popen(
            ["/bin/bash"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        fcntl.fcntl(self.shell.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
        self.shell_pid = self.shell.pid
    
    def chat_request(self, messages):
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )
        return response.choices[0].message

    def tool_request(self, messages):
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=self.tools
        )
        return response.choices[0].message

    def run_cmd(self, command: str, printcmd: bool) -> str:
        if printcmd:
            cwd = os.readlink(f"/proc/{self.shell_pid}/cwd")
            print(f"{cwd}$ {command}", end="")
            input()
        
        self.shell.stdin.write(command + "\n")
        self.shell.stdin.flush()
        
        time.sleep(0.1)
        
        output = ""
        while True:
            try:
                chunk = self.shell.stdout.read()
                if chunk is None:
                    break
                print(chunk, end="")
                output += chunk
            except (IOError, TypeError):
                break
        return output

    def execute_function_call(self, tool):
        args = json.loads(tool.function.arguments)
        if tool.function.name == "run_cmd":
            results = f"${args['command']}\n"
            results += self.run_cmd(args["command"], printcmd=True)
        else:
            results = f"Error: function {tool.function.name} does not exist"
        return results
