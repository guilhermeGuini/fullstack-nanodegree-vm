import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):

    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)

class MenuItem(Base):

    __tablename__ = 'menu_item'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))

    restaurant = relationship(Restaurant)

#We added this serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):
       
       return {
           'name'        : self.name,
           'description' : self.description,
           'id'          : self.id,
           'price'       : self.price,
           'course'      : self.course
       }

####### insert at end of file #######

engine = create_engine(
    "postgresql+psycopg2://postgres:@localhost:5432/postgres",
    connect_args={'options': '-csearch_path=test'})

Base.metadata.create_all(engine)