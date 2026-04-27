import os

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from google import genai
from dotenv import load_dotenv
import chromadb
from chunker import load_and_chunk, chunk_text
from scraper import scrape

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise Exception("GEMINI_API_KEY not set")
client = genai.Client(api_key=GEMINI_API_KEY)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
chroma_client = chromadb.PersistentClient(path="chromadbdata")
collection = chroma_client.get_or_create_collection(name="documents")
# documents = load_and_chunk("Documents/info.txt")

# if collection.count() == 0:
#     collection.add(
#         ids=[str(i) for i in range(len(documents))],
#         documents=documents,
#     )
#
#
# knowledge_base = model.encode(documents)
#
#
# def get_answer(query):
#     query_vector = model.encode(query)
#     query_vector = query_vector.reshape(1, -1)
#     context = cosine_similarity(query_vector, knowledge_base)
#
#     prompt = f"""Answer the question based ONLY on the context below.
#     Context: {documents[context.argmax()]}
#     Query: {query}
# """
#
#     response = client.models.generate_content(
#         model='gemini-3.1-flash-lite-preview',
#         contents=prompt,
#     )
#
#     return response.text


# print(get_answer("What is used for containerization?"))
# print(get_answer("What is machine learning?"))


def get_answer_from_collection(query):
    answer = collection.query(
        query_texts=query,
        include=["documents", "metadatas"],
    )
    context = answer["documents"]
    source = set(_["source"]  for _ in answer["metadatas"][0] if _ is not None)
    print(source)
    prompt = f"""Answer the question based ONLY on the context below.
    Context: {context}
    Query: {query}
"""
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite-preview',
        contents=prompt,
    )
    return {"answer": response.text, "sources": source}


# print(get_answer_from_collection("What is used for containerization?"))
# print(get_answer_from_collection("What is machine learning?"))


def add_source(url: str):
    try:
        existing = collection.get(where={"source": url})
    except Exception as e:
        print(f"ERROR IN add_source: {e}")
        return {"status": "error"}
    if existing["ids"]:
        print(f"Source {url} already exists")
        return {"status": "already_exists"}
    text = scrape(url)
    chunks = chunk_text(text)
    collection.add(
        ids=[f"{url}_{i}" for i in range(len(chunks))],
        documents=chunks,
        metadatas=[
            {"source": url } for _ in range(len(chunks))
        ])
    return {"status": "success"}

# print("First try")
# add_source("https://en.wikipedia.org/wiki/Python_(programming_language)")
# print("Second try")
# add_source("https://en.wikipedia.org/wiki/Python_(programming_language)")

# print(collection.peek())
