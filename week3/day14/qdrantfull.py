import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance,VectorParams,PointStruct,Filter,FieldCondition,MatchValue,MatchAny,PayloadSchemaType  #Distance-cosine similarity,VectorParams-embedding vector,PointStruct-structure of the point
from sentence_transformers import SentenceTransformer
from groq import Groq
import json

load_dotenv()

QDARNT_URL=os.getenv("QDRANT_URL")
QDRANT_API_KEY=os.getenv("QDRANT_API_KEY")
GROQ_API_KEY=os.getenv("GROQ_API_KEY")

client = QdrantClient(
    url=QDARNT_URL,
    api_key=QDRANT_API_KEY
)

print("Connected to Qdrant cloud!")

COLLECTION_NAME = "knowledge_filter"
EMBEDDING_SIZE = 384  # Size of the embedding vector

if client.collection_exists(COLLECTION_NAME):
    print(f"Deleting existing collection: {COLLECTION_NAME}")
    client.delete_collection(COLLECTION_NAME)

client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=EMBEDDING_SIZE, 
        distance=Distance.COSINE,
    ),
)

print(f"Created Collection  {COLLECTION_NAME}")
print(f"Vector size: {EMBEDDING_SIZE}")
print("Distance: COSINE")
client.create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name="category",
    field_schema=PayloadSchemaType.KEYWORD
)


with open("knowledge.json", "r", encoding="utf-8") as f:
     documents= json.load(f)

print("loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Embedding model loaded!")
texts = [document["text"] for document in documents]
embeddings = model.encode(texts)

print(f"Generated embeddings for {len(embeddings)} embeddings")
print(f"Embedding size: {len(embeddings[0])}")

points = []

for i in range(len(documents)):
    point = PointStruct(
        id=i+1,
        vector=embeddings[i].tolist(),
        payload=documents[i]
    )
    points.append(point)

#Upload points to Qdrant

client.upsert(#upload+insert
    collection_name=COLLECTION_NAME,
    points=points
)

print(f"Uploaded {len(points)} documents to Qdrant!")

#search qdrant

def search(query,top_k=3):
   query_vector = model.encode([query])[0].tolist()  
   results=client.query_points(
       collection_name=COLLECTION_NAME,
       query=query_vector,
       limit=top_k,
       with_payload=True,
   ).points

   return results

def search_with_filter(query,query_filter,top_k=3):
   query_vector = model.encode([query])[0].tolist()  
   results=client.query_points(
       collection_name=COLLECTION_NAME,
       query=query_vector,
       limit=top_k,
       query_filter=query_filter,
       with_payload=True,
   ).points

   return results

reimbursement_filter=Filter(
    must=[
        FieldCondition(
            key="category",
            match=MatchValue(value="reimbursement")
        )
    ]
)

query="How many vacation days do I get?"
results=search_with_filter(query,reimbursement_filter,top_k=3)
print("\nSearch Results:")

for result in results:
    print(f"Score: {result.score:.3f}")
    print(result.payload["text"])
    print()

groq_client= Groq(
    api_key=GROQ_API_KEY
)    

def ask_llm(question,context):
    prompt = f"""
Answer the question using only the information provided below.

Context: {context}
Question: {question}
If the answer is not present in the context,say"I don't know based on the provided information."
"""

    response= groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role":"user",
                "content":prompt   
            }
        ]
    )

    return response.choices[0].message.content

#Complete RAG pipeline

question="How many vacation days do I get?"
results=search(question,top_k=3)

context="\n".join([result.payload["text"] for result in results])
answer=ask_llm(question,context)

print("\nAnswer:")
print(answer)