import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from functions.call_functions import available_functions
from functions.call_functions import call_function
import json

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

# should the loop start here?
for i in range(20):
    # make a user call
    response = call_agent(messages, available_functions)
    
    # Receive agent response
    # Update history

# def call_agent(messages, available_functions):
#     response = client.chat.completions.create(
#         model="openrouter/free",
#         messages=messages,
#         tools=available_functions,
#     )

#     return response

response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    tools=available_functions,
)


if not response.usage:
    raise RuntimeError("Response invalid - Usage does not exist")

# verbose additions to completion
if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage.prompt_tokens}") 
    print(f"Response tokens: {response.usage.completion_tokens}")

# completion - print messsage and then tool calls check
print(f"{response.choices[0].message.content}")

if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        #print(f"Calling function: {tool_call.function.name}({function_args})")
        res = call_function(tool_call, verbose=args.verbose)
        if not res["content"]:
            raise Exception("tool call result is something that is either None or an empty string?")
        if args.verbose:
            print(f"-> {res['content']}")
