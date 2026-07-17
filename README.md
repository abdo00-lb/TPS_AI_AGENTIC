# AI Agentic — Master BDCC

Dépôt principal regroupant l’ensemble des Labs et TPs du module **SMA et IAD — Master BDCC | Prof. RETAL SARA**.

## Structure

| Dossier | Sujet |
|---|---|
| [Lab1-prompt-engineering](./Lab1-prompt-engineering) | Ingénierie des prompts : tokenisation, Ollama, Groq, OpenAI, JSON et images |
| [Lab2-langchain-agents](./Lab2-langchain-agents) | Agents avec LangChain : agent chef personnel, mémoire et recherche web |
| [Lab3-RAG](./Lab3-RAG) | RAG sur PDF avec embeddings Hugging Face et agent SQL sur Chinook |
| [Lab4-MCP](./Lab4-MCP) | Model Context Protocol : stdio, serveur de temps et streamable-http |
| [Lab5-LangGraph_Studio](./Lab5-LangGraph_Studio) | LangGraph Studio : visualisation, debug d’agents et système multi-agents hiérarchique |
| [Lab6-Contexte_et_Etat](./Lab6-Contexte_et_Etat) | Contexte par invocation (`ReaderProfile`) et état persisté (`LibraryState`) |
| [Lab7-Human_In_The_Loop](./Lab7-Human_In_The_Loop) | Agent HITL : `interrupt()`, approve, reject et edit |
| [Lab8-Workflow_avec_LangGraph](./Lab8-Workflow_avec_LangGraph) | Workflows LangGraph : graphe simple, reducers, état des messages, branchements conditionnels et boucles |
| [Lab9-Agent_avec_LangGraph](./Lab9-Agent_avec_LangGraph) | Agent LangGraph : tools, agent comme nœud, HITL fonctionnel, historique et fork |
| [TP-Chef_personnel](./TP-Chef_personnel) | Agent chef cuisinier : RAG, mémoire, recherche web et system prompt |
| [Evaluation-finale](./Evaluation-finale) | Évaluation finale : RAG agentique LangGraph sur l’éducation financière personnelle au Maroc |

## Prérequis communs

- Python >= 3.10
- [uv](https://docs.astral.sh/uv/) pour la gestion des dépendances et des environnements [web:47][web:146]
- [Ollama](https://ollama.com/) avec le modèle `llama3.2:3b`

```bash
ollama pull llama3.2:3b
```

Le modèle `llama3.2:3b` est bien utilisé couramment avec Ollama, et le pattern `ollama pull ...` correspond au mode d’installation habituel des modèles locaux. [web:151][web:153][web:157]

## Exécution

Chaque lab est autonome et peut être exécuté depuis son propre dossier :

```bash
cd Lab6-Contexte_et_Etat
uv sync
uv run --active python agent_context.py
uv run --active python agent_state.py
```

`uv` crée et maintient un environnement de projet, généralement dans `.venv`, puis `uv run` exécute les commandes dans cet environnement. [web:146][web:147]

## Remarques

- Les fichiers `.env` ne doivent pas être versionnés sur GitHub.
- Un fichier `.env.example` peut être fourni dans chaque lab pour montrer les variables attendues.
- Certains labs nécessitent des clés API optionnelles, par exemple `TAVILY_API_KEY` ou `LANGSMITH_API_KEY`.