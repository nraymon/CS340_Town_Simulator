from flask import Flask, render_template
from flask import request, redirect
from db_connector.db_connector import connect_to_database, execute_query
import re

app = Flask(__name__)
app.static_folder = 'static'

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
    return redirect("/edit", code=302)

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

@app.route('/deleteTradeGoodFromShop/<id>/<name>', methods=['POST'])
def removeGoodFromShop(id, name):
    db_connection = connect_to_database()
    print(id)
    print(name)

    fsname = name.replace("'", "\\'")

    query = "SELECT id FROM Shops WHERE shopName = '%s';" % (fsname)
    sname = execute_query(db_connection, query).fetchall()
    shopId = sname[0][0]

    print("GOT SHOP ID")

    query = "DELETE FROM Inventories WHERE goodId = '%s' AND shopId = '%s';" % (id, shopId)
    resp = execute_query(db_connection, query).fetchall()

    print("DELETED")
    
    # get inventory for selected shop
    query = "SELECT tg.name, tg.value, tg.quantity, tg.description, tg.weight, tg.id FROM TradeGoods tg LEFT JOIN Inventories i ON tg.id = i.goodId LEFT JOIN Shops s ON i.shopId = s.id WHERE s.id = '%s';" % (shopId)
    shopInv = execute_query(db_connection, query).fetchall()

    # get all shops
    query = "SELECT shopName, shopkeep, shopDescription, id FROM Shops;"
    shops = execute_query(db_connection, query).fetchall()

    # get all trade goods for dropdown
    query = "SELECT name, value, quantity, description, weight, id FROM TradeGoods"
    tradeGoods = execute_query(db_connection, query).fetchall()

    # render template with shop inventory
    return render_template('editShopInventory.html', shops=shops, shopInv=shopInv, tradeGoods=tradeGoods, name=name)


# edit shop inventory
# handles rendering the edit page with basic data + shop inventory table data for editing
# @app.route('/edit/shopInventory', methods=['POST'])
# def editShopInventory():
#     db_connection = connect_to_database()
#     if request.method == 'POST':

#         query = "SELECT shopName, shopkeep, shopDescription, id FROM Shops;"
#         shops = execute_query(db_connection, query).fetchall()

#         # # get all trade goods for table
#         # query = "SELECT name, value, quantity, description, weight, id FROM TradeGoods"
#         # tradeGoods = execute_query(db_connection, query).fetchall()

#         # query = "SELECT name, greeting, id FROM NPCs"
#         # npcs = execute_query(db_connection, query).fetchall()

#         # query = "SELECT id, name, description, reward FROM Quests;"
#         # quests = execute_query(db_connection, query).fetchall()

#         # # render with dropdown data
#         # return render_template('edit.html', shops=shops, tradeGoods=tradeGoods, npcs=npcs, quests = quests)

#         # get shop names
#         sname = request.form["sname"]
#         fsname = sname.replace("'", "\\'")

#         # get inventory for selected shop
#         query = "SELECT tg.name, tg.value, tg.quantity, tg.description, tg.weight, tg.id FROM TradeGoods tg LEFT JOIN Inventories i ON tg.id = i.goodId LEFT JOIN Shops s ON i.shopId = s.id WHERE s.shopName = '%s';" % (fsname)
#         shopInv = execute_query(db_connection, query).fetchall()
        
#         # render template with shop inventory
#         return render_template('edit.html', shops=shops, shopInv=shopInv)


@app.route('/editShopInventory', methods=['POST', 'GET'])
def editShopInventory():
    db_connection = connect_to_database()
    query = "SELECT shopName, shopkeep, shopDescription, id FROM Shops;"
    shops = execute_query(db_connection, query).fetchall()
    # get all trade goods for dropdown
    query = "SELECT name, value, quantity, description, weight, id FROM TradeGoods"
    tradeGoods = execute_query(db_connection, query).fetchall()

    if request.method == 'GET':
        print("GETTING ************************************")
        sname = shops[0][0]
        print(sname)
        fsname = sname.replace("'", "\\'")

        # get inventory for selected shop
        query = "SELECT tg.name, tg.value, tg.quantity, tg.description, tg.weight, tg.id FROM TradeGoods tg LEFT JOIN Inventories i ON tg.id = i.goodId LEFT JOIN Shops s ON i.shopId = s.id WHERE s.shopName = '%s';" % (fsname)
        shopInv = execute_query(db_connection, query).fetchall()
        
        # render template with shop inventory
        return render_template('editShopInventory.html', shops=shops, shopInv=shopInv, tradeGoods=tradeGoods, name=sname)

    elif request.method == 'POST':
        print("POSTING ************************************")
        # # get all trade goods for table
        # query = "SELECT name, value, quantity, description, weight, id FROM TradeGoods"
        # tradeGoods = execute_query(db_connection, query).fetchall()

        # query = "SELECT name, greeting, id FROM NPCs"
        # npcs = execute_query(db_connection, query).fetchall()

        # query = "SELECT id, name, description, reward FROM Quests;"
        # quests = execute_query(db_connection, query).fetchall()

        # # render with dropdown data
        # return render_template('edit.html', shops=shops, tradeGoods=tradeGoods, npcs=npcs, quests = quests)

        # get shop names
        sname = request.form["sname"]
        fsname = sname.replace("'", "\\'")
        print(sname)

        # get inventory for selected shop
        query = "SELECT tg.name, tg.value, tg.quantity, tg.description, tg.weight, tg.id FROM TradeGoods tg LEFT JOIN Inventories i ON tg.id = i.goodId LEFT JOIN Shops s ON i.shopId = s.id WHERE s.shopName = '%s';" % (fsname)
        shopInv = execute_query(db_connection, query).fetchall()
        
        # render template with shop inventory
        return render_template('editShopInventory.html', shops=shops, shopInv=shopInv, tradeGoods=tradeGoods, name=sname)


#add npc to db
@app.route('/edit/addNPC', methods=['POST'])
def editAddNPC():
    db_connection = connect_to_database()

    # assigns the information received from the webpage
    npcName = request.form["npcName"]
    greet = request.form["greeting"]
    place = request.form["foundin"]

    # builds the query and adds the new npc with the information gathered from the webpage
    query = "INSERT INTO NPCs (name, greeting) VALUES ('%s', '%s');" % (npcName, greet)
    execute_query(db_connection, query)
    return redirect("/edit", code=302)


# add quests to the database
@app.route('/edit/addQuest', methods=['POST'])
def editAddQuest():
    db_connection = connect_to_database()

    # assigns the information received from the webpage
    qName = request.form["questName"]
    qDesc = request.form["description"]
    qRew = request.form["reward"]

    # builds the query to insert the desired information from the webpage
    query = "INSERT INTO Quests (name, description, reward) VALUES ('%s', '%s', '%s')" % (qName, qDesc, qRew)
    execute_query(db_connection, query)
    return redirect("/edit", code=302)


# allows the user to edit the values of a trade good
@app.route('/edit/editTradeGood', methods=['POST'])
def editTradeGood():
    db_connection = connect_to_database()

    if request.method == 'POST':
        good = request.form["good"]
        price = request.form["price"]
        quant = request.form["quant"]
        desc = request.form["desc"]
        weight = request.form["weight"]
        iden = request.form["id"]

        query = "UPDATE TradeGoods SET name = '%s', value = '%s', quantity = '%s', description = '%s', weight = '%s' WHERE id = '%s'" % (good, price, quant, desc, weight, iden)

        execute_query(db_connection, query)
        return redirect("/edit", code=302)


# this adds a TradeGood item to a Shop's inventory
@app.route('/addTradeGoodToShop', methods=['POST'])
def addTradeGoodToShop():
    print("ADDING TRADE GOOD")
    db_connection = connect_to_database()

    if request.method == 'POST':

        item = request.form["itemToShop"]
        shop = request.form["shopToItem"]

        print(item)
        print(shop)

        query = "INSERT INTO Inventories (goodId, shopId) VALUES ('%s', '%s');" % (item, shop)
        execute_query(db_connection, query)

        # get inventory for selected shop
        query = "SELECT tg.name, tg.value, tg.quantity, tg.description, tg.weight, tg.id FROM TradeGoods tg LEFT JOIN Inventories i ON tg.id = i.goodId LEFT JOIN Shops s ON i.shopId = s.id WHERE s.id = '%s';" % (shop)
        shopInv = execute_query(db_connection, query).fetchall()
        
        # get specific shop name
        query = "SELECT shopName id FROM Shops WHERE id = '%s';" % (shop)
        sname = execute_query(db_connection, query).fetchall()
        print(sname)
        shopName = sname[0][0]
        print(shopName)

        # get all shops
        query = "SELECT shopName, shopkeep, shopDescription, id FROM Shops;"
        shops = execute_query(db_connection, query).fetchall()

        # get all trade goods for dropdown
        query = "SELECT name, value, quantity, description, weight, id FROM TradeGoods"
        tradeGoods = execute_query(db_connection, query).fetchall()

        # render template with shop inventory
        return render_template('editShopInventory.html', shops=shops, shopInv=shopInv, tradeGoods=tradeGoods, name=shopName)


# adds a quest to an NPC
@app.route('/edit/addQuestToNpc', methods=['POST'])
def addQuestToNpc():
    db_connection = connect_to_database()

    if request.method == 'POST':

        quest = request.form["questToNpc"]
        npc = request.form["npcToQuest"]

        query = "INSERT INTO NpcQuests (npcId, questId) VALUES ('%s', '%s');" % (npc, quest)
        execute_query(db_connection, query)

        return redirect("/edit", code=302)


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

        query = "SELECT name, greeting, id FROM NPCs"
        npcs = execute_query(db_connection, query).fetchall()

        query = "SELECT id, name, description, reward FROM Quests;"
        quests = execute_query(db_connection, query).fetchall()

        # render with dropdown data
        return render_template('edit.html', shops=shops, tradeGoods=tradeGoods, npcs=npcs, quests = quests)


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
# @app.route('/editShopInventory', methods=['POST', 'GET'])
# def editShopInventory():
#     print("fetching things")
#     db_connection = connect_to_database()

#     if request.method == 'GET':
#         #query = "SELECT tg.name, s.shopName, s.shopkeep FROM TradeGoods tg LEFT JOIN Inventories i ON tg.id = i.goodId LEFT JOIN Shops s ON i.shopId = s.id WHERE s.shopName = 'Gnome Depot';"
#         query = "SELECT s.shopName FROM Shops s;"
#         snames = execute_query(db_connection, query).fetchall()
#         print(snames)
#         return render_template('editShopInventory.html', rows=snames)

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
#         return render_template('editShopInventory.html', shops=snames, name=sname, shopInv=inv)
