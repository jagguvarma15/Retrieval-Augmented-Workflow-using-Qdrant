import os
os.environ["OPENAI_API_KEY"] = " "  # Replace with your actual key

# build_index.py
import os

from langchain_community.document_loaders import JSONLoader
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

# 1. Load environment variables
# reads OPENAI_API_KEY from .env
# 2. Load contract clauses from CUAD JSON
loader = JSONLoader(
    file_path="data/cuad.json",  # Path to your CUAD file
    jq_schema=".data[].paragraphs[].qas[].answers[].text"  # Extracts each answer text
)
docs = loader.load()  # List of LangChain Document objects with .page_content
# 3. Initialize Qdrant client and vector store
client = QdrantClient(url="http://localhost:6333")
vectorstore = QdrantVectorStore(
    client=client,
    collection_name="cuad_contracts",
    embedding=OpenAIEmbeddings(),  # Uses OPENAI_API_KEY
)
# 4. Index (embeddings + store) all documents
vectorstore.add_documents(docs)
print(f"Indexed {len(docs)} documents into Qdrant collection 'cuad_contracts'.")