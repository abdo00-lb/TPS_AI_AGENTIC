from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent


loader = PyPDFLoader("acmecorp-employee-handbook.pdf")
documents = loader.load()

print(f"Pages chargées : {len(documents)}")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    add_start_index=True,
)
chunks = splitter.split_documents(documents)

print(f"Nombre de chunks : {len(chunks)}")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = InMemoryVectorStore(embeddings)
doc_ids = vector_store.add_documents(chunks)

print(f"Documents indexés : {len(doc_ids)}")

query = "How many days of vacation does an employee get in their first year?"
results = vector_store.similarity_search(query)

print("\n--- Résultat de la recherche sémantique ---")
print(results[0])


@tool
def search_handbook(query: str) -> str:
    """Search the employee handbook for relevant information."""
    matches = vector_store.similarity_search(query)
    return matches[0].page_content


llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0,
)

agent = create_react_agent(
    model=llm,
    tools=[search_handbook],
    prompt="You are a helpful agent that can search the employee handbook for information.",
)

response = agent.invoke(
    {
        "messages": [
            HumanMessage(
                content="How many days of vacation does an employee get in their first year?"
            )
        ]
    }
)

print("\n--- Réponse de l'Agent RAG ---")
print(response["messages"][-1].content)