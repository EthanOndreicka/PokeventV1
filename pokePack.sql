CREATE TABLE cards IF NOT EXISTS(
    card_id INT AUTO_INCREMENT PRIMARY KEY,
    card_name VARCHAR(100) NOT NULL,
    card_image VARCHAR(255) NOT NULL,
    card_set VARCHAR(100) NOT NULL,
    card_rarity VARCHAR(50) NOT NULL,
    card_value INT NOT NULL,
    pack_id INT,
    FOREIGN KEY (pack_id) REFERENCES all_packs(pack_id)
);

CREATE TABLE all_packs IF NOT EXISTS(
    pack_id INT AUTO_INCREMENT PRIMARY KEY,
    pack_name VARCHAR(100) NOT NULL,
    pack_description TEXT,
    pack_release_date DATE,
    pack_price DECIMAL(10, 2) NOT NULL,
    card_pack_table_name VARCHAR(100) NOT NULL
);

CREATE TABLE card_pack IF NOT EXISTS (
    card_pack_id INT AUTO_INCREMENT PRIMARY KEY,
    pack_id INT NOT NULL,
    card_id INT NOT NULL,
    card_rarity VARCHAR(50) NOT NULL,
    card_image VARCHAR(255) NOT NULL,
    card_value INT NOT NULL,
    FOREIGN KEY (pack_id) REFERENCES all_packs(pack_id),
    FOREIGN KEY (card_id) REFERENCES cards(card_id)
);

-- Inserting cards with corresponding pack_id
INSERT INTO cards (card_name, card_image, card_set, card_rarity, card_value, pack_id)
VALUES ('Card A', 'image1.jpg', 'Set A', 'Rare', 10, 1),
       ('Card B', 'image2.jpg', 'Set A', 'Common', 5, 1),
       ('Card C', 'image3.jpg', 'Set B', 'Legendary', 20, 2);
