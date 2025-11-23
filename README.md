#  Local RAG Search System with Configurable YAML Pipeline

## Introduction
This project implements a **fully local Retrieval-Augmented Generation (RAG) system** that allows users to query company-related information using documents stored on their machine.  
It works without cloud dependencies and ensures **data privacy**, making it ideal for enterprise environments.

The system:
- Loads documents from a folder
- Splits and embeds them
- Stores embeddings in a FAISS vector index
- Retrieves relevant context
- Generates answers using a **local LLM via Ollama**

# Key Features
✅ 100% local execution (no external APIs)  
✅ Multi-format document ingestion:
- PDF, DOCX, TXT, CSV, JSON, Excel  
✅ Configurable embeddings and chunking  
✅ FAISS-based similarity search  
✅ Local LLM inference via Ollama  
✅ YAML-driven settings (models, paths, prompts, topics)  
✅ Modular and extendable architecture  

# System Architecture

Documents → Chunking → Embeddings → FAISS Index → Retrieval → Prompt Filling → LLM Response


# Components
| Component | Responsibility |
|----------|----------------|
| `data_loader.py` | Reads and loads supported file types |
| `embedding.py` | Splits text and generates embeddings |
| `vectorstore.py` | Stores and queries embeddings using FAISS |
| `local_llm.py` | Loads and manages local LLM |
| `rag_search.py` | Performs retrieval + generation workflow |
| `config.yaml` | Centralized settings |

# Project Structure
project/
│
├─ src/
│ ├─ components/
│ │ ├─ data_loader.py
│ │ ├─ embedding.py
│ │ ├─ vectorstore.py
│ │ ├─ local_llm.py
│ │
│ ├─ rag_search.py
│
├─ data/ # Place your documents here
├─ faiss_store/ # Auto-generated vector index
├─ config.yaml # Configuration file
├─ requirements.txt
├─ README.md

Installation & Setup
1. Clone the repository
git clone <your-repo-url>
cd project
2. Install dependencies
pip install -r requirements.txt
3. Install & start Ollama
ollama pull mistral
4. Add documents
5. Run a sample query

🤖 How It Works Internally
1️⃣ Document Loading

Scans folder and loads supported formats

2️⃣ Chunking

Documents are broken into overlapping text blocks

3️⃣ Embedding

Chunks converted into dense vectors using SentenceTransformers

4️⃣ FAISS Indexing

Vectors stored for fast similarity lookup

5️⃣ Querying

User question embedded and compared to stored vectors

6️⃣ Prompt Construction

Template injected with:

context

company name

allowed topics

7️⃣ Local LLM Generates Answer

Based only on allowed topics and given rules

Author

Pranjal Singh
AI | RAG | Automation Systems