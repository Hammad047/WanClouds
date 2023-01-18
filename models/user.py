from app import db
from sqlalchemy import Column
from sqlalchemy import String


class User(db.Model):
    # COLUMNS OF USER TABLE
    name = Column(String(45))
    email = Column(String(100), primary_key=True)
    password = Column(String(200))

    __tablename__ = 'user'

    # Setting values to the table
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    # To make the changing in the table
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
