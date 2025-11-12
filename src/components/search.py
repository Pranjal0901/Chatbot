import os
from dotenv import load_dotenv
from langchain_community.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from src.components.vectorstore import FaissVectorStore
from src.components.local_llm import LoadLLM

load_dotenv()


class RAGSearch:
    """
    RAG pipeline to retrieve company-relevant information and answer only
    sales and marketing domain questions using a local LLM.
    """

    def __init__(self, persist_dir: str = "faiss_store", embedding_model: str = "all-MiniLM-L6-v2"):
        print("[INFO] 🚀 Initializing RAGSearch...")

        # Initialize FAISS vector store and retriever
        self.vectorstore = FaissVectorStore(persist_dir=persist_dir, embedding_model=embedding_model)
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})

        # Build the LLM chain
        self.qa_chain = self._build_rag_chain()
        print("[INFO] ✅ RAGSearch initialized successfully.")

    def _build_rag_chain(self):
        """
        Build Retrieval-Augmented QA chain with strict sales/marketing rules.
        """
        llm_loader = LoadLLM(model_name="mistral")
        llm = llm_loader.get_model()

        prompt_template = """
        You are the official AI assistant for [COMPANY NAME].

        ONLY answer questions about:
        - Sales
        - Marketing
        - Lead generation
        - Company products & services
        - Company policies

        If a user asks anything outside this domain, reply:

        "I can only assist with sales and marketing questions related to our company."

        Do NOT mention or discuss:
        - Other companies
        - Competitors
        - Names of external brands
        - Unrelated domains

        If someone asks about another company or tries to compare:
        "I cannot discuss other companies. Please ask about our company's sales and marketing."

        Use the provided context (if available) to answer the question clearly and accurately.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """

        PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

        chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.retriever,
            chain_type_kwargs={"prompt": PROMPT}
        )

        print("[INFO] 🔗 RetrievalQA chain successfully built.")
        return chain

    def search(self, query: str) -> str:
        """
        Perform retrieval-augmented search and return the generated answer.
        """
        if not query or not isinstance(query, str):
            return "[ERROR] Invalid query. Please provide a valid text input."

        print(f"[INFO] 🔍 Query received: {query}")
        try:
            result = self.qa_chain.run(query)
            print("[INFO] ✅ Query answered successfully.")
            return result.strip()
        except Exception as e:
            print(f"[ERROR] ❌ Error while generating answer: {e}")
            return "Sorry, I encountered an issue while generating your answer. Please try again."

