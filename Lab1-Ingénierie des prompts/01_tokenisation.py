import tiktoken


def count_tokens(text: str, encoding_name: str = "o200k_base") -> int:
    """Return the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(text))


encoding = tiktoken.encoding_for_model("gpt-4o")
print("Encoding utilise:", encoding.name)

system_message = """
Perform Sentiment analysis of the review presented in the user message.
The result should be positive or negative.
Do not justify your response.
"""

tokens = encoding.encode(system_message)

print("Nombre de tokens du prompt system:", len(tokens))
print("Liste des tokens:", tokens)
print("Reconstruction token par token:")
for token in tokens:
    piece = encoding.decode_single_token_bytes(token).decode("utf-8", errors="ignore")
    print(piece, end="")

print("\n")
print("Exemple simple:", count_tokens("tiktoken is great!"))