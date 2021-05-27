-- User --

INSERT INTO users (
    person_username,
    person_password, 
    person_email
)
VALUES 
(
    'Marega',
    'Maregod', 
    'marega@god.kekw'
),
(
    'Pedro Mitalves',
    'PoteDouro',
    'seradesta@might.actually'
);


-- Administrator --

INSERT INTO administrator (
    person_username, 
    person_password, 
    person_email
)
VALUES 
(
    'admin',
    'admin', 
    'admin@admin.admin'
);


-- Auction --

INSERT INTO auction (
    item,
    min_price,
    end_date,
    administrator_person_id
)
VALUES 
(12344, 32.3, TIMESTAMP '2021-06-12 04:05:06', 1),
(420, 4.20, TIMESTAMP '2021-04-20 04:20:00', 1);
(123, 123.4, TIMESTAMP '2021-01-23 01:23:45', 2),


-- Information --

INSERT INTO information (
    title,
    description,
    auction_id
)
VALUES 
(
    'Lorem Ipsium', 
    'Solumn Dolorem', 
    1
);