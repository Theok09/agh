import requests
import time
from random import randint

# Constants
FRAGMENT_URL = "https://fragment.com/username/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# Function to fetch random usernames
def get_random_usernames():
    api_url = "https://random-word-api.vercel.app/api?words=10"
    try:
        response = requests.get(api_url, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching usernames. Status code: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error connecting to the API: {e}")
        return []

# Function to check username status on Fragment
def check_username_fragment(username):
    try:
        url = FRAGMENT_URL + username
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            if "is available" in response.text:
                print(f"✅ Username '{username}' is available!")
                return "Available"
            elif "is not available" in response.text:
                print(f"❌ Username '{username}' is unavailable.")
                return "Unavailable"
            else:
                print(f"⚠️ Unknown status for username '{username}'.")
                return "Unknown"
        elif response.status_code == 404:
            print(f"❌ Username '{username}' not found (404).")
            return "Not Found"
        else:
            print(f"⚠️ Unexpected error for username '{username}'. Status code: {response.status_code}")
            return "Error"
    except Exception as e:
        print(f"Error checking username '{username}': {e}")
        return "Error"

# Function to save results to a file
def save_results_to_file(results, filename="results.txt"):
    try:
        with open(filename, "w") as file:
            for username, status in results.items():
                file.write(f"{username}: {status}\n")
        print(f"✅ Results saved to '{filename}'.")
    except Exception as e:
        print(f"Error saving results: {e}")

# Main program execution
def main():
    usernames = get_random_usernames()
    if not usernames:
        print("⚠️ No usernames to check.")
        return
    
    print(f"🟢 Starting checks for usernames: {usernames}")
    results = {}

    for username in usernames:
        status = check_username_fragment(username)
        results[username] = status
        time.sleep(randint(1, 3))  # Random delay to avoid being blocked

    save_results_to_file(results)

if __name__ == "__main__":
    main()
