from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.postgres import PostgresTools
from dotenv import load_dotenv
import os

#
load_dotenv()

#
HOST = os.getenv("HOST")
DB_NAME = os.getenv("DB_NAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

# Initialize PostgresTools with connection details
postgres_tools = PostgresTools(
    host=HOST,
    port=5432,
    db_name=DB_NAME,
    user=USER,
    password=PASSWORD,
    table_schema="public",
)

# Create an agent with the PostgresTools
agent = Agent(tools=[postgres_tools],
              model=Groq(id="llama-3.3-70b-versatile"))

agent.print_response("Fale todas as tabelas do banco de dados", markdown=True)
