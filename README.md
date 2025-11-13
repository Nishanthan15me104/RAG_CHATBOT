# 🚀 Project Structure: Intelligent Agent System Development

This document outlines the core components and structure of a project focused on developing and deploying production-grade intelligent agents using LangGraph and high-speed inference platforms like Groq.

---

## 1. Agent Core & Orchestration (`/agent_core`)

This module houses the central intelligence and decision-making logic of the system.

* `agent_core/`
    * `langgraph_flow.py`: Defines the **Finite State Machine (FSM)** and conditional routing logic using LangGraph.
    * `multi_agent_router.py`: Logic for coordinating actions between specialized agents (e.g., Planner, Retriever).


---

## 2. Retrieval-Augmented Generation (RAG) System (`/rag_pipeline`)

Dedicated to efficient knowledge management and information retrieval.

* `rag_pipeline/`
    * `ingestion.py`: Scripts for document parsing, chunking, and metadata extraction from sources (e.g., Wikipedia).
    * `vector_db_config.py`: Configuration and connection logic for the chosen vector store (e.g., Pinecone, Chroma).
    * `retrieval_strategies.py`: Implementation of complex search techniques like **HyDE** and **re-ranking** algorithms.
    * `knowledge_base/`
        * `stanford_data/`: Ingested and cleaned Stanford Encyclopedia data.

---

## 3. Backend Services & Deployment (`/backend_service`)

The layer responsible for hosting the agent and exposing it as a scalable service.

* `backend_service/`
    * `main.py`: **FastAPI** application defining **RESTful API** endpoints.
    * `Dockerfile`: Configuration file for **Docker** containerization.
    * `docker-compose.yml`: Orchestration file for managing service dependencies.

---

## 4. Memory & State Management (`/memory`)

Manages the short-term and long-term persistence for dynamic conversations.

* `memory/`
    * `mongodb_client.py`: Configuration and client setup for **MongoDB**.
    * `conversation_history.py`: Logic for storing and retrieving short-term conversation context.
    * `long_term_schemas.py`: Data models for persistent state and user profiles.

---

## 5. LLM Integration & Tooling (`/config`)

Centralized configuration for external services and modern development practices.

* `config/`
    * `llm_providers.py`: API wrappers and configuration for **GroqCloud** integration.
    * `tools/`
        * `tool_definitions.py`: Definition and registration of external **Tool Calling** functions.
    * `.ruff.toml`: Configuration file for the `ruff` linter.
    * `requirements.txt` / `pyproject.toml`: Dependency files using `uv` best practices.

---

## 6. LLMOps & Evaluation (`/llmops`)

Ensures ongoing quality, performance, and maintainability.

* `llmops/`
Observability for RAG agents (part of LLMOps): evaluating agents, prompt monitoring, prompt versioning, etc. - which is done by using comet ml opik
