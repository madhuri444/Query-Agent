# Query-Agent
This repository contains a Kubernetes AI agent designed to interpret user queries and retrieve relevant information about applications deployed in a Kubernetes cluster. The agent processes natural language inputs from users, interprets them into Kubernetes commands, executes those commands, and returns refined responses.

Approach
Overview
This agent uses a Flask-based API to receive queries from users, which are then processed by an LLM (Large Language Model) capable of understanding natural language and generating Kubernetes commands. The commands are executed on the local operating system, and the results are refined and returned to the user in a structured JSON format.

Key Components
Flask API with Pydantic:

A POST endpoint (/query) receives user queries in JSON format.
The Pydantic model (QueryResponse) ensures structured validation and response formatting.
Query Processing by the LLM:

Upon receiving a query, the LLM interprets the natural language input and generates a suitable Kubernetes command.
The LLM references the Kubernetes config file (~/.kube/config) to understand the cluster configuration and ensure commands are aligned with the current cluster context.
Command Execution:

The generated command is executed on the local system.
Execution is logged for traceability and debugging.
Response Refinement and Return:

The command output is processed by the LLM to improve readability and context.
A refined response is returned to the user in JSON format.
Flow of Execution
User sends a query via POST request to the /query endpoint.
Flask API receives the query and logs it.
The LLM interprets the query and generates a Kubernetes command based on the query intent.
The generated command is executed on the local operating system.
Output from the command execution is sent back to the LLM for refinement.
A user-friendly response is sent back to the user in JSON format.
Example
For a query like "How many pods are in the default namespace?", the agent:

Generates the command kubectl get pods -n default.
Executes the command on the local system.
Returns the output with a refined response: "There are 5 pods in the default namespace."


