import sqlite3

# create connection
connection = (sqlite3.connect("sqlite.db"))

# need a cursor to execute the SQL language that is our queries
cursor = connection.cursor()

# 1. create a table
cursor.execute("""
     CREATE TABLE IF NOT EXISTS shipments(
        id INTEGER PRIMARY KEY,
        content TEXT,
        weight REAL,
        status TXT
    )
""")

# 2. Add data to shipments
cursor.execute("""
     INSERT INTO shipments
     VALUES
     ( 12346, 'basalt', 18.4, 'in transit'),
     ( 12347, 'yarn', 10.4, 'out to deliver'),
     ( 12348, 'wool', 8.2, 'placed'),
     ( 12349, 'steel ball', 13.4, 'in transit')

""")
connection.commit()


# 3. Read data from shipments
cursor.execute("""
     SELECT *FROM shipments
     WHERE id = 12348
""")
result = cursor.fetchall()
print (result)


# 4. Update a shipment
cursor.execute("""
    UPDATE shipments SET status = 'in transit'
    WHERE id = 12348
""")
connection.commit()

# or you can update like this too
id = 12346
status = "in transit"
cursor.execute("""
    UPDATE shipments SET status = ?
    WHERE id = ?
""",(status,id))
connection.commit()

# or you can update like this
id = 12346
status = "in transit"
cursor.execute("""
    UPDATE shipments SET status = :status
    WHERE id = :id
""",{"status":status,"id":id}
)

# 5. delete duplicate rows
cursor.execute("""
    SELECT id, COUNT(*)
    FROM shipments
    GROUP BY id
    HAVING COUNT(*) > 1
""")
print(cursor.fetchall())

cursor.execute("""
    DELETE FROM shipments
    WHERE rowid NOT IN (
        SELECT MIN(rowid)
        FROM shipments
        GROUP BY id
    )
""")
connection.commit()


# close connection
connection.close()