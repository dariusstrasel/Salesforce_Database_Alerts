import os
import sys
import sqlite3
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine



class Database:

    def __init__(self, name):
        self.location = '../'
        self.filename = name + '.db'
        self.database_path = self.location + self.filename
        self.database_connection = sqlite3.connect(self.database_path)

    def open_cursor(self, sql_statement):
        cursor = self.database_connection.cursor()
        try:
            cursor.execute(sql_statement)
            self.database_connection.commit()
        except Exception:
            self.database_connection.rollback()
            self.database_conn;ection.close()


def init_database():

    Base = declarative_base()

    class Person(Base):
        __tablename__ = 'person'
        # Here we define columns for the table person
        # Notice that each column is also a normal Python instance attribute.
        id = Column(Integer, primary_key=True)
        name = Column(String(250), nullable=False)

    class Address(Base):
        __tablename__ = 'address'
        # Here we define columns for the table address.
        # Notice that each column is also a normal Python instance attribute.
        id = Column(Integer, primary_key=True)
        street_name = Column(String(250))
        street_number = Column(String(250))
        post_code = Column(String(250), nullable=False)
        person_id = Column(Integer, ForeignKey('person.id'))
        person = relationship(Person)

    # Create an engine that stores data in the local directory's
    # sqlalchemy_example.db file.
    engine = create_engine('sqlite:///sqlalchemy_example.db')

    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)


queries_database = Database("sqlalchemy_example")
# init_database()
