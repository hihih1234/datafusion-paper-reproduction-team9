import pyarrow as pa
import pyarrow.compute as pc

from datafusion import SessionContext, udf


def price_band(arr: pa.Array) -> pa.Array:
    threshold = pa.scalar(50000, type=pa.decimal128(15, 2))
    cond = pc.greater_equal(arr, threshold)

    return pc.if_else(
        cond,
        pa.scalar("HIGH"),
        pa.scalar("NORMAL")
    )


price_band_udf = udf(
    price_band,
    [pa.decimal128(15, 2)],
    pa.string(),
    "immutable",
    "price_band"
)


ctx = SessionContext()

ctx.register_parquet(
    "lineitem",
    r"D:\datafusion-demo\data\tpch_sf10_parquet_official\lineitem\part-0.parquet"
)

ctx.register_udf(price_band_udf)

query = """
SELECT
    price_band(l_extendedprice) AS price_band,
    COUNT(*) AS row_count,
    SUM(l_extendedprice) AS total_price
FROM lineitem
GROUP BY price_band(l_extendedprice)
ORDER BY price_band
"""

ctx.sql(query).show()