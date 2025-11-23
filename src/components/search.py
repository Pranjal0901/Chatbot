import yaml
import os
from src.components.data_loader import load_all_documents
from src.components.vectorstore import FaissVectorStore
from src.components.local_llm import LoadLLM

class RAGSearch:
    """
     Retrieves company-relevant information & answers strictly
     domain related questions using a local LLM.
    """

    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        
        persist_dir = config["rag"]["persist_dir"]
        embedding_model = config["rag"]["embedding_model"]

        # Initialize FAISS retriever
        self.vectorstore = FaissVectorStore(persist_dir,embedding_model)

        # Load or build vectorstore
        faiss_path = os.path.join(persist_dir,"faiss.index")
        meta_path = os.path.join(persist_dir,"metadata.pkl")
        if not(os.path.exists(faiss_path) and os.path.exists(meta_path)):
            docs = load_all_documents("data")
        else:
            self.vectorstore.load()

        loader = LoadLLM(
            model_name=config["llm"]["model_name"],
            num_ctx=config["llm"]["num_ctx"]
        )
        self.llm = loader.get_model()

    def search_and_summarize(self, query: str,top_k:int = 5) -> str:
        results = self.vectorstore.query(query,top_k=top_k)
        texts = [r["metadata"].get("text", "")for r in results if r["metadata"]]
        context = "\n\n".join(texts)
        if not context:
            return "No relevant document found."
        
        # # Loading prompt using YAML file
        # with open("config.yaml","r") as file:
        #     config = yaml.safe_load(file)

        # prompt_cfg = config["prompt"]
        # system_cfg = prompt_cfg["system"]
        # template = prompt_cfg["template"]


        # # Build allowed topics bullet list
        # allowed_topics_formatted = "\n".join(f"- {t}" for t in system_cfg["allowed_topics"])
        
        # # Main template
        # final_prompt = template.format(
        #     company_name=system_cfg["company_name"],
        #     allowed_topics=allowed_topics_formatted,
        #     disallowed_response=system_cfg["disallowed_response"],
        #     competitor_response=system_cfg["competitor_response"],
        #     context=context,
        #     question=query
        # )
        
        prompt = """
        You are the official AI assistant for Tata.

        ONLY answer questions about:
        - Sales
        - Marketing
        - Lead generation
        - Company products & services
        - Company policies

        If a user asks anything outside these domains, reply:
        "I can only assist with sales and marketing questions related to our company."

        Do NOT mention:
        - Other companies
        - Competitors
        - External brands
        - Unrelated topics

        If someone asks about another company:
        "I cannot discuss other companies. Please ask about our company's sales and marketing."

        Use the context (if provided) to answer clearly.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """
        final_prompt = prompt.format(context=context,question=query)
        response = self.llm.invoke(final_prompt)
        return response