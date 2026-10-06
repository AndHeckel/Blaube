import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from functions.call_functions import available_functions
from functions.call_functions import call_function
import sys

# parser config
parser = argparse.ArgumentParser(description="Blaube")
parser.add_argument("user_prompt", type=str, help="user prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()


# api config
load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("OPENROUTER_API_KEY not found in .env")



messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
        ]

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def call_agent(messages, available_functions, verbose):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    if not response.usage:
        raise RuntimeError("Response invalid - Usage does not exist")

    # Verbose output
    if verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}") 
        print(f"Response tokens: {response.usage.completion_tokens}")

    return response

def tool_uses(response, verbose):
    tool_calls = []
    
    if response.choices[0].message.tool_calls:
        for tool_call in response.choices[0].message.tool_calls:
            #print(f"Calling function: {tool_call.function.name}({function_args})")
            res = call_function(tool_call, verbose=args.verbose)
            if not res["content"]:
                raise Exception("tool call result is something that is either None or an empty string?")
            if verbose:
                print(f"-> {res['content']}")
            tool_calls.append(res)

    return tool_calls

# Agent loop
def main():
    for i in range(20):
        # Call the agent, gather
        response = call_agent(messages, available_functions, args.verbose)
        message = response.choices[0].message
        tool_calls = tool_uses(response, args.verbose)
  
        # Update the history and tool calls
        messages.append(message)
        for obj in tool_calls:
            messages.append(obj)

        if not tool_calls:
            print(f"final message:\n{message.content}")
            return 0
    return 1

if __name__ == "__main__":
    res = main()
    if res is None:
        res = 1
    sys.exit(res)