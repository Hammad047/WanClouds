# from sqlalchemy import Column, String, Integer
# from app.db import db
#
# # TABLE FOR USER
# class user_data(db.Model):
#     # COLUMNS OF USER TABLE
#     name = Column(String(45))
#     email = Column(String(100), primary_key=True)
#     password = Column(String(200))
#     # TABLE NAME = "users"
#     __tablename__ = "users"
#
#     # Setting values to the table
#     def __init__(self, name, email, password):
#         self.name = name
#         self.email = email
#         self.password = password
#
#     # To make the changing in the table
#     def create(self):
#         db.session.add(self)
#         db.session.commit()
#         return self
#
#
# # TABLE FOR CAR
# class car_data(db.Model):
#     object_id = Column(String(45), primary_key=True)
#     year = Column(Integer)
#     make = Column(String(45))
#     model = Column(String(45))
#     category = Column(String(45))
#     created_at = Column(String(45))
#     updated_at = Column(String(45))
#     # Tablename = "cars"
#     __tablename__ = "cars"
#
#     # Setting values to the table
#     def __init__(self, objectid, year, make, model, category, createdate, updatedate):
#         self.object_id = objectid
#         self.year = year
#         self.make = make
#         self.model = model
#         self.category = category
#         self.created_at = createdate
#         self.updated_at = updatedate
#
#     # To make the changing in the table
#     def create(self):
#         db.session.add(self)
#         db.session.commit()
#         return self
#
#     # To Display the table data
#     def display(self):
#         return {
#             "object_id": self.object_id,
#             "year": self.year,
#             "make": self.make,
#             "model": self.model,
#             "category": self.category,
#             "created_at": self.created_at,
#             "updated_at": self.updated_at
#         }
