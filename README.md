# 🚀 PhiloAgent: Production-Grade Intelligent Agent System

This project implements a multi-agent philosophical assistant using LangGraph for orchestration, Groq for low-latency inference, and MongoDB for persistent long-term memory.

---
## 📁 Project Structure
```bash
RAG_Powered_conversationalAI/
├── philoagent/
│ ├── data/
│ │ ├── pycache/
│ │ ├── init.py
│ │ ├── deduplicate_documents.py
│ │ └── extract.py
│ │
│ ├── src/
│ │ └── philoagents/
│ │ ├── application/
│ │ │ ├── conversation_service/
│ │ │ │ └── pycache/
│ │ │ │
│ │ │ ├── workflow/
│ │ │ │ ├── pycache/
│ │ │ │ ├── init.py
│ │ │ │ ├── chains.py
│ │ │ │ ├── edges.py
│ │ │ │ ├── graph.py
│ │ │ │ ├── nodes.py
│ │ │ │ ├── state.py
│ │ │ │ └── tools.py
│ │ │ │
│ │ │ ├── generate_response.py
│ │ │ ├── reset_conversation.py
│ │ │ │
│ │ │ ├── evaluation/
│ │ │ │ ├── init.py
│ │ │ │ ├── evaluate.py
│ │ │ │ ├── generate_dataset.py
│ │ │ │ └── upload_dataset.py
│ │ │ │
│ │ │ ├── rag/
│ │ │ │ ├── init.py
│ │ │ │ ├── embeddings.py
│ │ │ │ ├── retrievers.py
│ │ │ │ └── splitters.py
│ │ │ │
│ │ │ └── long_term_memory.py
│ │ │
│ │ ├── domain/
│ │ │ ├── init.py
│ │ │ ├── evaluation.py
│ │ │ ├── exceptions.py
│ │ │ ├── philosopher.py
│ │ │ ├── philosopher_factory.py
│ │ │ └── prompts.py
│ │ │
│ │ ├── infrastructure/
│ │ │ ├── mongo/
│ │ │ │ ├── init.py
│ │ │ │ ├── client.py
│ │ │ │ └── indexes.py
│ │ │ │
│ │ │ ├── api.py
│ │ │ ├── api2.py
│ │ │ ├── config.py
│ │ │ └── opik_utils.py
│ │ │
│ │ └── tools/
│ │
│ ├── philoagents_ui/
│ │ ├── streamlit1.py
│ │ ├── streamlit2.py
│ │ └── streammock.py
│ │
│ ├── .dockerignore
│ ├── .env
│ ├── .env.example
│ ├── .python-version
│ ├── Dockerfile
│ ├── docker-compose.yml
│ ├── langgraph.json
│ ├── pyproject.toml
│ ├── uv.lock
│ ├── requirements.txt
│ └── README.md

```

## Deep Dive: Project Architecture

### 1. Workflow Orchestration (`philoagent/src/application/workflow/`)

The core of the system is a Stateful Finite State Machine (FSM). Unlike simple linear chains, this allows for cycles, retries, and complex decision-making.

- **graph.py**: The central entry point where Nodes and Edges are compiled into a LangGraph.
- **state.py**: Defines the TypedDict that carries the conversation state, including the shared memory buffer and document context.
- **nodes.py & edges.py**: Houses the discrete units of logic (e.g., "Analyze Query", "Retrieve Context") and the conditional routing logic (e.g., "Does the context answer the user's question?").

---

### 2. Advanced RAG Pipeline (`philoagent/src/application/rag/`)

The system uses a robust retrieval strategy specifically optimized for philosophical texts (Stanford Encyclopedia of Philosophy).

- **splitters.py**: Implements semantic or recursive character splitting to maintain philosophical context.
- **retrievers.py**: Contains logic for Hybrid Search or Self-Querying to ensure high-precision retrieval.
- **embeddings.py**: Managed interface for vectorizing queries using modern embedding models.

---

### 3. Domain-Driven Design (`philoagent/src/domain/`)

To ensure the system is "philosopher-agnostic," we use a domain layer to abstract the "Business Logic" of philosophy.

- **philosopher_factory.py**: Uses the Factory Pattern to dynamically load different personas (Socrates, Kant, etc.) with specific behavioral constraints.
- **prompts.py**: A centralized "Prompt Bank" ensuring version control and consistency across different agent nodes.

---

### 4. Infrastructure & Persistence (`philoagent/src/infrastructure/`)

Ensures the system is production-ready with scalable backend services.

- **MongoDB Integration (`mongo/`)**: Handles persistent state and long-term memory, allowing the agent to "remember" users across sessions.
- **FastAPI Layer (`api.py`)**: Exposes the agentic logic as high-performance REST endpoints.
- **High-Speed Inference**: Integrated with Groq via `config.py` to achieve sub-second response times for complex reasoning.

---

### 5. LLMOps & Evaluation (`philoagent/src/application/evaluation/`)

We treat LLM performance as a measurable engineering metric rather than "vibes."

- **Observability**: Integrated with Comet ML Opik (`opik_utils.py`) for full-trace logging, cost monitoring, and prompt versioning.
- **Evaluation Framework (`evaluate.py`)**: Automates RAG evaluation metrics (Faithfulness, Answer Relevance) using a synthetic dataset generated by the system itself (`generate_dataset.py`).

---

## 📦 Deployment & Tooling

- **Package Management**: Managed by `uv` (as seen in `uv.lock` and `pyproject.toml`) for 10x faster dependency resolution.
- **Containerization**: Fully Dockerized with a multi-stage `Dockerfile` and `docker-compose.yml` for local orchestration of the API, UI, and Database.
- **UI Layer (`philoagents_ui/`)**: Multiple Streamlit entry points for testing different interaction paradigms (Streaming vs. Batch).

---

## 💡 Why this architecture matters for an interview

- **Scalability**: The separation of application and infrastructure means you can switch from MongoDB to Pinecone, or Groq to OpenAI, by only changing the infrastructure layer.
- **Reliability**: By including an `evaluation/` module, you demonstrate that you build agents that can be tested and validated before deployment.
- **Efficiency**: Using `uv` and LangGraph shows you are utilizing the most performant and modern tools in the Python/AI ecosystem.
