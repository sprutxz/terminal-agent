tools = [
    {
        "type": "function",
        "function": {
            "name": "run_cmd",
            "description": "run a terminal command",
            "parameters": {
                "type": "object",
                "properties":{
                    "command":{
                        "type": "string",
                        "description": "the command to run in the terminal"
                    }
                },
                "required": ["command"]
            }
        },
    },
    {
        "type": "function",
        "function": {
            "name": "end_task_session",
            "description": "function to end task",
        }
    }
]