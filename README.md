# AIOps Project

AIOps is an AI-powered operations assistant built with LangGraph and LangChain that helps automate workflow configurations for various integrations.

## Overview

This project implements an AI agent system that can:
- Process user requests related to workflow configurations
- Select appropriate integration actions based on the user's needs
- Guide users through the required input collection process
- Generate configuration proposals for various integration actions

## Project Structure

```
├── graph.py            # Main LangGraph implementation
├── state.py            # State management classes for the agent
├── requirement.txt     # Project dependencies
├── langgraph.json      # LangGraph configuration
└── prompts/            # Prompt templates for the AI agent
    ├── Agent_Instructions.txt      # Core agent instructions
    ├── integration_actions.txt     # Available integration actions
    ├── Prompt_Decorators.txt       # Prompt formatting and decorators
    ├── workflow_context.txt        # Context for workflow processing
    └── workflow_spec.txt           # Workflow specification format
```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd aiops
   ```

2. Install dependencies:
   ```bash
   pip install -r requirement.txt
   ```

3. Set up environment variables:
   Create a `.env` file with the necessary API keys:
   ```
   # OpenAI API Key
   OPENAI_API_KEY=your_openai_key

   # Optional: Google Generative AI API Key (if using Gemini)
   API_KEY_GEMINI=your_gemini_key

   # Optional: LangSmith (if using for tracing)
   LANGCHAIN_API_KEY=your_langchain_api_key

   # Optional: Langfuse (if using for tracing)
   LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
   LANGFUSE_SECRET_KEY=your_langfuse_secret_key
   ```

## Usage

You can run the agent using LangGraph CLI:

```bash
langgraph dev --allow-blocking
```

This will start the agent, which can then accept user requests and help configure workflows based on various integration actions.

## How It Works

1. The agent receives a user request (e.g., "Create a spreadsheet with my summarized scraped pages results")
2. It analyzes the request and selects the most relevant integration action from the available options
3. The agent identifies all required input values and asks the user for any missing information
4. Once all inputs are collected, it generates a configuration proposal for the chosen action
5. The workflow configuration can then be executed through the AirOps platform

## Development

To extend the agent with new capabilities:

1. Add new integration actions to `prompts/integration_actions.txt`
2. Update prompt templates in the `prompts/` directory as needed
3. Modify the state management in `state.py` if additional state tracking is required
4. Enhance the graph workflow in `graph.py` to add new agent behaviors

## Dependencies

- LangGraph
- LangChain
- LangChain MCP Adapters
- LangSmith (optional, for tracing)
- Langfuse (optional, for tracing)
- OpenAI API
- Google Generative AI (optional)

## License

[Add license information here]
