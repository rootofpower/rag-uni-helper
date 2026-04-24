import chromadbdata

from chunker import load_and_chunk

client = chromadbdata.PersistentClient(path="chromadbdata")
collection = client.get_or_create_collection(name="documents")

documents = load_and_chunk("./Documents/info.txt")

collection.add(
    ids= [str(i) for i in range(len(documents))],
    documents=documents,
)

query = collection.query(
    query_texts=["What is machine learning?"],
    n_results=3,
    include=["documents"]
)

print(query["documents"])
