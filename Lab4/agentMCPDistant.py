import asyncio
import socket
import threading
import time

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from mcp.server.fastmcp import FastMCP


load_dotenv()

HOST = "127.0.0.1"
PORT = 8000

mcp_server = FastMCP("travel_server", host=HOST, port=PORT)


@mcp_server.tool()
def search_flights(origin: str, destination: str, date: str) -> str:
    """Search for available flights between two cities on a given date."""
    return (
        f"Flights from {origin} to {destination} on {date}:\n"
        f"- AT 601 | 08:00 → 09:15 | Direct | 850 MAD\n"
        f"- AT 603 | 14:30 → 15:45 | Direct | 920 MAD\n"
        f"- AT 605 | 19:00 → 20:15 | Direct | 780 MAD"
    )


@mcp_server.tool()
def get_flight_price(flight_number: str) -> str:
    """Get the price and details of a specific flight."""
    prices = {
        "AT 601": "850 MAD - Economy class, 1 bag included",
        "AT 603": "920 MAD - Economy class, 1 bag included",
        "AT 605": "780 MAD - Economy class, carry-on only",
    }
    return prices.get(flight_number, f"Flight {flight_number} not found")


def wait_for_server(host: str, port: int, timeout: int = 10) -> bool:
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.3)
    return False


def run_server():
    mcp_server.run(transport="streamable-http")


async def main():
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()

    if not wait_for_server(HOST, PORT):
        raise RuntimeError("MCP HTTP server did not start in time")

    print(f"Serveur MCP HTTP démarré sur http://{HOST}:{PORT}/mcp")

    client = MultiServerMCPClient(
        {
            "travel_server": {
                "transport": "streamable_http",
                "url": f"http://{HOST}:{PORT}/mcp",
            }
        }
    )

    tools = await client.get_tools()
    print(f"Tools disponibles : {[tool.name for tool in tools]}")

    llm = ChatOllama(model="llama3.2:3b", temperature=0)

    agent = create_agent(
        model=llm,
        tools=tools,
        checkpointer=InMemorySaver(),
        system_prompt="You are a travel agent. No follow up questions.",
    )

    config = {"configurable": {"thread_id": "1"}}

    response = await agent.ainvoke(
        {
            "messages": [
                HumanMessage(
                    content="Get me a direct flight from Rabat to Agadir on August 31st"
                )
            ]
        },
        config=config,
    )

    print(response["messages"][-1].content)


asyncio.run(main())