from flask import Flask, request, jsonify, render_template
import lucene
from bert_faiss_search import compute_bert_embedding, search_similar, load_faiss_index

# Initialize the JVM only if it hasn't been initialized yet
if not lucene.getVMEnv():
    print("Initializing JVM...")
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
else:
    print("JVM is already running.")

from LLM import query_llm  # Import the query_llm function
from lucene_retriever_updated import search_stackoverflow

# Load Faiss index and metadata for BERT-based search
faiss_index, faiss_metadata = load_faiss_index("stackoverflow_bert_embeddings.npy", "stackoverflow_bert_metadata.json", "faiss_bert_index.idx")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Serve the index.html file

@app.route('/api/search', methods=['GET'])
def api_search():
    query = request.args.get('query', '').strip()
    search_method = request.args.get('method', 'lucene').strip().lower()  # Default to Lucene
    print("Chosen Search Method is:", search_method)
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    # Attach the current thread to the JVM
    vm_env = lucene.getVMEnv()
    if vm_env:
        print("Attaching thread to JVM...")
        vm_env.attachCurrentThread()
    else:
        return jsonify({"error": "JVM is not running"}), 500

    # Perform search based on the selected method
    if search_method == "bert":
        print("🔍 Performing BERT-based search...")
        query_embedding = compute_bert_embedding(query)
        results = search_similar(query_embedding, faiss_index, faiss_metadata, top_k=15)
        # Normalize BERT results to match Lucene format
        normalized_results = []
        for result in results:
            normalized_results.append({
                "title": result["title"],
                "link": result["link"],
                "tags": ", ".join(result["tags"]),  # Convert tags array to comma-separated string
                "problem_statement": result["problem_statement"],
                "answer_snippet": "No answer available",  # Placeholder for answer_snippet
                "priority": 0,  # Placeholder for priority
                "score": 1.0 - (result["distance"] / 100)  # Normalize distance to a score
            })
        results = normalized_results
    else:
        print("🔍 Performing Lucene-based search...")
        results = search_stackoverflow(query, field="body")

    return jsonify(results)

# New route for query_llm
@app.route('/api/llm', methods=['GET'])
def api_llm():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    # Attach the current thread to the JVM
    vm_env = lucene.getVMEnv()
    if vm_env:
        print("Attaching thread to JVM...")
        vm_env.attachCurrentThread()
    else:
        return jsonify({"error": "JVM is not running"}), 500

    # Call the query_llm function
    result = query_llm(query)
    if isinstance(result, tuple):
        llm_response, results = result
    else:
        llm_response = result
        results = []

    return jsonify({
        "llm_response": llm_response,
        "results": results
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
