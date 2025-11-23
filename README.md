#  Domain Specific Chatbot Using RAG

## Introduction
The **Domain Specific Chatbot using RAG and LLM** is an intelligent assistant designed to answer queries strictly within a defined knowledge domain using organization-specific documents. It retrieves relevant information from internal data sources and combines it with a local Large Language Model to generate accurate, context-aware responses. 
This approach ensures reliability, reduces hallucinations, and maintains data privacy by running entirely offline.


The system:
- Loads documents from a folder
- Splits and embeds them
- Stores embeddings in a FAISS vector index
- Retrieves relevant context
- Generates answers using a **local LLM via Ollama**

# Key Features
✅ 100% local execution (no external APIs)  
✅ Multi-format document ingestion:PDF, DOCX, TXT, CSV, JSON, Excel  
✅ Configurable embeddings and chunking  
✅ FAISS-based similarity search  
✅ Local LLM inference via Ollama  
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
| `search.py` | Performs retrieval + generation workflow |
| `config.yaml` | Centralized settings |

# Project Structure
CHATBOT/
│
├─ .venv/                      # Python virtual environment
├─ data/                       # Source documents for RAG
├─ faiss_store/                # Stored FAISS index & metadata
│
├─ src/
│  ├─ __pycache__/
│  │
│  ├─ components/
│  │  ├─ __pycache__/
│  │  ├─ data_loader.py        # Loads PDFs, DOCX, CSV, JSON, Excel
│  │  ├─ embedding.py          # Chunking + embeddings generation
│  │  ├─ local_llm.py          # Loads LLM via Ollama (YAML driven)
│  │  ├─ search.py             # RAG search logic
│  │  └─ vectorstore.py        # FAISS vector storage & retrieval
│  │
│  └─ templates/               # (For UI, prompts, or HTML if needed)
│
├─ application.py              # Entry point / execution script
├─ config.yaml                 # Central configuration file
├─ README.md                   # Project documentation
├─ requirements.txt            # Python package dependencies
├─ setup.py                    # Packaging / installation script
└─ .gitignore                  # Git ignored files


# Installation & Setup
1. Clone the repository
git clone <[https://github.com/Pranjal0901/Chatbot.git]>
cd project
2. Install dependencies
pip install -r requirements.txt
3. Install & start Ollama
ollama pull mistral
4. Add documents
5. Run a sample query

# How It Works Internally
1. Document Loading - Scans folder and loads supported formats
2. Chunking - Documents are broken into overlapping text blocks
3. Embedding - Chunks converted into dense vectors using Sentence Transformers
4. FAISS Indexing - Vectors stored for fast similarity lookup
5. Querying - User question embedded and compared to stored vectors
6. Local LLM Generates Answer - Based only on allowed topics and given rules

# Author

Pranjal Singh 
AI | RAG 