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
    message = agent.chat_request(summarize)
    print(f"Assistant> {message.content}")

def command_line_query(agent, command):
    output = agent.run_cmd(command, printcmd=False)
    content = f"${command}\n{output}"
    agent.messages.append({"role": "user", "content": content})