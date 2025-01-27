import requests
import json
import time

BASE_URL = "https://api.stackexchange.com/2.3"

# Fetch all tags containing the word "error"
def fetch_error_tags():
    error_tags = []
    page = 1
    while True:
        print(f"Fetching page {page} of tags...")
        response = requests.get(
            f"{BASE_URL}/tags",
            params={
                "order": "desc",
                "sort": "popular",
                "inname": "error",  # Search for tags containing "error"
                "site": "stackoverflow",
                "pagesize": 100,
                "page": page,
            },
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code != 200:
            print(f"Error fetching tags: {response.status_code} - {response.text}")
            break
        
        data = response.json()
        tags = data.get("items", [])
        if not tags:
            print("No more tags found.")
            break
        
        error_tags.extend([tag["name"] for tag in tags])
        
        if not data.get("has_more", False):  # Check if there are more pages of tags
            print("No more pages of tags to fetch.")
            break

        page += 1
        time.sleep(1)  # Respect API rate limits

    return error_tags


# Fetch questions for a specific tag
def fetch_questions(tag, pagesize=100):
    questions = []
    for page in range(1, 26):  # Fetch up to 25 pages
        print(f"Fetching page {page} of questions for tag: {tag}")
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
            print(f"Error fetching questions for tag {tag}: {response.status_code} - {response.text}")
            break
        
        data = response.json()
        if data.get("quota_remaining", 0) < 10:  # Stop if the quota is too low
            print("Quota is running low. Pausing for 15 mins...")
            time.sleep(900)

        
        # Handle backoff parameter if present
        if "backoff" in data:
            backoff_time = data["backoff"]
            print(f"API requests throttled. Backing off for {backoff_time} seconds...")
            time.sleep(backoff_time)
        
        items = data.get("items", [])
        if not items:
            print(f"No questions found for tag {tag} on page {page}.")
            break
        
        questions.extend(items)
        
        if not data.get("has_more", False):  # Stop if there are no more pages
            print(f"No more questions for tag {tag}.")
            break

        time.sleep(5)  # Respect API rate limits

    return questions


# Fetch answers for a list of question IDs
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

        time.sleep(5)

    return answers


# Save data to JSON file
def save_to_json(filename, questions, answers):
    combined_data = []
    for question in questions:
        question_id = question["question_id"]
        question_data = {
            "title": question["title"],
            "body": question.get("body", ""),  # Ensure body exists
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


# Main workflow
if __name__ == "__main__":
    # Step 1: Fetch all error-type tags
    error_tags = fetch_error_tags()
    print(f"Fetched {len(error_tags)} error-type tags. They are - {error_tags}")

    # Step 2: Fetch questions and answers for each tag
    for tag in error_tags:
        print(f"Processing tag: {tag}")
        
        # Fetch questions for the tag
        questions = fetch_questions(tag)
        print(f"Fetched {len(questions)} questions for tag: {tag}")

        # Fetch answers for the fetched questions
        question_ids = [q["question_id"] for q in questions]
        answers = fetch_answers(question_ids)

        # Save questions and answers to a JSON file
        filename = f"{tag}_questions.json"
        save_to_json(filename, questions, answers)

        # Pause between tags to avoid hitting rate limits
        time.sleep(30)
