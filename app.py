from flask import Flask, request, render_template, jsonify
import lucene
import jpype

if not lucene.getVMEnv():
    print("Initializing JVM at app.py...")
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
else:
    print("JVM is already running.")

from lucene_retriever_updated import search_stackoverflow

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    query = ""
    
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        if query:
            results = search_stackoverflow(query, field="body")
    
    return render_template('index.html', query=query, results=results)

@app.route('/api/search', methods=['GET'])
def api_search():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    vm_env = lucene.getVMEnv()
    if vm_env:
        print("Attaching thread to JVM...")
        vm_env.attachCurrentThread()
    else:
        return jsonify({"error": "JVM is not running"}), 500

    results = search_stackoverflow(query, field="body")
    # print(results)
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

