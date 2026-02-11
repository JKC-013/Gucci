import os
import argparse
from engine import NPCAgent, SimulationState

def main():
    print("==========================================")
    print("   GUCCI AI CO-WORKER SIMULATION ENGINE   ")
    print("==========================================")
    
    # Check for keys
    if not os.getenv("GEMINI_API_KEY"):
        print("\n[ERROR] GEMINI_API_KEY is missing!")
        print("Please set it in your environment or a .env file.")
        print("Example: export GEMINI_API_KEY='your_key_here'")
        return

    # Initialize State
    session = SimulationState(session_id="test-session-001")
    
    # Select Persona
    print("\nSelect a Co-worker to chat with:")
    print("1. Gucci Group CEO (Visionary, Protective)")
    print("2. Gucci Group CHRO (Supportive, People-focused)")
    choice = input("Enter choice (1 or 2): ")
    
    persona_id = "ceo" if choice == "1" else "chro"
    
    try:
        agent = NPCAgent(persona_id=persona_id)
        print(f"\n[System] initialized agent: {agent.persona.name}")
        print("[System] Ready. Type 'quit' to exit.\n")
        
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["quit", "exit"]:
                break
            
            print("...")
            result = agent.run(user_input, session)
            print(f"{agent.persona.name}: {result['assistant_message']}\n")
            
            # Optional: Show context used if debug flag (omitted for clean user exp)
            # if result['context_used']:
            #    print(f"[Debug Context]: {result['context_used'][:100]}...")

    except Exception as e:
        print(f"\n[CRITICAL ERROR] {e}")

if __name__ == "__main__":
    main()
