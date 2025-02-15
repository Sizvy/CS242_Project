import lucene
import os
import re
import sys
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.queryparser.classic import QueryParserBase
from org.apache.lucene.queryparser.classic import MultiFieldQueryParser
from org.apache.lucene.search import BooleanQuery, BooleanClause
from java.nio.file import Paths
from rich.console import Console
from rich.table import Table
from rich.text import Text
import time

### initialize lucene jvm
lucene.initVM()

### open index directory
index_dir = "stackoverflow_index"
if not os.path.exists(index_dir):
    print("error: index directory not found. run indexing script first.")
    exit()

directory = SimpleFSDirectory(Paths.get(index_dir))
reader = DirectoryReader.open(directory)
searcher = IndexSearcher(reader)
analyzer = StandardAnalyzer()

### rich console for colored output
console = Console()

def normalize_title(title):
    """removes special characters and converts to lowercase for title comparison"""
    return re.sub(r'\W+', '', title.lower())

def remove_duplicate_titles(results):
    """removes duplicate or very similar titles"""
    unique_results = []
    seen_titles = set()

    for res in results:
        norm_title = normalize_title(res["title"])
        if norm_title not in seen_titles:
            seen_titles.add(norm_title)
            unique_results.append(res)

        if len(unique_results) == 15:  ### stop at top 5 after removing duplicates
            break

    return unique_results

def escape_lucene_query(query_str):
    """Escapes special characters in Lucene queries."""
    return QueryParserBase.escape(query_str)

def search_stackoverflow(query_str, field="title", top_k=100):
    """searches stackoverflow index and sorts results"""
    query_str = escape_lucene_query(query_str)
    query_parser = QueryParser(field, analyzer)
    query = query_parser.parse(query_str)

    ### search the index (retrieve top_k results)
    hits = searcher.search(query, top_k).scoreDocs
    results = []

    for hit in hits:
        doc = searcher.doc(hit.doc)
        title = doc.get("title")
        link = doc.get("link")
        tags = doc.get("tags")
        body = doc.get("body")
        answers = doc.get("answers")
        score = hit.score

        ### extract problem statement and answer snippet
        problem_snippet = body[:150] + "..." if body else "No description"
        answer_snippet = (answers[:150] + "...") if answers else "No answer available"

        ### prioritize answers with more than 1000 characters
        priority = 2 if title.lower() == query_str.lower() else (1 if len(answers) > 1000 else 0)

        results.append({
            "title": title, "link": link, "tags": tags,
            "problem_statement": problem_snippet,
            "answer_snippet": answer_snippet, "priority": priority, "score": score
        })

    ### sort results (prioritize long answers, then by rank)
    results = sorted(results, key=lambda x: -x["priority"])

    ### remove duplicate or similar titles
    return remove_duplicate_titles(results)



def display_results(results):
    """displays search results in a structured, easy-to-read table"""
    if not results:
        console.print("[bold red]No results found![/bold red]")
        return

    table = Table(title="🔍 Search Results", show_header=True, header_style="bold cyan")
    table.add_column("Rank", justify="center", style="bold magenta")
    table.add_column("Title", style="bold white", overflow="fold")
    table.add_column("Problem Statement", style="dim", overflow="fold")
    table.add_column("URL", style="bold cyan", overflow="fold")
    table.add_column("Tags", style="blue", overflow="fold")
    table.add_column("Answer / Snippet", style="green", overflow="fold")
    table.add_column("Score", justify="right", style="bold yellow")

    for i, res in enumerate(results, 1):
        title_text = Text(res["title"], style="bold white")
        problem_text = Text(res["problem_statement"], style="dim")
        url_text = Text(f"[link={res['link']}]🔗 Open[/link]", style="bold cyan")  ### clickable URL
        tags_text = Text(res["tags"], style="blue")
        answer_text = Text(res["answer_snippet"], style="green")
        score_text = Text(f"{res['score']:.2f}", style="bold yellow")

        table.add_row(str(i), title_text, problem_text, url_text, tags_text, answer_text, score_text)
        table.add_section()  ### adds a row separator for better readability

    console.print(table)
    console.print("\n[bold green]✅ Found top results![/bold green] See details above 👆")

def paginate_results(results):
    """Displays results with pagination."""
    page_size = 5
    total_pages = (len(results) + page_size - 1) // page_size
    current_page = 0

    while True:
        start = current_page * page_size
        end = start + page_size
        console.clear()
        console.print(f"\n[bold cyan]Page {current_page + 1} of {total_pages}[/bold cyan]\n")

        display_results(results[start:end])

        if total_pages == 1:
            break  # No need for pagination if only one page

        console.print("[bold yellow]Press d for next page, a for previous, or q to quit.[/bold yellow]")

        key = input().strip().lower()
        if key == "q":
            break
        elif key == "d" and current_page < total_pages - 1:
            current_page += 1
        elif key == "a" and current_page > 0:
            current_page -= 1


def get_valid_query():
    while True:
        console.print("🔍 Enter your search query (Press Ctrl+D when done): ")
        query = sys.stdin.read().strip()
        if query:
            return query
        console.print("\n[bold red]⚠️ Query cannot be empty. Please enter a valid search term.[/bold red]")

if __name__ == "__main__":
    query = get_valid_query()
    
    try:
        start_time = time.perf_counter()
        results = search_stackoverflow(query, field="body")
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"\nExecution time: {execution_time} seconds")

        # results = search_stackoverflow(query, field="body")
        paginate_results(results)
    except Exception as e:
        console.print(f"\n[bold red]⚠️ Error processing query:[/bold red] {e}")

