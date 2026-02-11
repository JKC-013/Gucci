from typing import List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime
import logging
from personas import PERSONAS, Persona
from llm_client import LLMClient
from vector_db import QdrantStorage

logger = logging.getLogger("gucci_ai")

@dataclass
class Message:
    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class SimulationState:
    session_id: str
    history: List[Message] = field(default_factory=list)
    turn_count: int = 0

class NPCAgent:
    def __init__(self, persona_id: str):
        self.persona = PERSONAS.get(persona_id)
        if not self.persona:
            raise ValueError(f"Invalid Persona ID: {persona_id}")
        
        self.vector_db = QdrantStorage()
        self.llm_client = LLMClient()

    def _retrieve_context(self, query: str) -> str:
        """RAG Retrieval."""
        try:
            query_embedding = self.llm_client.embed_text(query)
            # Use top_k=3
            results = self.vector_db.search(query_embedding, top_k=3)
            return "\n\n".join(results)
        except Exception as e:
            logger.error(f"RAG Retrieval Error: {e}")
            return ""

    def run(self, user_message: str, state: SimulationState):
        """
        Main Engine Loop:
        1. Update History
        2. Retrieve Context (RAG)
        3. Build Prompt
        4. Generate Response (LLM)
        5. Return
        """
        state.history.append(Message(role="user", content=user_message))
        state.turn_count += 1
        
        context = self._retrieve_context(user_message)
        
        system_msg = self.persona.compile_prompt(context=context)
        
        # Build prompt for LLM (simplified for this demo, usually we send chat history object)
        full_prompt = f"{system_msg}\n\nCONVERSATION HISTORY:\n"
        for msg in state.history[-10:]: # Last 10 messages
            full_prompt += f"{msg.role.upper()}: {msg.content}\n"
        
        full_prompt += "\nASSISTANT:"
        
        response_text = self.llm_client.generate_response(full_prompt)
        
        state.history.append(Message(role="assistant", content=response_text))
        
        return {
            "assistant_message": response_text,
            "context_used": context
        }
