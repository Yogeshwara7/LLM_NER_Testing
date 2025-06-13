from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import spacy
import requests
from typing import List, Tuple
import json

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

class PromptRequest(BaseModel):
    prompt: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze_prompt(data: PromptRequest):
    prompt = data.prompt
    
    # Perform NER
    doc = nlp(prompt)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    # Paraphrasing instruction for LLM
    paraphrase_prompt = f"Paraphrase the following sentence, keeping the meaning but using different words:\n\n{prompt}"

    # Call Ollama API and handle NDJSON streaming response
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3.2", "prompt": paraphrase_prompt},
            stream=True
        )
        llm_response = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                llm_response += data.get("response", "")
        if not llm_response:
            llm_response = "Error: Could not get response from LLM"
    except Exception as e:
        llm_response = f"Error: Could not connect to Ollama API - {str(e)}"
    
    # Print input and response to terminal
    print("\n--- New Request ---")
    print(f"User Input: {prompt}")
    print(f"LLM Response: {llm_response}")
    print(f"Entities: {entities}")
    print("-------------------\n")

    return {
        "entities": entities,
        "response": llm_response
    } 