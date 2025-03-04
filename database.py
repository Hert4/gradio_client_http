import duckdb

conn = duckdb.connect("./data/fakedb.db")


def execute(sql_query):
    try:
        return conn.sql(sql_query).to_df().to_string()
    except Exception as e:
        return f"An error occurred: {str(e)}"


def formattedDB():
    try:
        tables = conn.execute("SHOW TABLES").fetchall()
        result = ""

        for table in tables:
            table_name = table[0]
            result += f"CREATE TABLE {table_name} (\n"
            columns = conn.execute(f"PRAGMA table_info('{table_name}');").fetchall()

            column_definitions = [
                f"    {col[1]} {col[2]} {'NOT NULL' if col[3] else ''} {'DEFAULT ' + str(col[4]) if col[4] else ''}".strip()
                for col in columns
            ]

            result += ",\n".join(column_definitions)
            result += "\n);\n"

        return result
    except Exception as e:
        return f"An error occurred: {str(e)}"


db_schema = formattedDB()
