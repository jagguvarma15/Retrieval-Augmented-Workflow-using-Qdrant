# main.py
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from chatbot_core import app as graph_app  # The compiled LangGraph

# 1. Create a FastAPI instance
app = FastAPI(
    title="CUAD RAG Agent",
    description="An agent that answers contract-related questions over the CUAD dataset.",
    version="1.0.0"
)

# 2. Define a Pydantic model for the API request
class QueryRequest(BaseModel):
    question: str

# 3. POST endpoint to ask a question (returns JSON)
@app.post("/ask", summary="Ask the RAG Agent", response_description="Answer from the agent")
def ask_question(req: QueryRequest):
    # Invoke the LangGraph agent; returns an AddableValuesDict
    result = graph_app.invoke({"input": req.question})
    # Extract the 'output' field (the generated answer)
    return {"answer": result["output"]}

# 4. GET endpoint for a simple HTML form (optional)
@app.get("/", response_class=HTMLResponse, summary="HTML Form")
def read_root():
    return """
    <html>
      <head><title>CUAD RAG Agent</title></head>
      <body>
        <h1>Ask the CUAD RAG Agent</h1>
        <form action="/ask_form" method="post">
          <label for="question">Question:</label>
          <input type="text" id="question" name="question" size="60"/>
          <button type="submit">Ask</button>
        </form>
      </body>
    </html>
    """

# 5. POST endpoint to handle the HTML form submission
@app.post("/ask_form", response_class=HTMLResponse, summary="HTML Form Submission")
def ask_form(question: str = Form(...)):
    result = graph_app.invoke({"input": question})
    answer = result["output"]
    return f"""
    <html>
      <head><title>CUAD RAG Agent - Answer</title></head>
      <body>
        <h1>Question:</h1>
        <p>{question}</p>
        <h1>Answer:</h1>
        <p>{answer}</p>
        <a href="/">Ask another question</a>
      </body>
    </html>
    """