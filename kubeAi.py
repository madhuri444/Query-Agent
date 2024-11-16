import os
from dotenv import load_dotenv    
from groq import Groq
import subprocess

# Load environment variables
load_dotenv()

KUBECONFIG_PATH = os.getenv("KUBECONFIG_PATH", "C:/Users/madhu/.kube/config")

# Define read-only and blocking commands
READ_ONLY_COMMANDS = ["get", "describe", "explain", "logs", "top", "events", "api-versions", "cluster-info"]
BLOCKING_COMMANDS = ["edit", "delete", "apply", "create", "replace", "patch", "scale"]

def execute_kubectl_command(command):
    # Add --kubeconfig flag to specify the config file
    full_command = f"{command} --kubeconfig={KUBECONFIG_PATH}"
    result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return f"Error executing command: {result.stderr}"

def interpret_query_to_kubectl(query):
    client = Groq(
         api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a Kubernetes assistant. Only respond with the exact kubectl command, and nothing else"},
            {"role": "user", "content": f"Translate the following query into a kubectl command:\n\nQuery: '{query}'"}
        ],
    )
      
    kubectl_command = chat_completion.choices[0].message.content.strip()
    return kubectl_command
    
def model_response(query, ans):
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": (
                "You are a Kubernetes AI assistant. Respond to each query with only the core answer based on the provided `kubectl` output:\n"
                "- For resource names, return only the primary name — the first identifiable word before any hyphens or extra identifiers.\n"
                "- For example, if the output is 'kubernetes-bootcamp-69ff4c7fd7-r8qdt', respond with 'kubernetes'.\n"
                "- For counts, provide just the number.\n"
                "- Keep responses as brief as possible, without any additional words, explanations, or formatting."
                "- Do not just respond with the API version unless specifically asked when query is related to config details"


            )},
            {"role": "user", "content": f"Query: '{query}'\nAnswer: '{ans}'"}
        ],
    )

    return chat_completion.choices[0].message.content.strip()

'''def execute_kubectl_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return f"Error executing command: {result.stderr}"
'''


def response(query):
    kubectl_command = interpret_query_to_kubectl(query)
    print(kubectl_command)
    
    # Check if any blocking command is in kubectl_command
    if not any(blocked in kubectl_command for blocked in BLOCKING_COMMANDS):
        sys_output = execute_kubectl_command(kubectl_command)
        #print(sys_output)
        final_response = model_response(query, sys_output)
    else:
        final_response = "Error: This action is not allowed. Only read-only queries are permitted."
    
    return final_response

