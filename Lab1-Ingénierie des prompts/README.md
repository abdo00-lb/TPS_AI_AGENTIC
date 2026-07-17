# TP Ingénierie des Prompts

Projet Python structuré à partir du document `1 TP Ingenierie des prompts.docx`.

## Fichiers

- `01_tokenisation.py` : tokenisation avec `tiktoken`
- `02_ollama_prompt.py` : prompt simple avec Ollama
- `03_groq_prompt.py` : prompt simple avec Groq
- `04_openai_prompt.py` : prompt simple avec OpenAI
- `05_aspect_sentiment_json.py` : analyse de sentiment avec sortie JSON
- `06_image_generation.py` : génération d'image
- `07_image_description.py` : description de `rag.png`

## Installation

Créer l'environnement virtuel :

```bash
uv venv
```

Installer les dépendances :

```bash
uv sync
```

## Activation de l'environnement

Sous Windows PowerShell :

```powershell
.venv\Scripts\Activate.ps1
```

Sous bash :

```bash
source .venv/bin/activate
```

## Configuration

Copier le fichier `.env.example` vers `.env`, puis renseigner les variables nécessaires :

```env
OPENAI_API_KEY=...
GROQ_API_KEY=...
OLLAMA_MODEL=llama3.2:3b
```

Le chargement des variables via `load_dotenv()` est une manière standard d’utiliser un fichier `.env` dans un projet Python. [web:41][web:44]

## Exécution

Chaque script peut être lancé séparément :

```bash
python 01_tokenisation.py
python 02_ollama_prompt.py
python 03_groq_prompt.py
python 04_openai_prompt.py
python 05_aspect_sentiment_json.py
python 06_image_generation.py
python 07_image_description.py
```

## Remarques

- `01_tokenisation.py` ne nécessite aucune clé API.
- `02_ollama_prompt.py` nécessite un serveur Ollama actif avec un modèle installé localement.
- `03_groq_prompt.py` à `07_image_description.py` nécessitent des clés API valides.
- Pour `01_tokenisation.py`, `tiktoken.encoding_for_model("gpt-4o")` est bien une approche standard pour récupérer l’encodeur adapté au modèle. [web:46][web:50][web:52]