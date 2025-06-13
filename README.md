# LLM & NER Analysis Project

This project implements a simple end-to-end system that combines Named Entity Recognition (NER) using spaCy and LLM response generation using Ollama. The system features a modern web interface built with FastAPI and TailwindCSS.

## Features

- Named Entity Recognition using spaCy
- LLM response generation using Ollama
- Modern web interface with real-time analysis
- Entity highlighting in both input and response
- Loading states and error handling

## Prerequisites

- Python 3.8 or higher
- Ollama installed and running locally
- A compatible LLM model pulled in Ollama (e.g., llama2)

## Setup

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

3. Make sure Ollama is running:
   ```bash
   # Start Ollama (if not already running)
   ollama serve
   ```

4. Pull the LLM model (if not already done):
   ```bash
   ollama pull llama2
   ```

## Running the Application

1. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

## Usage

1. Enter your prompt in the text area
2. Click "Analyze" to process the text
3. View the identified named entities and LLM response
4. Hover over highlighted entities to see their labels

## Project Structure

```
llm_ner_project/
├── main.py                # FastAPI application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Web interface
└── README.md             # This file
```

## Notes

- The application uses the `llama2` model by default. You can change this in `main.py` if you're using a different model.
- Make sure Ollama is running on the default port (11434)
- The spaCy model (`en_core_web_sm`) will be downloaded automatically if not present

## Troubleshooting

1. If you get a connection error to Ollama:
   - Ensure Ollama is running (`ollama serve`)
   - Check if the model is pulled (`ollama list`)

2. If spaCy model fails to load:
   - Try manually downloading: `python -m spacy download en_core_web_sm`

3. If the web interface doesn't load:
   - Check if FastAPI is running on port 8000
   - Try clearing your browser cache 