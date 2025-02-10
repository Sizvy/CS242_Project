import os
import sys
from huggingface_hub import InferenceClient
from lucene_retriever import search_stackoverflow  # Import Lucene retriever
from lucene_retriever import paginate_results, display_results
from huggingface_hub import login
from transformers import set_seed
from rich.console import Console
from rich.markdown import Markdown
import logging
set_seed(42)

console = Console()

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

# Configure logging
logging.basicConfig(filename="llm_errors.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

def query_llm(query):
    """Fetch Stack Overflow documents and use an LLM to generate an answer."""
    try:
        # Step 1: Retrieve top Stack Overflow posts using Lucene
        results = search_stackoverflow(query, field="body", top_k=15)

        if not results:
            return "No relevant Stack Overflow results found."

        # Step 2: Format retrieved documents into a prompt
        context = format_context(results)
        prompt = f"Using the following Stack Overflow discussions, answer the question concisely:\n\n{context}\n\nQuestion: {query}\nAnswer:"

        # Step 3: Query Hugging Face model
        try:
            output = client.text_generation(prompt, stream=True, max_new_tokens=1024)
        except Exception as e:
            logging.error(f"LLM API error: {str(e)}")
            return "An error occurred while querying the LLM."

        # Step 4: Collect streamed response
        collected_messages = []
        for chunk in output:
            if chunk:
                collected_messages.append(chunk)

        return ''.join(collected_messages), results

    except Exception as e:
        logging.error(f"General error in query_llm: {str(e)}")
        return "An unexpected error occurred."


if __name__ == "__main__":
    # user_query = input("\n🔍 Enter your search query: ").strip()
    console.print("\n🔍 Enter your search query (Press Ctrl+D when done): ")
    user_query = sys.stdin.read().strip()
    # Get LLM-generated response and Lucene search results
    result = query_llm(user_query)
    if isinstance(result, tuple):
       llm_response, results = result  # ✅ If it returns two values
    else:
        llm_response = result
        results = []  # ✅ Default empty list if missing

    llm_response, results = query_llm(user_query)

    # Display LLM-generated response first
    console.print("\n[bold cyan]🤖 AI-Generated Answer:[/bold cyan]\n")
    console.print(Markdown(llm_response))  # Format as Markdown for better readability

    # Display Lucene search results
    console.print("\n[bold yellow]🔍 Related Stack Overflow Discussions:[/bold yellow]\n")
    paginate_results(results)  # Use the function from lucene_retriever.py

