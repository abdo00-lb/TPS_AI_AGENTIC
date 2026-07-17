from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.messages import HumanMessage, SystemMessage


load_dotenv(override=True)

MODEL_NAME = "openai/gpt-oss-120b"

assistant = ChatGroq(model=MODEL_NAME, temperature=0)

system_msg = SystemMessage(
    content="You are a helpful assistant. The output should be in Markdown."
)
user_msg = HumanMessage(content="C'est quoi un Agent AI ?")

result = assistant.invoke([system_msg, user_msg])

print(result.content)