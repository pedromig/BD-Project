-- User --
INSERT INTO person (username, password, email)
VALUES (
        -- id: 1
        'admin',
        'admin',
        'admin@admin.admin'
    ),
    (
        -- id: 2
        'Marega',
        'Maregod',
        'marega@god.kekw'
    ),
    (
        -- id: 3
        'Pedro Mitalves',
        'PoteDouro',
        'seradesta@might.actually'
    );
-- Administrator --
INSERT INTO administrator (person_id)
VALUES (1);
-- User --
INSERT INTO users (person_id)
VALUES (2),
    (3);
-- Auction --
INSERT INTO auction (
        item,
        min_price,
        end_date,
        person_id
    )
VALUES (12344, 32.3, TIMESTAMP '2021-06-12 04:05:06', 2),
    (420, 4.20, TIMESTAMP '2021-04-20 04:20:00', 2),
    (123, 123.4, TIMESTAMP '2021-01-23 01:23:45', 3);
-- Information --
INSERT INTO information (title, description, auction_id, time_date)
VALUES (
        'Lorem Ipsium',
        'Solumn Dolorem',
        1,
        TIMESTAMP '2021-01-23 01:23:45'
    );
-- Licitations
INSERT INTO licitation (price, auction_id, person_id) 
VALUES 
    (100, 1, 2),
    (101, 1, 2),
    (102, 1, 3);