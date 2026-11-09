import os
import shutil
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

if len(df_queries) != 43 or len(duck_queries) != 43:
    raise RuntimeError(
        f"Expected 43 queries, got DF={len(df_queries)}, DuckDB={len(duck_queries)}"
    )

df_result = "clickbench_datafusion.csv"
duck_result = "clickbench_duckdb.csv"

for f in [df_result, duck_result]:
    if os.path.exists(f):
        os.remove(f)

print("========================================")
print("DATAFUSION 32.0.0 - CLICKBENCH")
print("========================================")

for i, query in enumerate(df_queries, start=1):
    print(f"\n>>> DataFusion Q{i}/43")

    subprocess.run(
        [
            PYTHON,
            r"..\common\run-query-datafusion.py",
            "create-multi-datafusion.sql",
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

with open("create-multi-duckdb.sql", encoding="utf-8") as f:
    setup_sql = f.read()

subprocess.run(
    [PYTHON, r"..\common\create-view-duckdb.py"],
    input=setup_sql,
    text=True,
    check=True,
)

print("\n========================================")
print("DUCKDB 0.9.1 - CLICKBENCH")
print("========================================")

for i, query in enumerate(duck_queries, start=1):
    print(f"\n>>> DuckDB Q{i}/43")

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

os.makedirs(r"..\results\latest", exist_ok=True)

shutil.copy2(
    df_result,
    r"..\results\latest\clickbench_datafusion_windows.csv"
)

shutil.copy2(
    duck_result,
    r"..\results\latest\clickbench_duckdb_windows.csv"
)

print("\n========================================")
print("ALL 43 QUERIES COMPLETED")
print("========================================")