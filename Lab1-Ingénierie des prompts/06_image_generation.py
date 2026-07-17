import base64
from pathlib import Path

from dotenv import load_dotenv
from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI


load_dotenv(override=True)

MODEL_NAME = "gpt-5.2"
OUTPUT_PATH = Path("generated_cat_java.png")

llm = ChatOpenAI(model=MODEL_NAME)

image_tool = {"type": "image_generation", "quality": "high"}
model_with_image = llm.bind_tools([image_tool])

prompt = "Je veux une photo d'un chat qui code du Java."

response = model_with_image.invoke([HumanMessage(content=prompt)])

image_block = response.content_blocks[0]
image_data = base64.b64decode(image_block["base64"])

OUTPUT_PATH.write_bytes(image_data)

print(f"Image générée: {OUTPUT_PATH.name}")