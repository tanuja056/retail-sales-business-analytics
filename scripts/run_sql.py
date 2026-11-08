import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "outputs" / "retail_analysis.db"
SQL_PATH = BASE_DIR / "sql" / "retail_analysis.sql"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

sql_content = SQL_PATH.read_text(encoding="utf-8")

queries = [
    query.strip()
    for query in sql_content.split(";")
    if query.strip()
]

for index, query in enumerate(queries, start=1):

    print("\n" + "=" * 60)
    print(f"SQL ANALYSIS {index}")
    print("=" * 60)

    cursor.execute(query)

    columns = [
        description[0]
        for description in cursor.description
    ]

    print(" | ".join(columns))
    print("-" * 60)

    for row in cursor.fetchall():
        print(" | ".join(str(value) for value in row))

connection.close()