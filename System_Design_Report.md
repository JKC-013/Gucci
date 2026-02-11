# Gucci AI Co-Worker Engine - System Design Report

## 1. Persona & Interaction Design (The "Soul")

Define distinct system prompts for each of the three AI co-workers.

### 1.1 Persona Definitions
Use a `Persona` class configuration to inject specific instructions.

*   **NPC A: Gucci Group CEO**
    *   **Tone:** Visionary, protective of the brand, authoritative but open to logic.
    *   **Hidden Constraints:** Will NOT compromise on "Brand DNA" for the sake of efficiency.
    *   **Key Knowledge:** Gucci Mission, Culture, NDA.
*   **NPC B: Gucci Group CHRO**
    *   **Tone:** Strategic, supportive, people-focused.
    *   **Goals:** Talent development, inter-brand mobility.
    *   **Key Knowledge:** Competency Framework (Vision, Entrepreneurship, Passion, Trust).
*   **NPC C: Regional Manager (Employer Branding)**
    *   **Tone:** Practical, operational, slightly overwhelmed.
    *   **Context:** Knows the on-the-ground reality, rollout challenges.

### 1.2 Dialogue Flow (Scripted Examples)
*   **Good Interaction:** User acknowledges brand distinctiveness while proposing a unified framework. CEO responds warmly.
*   **Bad Interaction:** User proposes a "one-size-fits-all" standard hiring process. CEO shuts it down citing "Brand Autonomy".

### 1.3 State Management
Implement a **Conversation History** mechanism.
*   **Storage:** In-memory dictionary (for prototype) or Redis/Database (for production), keyed by `session_id`.
*   **Structure:** `List[Dict[role, content]]`.
*   **Memory Depth:** Pass the last N turns to the LLM to ensure context retention.

## 2. System Architecture (The "Engine")

### 2.1 High-Level Diagram
```mermaid
graph TD
    User[User / Simulation Taker] -->|Message + PersonaID| API[FastAPI Orchestration Layer]
    API -->|Retrieve History| Memory[State Store (Redis/Memory)]
    API -->|Monitor| Director[Director / Supervisor Agent]
    Director --o|Intervention Hint| API
    API -->|Context Query| VectorDB[Qdrant (RAG)]
    API -->|Generate Response| LLM[LLM Engine (Gemini/OpenAI)]
    LLM --> API
    API --> User
```

### 2.2 Tool Use
*   **Knowledge Retrieval:** The primary tool is the RAG engine (accessing Gucci docs, policies).
*   **Mock Tools:** Define specific "function calls" or "tool triggers".
    *   *Example:* `lookup_competency_framework()` -> Returns the specific matrix.
    *   Implementation: Keyword detection or LLM function calling.

### 2.3 Latency vs. Quality
*   **Strategy:** Hybrid Approach.
    *   **Fast Path:** For simple chitchat, skip RAG.
    *   **Quality Path:** For domain questions, perform parallel RAG retrieval while processing input.
    *   **Streaming:** Stream the response token-by-token to reduce *perceived* latency.

## 3. The "Director" Layer (Orchestration)

### 3.1 Supervisor Agent
An invisible background agent that analyzes the *entire* conversation history, not just the last prompt.

### 3.2 Stuck Detection & Hints
*   **Trigger:** If the conversation loop count > 5 without progress markers (defined keywords like "approved", "framework", "plan").
*   **Action:** Injects a "System Note" or makes the NPC say something leading, e.g., "Maybe we should focus on the Competency Framework first?"

## 4. Prototype / Implementation Strategy

### 4.1 Tech Stack
*   **Language:** Python 3.10+
*   **API Framework:** FastAPI (Async, performant, easy to document).
*   **LLM Orchestration:** Manual OpenAI Client (lightweight) or LangChain (if complex chains needed). *Decision: Manual Client for transparency in this interview task.*
*   **Vector DB:** Qdrant (Low latency, easy docker setup).
*   **LLM Provider:** Gemini Flash/Pro (Cost-effective, large context window).

### 4.2 Proposed Code Structure
Adapt the `rag_bot_sys` structure:
*   `app.py`: Main API entry point.
*   `personas.py`: Definitions of CEO, CHRO, etc.
*   `engine.py`: Core logic for State + RAG + LLM generation.
*   `director.py`: Supervisor logic.

### 4.3 Validation
*   **Role-Playing Fidelity:** Tested via specific "Bad Actor" prompts.
*   **Architecture Soundness:** Validated by separation of concerns (API vs Engine vs Data).
