import os
import dotenv
from src.agent import TerminalAgent

def natural_language_query(agent, prompt):
    agent.messages.append({"role": "user", "content": prompt})
    
    while True:
        response = agent.tool_request(agent.messages)
        agent.messages.append(response)
        
        if response.tool_calls[0].function.name == "end_task_session":
            agent.messages.append({
                "role": "tool",
                "content": "ended task session",
                "tool_call_id": response.tool_calls[0].id
            })
            break
        
        for tool in response.tool_calls:
            if tool.function.name == "end_task_session":
                break
            
            output = agent.execute_function_call(tool)
            agent.messages.append({
                "role": "tool",
                "content": output,
                "tool_call_id": tool.id
            })
    
    summarize = agent.messages.copy() 
    summarize.append({"role": "system", "content": "summarize the results of the task in one sentence"})
    message = agent.send_message(summarize)
    print(f"Assistant> {message.content}")

def command_line_query(agent, command):
    output = agent.run_cmd(command, printcmd=False)
    content = f"${command}\n{output}"
    agent.messages.append({"role": "user", "content": command})    
    

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
                # output = agent.run_cmd(command, printcmd=False)
                # content = f"${command}\n{output}"
                # agent.messages.append({"role": "user", "content": content})
                command_line_query(agent, command)
            
            # if the prompt starts with "!", it is a natural language query
            else:
                # agent.messages.append({"role": "user", "content": prompt})
                # while True:
                #     response = agent.tool_request(agent.messages)
                #     agent.messages.append(response)
                    
                #     if response.tool_calls[0].function.name == "end_task_session":
                #         agent.messages.append({
                #             "role": "tool",
                #             "content": "ended task session",
                #             "tool_call_id": response.tool_calls[0].id
                #         })
                #         break
                    
                #     for tool in response.tool_calls:
                #         if tool.function.name == "end_task_session":
                #             break
                        
                #         output = agent.execute_function_call(tool)
                #         agent.messages.append({
                #             "role": "tool",
                #             "content": output,
                #             "tool_call_id": tool.id
                #         })
                
                # summarize = agent.messages.copy() 
                # summarize.append({"role": "system", "content": "summarize the results of the task in one sentence"})
                # message = agent.send_message(summarize)
                # print(f"Assistant> {message.content}")
                command = prompt[1:]
                natural_language_query(agent, command)
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
