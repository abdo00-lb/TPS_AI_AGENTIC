# LAB 4 : Le Model Context Protocol (MCP)

**Master BDCC — SMA et IAD**  
**Prof. RETAL SARA**

## Objectif

Intégrer le **Model Context Protocol (MCP)** avec LangChain afin de connecter des agents LLM à des serveurs MCP locaux ou distants via différents transports, notamment **stdio** et **streamable-http**. [web:98][web:145]

---

## Structure du projet

```text
Lab4-MCP/
├── mcp_local_server.py      # Serveur MCP local (stdio) : tools + resources + prompts
├── mcp_http_server.py       # Serveur MCP HTTP local (streamable-http)
├── agentMCP.py              # Partie 1 : agent avec serveur MCP local
├── agentMCPTime.py          # Partie 2 : agent avec serveur MCP de temps
├── agentMCPDistant.py       # Partie 3 : agent avec serveur MCP distant (HTTP)
├── pyproject.toml
├── .env.example
└── .gitignore
```

---

## Prérequis

- Python >= 3.10
- [uv](https://docs.astral.sh/uv/) installé [web:40]
- [Ollama](https://ollama.com/) avec le modèle `llama3.2:3b`
- Une clé API Tavily dans le fichier `.env`

### Installation

```bash
# Copier le fichier d'environnement
cp .env.example .env

# Renseigner les clés API dans .env
# Puis installer les dépendances
uv sync
```

La commande `uv sync` est cohérente avec le workflow standard d’un projet Python géré avec `uv`. [web:40][web:42]

Sous Windows, tu peux ajouter :

```bash
python -m ensurepip
pip3 install pywin32
```

---

## Partie 1 — Serveur MCP local

Le fichier `mcp_local_server.py` expose :
- un **tool** : `search_web` ;
- une **resource** : le README du dépôt `langchain-mcp-adapters` ;
- un **prompt** système pour l’assistant.

```bash
uv run --active python agentMCP.py
```

Avec `MultiServerMCPClient`, il est possible de récupérer dynamiquement les tools, les prompts et les resources depuis un serveur MCP. [web:137][web:141]

### Résultat attendu

```text
{'messages': [..., AIMessage(content='The langchain-mcp-adapters library is a
lightweight wrapper that makes Anthropic Model Context Protocol (MCP) tools
compatible with LangChain and LangGraph...')]}
```

---

## Partie 2 — Serveur MCP de temps

Cette partie utilise `mcp-server-time`, un serveur MCP dédié aux requêtes liées à l’heure et aux fuseaux horaires. Le package peut être installé via `pip install mcp-server-time`, puis lancé comme module Python. [web:123]

```bash
uv run --active python agentMCPTime.py
```

### Résultat attendu

```text
The current time in Japan is 3:30 AM on Saturday (June 6th, 2026),
considering the 13-hour time difference from New York.
```

### Note Windows

Le dépôt `mcp-server-time` documente l’option `--local-timezone` et montre aussi une exécution via `python -m mcp_server_time`, ce qui peut être utile si l’exécutable direct pose problème sur certaines machines. [web:123]

---

## Partie 3 — Serveur MCP distant

Cette partie montre comment connecter un agent à un serveur MCP via le transport `streamable-http`. Dans ton projet, un serveur de voyage local est démarré automatiquement, puis exposé sur une URL HTTP consommée par le client MCP. [web:98][web:140]

```bash
uv run --active python agentMCPDistant.py
```

### Résultat attendu

```text
Serveur MCP HTTP démarré sur http://127.0.0.1:8000/mcp
Tools disponibles : ['search_flights', 'get_flight_price']

Here are the direct flight options from Rabat to Agadir on August 31st:
* Atlas Blue (AT) - Flight 601: Departing at 08:00, arriving at 09:15
* Atlas Blue (AT) - Flight 603: Departing at 14:30, arriving at 15:45
* Atlas Blue (AT) - Flight 605: Departing at 19:00, arriving at 20:15
```

---

## Architecture MCP

```text
Agent LLM (LangChain)
    │
    └── MultiServerMCPClient
            │
            ├── stdio transport ──────► mcp_local_server.py
            ├── stdio transport ──────► mcp-server-time
            └── streamable-http ─────► http://127.0.0.1:8000/mcp
```

LangChain documente `MultiServerMCPClient` comme un client capable de se connecter à plusieurs serveurs MCP et d’en charger les tools, prompts et resources. [web:137][web:139]

---

## Dépendances principales

| Package | Rôle |
|---|---|
| `langchain-mcp-adapters` | Client MCP pour LangChain/LangGraph [web:99][web:139] |
| `mcp` | Implémentation du protocole MCP et base pour créer des serveurs MCP [web:98][web:145] |
| `fastmcp` | Framework simplifié pour créer des serveurs MCP [web:98] |
| `mcp-server-time` | Serveur MCP pour les requêtes liées au temps [web:123] |
| `langchain-ollama` | Utilisation d’un modèle local via Ollama |
| `tavily-python` | Recherche web |
| `langgraph` | Runtime d’agents et orchestration |