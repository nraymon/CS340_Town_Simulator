from flask import Flask, render_template
from flask import request, redirect
from db_connector.db_connector import connect_to_database, execute_query
import re

app = Flask(__name__)

# home
@app.route('/', methods=['GET'])
def home():
    print("fetching home")
    db_connection = connect_to_database()

    #query = "SELECT tg.name, s.shopName, s.shopkeep FROM TradeGoods tg LEFT JOIN Inventories i ON tg.id = i.goodId LEFT JOIN Shops s ON i.shopId = s.id WHERE s.shopName = 'Gnome Depot';"
    query = "SELECT s.shopName, s.id FROM Shops s;"
    snames = execute_query(db_connection, query).fetchall()
    print(snames)
    return render_template('home.html', shops=snames)

# npc
@app.route('/npc', methods=['GET'])
def npc():
    return render_template('npc.html')

@app.route('/edit/createTradeGood', methods=['POST'])
def createTradeGood():
    db_connection = connect_to_database()
    name = request.form["name"]
    price = request.form["price"]
    quantity = request.form["quantity"]
    description = request.form["description"]
    weight = request.form["weight"]
    query = "INSERT INTO TradeGoods (name, value, quantity, description, weight) VALUES ('%s', '%d', '%d', '%s', '%d');" % (name, int(price), int(quantity), description, int(weight))
    print(query)
    execute_query(db_connection, query).fetchall()
    return redirect("/edit", code=200)

# deletes a tradegood from runswick entirely
@app.route('/edit/deleteTradeGood/<id>', methods=['POST'])
def deleteTradeGood(id):
    db_connection = connect_to_database()
    # query to delete trade good from shop inventories
    query = "DELETE FROM Inventories WHERE goodId = '%d';" % (int(id))
    execute_query(db_connection, query)
    # query to delete trade good itself
    query = "DELETE FROM TradeGoods WHERE id = '%d';" % (int(id))
    execute_query(db_connection, query)
    # get shops for drop down
    query = "SELECT shopName, shopkeep, shopDescription, id FROM Shops;"
    shops = execute_query(db_connection, query).fetchall()
    # get all trade goods for table
    query = "SELECT name, value, quantity, description, weight, id FROM TradeGoods"
    tradeGoods = execute_query(db_connection, query).fetchall()
    # render template with updated shop inventory
    return render_template('edit.html', shops=shops, tradeGoods=tradeGoods)


# edit shop inventory
# handles rendering the edit page with basic data + shop inventory table data for editing
@app.route('/edit/shopInventory', methods=['POST'])
def editShopInventory():
    db_connection = connect_to_database()
    if request.method == 'POST':
        # get shop names
        sname = request.form["sname"]
        fsname = sname.replace("'", "\\'")
        query = "SELECT shopName, shopkeep, shopDescription, id FROM Shops;"
        shops = execute_query(db_connection, query).fetchall()
        # get inventory for selected shop
        query = "SELECT tg.name, tg.value, tg.quantity, tg.description, tg.weight, tg.id FROM TradeGoods tg LEFT JOIN Inventories i ON tg.id = i.goodId LEFT JOIN Shops s ON i.shopId = s.id WHERE s.shopName = '%s';" % (fsname)
        shopInv = execute_query(db_connection, query).fetchall()
        # render template with shop inventory
        return render_template('edit.html', shops=shops, shopInv=shopInv)


# basic edit screen rendering
@app.route('/edit', methods=['POST', 'GET'])
def edit():
    print("edit")
    db_connection = connect_to_database()
    if request.method == 'GET':
        # get shop names for dropdown
        query = "SELECT shopName, shopkeep, shopDescription, id FROM Shops;"
        shops = execute_query(db_connection, query).fetchall()

        # get all trade goods for table
        query = "SELECT name, value, quantity, description, weight, id FROM TradeGoods"
        tradeGoods = execute_query(db_connection, query).fetchall()
        # render with dropdown data
        return render_template('edit.html', shops=shops, tradeGoods=tradeGoods)


# shops - edited by ryan to display info from id rather than selecting from drop down so we can direct users to individual shop pages
@app.route('/shop/<id>', methods=['POST', 'GET'])
def shop(id):
    print("fetching things")
    db_connection = connect_to_database()
    query = "SELECT shopName, shopkeep, shopDescription, id FROM Shops WHERE id = '%d';" % (int(id))
    shopInfo = execute_query(db_connection, query).fetchall()
    print(shopInfo)
    query = "SELECT tg.name, tg.value, tg.quantity, tg.description, tg.weight FROM TradeGoods tg LEFT JOIN Inventories i ON tg.id = i.goodId LEFT JOIN Shops s ON i.shopId = s.id WHERE s.id = '%d';" % (int(id))
    # data = (sname)
    inv = execute_query(db_connection, query).fetchall()
    print(inv)
    return render_template('shop.html', name=shopInfo[0][0], inv=inv)


# Nathans orignial shop page. I've been using this code for a lot of the edit screen stuff
# @townsim.route('/shop', methods=['POST', 'GET'])
# def shop():
#     print("fetching things")
#     db_connection = connect_to_database()

#     if request.method == 'GET':
#         #query = "SELECT tg.name, s.shopName, s.shopkeep FROM TradeGoods tg LEFT JOIN Inventories i ON tg.id = i.goodId LEFT JOIN Shops s ON i.shopId = s.id WHERE s.shopName = 'Gnome Depot';"
#         query = "SELECT s.shopName FROM Shops s;"
#         snames = execute_query(db_connection, query).fetchall()
#         print(snames)
#         return render_template('shop.html', rows=snames)

#     if request.method == 'POST':
#         sname = request.form["sname"]
#         # print(sname)
#         # sname = re.escape(sname)
#         fsname = sname.replace("'", "\\'")
#         print(sname)
#         query = "SELECT s.shopName FROM Shops s;"
#         snames = execute_query(db_connection, query).fetchall()
#         query = "SELECT tg.name, tg.value, tg.quantity, tg.description, tg.weight FROM TradeGoods tg LEFT JOIN Inventories i ON tg.id = i.goodId LEFT JOIN Shops s ON i.shopId = s.id WHERE s.shopName = '%s';" % (fsname)
#         # data = (sname)
#         inv = execute_query(db_connection, query).fetchall()
#         print(inv)
#         return render_template('shop.html', rows=snames, name=sname, inv=inv)
