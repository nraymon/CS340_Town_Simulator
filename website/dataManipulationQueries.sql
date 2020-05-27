-- The ':' character is used as a prefix in the below queries to denote a variable provided by backend code
-- I counted variables as any dynamic value that is used in any query including both user input and query parameters like shop and npc ids.

-- Every table should be used in at least one SELECT query.
-- select all shops
SELECT shopName FROM Shops;
-- select shop by shop id
SELECT shopName, shopkeep, shopDescription, id FROM Shops
WHERE id = :shopId;
-- select shop inventory from trade goods by shop id
SELECT G.name, G.description, G.value, G.quantity, G.weight, G.id FROM Shops S
INNER JOIN Inventories I ON S.id = I.shopId
INNER JOIN TradeGoods G ON G.id = I.goodId
WHERE S.id = :shopId;
-- select npc by id
SELECT N.name, N.greeting, N.id FROM NPCs N
WHERE id = :npcId;
-- select npc quests by npc id
SELECT Q.name, Q.description, Q.reward FROM NPCs N
INNER JOIN NpcQuests NQ ON N.id = NQ.npcId
INNER JOIN Quests Q ON Q.id = NQ.questId
WHERE N.id = :npcId;
-- select npcs at a shop by shop id
SELECT N.name FROM Shops S
INNER JOIN Locations L ON S.id = L.shopId
INNER JOIN NPCs N ON N.id = L.npcId
WHERE S.id = :shopId;


-- It should be possible to INSERT entries into every table individually.
-- insert new shop
INSERT INTO Shops (shopkeep, shopkeepId, shopName, shopDescription) VALUES(:shopkeepNameInput, :shopkeep_id_from_dropdown, :shopNameInput, :shopDescriptionInput);
-- insert new trade good
INSERT INTO TradeGoods (name, value, quantity, description) VALUES(:good_name_input, :good_value_input, :good_quantity_input, :good_description_input);
-- insert new quest
INSERT INTO Quests (name, description, reward) VALUES(:name_input, :description_input, :reward_input);
-- insert new npc
INSERT INTO NPCs (name, greeting) VALUES(:name_input, :greeting_input);


-- DELETE for at least one many-to-many relationship.
-- delete trade good from specific shop
DELETE FROM Inventories WHERE goodId = :good_id_from_UI_delete_button AND shopId = :shop_id_from_dropdown;
-- delete trade good from all shops
DELETE FROM Inventories WHERE goodId = :good_id_from_UI_delete_button;

-- You need to include one DELETE and one UPDATE function
-- delete trade good, will be used in conjunction with deleting the good from many-to-many relationship (need to add this to the UI, we only have deleting a good from a shop not actually deleting the good entirely)
DELETE FROM TradeGoods WHERE id = :good_id_from_UI_delete_button;
-- edit trade good
UPDATE TradeGoods SET name = :good_name_edit_input, value = :good_value_edit_input, quantity = :good_quantity_edit_input, description = :good_description_edit_input WHERE id= :good_id_from_UI_edit_button;


-- INSERT functionality for all relationships
-- add npc to shop
INSERT INTO Locations (npcId, shopId) VALUES (:npc_id_from_dropdown_input, :shop_id_from_dropdown_input)
-- add trade good to shop
INSERT INTO Inventories (goodId, shopId) VALUES (:good_id_from_dropdown_input, :shop_id_from_dropdown_input)
-- add quest to npc
INSERT INTO NpcQuests (npcId, questId) VALUES (:npc_id_from_dropdown_input, :quest_id_from_dropdown_input)
