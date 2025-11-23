import yaml
from typing import List, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np 
from src.components.data_loader import load_all_documents

class EmbeddingPipeline:
    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)

        self.chunk_size = config["rag"]["chunk_size"]
        self.chunk_overlap = config["rag"]["chunk_overlap"]
        self.model = SentenceTransformer(config["rag"]["model_name"])
        print(f"[INFO] Loaded embedding model: {config["rag"]["model_name"]}")

    def chunk_documents(self, documents:List[Any])->List[Any]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size = self.chunk_size,
            chunk_overlap = self.chunk_overlap,
            length_function = len,
            separators=["\n\n","\n"," ",""]
        )
        chunks = splitter.split_documents(documents)
        print(f"[INFO] Split {len(documents)} documents into {len(chunks)} chunks.")
        return chunks
    
    def embed_chunks(self, chunks:List[Any])->np.ndarray:
        texts = [chunk.page_content for chunk in chunks]
        print(f"[INFO] Generating embeddings for {len(texts)} chunks...")
        embeddings = self.model.encode(texts, show_progress_bar = True)
        print(f"[INFO] Embeddings shape:{embeddings.shape}")
        return embeddings
         
