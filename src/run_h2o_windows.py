import os
import subprocess
import sys

PYTHON = sys.executable

df_queries = [
    x.strip()
    for x in open("queries-datafusion.sql", encoding="utf-8")
    if x.strip()
]

duck_queries = [
    x.strip()
    for x in open("queries-duckdb.sql", encoding="utf-8")
    if x.strip()
]

if len(df_queries) != 10 or len(duck_queries) != 10:
    raise RuntimeError(
        f"Expected 10 queries, got DF={len(df_queries)}, DuckDB={len(duck_queries)}"
    )

df_result = "h2o_datafusion.csv"
duck_result = "h2o_duckdb.csv"

for f in [df_result, duck_result]:
    if os.path.exists(f):
        os.remove(f)

print("========================================")
print("DATAFUSION 32.0.0 - H2O-G")
print("========================================")

for i, query in enumerate(df_queries, start=1):
    print(f"\n>>> DataFusion Q{i}/10")

    subprocess.run(
        [
            PYTHON,
            r"..\common\run-query-datafusion.py",
            "create-single-datafusion.sql",
            str(i),
            "single",
            df_result,
        ],
        input=query,
        text=True,
        check=True,
    )

print("\n========================================")
print("PREPARE DUCKDB 0.9.1")
print("========================================")

for f in ["my-db.duckdb", "my-db.duckdb.wal"]:
    if os.path.exists(f):
        os.remove(f)

with open("create-single-duckdb.sql", encoding="utf-8") as f:
    setup_sql = f.read()

subprocess.run(
    [PYTHON, r"..\common\create-view-duckdb.py"],
    input=setup_sql,
    text=True,
    check=True,
)

print("\n========================================")
print("DUCKDB 0.9.1 - H2O-G")
print("========================================")

for i, query in enumerate(duck_queries, start=1):
    print(f"\n>>> DuckDB Q{i}/10")

    subprocess.run(
        [
            PYTHON,
            r"..\common\run-query-duckdb.py",
            str(i),
            "single",
            duck_result,
        ],
        input=query,
        text=True,
        check=True,
    )

print("\n========================================")
print("H2O-G Q1-Q10 COMPLETED")
print("========================================")