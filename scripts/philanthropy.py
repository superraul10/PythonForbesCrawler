import sqlite3
import os

def philanthropy_by_source(db_path="./database/billionaires.db", output_path="./output/philanthropy_by_source.txt"):
   
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()


    cursor.execute("""
        SELECT source, COUNT(*) as count
        FROM billionaires
        WHERE source IS NOT NULL
        GROUP BY source
        ORDER BY count DESC
    """)

    results = cursor.fetchall()
    conn.close()

 
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as file:
        file.write("Philanthropy Count by Source:\n")
        file.write("=" * 40 + "\n")
        for source, count in results:
            file.write(f"{source}: {count}\n")

    print(f"Philanthropy by source successfully saved to {output_path}")

if __name__ == "__main__":
    database_path = "./database/billionaires.db"
    output_file_path = "./output/philanthropy_by_source.txt"

    philanthropy_by_source(database_path, output_file_path)
