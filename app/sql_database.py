import sqlite3
from typing import Any

from app.schema import ShipmentCreate, ShipmentRead, ShipmentUpdate


class Database:
    def __init__(self):
        # Make connection with the database
        self.conn = sqlite3.connect("sqlite.db")

        # Create a cursor to execute SQL queries
        self.cur = self.conn.cursor()

        # Create the table if it doesn't exist
        self.create_table()

    # 1. Create a table
    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS shipments (
                id INTEGER PRIMARY KEY,
                content TEXT,
                weight REAL,
                status TEXT
            )
        """)
        self.conn.commit()

    # 2. Save shipment data
    def create(self, body: ShipmentCreate) -> int:

        # Find the highest ID
        self.cur.execute("SELECT MAX(id) FROM shipments")

        result = self.cur.fetchone()

        # If there are no shipments, start at 1
        new_id = (result[0] or 0) + 1

        # Add data to shipments
        self.cur.execute("""
            INSERT INTO shipments (id, content, weight, status)
            VALUES (:id, :content, :weight, :status)
        """, {
            "id": new_id,
            "content": body.content,
            "weight": body.weight,
            "status": "placed"
        })

        # Commit the changes
        self.conn.commit()

        return new_id

    # 3. Read data from shipments
    def get(self, id: int) -> dict[str, Any] | None:

        self.cur.execute("""
            SELECT id, content, weight, status
            FROM shipments
            WHERE id = ?
        """, (id,))

        row = self.cur.fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "content": row[1],
            "weight": row[2],
            "status": row[3]
        }

    # 4. Update a shipment
    def update(self, id:int, shipment: ShipmentUpdate) -> dict[str, Any] | None:

        self.cur.execute("""
            UPDATE shipments
            SET content = :content, weight = :weight, status = :status
            WHERE id = ?
        """, {
            "id" : id,
            **shipment.model_dump(),
            }
        )
        self.conn.commit()

        return self.get(id)

    # 5. Delete a shipment
    def delete(self, id: int) -> None:

        self.cur.execute("""
            DELETE FROM shipments
            WHERE id = ?
        """, (id,))

        self.conn.commit()

    # Close connection
    def close(self):
        self.conn.close()