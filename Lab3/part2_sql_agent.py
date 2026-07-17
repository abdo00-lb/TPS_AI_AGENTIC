from langchain_community.utilities import SQLDatabase
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent


db = SQLDatabase.from_uri("sqlite:///Chinook.db")


@tool
def sql_query(query: str) -> str:
    """Obtain information from the database using SQL queries."""
    try:
        print(f"Executing SQL query: {query}")
        return db.run(query)
    except Exception as error:
        return f"Error: {error}"


print("--- Test du tool sql_query ---")
print(sql_query.invoke("SELECT * FROM Artist LIMIT 10"))


llm = ChatOllama(model="llama3.2:3b", temperature=0)

prompt = """You are a SQL expert.

Rules:
- Only use sql_query tool
- The sql_query tool takes a SQL query as input and returns the result of the query.
- Only use available columns
- If information does not exist, say so
- Do not guess
- Return the results in a human readable format, not as raw SQL results.

Database schema:
Table Artist:
- ArtistId
- Name
"""

agent = create_react_agent(
    model=llm,
    tools=[sql_query],
    prompt=prompt,
)

response = agent.invoke(
    {
        "messages": [
            HumanMessage(content="Give me the first 5 artists in the database")
        ]
    }
)

print("\n--- Réponse de l'Agent SQL ---")
print(response["messages"][-1].content)