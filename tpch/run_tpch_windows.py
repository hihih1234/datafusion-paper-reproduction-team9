import os
import shutil
import subprocess
import sys

PYTHON = sys.executable

queries = [
    line.strip()
    for line in open("queries.sql", encoding="utf-8")
    if line.strip()
]

if len(queries) != 22:
    raise RuntimeError(f"Expected 22 queries, got {len(queries)}")

df_result = "tpch_datafusion.csv"
duck_result = "tpch_duckdb.csv"

for f in [df_result, duck_result]:
    if os.path.exists(f):
        os.remove(f)

print("========================================")
print("DATAFUSION 32.0.0 - TPC-H SF=10")
print("========================================")

for i, query in enumerate(queries, start=1):
    print(f"\n>>> DataFusion Q{i}/22")

    subprocess.run(
        [
            PYTHON,
            r"..\common\run-query-datafusion.py",
            "create-win-datafusion.sql",
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

with open("create-win-duckdb.sql", encoding="utf-8") as f:
    setup_sql = f.read()

subprocess.run(
    [PYTHON, r"..\common\create-view-duckdb.py"],
    input=setup_sql,
    text=True,
    check=True,
)

print("\n========================================")
print("DUCKDB 0.9.1 - TPC-H SF=10")
print("========================================")

for i, query in enumerate(queries, start=1):
    print(f"\n>>> DuckDB Q{i}/22")

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
    r"..\results\latest\tpch_datafusion_windows_sf10.csv"
)

shutil.copy2(
    duck_result,
    r"..\results\latest\tpch_duckdb_windows_sf10.csv"
)

print("\n========================================")
print("ALL 22 QUERIES COMPLETED")
print("========================================")
print("DataFusion:", df_result)
print("DuckDB:", duck_result)