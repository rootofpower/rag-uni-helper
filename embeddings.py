from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

text = "Hi, how was your day?"
vector = model.encode(text)

print(type(vector), vector.shape)
print(vector[:5])

text1 = "How to install Python?"
text2 = "Python installation guide"
text3 = "pip install numpy"

vector1 = model.encode(text1)
vector2 = model.encode(text2)
vector3 = model.encode(text3)

print(type(vector1), vector1.shape)
print(type(vector2), vector2.shape)
print(type(vector3), vector3.shape)

vector1 = vector1.reshape(1, -1)
vector2 = vector2.reshape(1, -1)
vector3 = vector3.reshape(1, -1)
print(vector1.shape)
print(cosine_similarity(vector1, vector2))
print(cosine_similarity(vector1, vector3))
print(cosine_similarity(vector2, vector3))

documents = [
    "Python is a programming language",
    "FastAPI is a web framework for Python",
    "PostgreSQL is a relational database",
    "Docker is used for containerization",
    "Machine learning uses algorithms to learn from data"
]

knowledge_base = model.encode(documents)

print(knowledge_base.shape)

query = "What is a web framework?"

query_vector = model.encode(query)

query_vector = query_vector.reshape(1, -1)
answer = cosine_similarity(query_vector, knowledge_base)
print(query_vector.shape)
print(answer)
print(documents[answer.argmax()])
