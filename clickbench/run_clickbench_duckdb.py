import os
import subprocess
import sys

PYTHON = sys.executable

queries = [
    x.strip()
    for x in open("queries-duckdb.sql", encoding="utf-8")
    if x.strip()
]

if len(queries) != 43:
    raise RuntimeError(f"Expected 43 queries, got {len(queries)}")

result_file = "clickbench_duckdb.csv"

if os.path.exists(result_file):
    os.remove(result_file)

for f in ["my-db.duckdb", "my-db.duckdb.wal"]:
    if os.path.exists(f):
        os.remove(f)

print("========================================")
print("PREPARE DUCKDB 0.9.1")
print("========================================")

with open("create-multi-duckdb.sql", encoding="utf-8") as f:
    setup_sql = f.read()

subprocess.run(
    [PYTHON, r"..\common\create-view-duckdb.py"],
    input=setup_sql,
    text=True,
    check=True,
)

print("========================================")
print("DUCKDB 0.9.1 - CLICKBENCH Q1-Q43")
print("========================================")

for i, query in enumerate(queries, start=1):
    print(f"\n>>> DuckDB Q{i}/43")

    subprocess.run(
        [
            PYTHON,
            r"..\common\run-query-duckdb.py",
            str(i),
            "single",
            result_file,
        ],
        input=query,
        text=True,
        check=True,
    )

print("\n========================================")
print("DUCKDB Q1-Q43 COMPLETED")
print("========================================")