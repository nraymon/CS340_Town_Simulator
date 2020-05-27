DROP TABLE IF EXISTS Shops;
CREATE TABLE Shops (
	id int(11) NOT NULL UNIQUE AUTO_INCREMENT,
	shopkeep varchar(255) NOT NULL,
	shopkeepId int(11) NOT NULL,
	shopName varchar(255) NOT NULL,
	shopDescription varchar(255) NOT NULL,
	PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS TradeGoods;
CREATE TABLE TradeGoods (
	id int(11) NOT NULL UNIQUE AUTO_INCREMENT,
	name varchar(255) NOT NULL,
	value int(11) NOT NULL,
	quantity int(11) NOT NULL,
	description varchar(255) NOT NULL,
	weight int(11) NOT NULL,
	PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS Locations;
CREATE TABLE Locations (
	id int(11) NOT NULL UNIQUE AUTO_INCREMENT,
	npcId int(11) NOT NULL,
	shopid int(11) NOT NULL,
	PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS Inventories;
CREATE TABLE Inventories (
	id int(11) NOT NULL UNIQUE AUTO_INCREMENT,
	goodId int(11) NOT NULL,
	shopId int(11) NOT NULL,
	PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS NPCs;
CREATE TABLE NPCs (
	id int(11) NOT NULL UNIQUE AUTO_INCREMENT,
	name varchar(255) NOT NULL,
	greeting varchar(255) NOT NULL,
	PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS Quests;
CREATE TABLE Quests (
	id int(11) NOT NULL UNIQUE AUTO_INCREMENT,
	name varchar(255) NOT NULL,
	description varchar(255) NOT NULL,
	reward varchar(255) NOT NULL,
	PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS NpcQuests;
CREATE TABLE NpcQuests (
	id int(11) NOT NULL UNIQUE AUTO_INCREMENT,
	npcId int(11) NOT NULL,
	questId int(11) NOT NULL,
	PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

ALTER TABLE Shops
ADD FOREIGN KEY (shopkeepId) REFERENCES NPCs (id) ON DELETE CASCADE;

ALTER TABLE Locations
ADD FOREIGN KEY (npcId) REFERENCES NPCs(id) ON DELETE CASCADE;
ALTER TABLE Locations
ADD FOREIGN KEY (shopId) REFERENCES Shops(id) ON DELETE CASCADE;

ALTER TABLE Inventories
ADD FOREIGN KEY (goodId) REFERENCES TradeGoods(id) ON DELETE CASCADE;
ALTER TABLE Inventories
ADD FOREIGN KEY (shopId) REFERENCES Shops(id) ON DELETE CASCADE;

ALTER TABLE NpcQuests
ADD FOREIGN KEY (npcId) REFERENCES NPCs(id) ON DELETE CASCADE;
ALTER TABLE NpcQuests
ADD FOREIGN KEY (questId) REFERENCES Quests(id) ON DELETE CASCADE;

INSERT INTO NPCs (name, greeting) VALUES("Jacob the tanner", "Hello there, what can I do for you? I'd really rather see you around my shop why don't you come by sometime?");
INSERT INTO NPCs (name, greeting) VALUES("Nezeim Bhammein", "Hello traveler, good to see new faces around the town every now and then.");
INSERT INTO NPCs (name, greeting) VALUES("Althea the sorceror", "Hmm, perhaps I can find a use for a fighter like you..");
INSERT INTO NPCs (name, greeting) VALUES("Pa Gnomio", "Well hello there! This is Gnome Depot what can Pa Gnomio do for you?");
INSERT INTO NPCs (name, greeting) VALUES("Balthar", "This is Balthar's Blunts and Blades, but we got all kinds a' weapons. What might ye be lookin for?");
INSERT INTO NPCs (name, greeting) VALUES("Dolmyr", "Welcome to Hammer Time, Stop! by if you're looking for armor or something made to order!");

INSERT INTO  Shops (shopkeep, shopkeepId, shopName, shopDescription) VALUES("Pa Gnomio", 4, "Gnome Depot", "Raw material and ore");
INSERT INTO  Shops (shopkeep, shopkeepId, shopName, shopDescription) VALUES("Balthar", 5, "Balthar's Blunts and Blades", "Armory");
INSERT INTO  Shops (shopkeep, shopkeepId, shopName, shopDescription) VALUES("Dolmyr", 6, "Hammer Time", "Forge, Blacksmith");

INSERT INTO TradeGoods (name, value, quantity, description, weight) VALUES("Rope", 5, 3, "length of 50 feet", .2);
INSERT INTO TradeGoods (name, value, quantity, description, weight) VALUES("Battleaxe", 10, 10, "Slashing Damage", 4);
INSERT INTO TradeGoods (name, value, quantity, description, weight) VALUES("Bedroll", 1, 2, "used for to long rest", 7);

INSERT INTO Inventories (goodId, shopId) VALUES (1, 1);
INSERT INTO Inventories (goodId, shopId) VALUES (2, 1);
INSERT INTO Inventories (goodId, shopId) VALUES (3, 2);

INSERT INTO Locations (npcId, shopId) VALUES (4, 1);
INSERT INTO Locations (npcId, shopId) VALUES (5, 2);
INSERT INTO Locations (npcId, shopId) VALUES (6, 3);

INSERT INTO Quests (name, description, reward) VALUES("Hunt local poachers", "A band of poachers have been killling the local wildlife without regard for the law. Hunt them down and you'll receive a might reward.", "Anything you can loot from their hideout plus 150 gold pices.");

INSERT INTO NpcQuests (npcId, questId) VALUES (1, 1);