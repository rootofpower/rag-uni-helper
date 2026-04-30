import chromadb
from chromadb.api.models import Collection

client = chromadb.PersistentClient(path="chromadbdata")


def get_collection(collection_name: str) -> Collection:
    collection = client.get_collection(collection_name)
    return collection


def create_collection(collection_name: str) -> dict:
    client.get_or_create_collection(collection_name)
    return {"status": "success",
            "message": f"Collection {collection_name} created successfully"
            }


def delete_collection(collection_name: str) -> dict:
    client.delete_collection(collection_name)
    return {"status": "success",
            "message": f"Collection {collection_name} deleted successfully"
            }


def clear_collection(collection_name: str) -> dict:
    client.delete_collection(collection_name)
    client.create_collection(collection_name)
    return {"status": "success",
            "message": f"Collection {collection_name} cleared successfully"
            }


def query_collection(collection_name: str, query: str) -> tuple:
    collection = client.get_collection(collection_name)
    answer = collection.query(
        query_texts=query,
        include=["documents", "metadatas"],
    )
    context = answer["documents"]
    source = set(_["source"] for _ in answer["metadatas"][0] if _ is not None)

    return context, source


def add_documents(
    collection_name: str,
    ids: list[str],
    documents: list[str],
    metadatas: list[dict]
) -> dict:
    collection = client.get_collection(collection_name)
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
    )
    return {"status": "success",
            "message": f"Document(s) added to collection {collection_name} successfully"
            }


def get_documents(collection_name: str, where: dict) -> dict:
    collection = client.get_collection(collection_name)
    context = collection.get(where=where)
    return context


def list_collection() -> list:
    return [collection.name for collection in client.list_collections()]


def documents_count(collection_name: str) -> int:
    return client.get_collection(collection_name).count()
