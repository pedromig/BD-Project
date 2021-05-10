INSERT INTO users(person_username, person_password, person_email)
VALUES ('Marega', 'Maregod', 'marega@god.kekw');
INSERT INTO users(person_username, person_password, person_email)
VALUES (
        'Pedro Mitalves',
        'PoteDouro',
        'seradesta@might.actually'
    );
INSERT INTO administrator(person_username, person_password, person_email)
VALUES ('admin', 'admin', 'admin@admin.admin');
INSERT INTO auction(
        item,
        min_price,
        end_date,
        administrator_person_id
    )
VALUES (12344, 32.3, TIMESTAMP '2021-06-12 04:05:06', 1);
INSERT INTO information(title, description, auction_id)
values ('Lorem Ipsium', 'Solumn Dolorem', 1);