from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base

engine = create_engine('sqlite:///restaurant.db', echo=True)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def get_restaurants():
    items = session.query(Restaurant).all()
    return items


def get_restaurant_by_id(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return restaurant


def create_restaurant(new_restaurant):
    restaurant = Restaurant(name=new_restaurant)
    session.add(restaurant)
    session.commit()


def update_restaurant(restaurant):
    session.add(restaurant)
    session.commit()


def delete_restaurant(restaurant):
    session.delete(restaurant)
    session.commit()
