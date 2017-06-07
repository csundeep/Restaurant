from flask import Flask, render_template, redirect, request, url_for

from database_setup import MenuItem
from menuitemdataaccess import get_menu_items_by_restaurant_id, persist_menu_item_for_restaurant, get_menu_item_by_id, \
    delete_menu_item
from restaurantdataaccess import create_restaurant, get_restaurant_by_id, get_restaurants, update_restaurant, \
    delete_restaurant

app = Flask(__name__)


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    restaurants = get_restaurants()
    return render_template("restaurant/restaurant.html", restaurants=restaurants)


@app.route('/restaurants/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        name = request.form['name']
        create_restaurant(name)
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('restaurant/newrestaurant.html')


@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    if request.method == 'POST':
        restaurant = get_restaurant_by_id(restaurant_id)
        if restaurant:
            restaurant.name = request.form['newRestaurantName']
            update_restaurant(restaurant)
        return redirect(url_for('showRestaurants'))
    else:
        restaurant = get_restaurant_by_id(restaurant_id)
        return render_template('restaurant/editrestaurant.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    if request.method == 'POST':
        restaurant = get_restaurant_by_id(restaurant_id)
        if restaurant:
            delete_restaurant(restaurant)
        return redirect(url_for('showRestaurants'))
    else:
        restaurant = get_restaurant_by_id(restaurant_id)
        return render_template('restaurant/deleterestaurant.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = get_restaurant_by_id(restaurant_id)
    items = get_menu_items_by_restaurant_id(restaurant_id)
    return render_template('menu/menu.html', restaurant=restaurant, items=items)


@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        try:
            newItem = MenuItem(
                name=request.form['name'], restaurant_id=restaurant_id)
            persist_menu_item_for_restaurant(newItem)
        except Exception as e:
            print(e)
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('menu/newmenuitem.html', restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        try:
            menuitem = get_menu_item_by_id(menu_id)
            menuitem.name = request.form['newMenuItemName'];
            persist_menu_item_for_restaurant(menuitem)
        except Exception as e:
            print(e)
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        menuitem = get_menu_item_by_id(menu_id)
        restaurant = get_restaurant_by_id(restaurant_id)
        return render_template('menu/editmenuitem.html', menuitem=menuitem, restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        try:
            menuitem = get_menu_item_by_id(menu_id)
            delete_menu_item(menuitem)
        except Exception as e:
            print(e)
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        menuitem = get_menu_item_by_id(menu_id)
        restaurant = get_restaurant_by_id(restaurant_id)
        return render_template('menu/deletemenuitem.html', restaurant_id=restaurant_id, menuitem=menuitem,
                               restaurant=restaurant)


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=5000)
