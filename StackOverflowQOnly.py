import requests
import json
import time

BASE_URL = "https://api.stackexchange.com/2.3"

def fetch_questions(tag="runtime-error", pagesize=100, max_pages=5):
    questions = []
    for page in range(1, max_pages + 1):
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
            },
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code != 200:
            print(f"Error fetching questions: {response.status_code} - {response.text}")
            break
        
        data = response.json()
        print(f"Quota Remaining: {data.get('quota_remaining', 'Unknown')}")
        
        items = data.get("items", [])
        if not items:
            print("No questions found on this page.")
            break
        
        questions.extend(items)
        
        if not data.get("has_more", False):
            print("No more pages to fetch.")
            break

        time.sleep(1)

    return questions



# Save questions and their metadata in a JSON file
def save_to_json(filename, questions):
    combined_data = []
    for question in questions:
        question_data = {
            "title": question["title"],
            "link": question["link"],
            "creation_date": question["creation_date"],
            "score": question["score"],
            "tags": question["tags"],
        }
        combined_data.append(question_data)

    with open(filename, "w") as f:
        json.dump(combined_data, f, indent=4)
    print(f"Saved data to {filename}")


# Main workflow
if __name__ == "__main__":
    # Fetch questions
    questions = fetch_questions(tag="runtime-error", max_pages=5)
    
    # Print number of questions fetched
    print(f"Fetched {len(questions)} questions.")
    
    # Save questions to a JSON file
    save_to_json("runtime_error_questions.json", questions)
