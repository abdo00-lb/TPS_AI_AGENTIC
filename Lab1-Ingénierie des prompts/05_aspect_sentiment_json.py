import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv(override=True)

PROMPT = """
Analyse les sentiments par aspect dans les avis sur des ordinateurs portables.

Aspects possibles :
- screen
- keyboard
- pad

Pour chaque avis :
- détecter les aspects présents ;
- attribuer à chaque aspect une polarité : positive, negative ou neutral ;
- retourner un objet JSON avec :
  - category : liste des aspects
  - polarity : liste des polarités correspondantes ;
- si un aspect n'apparaît pas, lui attribuer la polarité neutral.
"""

review = "L'ecran est tres bon, mais je n'ai pas aime le pad. Le clavier est acceptable."

client = ChatOpenAI(
    model="gpt-5.2",
    temperature=0,
    model_kwargs={
        "response_format": {"type": "json_object"}
    },
)

messages = [
    {"role": "system", "content": PROMPT},
    {"role": "user", "content": review},
]

response = client.invoke(messages)
payload = json.loads(response.content)

print(response.content)
print("\nJSON parse:", payload)
print("Premiere polarite:", payload["polarity"][0])