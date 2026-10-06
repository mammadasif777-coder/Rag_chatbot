from pypdf import PdfReader
import chromadb
from google import genai

chroma = chromadb.PersistentClient(path="db")
collection = chroma.get_or_create_collection("docs")
def reset_collection():
    global collection
    chroma.delete_collection("docs")
    collection = chroma.get_or_create_collection("docs")
llm = genai.Client()   # reads GEMINI_API_KEY from the environment

def load_pdf(path):
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def chunk_text(text, size=800, overlap=150):
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks

def add_document(path, doc_name):
    chunks = chunk_text(load_pdf(path))
    collection.upsert(
        documents=chunks,
        ids=[f"{doc_name}-{i}" for i in range(len(chunks))],
        metadatas=[{"source": doc_name, "chunk": i} for i in range(len(chunks))],
    )
    return len(chunks)

def retrieve(question, k=4):
    broad = any(w in question.lower() for w in
                ["abstract", "summary", "summarize", "overview", "what is this"])
    if broad:
        res = collection.get(where={"chunk": {"$lt": 10}},
                             include=["documents", "metadatas"])
        pairs = sorted(zip(res["metadatas"], res["documents"]),
                       key=lambda p: p[0]["chunk"])
        return [doc for _, doc in pairs]
    result = collection.query(query_texts=[question], n_results=k)
    return result["documents"][0]
def answer(question):
    context = "\n\n---\n\n".join(retrieve(question))
    prompt = f"""Answer the question using ONLY the context below.
If the answer is not in the context, say "I couldn't find that in the document."

Context:
{context}

Question: {question}"""
    reply = llm.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
    )
    return reply.text