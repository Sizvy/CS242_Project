import os
import json
import time
import numpy as np
import faiss
import torch
from transformers import BertTokenizer, BertModel

# file paths
EMBEDDING_FILE = "stackoverflow_bert_embeddings.npy"
METADATA_FILE = "stackoverflow_bert_metadata.json"
FAISS_INDEX_FILE = "faiss_bert_index.idx"

# model settings (bert on cpu)
MODEL_NAME = "bert-base-uncased"
MAX_TOKENS = 512  # max token limit for bert
DEVICE = "cpu"  # explicitly using cpu for bert processing (no gpu on cs242)

### track time for loading bert tokenizer and model
bert_load_start = time.time()
print("🔹 loading bert tokenizer and model...")

### load tokenizer and model on cpu
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model = BertModel.from_pretrained(MODEL_NAME).to(DEVICE)
model.eval()

### calculate bert model loading time
bert_load_time = time.time() - bert_load_start
print(f"✅ bert model loaded in {bert_load_time:.4f} sec")


def load_faiss_index(embedding_file, metadata_file, index_file):
    """
    loads faiss index and metadata with timing.
    """
    start_time = time.time()
    print("🔹 loading embeddings and metadata...")

    ### load embeddings
    embedding_load_start = time.time()
    embeddings = np.load(embedding_file)
    embedding_load_time = time.time() - embedding_load_start

    ### load metadata
    metadata_load_start = time.time()
    with open(metadata_file, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    metadata_load_time = time.time() - metadata_load_start

    ### determine embedding dimension
    num_vectors, embedding_dim = embeddings.shape
    print(f"✅ loaded {num_vectors} embeddings with dimension {embedding_dim}.")
    print(f"⏱️ embedding load time: {embedding_load_time:.4f} sec")
    print(f"⏱️ metadata load time: {metadata_load_time:.4f} sec")

    ### load or create faiss index
    faiss_start = time.time()
    if os.path.exists(index_file):
        print("🔹 loading existing faiss index...")
        index = faiss.read_index(index_file)
    else:
        print("🔹 creating new faiss index...")
        index = faiss.IndexFlatL2(embedding_dim)  # l2 distance-based search
        index.add(embeddings)
        faiss.write_index(index, index_file)
        print(f"✅ faiss index saved to '{index_file}'.")

    ### calculate faiss index load time
    faiss_load_time = time.time() - faiss_start
    print(f"⏱️ faiss index load time: {faiss_load_time:.4f} sec")

    total_load_time = time.time() - start_time
    print(f"⏱️ total load time: {total_load_time:.4f} sec\n")

    return index, metadata


def compute_bert_embedding(query):
    """
    computes bert embedding for a given query (on cpu) and tracks time.
    """
    bert_start_time = time.time()

    ### tokenize and encode query for bert
    with torch.no_grad():
        inputs = tokenizer(query, padding=True, truncation=True, max_length=MAX_TOKENS, return_tensors="pt").to(DEVICE)
        output = model(**inputs)
        query_embedding = output.last_hidden_state[:, 0, :].cpu().numpy()  # extract [cls] token representation

    ### calculate bert embedding computation time
    bert_time_taken = time.time() - bert_start_time
    print(f"⏱️ bert embedding computation time: {bert_time_taken:.4f} sec")

    return query_embedding


def search_similar(query_embedding, index, metadata, top_k=5):
    """
    searches for the top_k most similar questions using faiss with timing.
    """
    search_start_time = time.time()

    ### ensure the query vector has the correct shape for faiss
    query_embedding = np.array(query_embedding, dtype=np.float32)

    ### perform faiss search
    faiss_search_start = time.time()
    distances, indices = index.search(query_embedding, top_k)
    faiss_search_time = time.time() - faiss_search_start
    ### collect results
    results = []
    for idx, dist in zip(indices[0], distances[0]):
        body = metadata[idx]["body"]
        problem_snippet = body[:150] + "..." if body else "No description"
        results.append({
            "title": metadata[idx]["title"],
            "link": metadata[idx]["link"],
            "tags": metadata[idx]["tags"],
            "problem_statement": problem_snippet,
            "distance": float(dist)
        })

    ### calculate faiss search time
    search_total_time = time.time() - search_start_time
    print(f"⏱️ faiss search time: {faiss_search_time:.4f} sec")
    print(f"⏱️ total search time: {search_total_time:.4f} sec")

    return results


def test_faiss_search():
    """
    test faiss search with a query, tracking bert embedding computation time and faiss search time.
    """
    ### load faiss index and metadata
    index, metadata = load_faiss_index(EMBEDDING_FILE, METADATA_FILE, FAISS_INDEX_FILE)

    ### example query
    query_text = "When to catch java.lang.Error?"
    print(f"\n🔍 computing bert embedding for query: \"{query_text}\"...\n")
    
    ### compute bert embedding for query
    query_embedding = compute_bert_embedding(query_text)

    print(f"\n🔍 searching for similar questions...\n")
    
    ### perform faiss search
    search_results = search_similar(query_embedding, index, metadata, top_k=5)

    ### display search results
    for i, result in enumerate(search_results, 1):
        print(f"\n🔹 result {i}: {result['title']} (distance: {result['distance']:.4f})")
        print(f"🔗 link: {result['link']}\n🏷️ tags: {result['tags']}\n")


# run the test search
if __name__ == "__main__":
    test_faiss_search()
