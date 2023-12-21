import csv
import requests

def get_language_choice():
    languages = ["Javascript", "PHP", "Python", "SQL"]
    print("Solutions in which language do you want to download?\n")
    for i, language in enumerate(languages, 1):
        print(f"{i}) {language}")
    choice = input("\nPlease choose a number: ")
    if choice.isdigit() and 1 <= int(choice) <= len(languages):
        return languages[int(choice) - 1].lower()
    else:
        print("Sorry, use number from list.")
        return None

def fetch_challenge_data(language):
    completed_challenges = []
    for page in range(0, 5):
        response = requests.get(f"https://www.codewars.com/api/v1/users/YOUR_NIKNAME_HERE/code-challenges/completed?page={page}")
        if response.status_code == 200:
            data = response.json()
            completed_challenges.extend(data['data'])
    return [ch['id'] for ch in completed_challenges if language in ch['completedLanguages']]

def fetch_kata_details(challenge_ids):
    kata_details = []
    for ch_id in challenge_ids:
        kata_response = requests.get(f"https://www.codewars.com/api/v1/code-challenges/{ch_id}")
        if kata_response.status_code == 200:
            kata_data = kata_response.json()
            name = kata_data.get('name', 'N/A')
            description = kata_data.get('description', 'N/A')
            url = kata_data.get('url', 'N/A')
            rank = kata_data.get('rank', {}).get('name', 'N/A')
            kata_details.append([name, description, url, rank])
    return kata_details

def write_to_csv(kata_details, language):
    with open(f'{language}-katas.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Name', 'Description', 'URL', 'Rank'])
        for detail in kata_details:
            writer.writerow(detail)

def main():
    language = get_language_choice()
    if language:
        challenge_ids = fetch_challenge_data(language)
        kata_details = fetch_kata_details(challenge_ids)
        write_to_csv(kata_details, language)
        print(f'CSV file for {language} challenges created successfully.')

if __name__ == "__main__":
    main()