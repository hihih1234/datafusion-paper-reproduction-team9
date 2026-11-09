import os
import shutil
import glob
import pyarrow as pa
import pyarrow.parquet as pq
from datafusion import SessionContext

SRC = r"data\tpch_sf10_csv"
DST = r"tpch\tpch_dataset"

D = pa.decimal128(15, 2)
I64 = pa.int64()
I32 = pa.int32()
S = pa.string()
DATE = pa.date32()

schemas = {
    "part": pa.schema([
        pa.field("p_partkey", I64, nullable=False),
        pa.field("p_name", S, nullable=False),
        pa.field("p_mfgr", S, nullable=False),
        pa.field("p_brand", S, nullable=False),
        pa.field("p_type", S, nullable=False),
        pa.field("p_size", I32, nullable=False),
        pa.field("p_container", S, nullable=False),
        pa.field("p_retailprice", D, nullable=False),
        pa.field("p_comment", S, nullable=False),
    ]),

    "supplier": pa.schema([
        pa.field("s_suppkey", I64, nullable=False),
        pa.field("s_name", S, nullable=False),
        pa.field("s_address", S, nullable=False),
        pa.field("s_nationkey", I64, nullable=False),
        pa.field("s_phone", S, nullable=False),
        pa.field("s_acctbal", D, nullable=False),
        pa.field("s_comment", S, nullable=False),
    ]),

    "partsupp": pa.schema([
        pa.field("ps_partkey", I64, nullable=False),
        pa.field("ps_suppkey", I64, nullable=False),
        pa.field("ps_availqty", I32, nullable=False),
        pa.field("ps_supplycost", D, nullable=False),
        pa.field("ps_comment", S, nullable=False),
    ]),

    "customer": pa.schema([
        pa.field("c_custkey", I64, nullable=False),
        pa.field("c_name", S, nullable=False),
        pa.field("c_address", S, nullable=False),
        pa.field("c_nationkey", I64, nullable=False),
        pa.field("c_phone", S, nullable=False),
        pa.field("c_acctbal", D, nullable=False),
        pa.field("c_mktsegment", S, nullable=False),
        pa.field("c_comment", S, nullable=False),
    ]),

    "orders": pa.schema([
        pa.field("o_orderkey", I64, nullable=False),
        pa.field("o_custkey", I64, nullable=False),
        pa.field("o_orderstatus", S, nullable=False),
        pa.field("o_totalprice", D, nullable=False),
        pa.field("o_orderdate", DATE, nullable=False),
        pa.field("o_orderpriority", S, nullable=False),
        pa.field("o_clerk", S, nullable=False),
        pa.field("o_shippriority", I32, nullable=False),
        pa.field("o_comment", S, nullable=False),
    ]),

    "lineitem": pa.schema([
        pa.field("l_orderkey", I64, nullable=False),
        pa.field("l_partkey", I64, nullable=False),
        pa.field("l_suppkey", I64, nullable=False),
        pa.field("l_linenumber", I32, nullable=False),
        pa.field("l_quantity", D, nullable=False),
        pa.field("l_extendedprice", D, nullable=False),
        pa.field("l_discount", D, nullable=False),
        pa.field("l_tax", D, nullable=False),
        pa.field("l_returnflag", S, nullable=False),
        pa.field("l_linestatus", S, nullable=False),
        pa.field("l_shipdate", DATE, nullable=False),
        pa.field("l_commitdate", DATE, nullable=False),
        pa.field("l_receiptdate", DATE, nullable=False),
        pa.field("l_shipinstruct", S, nullable=False),
        pa.field("l_shipmode", S, nullable=False),
        pa.field("l_comment", S, nullable=False),
    ]),

    "nation": pa.schema([
        pa.field("n_nationkey", I64, nullable=False),
        pa.field("n_name", S, nullable=False),
        pa.field("n_regionkey", I64, nullable=False),
        pa.field("n_comment", S, nullable=False),
    ]),

    "region": pa.schema([
        pa.field("r_regionkey", I64, nullable=False),
        pa.field("r_name", S, nullable=False),
        pa.field("r_comment", S, nullable=False),
    ]),
}

expected_rows = {
    "part": 2_000_000,
    "supplier": 100_000,
    "partsupp": 8_000_000,
    "customer": 1_500_000,
    "orders": 15_000_000,
    "lineitem": 59_986_052,
    "nation": 25,
    "region": 5,
}

os.makedirs(DST, exist_ok=True)

ctx = SessionContext()

for table, schema in schemas.items():
    print(f"\n=== {table} ===")

    src = os.path.join(SRC, f"{table}.csv")
    out = os.path.join(DST, table)

    if os.path.exists(out):
        shutil.rmtree(out)

    df = ctx.read_csv(
        src,
        schema=schema,
        has_header=True,
    )

    df.write_parquet(
        out,
        compression="zstd",
        compression_level=1,
    )

    files = glob.glob(os.path.join(out, "*.parquet"))
    if len(files) != 1:
        raise RuntimeError(
            f"{table}: expected 1 parquet file, got {len(files)}"
        )

    old_file = files[0]
    new_file = os.path.join(out, "part-0.parquet")
    os.rename(old_file, new_file)

    pf = pq.ParquetFile(new_file)

    rows = pf.metadata.num_rows
    groups = pf.metadata.num_row_groups
    codec = pf.metadata.row_group(0).column(0).compression
    size = os.path.getsize(new_file)

    print("rows       =", rows)
    print("expected   =", expected_rows[table])
    print("row_groups =", groups)
    print("compression=", codec)
    print("size_bytes =", size)

    if rows != expected_rows[table]:
        raise RuntimeError(
            f"{table}: row count mismatch: {rows}"
        )

    if codec != "ZSTD":
        raise RuntimeError(
            f"{table}: expected ZSTD, got {codec}"
        )

print("\nALL 8 TABLES CONVERTED SUCCESSFULLY")