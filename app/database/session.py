from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

# made an engine to work with our database, basically a connection to our database
engine = create_engine(
    # url to our database
    url = "sqlite:///sqlite.db",
    # echo=true to get the sql statements executed on our database printed on the terminal as well
    echo = True,
    # if running fastapi and database on single thread, will cause collision 
    connect_args={
        "check_same_thread" : False},
) 

# create table if doesnt exit already without writing any sql query 
# by just defining a model like this using sql model and 
# using its metadata create all method to create the tables

def create_db_table():
    SQLModel.metadata.create_all(engine)

# to get the data - interact with the database
# in order to get this session in endpoints we can use dependency injections
# session = dependency - injected into endpoints
