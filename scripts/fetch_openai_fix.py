import snowflake.connector
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

conn = snowflake.connector.connect(
    user='BIHACK2025',
    password='December2025barkul',
    account='GQNAKNG-EV95053',
    warehouse='COMPUTE_WH',
    database='BIHACK2025',
    schema='DM'
)

cur = conn.cursor()
cur.execute("""
    SELECT id, failed_sql, recommendation 
    FROM pipeline_errors 
    WHERE analyzed = TRUE AND recommendation IS NOT NULL 
    ORDER BY in_ts DESC 
    LIMIT 1 
""")
row = cur.fetchone()

if row:
    output_dir = "sql"
    output_file = os.path.join(output_dir, "openai_fix.sql")
    
    # Ensure the directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        with open(output_file, "w") as f:
            f.write(f"-- Original SQL:\n-- {row[1]}\n\n-- Fix Suggested by OpenAI:\n{row[2]}")
        cur.execute(f"UPDATE pipeline_errors SET analyzed = FALSE WHERE id = {row[0]}")
        logging.info(f"Fix written to {output_file} for error ID {row[0]}")
    except Exception as e:
        logging.error(f"Failed to write to {output_file}: {e}")
else:
    logging.info("No analyzed pipeline errors with recommendations found.")
    try:
        output_dir = "sql"
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, "openai_fix.sql"), "w") as f:
            f.write("-- No fix available.\n")
        logging.info("Empty fix file created.")
    except Exception as e:
        logging.error(f"Failed to write to sql/openai_fix.sql: {e}")
