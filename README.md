# Forbes Billionaires Crawler 

This project scrapes data from the Forbes Billionaires list, processes it, and saves the results to JSON files, text files, and a SQLite database. It includes scripts to perform various analyses and generate insights.

---

## About the Project

The Forbes Billionaires Crawler performs the following tasks:

1. **Data Scraping**  
   - Retrieves data from the Forbes API, including information about billionaires such as name, age, country, net worth, industries, and rank.

2. **Data Storage**  
   - Saves the data to a JSON file for local access.  
   - Stores the structured data in a SQLite database for querying and analysis.

3. **Analyses**  
   - Counts the number of unique industries and their occurrences.  
   - Determines how many billionaires are U.S. citizens and how many are not.  
   - Identifies the top 10 youngest billionaires.

---

## Features

- **Data Collection**  
  - Scrapes billionaire data using the Forbes API.  
  - Fetches additional profile details for each billionaire.

- **Data Storage**  
  - Saves data in JSON format.  
  - Stores data in a SQLite database for efficient querying.

- **Analytical Scripts**  
  - Count billionaires by their citizenship.  
  - Analyze the count of billionaires by their source of wealth.  
  - Identify the youngest billionaires.

- **Text Output**  
  - Analysis results are saved in text files for easy access.

---

## Requirements

- **Python 3.6+**
- Libraries:  
  - `requests`
  - `sqlite3` (comes pre-installed with Python)
  - `os`
  - `json`

---
