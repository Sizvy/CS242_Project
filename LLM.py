import os
from huggingface_hub import InferenceClient
from lucene_retriever import search_stackoverflow  # Import Lucene retriever
from huggingface_hub import login
from transformers import set_seed
set_seed(42)

os.environ['HF_TOKEN']="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"
login(token = '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')

# Hugging Face API setup
api_key = os.getenv("HF_TOKEN")  # Store API key in an environment variable
MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"

client = InferenceClient(base_url=API_URL, api_key=api_key)

def format_context(results):
    """Formats retrieved Stack Overflow results into a structured prompt."""
    context = "\n\n".join([
        f"Title: {res['title']}\nProblem: {res['problem_statement']}\nAnswer: {res['answer_snippet']}\nURL: {res['link']}"
        for res in results
    ])
    return context

def query_llm(query):
    """Fetch Stack Overflow documents and use an LLM to generate an answer."""
    
    # Retrieve top Stack Overflow posts using Lucene
    results = search_stackoverflow(query, field="body", top_k=5)
    
    if not results:
        return "No relevant Stack Overflow results found."

    # Format retrieved documents into a prompt
    context = format_context(results)
    prompt = f"Using the following Stack Overflow discussions, answer the question concisely:\n\n{context}\n\nQuestion: {query}\nAnswer:"

    # Query Hugging Face model
    output = client.text_generation(prompt, stream=True, max_new_tokens=1024)

    # Collect streamed response
    collected_messages = []
    for chunk in output:
        if chunk:
            collected_messages.append(chunk)

    return ''.join(collected_messages)

if __name__ == "__main__":
    user_query = input("Enter your search query: ").strip()
    response = query_llm(user_query)
    print("\n[Generated Answer]:", response)
