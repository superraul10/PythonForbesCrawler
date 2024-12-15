import sqlite3
import os

def count_by_country(db_path="./database/billionaires.db", output_path="./output/country_counts.txt"):
   
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # am facut un query in care am selectat cate persoane sunt din state si cate nu
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN country = 'United States' THEN 1 ELSE 0 END) AS us_count,
            SUM(CASE WHEN country != 'United States' THEN 1 ELSE 0 END) AS non_us_count
        FROM billionaires
    """)

    result = cursor.fetchone()
    us_count = result[0] or 0
    non_us_count = result[1] or 0

    conn.close()


    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as file:
        file.write(f"Number of billionaires from the United States: {us_count}\n")
        file.write(f"Number of billionaires from other countries: {non_us_count}\n")

    print(f"Country counts successfully saved to {output_path}")

if __name__ == "__main__":
    database_path = "./database/billionaires.db"
    output_file_path = "./output/country_counts.txt"

    count_by_country(database_path, output_file_path)
