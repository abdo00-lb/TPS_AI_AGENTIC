# LAB 3 : Retrieval-Augmented Generation (RAG)

**Master BDCC — SMA et IAD**  
**Prof. RETAL SARA**

## Objectif

Implémenter le pattern **RAG (Retrieval-Augmented Generation)** avec LangChain afin de permettre à un agent LLM de répondre à des questions à partir de sources externes :
- un fichier PDF ;
- une base de données SQL.

---

## Structure du projet

```text
Lab3-RAG/
├── part1_rag_pdf.py               # Partie 1 : Agent RAG sur PDF
├── part2_sql_agent.py             # Partie 2 : Agent SQL sur SQLite
├── acmecorp-employee-handbook.pdf # Document source
└── Chinook.db                     # Base de données SQLite
```

---

## Prérequis

- Python >= 3.10
- [Ollama](https://ollama.com/) avec le modèle `llama3.2:3b`
- Dépendances Python installées

```bash
ollama pull llama3.2:3b
pip install langchain langchain-community langchain-ollama langgraph \
            sentence-transformers pypdf sqlalchemy
```

---

## Partie 1 — Agent RAG sur PDF

**Fichier :** `part1_rag_pdf.py`

### Pipeline

```text
PDF → Chargement → Segmentation → Embeddings → Vector Store → Recherche sémantique → Agent
```

### Étapes

| Étape | Outil | Description |
|---|---|---|
| Chargement | `PyPDFLoader` | Extrait le texte du PDF page par page [web:91][web:93] |
| Segmentation | `RecursiveCharacterTextSplitter` | Découpe le contenu en chunks pour faciliter la recherche sémantique [web:91] |
| Embeddings | `HuggingFaceEmbeddings` | Transforme les chunks en vecteurs exploitables pour la recherche sémantique [web:92] |
| Vector Store | `InMemoryVectorStore` | Stocke les vecteurs en mémoire pour exécuter des recherches par similarité [web:85][web:92] |
| Recherche | `similarity_search()` | Retourne les documents les plus proches de la question posée [web:85][web:87] |
| Agent | `create_react_agent` + tool personnalisé | Permet au modèle d’utiliser la recherche documentaire pour répondre [web:86] |

### Exécution

```bash
python part1_rag_pdf.py
```

### Résultat attendu

```text
Pages chargées : N
Nombre de chunks : N
Documents indexés : N

--- Résultat de la recherche sémantique ---
page_content='... vacation policy ...' metadata={'page': X, ...}

--- Réponse de l'Agent RAG ---
Based on the employee handbook, employees in their first year receive X days of vacation...
```

### Schéma de fonctionnement

```text
Question utilisateur
        │
        ▼
Agent LLM (llama3.2:3b)
        │
        └── tool : search_handbook(query)
                        │
                        ▼
               InMemoryVectorStore
               similarity_search()
                        │
                        ▼
               Chunk pertinent extrait
               depuis le PDF
                        │
                        ▼
               Réponse contextualisée
```

---

## Partie 2 — Agent SQL sur SQLite

**Fichier :** `part2_sql_agent.py`  
**Base utilisée :** `Chinook.db`

### Pipeline

```text
Question en langage naturel → Agent LLM → sql_query tool → SQLite → Résultat → Réponse en langage naturel
```

### Exécution

```bash
python part2_sql_agent.py
```

### Résultat attendu

```text
--- Test du tool sql_query ---
[(1, 'AC/DC'), (2, 'Accept'), (3, 'Aerosmith'), ...]

--- Réponse de l'Agent SQL ---
Here are the first 5 artists in the database:
1. AC/DC
2. Accept
3. Aerosmith
4. Alanis Morissette
5. Alice In Chains
```

### Schéma utilisé

```sql
Table Artist:
  - ArtistId  INTEGER (PK)
  - Name      TEXT
```

### Règles de l’agent SQL

L’agent doit :
- utiliser uniquement le tool `sql_query` ;
- ne pas inventer d’information ;
- signaler si l’information n’existe pas ;
- retourner une réponse lisible en langage naturel.

Cette logique est cohérente avec les exemples d’agents SQL LangChain, où le modèle s’appuie sur un accès contrôlé à la base via `SQLDatabase` et des tools dédiés. [web:70][web:72][web:94]

---

## Différences entre les deux approches

| Critère | Partie 1 — RAG PDF | Partie 2 — SQL Agent |
|---|---|---|
| Source de données | Document PDF | Base SQLite |
| Mode d’accès | Recherche vectorielle | Requête SQL |
| Indexation | Oui, via embeddings | Non dans cette version |
| Recherche | Similarité sémantique | Recherche exacte |
| Rôle du LLM | Synthétiser le contexte retrouvé | Générer une requête puis reformuler le résultat |
| Cas d’usage idéal | Questions ouvertes sur documents | Questions précises sur données structurées |

---

## Concept du RAG

```text
Sans RAG :
Question → LLM → Réponse potentiellement incomplète ou incorrecte

Avec RAG :
Question → Retrieval des documents pertinents
                │
                ▼
        LLM + contexte récupéré
                │
                ▼
        Réponse plus précise et contextualisée
```