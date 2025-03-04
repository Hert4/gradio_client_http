import duckdb

conn = duckdb.connect("./data/data.db")


conn.sql(
    """\
SELECT * FROM Users
"""
).show()
