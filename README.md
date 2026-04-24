# Rag-uni-helper

System which will scrap given sources, 
chunk it, write to vector database, and after this 
will be able to answer some questions about given sources

# Current implementation

Simple system which uses ChromaDB as knowledge base and gives answer based on info in db.
Uses Gemini as LLM for better structurization of answer
also have (for now) one FastAPI endpoint

PROJECT IS STILL IN PROGRESS

tech stack:

- sentence-transformers — text embeddings
- ChromaDB — vector database
- Gemini API — answer generation  
- FastAPI — REST API


How to run:
```
    pip install -r requirements.txt
    uvicorn api:app --reload
```