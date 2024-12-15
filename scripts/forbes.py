import requests
import json
import os
import sqlite3

# Aici ma folosesc de API-ul Forbes pentru a colecta date despre miliardari (practic codul generat pe Insomnia, doar ca putin modificat)

def get_billionaire_data(page):
    base_url = "https://www.forbes.com/forbesapi/person/billionaires/2024/position/true.json"
    params = {
        "fields": "uri,finalWorth,age,country,source,rank,category,personName,industries,organization,gender,firstName,lastName,squareImage,bios,status,countryOfCitizenship",
        "page": page
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json",
        "Connection": "keep-alive"
    }

    try:
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch page {page}, status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None

# Aici ma folosesc de ce am generat anterior si colectez datele despre fiecare in parte

def fetch_profile_details(uri):
    profile_url = f"https://www.forbes.com/forbesapi/person/{uri}.json"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(profile_url, headers=headers)
        if response.status_code == 200:
            profile_data = response.json().get("person", {})
            person_lists = profile_data.get("personLists", [])

            latest = next((entry for entry in person_lists if entry.get("year") == 2024), None)
            if latest:
                return {
                    "name": latest.get("personName"),
                    "age": latest.get("age"),
                    "country": latest.get("country"),
                    "finalWorth": latest.get("finalWorth"),
                    "source": latest.get("source"),
                    "rank": latest.get("rank"),
                    "industries": latest.get("industries"),
                    "bios": latest.get("bios", []),
                    "image": latest.get("squareImage"),
                }
            else:
                print("No recent data found for profile.")
                return None
        else:
            print(f"Failed to fetch profile {uri}, status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Profile request error: {e}")
        return None

# Aici imbin functiile de mai sus pentru a colecta datele despre miliardari
def collect_billionaires(limit=200):
    page = 1 # Pagina de start
    billionaires = []

    while len(billionaires) < limit:
        data = get_billionaire_data(page)
        if not data or "personList" not in data or "personsLists" not in data["personList"]:
            break

        for person in data["personList"]["personsLists"]:
            if len(billionaires) >= limit:
                break

            profile_uri = person.get("uri")
            if profile_uri:
                profile_data = fetch_profile_details(profile_uri)
                if profile_data:
                    billionaires.append(profile_data)

        page += 1

    return billionaires

# Salvez datele intr-un JSON pentru a le pune ulterior intr-un sqlite database

def save_data_to_file(billionaires, filename="./database/billionaires.json"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as file:
        json.dump(billionaires, file, indent=4)
    print(f"Data successfully saved to {filename}")

#Functie de creat baza de date
def create_database(db_path="./database/billionaires.db"):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS billionaires (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            country TEXT,
            finalWorth REAL,
            source TEXT,
            rank INTEGER,
            industries TEXT,
            bios TEXT,
            image TEXT
        )
    """)

    conn.commit()
    conn.close()
    print(f"Database created or already exists at {db_path}")

def save_json_to_database(json_path, db_path="./database/billionaires.db"):
    # Conectăm la baza de date
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Citim datele din fișierul JSON
    with open(json_path, "r") as file:
        billionaires = json.load(file)

    # Inserăm datele în tabel
    for billionaire in billionaires:
        cursor.execute("""
            INSERT INTO billionaires (name, age, country, finalWorth, source, rank, industries, bios, image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            billionaire.get("name"),
            billionaire.get("age"),
            billionaire.get("country"),
            billionaire.get("finalWorth"),
            billionaire.get("source"),
            billionaire.get("rank"),
            ", ".join(billionaire.get("industries", []) if billionaire.get("industries") else []),
            ", ".join(billionaire.get("bios", []) if billionaire.get("bios") else []),
            billionaire.get("image")
        ))

    conn.commit()
    conn.close()
    print(f"Data from {json_path} successfully saved to {db_path}")



if __name__ == "__main__":
    billionaire_list = collect_billionaires(limit=200)
    #salvam in json
    save_data_to_file(billionaire_list)
    #pathurile
    json_file_path = "./database/billionaires.json"
    database_path = "./database/billionaires.db"

    
    create_database(database_path)


    save_json_to_database(json_file_path, database_path)
