import sqlite3
import os

def get_top_youngest(db_path="./database/billionaires.db", output_path="./output/youngest_billionaires.txt"):

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

   # cursor (ca asa am facut la sgbd :) ) in care o sa retinem ce query vrem sa facem
    cursor.execute("""
        SELECT name, age, country, finalWorth, source
        FROM billionaires
        WHERE age IS NOT NULL
        ORDER BY age ASC
        LIMIT 10
    """)

    youngest_billionaires = cursor.fetchall()
    conn.close()

   #fusuer de output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # am pus rezultatul intr-un .txt
    with open(output_path, "w") as file:
        file.write("Top 10 Youngest Billionaires:\n")
        file.write("====================================\n")
        for idx, billionaire in enumerate(youngest_billionaires, start=1):
            name, age, country, finalWorth, source = billionaire
            file.write(f"{idx}. {name} (Age: {age})\n")
            file.write(f"   Country: {country}, Net Worth: ${finalWorth}B, Source: {source}\n\n")

    print(f"Top 10 youngest billionaires saved to {output_path}")

if __name__ == "__main__":
   
    database_path = "./database/billionaires.db"

    output_file_path = "./output/youngest_billionaires.txt"

   
    get_top_youngest(database_path, output_file_path)
