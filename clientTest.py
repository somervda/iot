#!/usr/bin/python3

# see https://www.psycopg.org/psycopg3/docs/basic/usage.html 

# Note: the module name is psycopg, not psycopg3
import psycopg
import time

start=time.time()

# Connect to an existing database
with psycopg.connect("dbname=iotdb user=pi") as conn:

    # Open a cursor to perform database operations
    with conn.cursor() as cur:

        # Execute a command: this creates a new table
        # cur.execute("""
        #     CREATE TABLE test (
        #         id serial PRIMARY KEY,
        #         num integer,
        #         data text)
        #     """)

        # Pass data to fill a query placeholders and let Psycopg perform
        # the correct conversion (no SQL injections!)
        cur.execute(
            "INSERT INTO test (num, data) VALUES (%s, %s)",
            (500, "abc'def"))

        # Query the database and obtain data as Python objects.
        cur.execute("SELECT * FROM test")

        print("cur:",cur.rowcount,cur.description)
        # will return (1, 100, "abc'def")

        # You can use `cur.fetchmany()`, `cur.fetchall()` to return a list
        # of several records, or even iterate on the cursor
        for row in cur.fetchall():
            print("row:",row)

        print("duration:",time.time() - start)

        # Make the changes to the database persistent
        conn.commit()