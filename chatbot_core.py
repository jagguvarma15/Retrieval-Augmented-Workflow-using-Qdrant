# chatbot_core.py
import os
os.environ["OPENAI_API_KEY"] = " "  # Replace with your actual key

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain.chains import RetrievalQA
from langgraph.graph import StateGraph
from qdrant_client import QdrantClient
from pydantic import BaseModel

# 1) Define separate Pydantic schemas for input vs. output

class InputState(BaseModel):
    input: str

class OutputState(BaseModel):
    input: str
    output: str

# 2) Initialize embeddings + Qdrant client

embedding_model = OpenAIEmbeddings()
client = QdrantClient(url="http://localhost:6333")

# 3) Load Qdrant vector store with embeddings (dense mode)

vectorstore = QdrantVectorStore(
    client=client,
    collection_name="cuad_contracts",
    embedding=embedding_model,
)

retriever = vectorstore.as_retriever()

# 4) Set up LLM + RetrievalQA chain

llm = ChatOpenAI(model="gpt-4")
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# 5) Define LangGraph node: takes InputState, returns OutputState

def query_node(state: InputState) -> OutputState:
    answer = qa_chain.run(state.input)
    return OutputState(input=state.input, output=answer)

# 6) Build the StateGraph using the exact keywords your version expects:
#
#     • `input=InputState`
#     • `output=OutputState`
#
# (Note: not `input_model`/`output_model` or `input_schema`/`output_schema`, 
#  but simply `input=` and `output=`.)

builder = StateGraph(
    input=InputState,
    output=OutputState,
)

builder.add_node("query", query_node)
builder.set_entry_point("query")
builder.set_finish_point("query")

# This `app` is the compiled graph, invoked via .invoke()
app = builder.compile()