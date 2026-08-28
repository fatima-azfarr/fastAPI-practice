import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from app.schema import ShipmentCreate, ShipmentStatusUpdate, ShipmentUpdate


# run database on different thread
class Database:
   
    def connect_to_db(self):
        # make connection to the database
        print("Connected to sqlite.db...")
        DB_PATH = Path(__file__).parent / "sqlite.db"
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)

        # get cursor to execute the queries
        self.cur = self.conn.cursor()

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
        print("....closing connection.")
        self.conn.close()


    # when we enter the context i.e database, we have to go ahead and create the connection.
    '''def __enter__(self):
        # create the connection
        print("Enter the context.")
        self.connect_to_db()
        # create table if already not there
        self.create_table()
        return self # thats the database instance

    # when we exit the context i.e database, we close the connection
    def __exit__(self, *arg):
        print("Exiting the context.")
        #disposal of the state
        self.close()'''

    
# if we import from another pakage/module - we use function approach
@contextmanager
def managed_db():

    #initialise
    db = Database()

    # setup
    print("Enter the setup....")
    db.connect_to_db()
    db.create_table()

    # generator function
    yield db
    print("....Exiting the context")

    #disposal
    db.close()


# initialized, make a connection to the database, perform the actions and then close it as well.
# Context manager - does this automatically where database is the context and manager deals with opening and closing of the connection
    
#context manager - 
with managed_db() as db:
    print(db.get(1))
    print(db.get(2))






    
    