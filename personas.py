from dataclasses import dataclass

@dataclass
class Persona:
    id: str
    name: str
    system_prompt: str
    style_guide: str

    def compile_prompt(self, context: str = "") -> str:
        return f"""
ROLE: {self.name}

CORE INSTRUCTIONS:
{self.system_prompt}

STYLE GUIDE:
{self.style_guide}

CONTEXT FROM KNOWLEDGE BASE:
{context}

Now respond to the user based on the context above.
"""

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
