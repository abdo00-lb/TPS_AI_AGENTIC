import base64

from dotenv import load_dotenv
from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI


def encode_image(path: str) -> str:
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


load_dotenv(override=True)

image_path = "rag.png"
image_b64 = encode_image(image_path)

llm = ChatOpenAI(model="gpt-5.2")

message = HumanMessage(
    content=[
        {"type": "text", "text": "Qu'est-ce que tu vois dans cette image ?"},
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{image_b64}"},
        },
    ]
)

response = llm.invoke([message])

print(response.content)