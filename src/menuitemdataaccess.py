from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, MenuItem

engine = create_engine('sqlite:///restaurant.db', echo=True)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def get_menu_items_by_restaurant_id(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return items


def get_menu_item_by_id(menu_id):
    menu_item = session.query(MenuItem).filter_by(id=menu_id).one()
    return menu_item


def persist_menu_item_for_restaurant(menu_item):
    session.add(menu_item)
    session.commit()

def delete_menu_item(menu_item):
    session.delete(menu_item)
    session.commit()
