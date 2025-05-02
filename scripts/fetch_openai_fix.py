import snowflake.connector
import os

conn = snowflake.connector.connect(
    user='BIHACK2025',
    password='December2039',
    account='EV95053',
    warehouse='COMPUTE_WH',
    database='BIHACK2025',
    schema='DM'
)

cur = conn.cursor()
cur.execute("""
    SELECT id, failed_sql, recommendation 
    FROM pipeline_errors 
    WHERE analyzed = TRUE AND recommendation IS NOT NULL 
    ORDER BY created_at DESC 
    LIMIT 1
""")
row = cur.fetchone()

if row:
    with open("sql/openai_fix.sql", "w") as f:
        f.write(f"-- Original SQL:\n-- {row[1]}\n\n-- Fix Suggested by OpenAI:\n{row[2]}")
    cur.execute(f"UPDATE pipeline_errors SET analyzed = FALSE WHERE id = {row[0]}")
