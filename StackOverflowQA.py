import requests
import json
import time

BASE_URL = "https://api.stackexchange.com/2.3"

def fetch_questions(tag="runtime-error", pagesize=100):
    questions = []
    page = 1
    while True:
        print(f"Fetching page {page} of questions...")
        response = requests.get(
            f"{BASE_URL}/questions",
            params={
                "order": "desc",
                "sort": "activity",
                "tagged": tag,
                "site": "stackoverflow",
                "pagesize": pagesize,
                "page": page,
                "filter": "withbody",  # Request the question body
            },
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code != 200:
            print(f"Error fetching questions: {response.status_code} - {response.text}")
            break
        
        data = response.json()
        
        # Handle backoff parameter if present
        if "backoff" in data:
            backoff_time = data["backoff"]
            print(f"API requests throttled. Backing off for {backoff_time} seconds...")
            time.sleep(backoff_time)
        
        print(f"Quota Remaining: {data.get('quota_remaining', 'Unknown')}")
        
        items = data.get("items", [])
        if not items:
            print("No questions found on this page.")
            break
        
        questions.extend(items)
        
        if not data.get("has_more", False):  # Check if there are more pages to fetch
            print("No more pages to fetch.")
            break

        page += 1
        time.sleep(1)  # Basic rate-limiting delay between requests

    return questions



def fetch_answers(question_ids):
    answers = {}
    chunk_size = 20  
    for i in range(0, len(question_ids), chunk_size):
        chunk = question_ids[i:i + chunk_size]
        print(f"Fetching answers for question IDs: {chunk}")
        response = requests.get(
            f"{BASE_URL}/questions/{';'.join(map(str, chunk))}/answers",
            params={
                "order": "desc",
                "sort": "votes",
                "site": "stackoverflow",
                "filter": "withbody",  
            },
        )
        if response.status_code != 200:
            print(f"Error fetching answers: {response.status_code} - {response.text}")
            continue

        data = response.json()
        for answer in data.get("items", []):
            question_id = answer.get("question_id")
            if question_id:
                answers.setdefault(question_id, []).append(answer)

        time.sleep(1)

    return answers


def save_to_json(filename, questions, answers):
    combined_data = []
    for question in questions:
        question_id = question["question_id"]
        question_data = {
            "title": question["title"],
            "body": question["body"],
            "link": question["link"],
            "creation_date": question["creation_date"],
            "score": question["score"],
            "tags": question["tags"],
            "answer_count": question["answer_count"],
            "answers": answers.get(question_id, []),
        }
        combined_data.append(question_data)

    with open(filename, "w") as f:
        json.dump(combined_data, f, indent=4)
    print(f"Saved data to {filename}")


if __name__ == "__main__":
    # Fetch all questions with the tag "runtime-error"
    questions = fetch_questions(tag="compiler-errors")
    print(f"Fetched {len(questions)} questions.")

    # Fetch answers for the fetched questions
    question_ids = [q["question_id"] for q in questions]
    answers = fetch_answers(question_ids)

    # Save everything to a JSON file
    save_to_json("QA.json", questions, answers)
