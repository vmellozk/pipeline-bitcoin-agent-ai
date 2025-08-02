from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv
import os

#
load_dotenv()

#
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

#
agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    description="Aqui deve ser especificado a descrição do tipo de agente.",
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True
)

#
agent.print_response("Aqui o prompt.", stream=True)
