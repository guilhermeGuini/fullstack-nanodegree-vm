from flask import Flask, json, request, redirect, render_template, url_for, flash, jsonify

from db.database_setup import Restaurant, MenuItem
from db.connect import Connection

conn = Connection()
session = conn.connect()
app = Flask(__name__)

@app.route('/')
@app.route('/restaurants/')
def restaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurant.html', restaurants = restaurants)

@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return render_template('menu.html', restaurant=restaurant, items = items)

@app.route('/restaurants/<int:restaurant_id>/menu/create', methods=['GET', 'POST'])
def createMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()

    if request.method == 'GET':
        return render_template('menu-item.html', restaurant=restaurant)

    newMenuItem = MenuItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], course = request.form['course'], restaurant = restaurant)
    session.add(newMenuItem)
    session.commit()
    flash('new menu item created!')

    return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    menuitem = session.query(MenuItem).filter_by(restaurant_id = restaurant.id, id = menu_id).one()

    if request.method == 'GET':
        return render_template('menu-item-edit.html', restaurant = restaurant, menuitem = menuitem)

    menuitem.name = request.form['name']
    menuitem.course = request.form['course']
    menuitem.description = request.form['description']
    menuitem.price = request.form['price']

    session.add(menuitem)
    session.commit()
    flash('menu item edited!')

    return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    menuitem = session.query(MenuItem).filter_by(restaurant_id = restaurant.id, id = menu_id).one()

    if request.method == 'GET':
        return render_template('menu-item-delete.html', restaurant = restaurant, menuitem = menuitem)

    session.delete(menuitem)
    session.commit()
    flash('menu item deleted!')

    return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def findByRestaurantMenuJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(MenuItem = item.serialize)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)