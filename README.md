# AI Co-Worker Engine (Gucci Simulation) - Interview Submission

## Overview
This repository contains the design and functional prototype for the **AI Co-Worker Engine**, specifically tailored for the "Gucci Group: Leadership Development" simulation scenario.

The solution is divided into two main components:
1.  **System Design Report:** A comprehensive architectural breakdown (The "Think").
2.  **Functional Prototype:** A runnable Python engine using RAG and LLMs (The "Build").

## Repository Structure

*   `System_Design_Report.md`: **[READ THIS FIRST]** Covers Parts 1, 2, and 3 of the assignment (Personas, Architecture, Orchestration).
*   `test_run.py`: The entry point script to chat with the AI Co-workers.
*   `engine.py`: Core logic for State Management and RAG context retrieval.
*   `personas.py`: Configuration for the **Gucci CEO** and **CHRO** characters.
*   `llm_client.py`: Wrapper for the Gemini API (handling Free Tier limits).
*   `config.py`: Configuration settings.

## Addressing the Assignment Requirements

### Part 1: Persona & Interaction Design
**Location:** `System_Design_Report.md` (Section 1)
*   Defined the "Soul" of the Gucci CEO (Visionary, Protective) and CHRO (Supportive).
*   Drafted "Good vs. Bad" dialogue scripts to demonstrate fidelity.

### Part 2: System Architecture
**Location:** `System_Design_Report.md` (Section 2)
*   **Architecture:** High-level Mermaid diagram showing the flow from User -> Orchestrator -> RAG -> LLM.
*   **Scalability:** Implemented a **Vector Database (Qdrant)** for knowledge retrieval, ensuring the system can handle thousands of documents without context window overflow.

### Part 3: The "Director" Layer
**Location:** `System_Design_Report.md` (Section 3)
*   Designed an invisible "Supervisor Agent" concept to monitor conversation health and inject hints if the user gets stuck.

### Part 4: Prototype / Implementation
**Location:** `test_run.py` & `engine.py`
*   **Tech Stack:** Python 3.10+, Google Gemini (LLM), Qdrant (Vector DB).
*   **Functionality:**
    *   **Dynamic Role-Playing:** The AI adheres to the specific "Gucci DNA" constraints.
    *   **Context Awareness:** Uses RAG to pull relevant context before answering.
    *   **Memory:** Retains conversation history for coherent multi-turn dialogue.

## How to Test the Prototype

To minimize friction, I have included a simple CLI script.

### 1. Prerequisites
*   Python 3.10+
*   `pip`

### 2. Installation
```bash
pip install google-generativeai qdrant-client python-dotenv
```

### 3. Configuration
Set your API keys in `config.py` (or environment variables).
*   `GEMINI_API_KEY`: Required (Free Tier is fine).
*   `QDRANT_URL/KEY`: Required for RAG (or use local/memory mode if configured).

### 4. Run
```bash
python test_run.py
```
*Select a character (1 for CEO, 2 for CHRO) and start chatting.*

## Tech Stack Decisions

*   **LLM (Google Gemini):** Chosen for its large context window and cost-effectiveness (Free Tier) for prototyping.
*   **Vector DB (Qdrant):** Chosen for low latency and ease of deployment (Docker/Cloud).
*   **Orchestration (Custom Python):** Used a lightweight custom class (`NPCAgent`) instead of heavy frameworks (LangChain) to demonstrate clear understanding of the underlying logic and control flow.

---
**Note on API Limits:**
This prototype uses the **Free Tier** of Google Gemini. If you encounter a "System Unavailable" message, it is due to the request-per-minute quotas. The system is designed to handle this gracefully by informing the user.

### 5. Running the UI (Streamlit)

**[Streamlit Live Demo](https://aiguccigroup.streamlit.app/)**

To run it locally:
1.  Ensure you have installed the dependencies:
    ```bash
    pip install streamlit
    ```
2.  Run the app:
    ```bash
    streamlit run app.py
    ```
This will open the simulation in your default web browser.
