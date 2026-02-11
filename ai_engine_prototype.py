import logging
import uuid
import os
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime

# --- Mocking External Libraries for the Prototype ---
# In a real app, these would be:
# from openai import OpenAI
# from vector_db import QdrantStorage

logger = logging.getLogger("ai_engine")
logging.basicConfig(level=logging.INFO)

# --- 1. Data Structures & State Management ---

@dataclass
class Message:
    role: str  # "user", "assistant", "system", "director"
    content: str
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class SimulationState:
    session_id: str
    history: List[Message] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)  # Arbitrary facts learned
    turn_count: int = 0

# --- 2. Persona Definitions ---

class Persona:
    def __init__(self, id: str, name: str, system_prompt: str, style_guide: str):
        self.id = id
        self.name = name
        self.system_prompt = system_prompt
        self.style_guide = style_guide

    def compile_prompt(self, context: str = "") -> str:
        """Combines the persona's soul with dynamic context."""
        return f"""
        ROLE: {self.name}
        
        CORE INSTRUCTIONS:
        {self.system_prompt}
        
        STYLE GUIDE:
        {self.style_guide}
        
        CONTEXT FROM KNOWLEDGE BASE:
        {context}
        """

# Define the Gucci Personas
PERSONAS = {
    "ceo": Persona(
        id="ceo",
        name="Gucci Group CEO",
        system_prompt="""
        You are the CEO of Kering/Gucci Group. You value Brand Autonomy above all else.
        Your goal is to ensure the Group DNA is respected while allowing individual brands (YSL, Gucci, Bottega) to flourish independently.
        If the user suggests a 'one-size-fits-all' centralization, REJECT IT firmly but professionally.
        """,
        style_guide="Direct, visionary, protective, executive brevity."
    ),
    "chro": Persona(
        id="chro",
        name="Gucci Group CHRO",
        system_prompt="""
        You are the Chief HR Officer. Your mission is Talent Development and Mobility.
        You care about the Competency Framework: Vision, Entrepreneurship, Passion, Trust.
        You want to support the brands, not police them.
        """,
        style_guide="Encouraging, questions-focused, strategic."
    )
}

# --- 3. The "Director" Layer (Supervisor) ---

class DirectorAgent:
    """Invisible supervisor that monitors the chat."""
    
    def analyze(self, state: SimulationState) -> Optional[str]:
        """
        Checks if the user is stuck or off-track.
        Returns a 'Hint' string if intervention is needed, else None.
        """
        # specialized logic: If conversation is too long (> 5 turns) and no "agreement" reached
        if state.turn_count > 5:
             # Heuristic check (in reality, another LLM call would analyze this)
             last_msg = state.history[-1].content.lower()
             if "?" in last_msg and "help" in last_msg:
                 return "Hint: Try asking the CEO about 'Brand Autonomy' constraints."
        return None

# --- 4. Main Engine Class (The "Prototype") ---

class NPCAgent:
    def __init__(self, persona_id: str, vector_db_client=None):
        self.persona = PERSONAS.get(persona_id)
        if not self.persona:
            raise ValueError(f"Invalid Persona ID: {persona_id}")
        self.vector_db = vector_db_client
        self.llm = self._mock_llm_client() # Mocking the connection

    def _mock_llm_client(self):
        # In reality: return OpenAI(api_key=...)
        return "MockLLM"

    def _retrieve_context(self, query: str) -> str:
        """Simulate RAG retrieval."""
        # real implementation:
        # return self.vector_db.search(query)
        return "Context: Gucci Group brands operate with high autonomy."

    def _generate_reply(self, messages: List[Dict]) -> str:
        """Simulate LLM Generation."""
        # Real implementation: client.chat.completions.create(...)
        last_user_msg = messages[-1]['content']
        if "centralize" in last_user_msg.lower():
             return "I cannot accept a centralized approach. It destroys our Brand DNA."
        return f"[{self.persona.name}]: I hear your point about {last_user_msg[:10]}..."

    def run(self, user_message: str, state: SimulationState):
        """
        Main Function: Takes message, updates state, returns response + flags.
        """
        # 1. Update State
        state.history.append(Message(role="user", content=user_message))
        state.turn_count += 1
        
        # 2. RAG (Retrieval)
        context = self._retrieve_context(user_message)
        
        # 3. Construct Payload
        system_msg = self.persona.compile_prompt(context=context)
        messages_payload = [{"role": "system", "content": system_msg}]
        
        # Add history (last 5 turns for context window)
        for msg in state.history[-5:]:
            messages_payload.append({"role": msg.role, "content": msg.content})
            
        # 4. Generate Response
        response_text = self._generate_reply(messages_payload)
        
        # 5. Update State with Reply
        state.history.append(Message(role="assistant", content=response_text))
        
        # 6. Director Check (Parallel or Post-process)
        director = DirectorAgent()
        hint = director.analyze(state)
        
        return {
            "assistant_message": response_text,
            "state_snapshot": state,
            "director_hint": hint
        }

# --- 5. Runnable Script (Demo) ---

if __name__ == "__main__":
    # Initialize
    print("--- Starting Simulation Session ---")
    session = SimulationState(session_id="sim-001")
    agent = NPCAgent(persona_id="ceo")
    
    # Turn 1
    user_input = "I think we should centralize the hiring process for all brands."
    print(f"User: {user_input}")
    
    result = agent.run(user_input, session)
    print(f"Agent: {result['assistant_message']}")
    
    if result['director_hint']:
        print(f"*** DIRECTOR INTERVENTION: {result['director_hint']} ***")
    
    # Turn 2
    user_input = "But it would save money?"
    print(f"\\nUser: {user_input}")
    result = agent.run(user_input, session)
    print(f"Agent: {result['assistant_message']}")
