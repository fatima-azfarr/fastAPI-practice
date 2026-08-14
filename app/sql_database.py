import sqlite3
from typing import Any

from app.schema import ShipmentCreate, ShipmentStatusUpdate, ShipmentUpdate


# run database on different thread
class Database:
    def __init__(self):
        self.conn = sqlite3.connect("sqlite.db", check_same_thread=False)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS shipments (
                id INTEGER PRIMARY KEY,
                content TEXT,
                weight REAL,
                destination TEXT,
                status TEXT
            )
        """)
        self.conn.commit()

    # CREATE
    def create(self, body: ShipmentCreate) -> int:
        self.cur.execute("""
            INSERT INTO shipments (content, weight, destination, status)
            VALUES (:content, :weight, :destination, :status)
        """, {
            "content": body.content,
            "weight": body.weight,
            "destination": body.destination,
            "status": "placed"
        })

        self.conn.commit()

        return self.cur.lastrowid

    # GET
    def get(self, id: int) -> dict[str, Any] | None:
        self.cur.execute("""
            SELECT * FROM shipments
            WHERE id = ?
        """, (id,))

        row = self.cur.fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "content": row[1],
            "weight": row[2],
            "destination": row[3],
            "status": row[4]
        }

    # PATCH (status only)
    def patch(self, id: int, shipment: ShipmentStatusUpdate) -> dict[str, Any] | None:
        self.cur.execute("""
            UPDATE shipments
            SET status = :status
            WHERE id = :id
        """, {
            "id": id,
            **shipment.model_dump()
        })
        self.conn.commit()
        return self.get(id)

    # UPDATE (full replace)
    def update(self, id: int, shipment: ShipmentUpdate) -> dict[str, Any] | None:
        self.cur.execute("""
            UPDATE shipments
            SET content = :content, weight = :weight, destination = :destination, status = :status
            WHERE id = :id
        """, {
            "id": id,
            **shipment.model_dump()
        })
        self.conn.commit()
        return self.get(id)

    # DELETE
    def delete(self, id: int) -> None:
        self.cur.execute("""
            DELETE FROM shipments
            WHERE id = ?
        """, (id,))

        self.conn.commit()

    def close(self):
        self.conn.close()