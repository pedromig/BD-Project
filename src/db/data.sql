
------------------------------------------------- IMPORTANT RULES -------------------------------------------------------

-- If you add a row to the auction table be sure to add the corresponding row to the information table (and vice-versa)
-- If you add a row to the person table be sure to add the corresponding row to the user or adminstrator tables (and vice-versa)


-------------------------------------------------  People ----------------------------------------------------------

INSERT INTO person (username, password, email) VALUES ('admin', 'admin', 'admin@gmail.com');
INSERT INTO person (username, password, email) VALUES ('dalliband0', 'bYvrJlzRpGMJ', 'tdelgardo0@de.vu');
INSERT INTO person (username, password, email) VALUES ('cmonshall1', '2PGgNoCQO', 'dfrizzell1@elegantthemes.com');
INSERT INTO person (username, password, email) VALUES ('afoulks2', 'KELU6iJEG9', 'qrodnight2@chronoengine.com');
INSERT INTO person (username, password, email) VALUES ('hcudbertson3', 'NduT80reK', 'pstert3@yandex.ru');
INSERT INTO person (username, password, email) VALUES ('acowndley4', 'PWlTS6B', 'gbromhead4@51.la');
INSERT INTO person (username, password, email) VALUES ('ppolo5', '9lPQiHBL', 'cshyram5@cnbc.com');
INSERT INTO person (username, password, email) VALUES ('chamerton6', 'wU5IoYba', 'arupel6@thetimes.co.uk');
INSERT INTO person (username, password, email) VALUES ('wburehill7', 'hlqBOMmN24', 'adahler7@last.fm');
INSERT INTO person (username, password, email) VALUES ('emonelli8', 'zBFu2MdehyJ', 'xpetticrew8@arizona.edu');
INSERT INTO person (username, password, email) VALUES ('jgoldring9', 'imPIfk7x', 'ubuer9@japanpost.jp');
INSERT INTO person (username, password, email) VALUES ('npavela', 'yxdSfle1', 'thaira@miibeian.gov.cn');
INSERT INTO person (username, password, email) VALUES ('dhackingeb', 'hzG72P66CegK', 'nmillikenb@miitbeian.gov.cn');
INSERT INTO person (username, password, email) VALUES ('kpelchatc', 'GFcODYRR', 'hbaalhamc@reverbnation.com');
INSERT INTO person (username, password, email) VALUES ('ballanbyd', 'RDeG8m17Rzc', 'nlittled@thetimes.co.uk');
INSERT INTO person (username, password, email) VALUES ('fdurdene', 'FLXKEKJABg', 'bgoodbodye@netlog.com');
INSERT INTO person (username, password, email) VALUES ('kwickettf', 'dcMfaBtlwYze', 'drodearf@cdc.gov');
INSERT INTO person (username, password, email) VALUES ('jmcinteerg', 'axt1IKzbq', 'chrinchenkog@pinterest.com');
INSERT INTO person (username, password, email) VALUES ('sshenleyh', 'dv5rzfs', 'rtrudgianh@alibaba.com');
INSERT INTO person (username, password, email) VALUES ('ofrankishi', '3G7jcEqlb', 'lhuskinsoni@linkedin.com');
INSERT INTO person (username, password, email) VALUES ('rabraminoj', 'Ak683z8BFPoL', 'sraimbauldj@unesco.org');
INSERT INTO person (username, password, email) VALUES ('loffenerk', 'Dy6uyx2q', 'ctaylourk@miitbeian.gov.cn');
INSERT INTO person (username, password, email) VALUES ('agammilll', '7gFVKcVEX', 'lgrinishinl@deviantart.com');
INSERT INTO person (username, password, email) VALUES ('cbickmorem', 'dCMQ9k4FI', 'pcritophm@parallels.com');
INSERT INTO person (username, password, email) VALUES ('trudledgen', 'FvTbzxy6', 'tfryern@blogger.com');
INSERT INTO person (username, password, email) VALUES ('mswindellso', 'L4U6onlw4b1w', 'fliveno@devhub.com');
INSERT INTO person (username, password, email) VALUES ('llarverp', 'hRfsbO', 'rrenep@baidu.com');
INSERT INTO person (username, password, email) VALUES ('cvonasekq', 'Nb3zK2fqy', 'ceckhardq@blogspot.com');
INSERT INTO person (username, password, email) VALUES ('llyptritr', '6ZFc6t3', 'tfancuttr@blogger.com');
INSERT INTO person (username, password, email) VALUES ('smackennys', 'cxMsStIzN', 'mpuseys@theatlantic.com');
INSERT INTO person (username, password, email) VALUES ('bprobettst', '5X24sXn4al', 'gmckinleyt@tumblr.com');

-------------------------------------------------  Admin ----------------------------------------------------------

INSERT INTO administrator (person_id) VALUES (1);

-------------------------------------------------  Users ----------------------------------------------------------

INSERT INTO users (person_id) VALUES (2);
INSERT INTO users (person_id) VALUES (3);
INSERT INTO users (person_id) VALUES (4);
INSERT INTO users (person_id) VALUES (5);
INSERT INTO users (person_id) VALUES (6);
INSERT INTO users (person_id) VALUES (7);
INSERT INTO users (person_id) VALUES (8);
INSERT INTO users (person_id) VALUES (9);
INSERT INTO users (person_id) VALUES (10);
INSERT INTO users (person_id) VALUES (11);
INSERT INTO users (person_id) VALUES (12);
INSERT INTO users (person_id) VALUES (13);
INSERT INTO users (person_id) VALUES (14);
INSERT INTO users (person_id) VALUES (15);
INSERT INTO users (person_id) VALUES (16);
INSERT INTO users (person_id) VALUES (17);
INSERT INTO users (person_id) VALUES (18);
INSERT INTO users (person_id) VALUES (19);
INSERT INTO users (person_id) VALUES (20);
INSERT INTO users (person_id) VALUES (21);
INSERT INTO users (person_id) VALUES (22);
INSERT INTO users (person_id) VALUES (23);
INSERT INTO users (person_id) VALUES (24);
INSERT INTO users (person_id) VALUES (25);
INSERT INTO users (person_id) VALUES (26);
INSERT INTO users (person_id) VALUES (27);
INSERT INTO users (person_id) VALUES (28);
INSERT INTO users (person_id) VALUES (29);
INSERT INTO users (person_id) VALUES (30);

-------------------------------------------------  Auctions --------------------------------------------------------

INSERT INTO auction (item, min_price, end_date, person_id) VALUES (1234, 32.3, '2021-06-12 04:05:06', 2);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (420, 4.20,  '2021-04-20 04:20:00', 2);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (123, 123.4, '2021-01-23 01:23:45', 3);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (414, 50.16, '2021-04-17 19:35:18', 16);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (132, 80.57, '2021-05-16 01:25:26', 26);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (481, 84.77, '2021-05-17 22:25:25', 27);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (156, 64.14, '2021-12-19 05:12:57', 26);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (789, 16.91, '2021-04-20 00:08:05', 22);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (617, 84.53, '2021-06-19 00:35:30', 12);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (596, 77.71, '2021-10-06 21:21:22', 10);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (91, 31.35, '2021-04-14 16:44:37', 27);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (112, 76.98, '2020-06-29 02:11:25', 19);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (258, 89.83, '2020-07-11 23:47:57', 20);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (282, 68.49, '2020-11-17 15:37:21', 2);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (374, 92.19, '2020-06-05 17:20:06', 26);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (851, 38.55, '2020-09-11 11:47:12', 21);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (997, 50.44, '2020-06-14 04:06:30', 15);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (994, 10.81, '2020-06-18 17:43:56', 11);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (604, 67.36, '2021-04-23 09:30:30', 20);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (613, 78.68, '2021-04-12 02:41:28', 16);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (125, 79.44, '2021-06-12 07:02:37', 16);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (531, 20.64, '2021-03-30 14:09:48', 13);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (778, 28.09, '2021-05-11 14:52:37', 19);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (747, 91.78, '2021-01-08 23:03:56', 29);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (492, 53.58, '2021-04-12 14:47:49', 13);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (99, 60.66, '2021-08-07 12:30:15', 5);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (760, 62.78, '2021-01-08 02:52:38', 19);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (59, 35.83, '2020-08-10 19:25:27', 20);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (542, 16.33, '2021-01-13 23:28:56', 28);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (252, 94.1, '2020-07-22 04:42:36', 10);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (80, 8.56, '2021-03-07 08:52:55', 9);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (684, 93.73, '2020-11-29 02:14:28', 15);
INSERT INTO auction (item, min_price, end_date, person_id) VALUES (429, 73.3, '2020-10-25 17:50:32', 3);


-------------------------------------------------  Information --------------------------------------------------------


INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('nulla ac', 'Pellentesque ultrices mattis odio.', 'Morbi a ipsum.', 4, '2019-03-01 05:28:23');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('at nibh', 'Duis bibendum.', 'Morbi non lectus.', 14, '2018-11-01 21:03:22');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('nulla', 'Pellentesque viverra pede ac diam.', 'Aenean auctor gravida sem.', 10, '2019-07-04 18:14:25');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('mi', 'Fusce posuere felis sed lacus.', 'Nulla facilisi.', 20, '2019-03-06 11:20:26');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('dapibus at', 'Morbi ut odio.', 'Morbi porttitor lorem id ligula.', 26, '2019-12-20 08:18:41');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('primis', 'Nulla justo.', 'Aliquam erat volutpat.', 19, '2019-08-09 17:12:26');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('felis sed', 'In congue.', 'Nunc purus.', 7, '2019-04-02 21:58:42');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('malesuada', 'Aenean auctor gravida sem.', 'Etiam justo.', 17, '2019-10-24 01:55:04');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('aliquam', 'Morbi quis tortor id nulla ultrices aliquet.', 'Cras non velit nec nisi vulputate nonummy.', 24, '2018-11-20 19:46:08');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('lacus', 'Etiam pretium iaculis justo.', 'Nunc rhoncus dui vel sem.', 30, '2019-04-08 20:50:21');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('dui', 'Etiam justo.', 'Maecenas rhoncus aliquam lacus.', 29, '2019-01-23 03:06:23');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('nibh', 'Pellentesque ultrices mattis odio.', 'Cras pellentesque volutpat dui.', 23, '2019-08-08 08:49:13');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('sem duis', 'Vivamus metus arcu, adipiscing molestie, hendrerit at, vulputate vitae, nisl.', 'Vestibulum ac est lacinia nisi venenatis tristique.', 23, '2019-01-11 17:52:53');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('in felis', 'Curabitur gravida nisi at nibh.', 'Quisque porta volutpat erat.', 14, '2019-10-27 20:52:22');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('morbi', 'Curabitur at ipsum ac tellus semper interdum.', 'Fusce consequat.', 3, '2019-06-17 00:35:21');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('lectus pellentesque', 'Aenean fermentum.', 'Nunc purus.', 26, '2019-03-02 10:51:06');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('dis parturient', 'Cras pellentesque volutpat dui.', 'In hac habitasse platea dictumst.', 6, '2019-01-01 23:23:23');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('pulvinar sed', 'Morbi sem mauris, laoreet ut, rhoncus aliquet, pulvinar sed, nisl.', 'Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Duis faucibus accumsan odio.', 24, '2019-02-11 02:42:26');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('at feugiat', 'Mauris lacinia sapien quis libero.', 'Aenean auctor gravida sem.', 2, '2019-09-01 02:26:39');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('nibh in', 'Sed ante.', 'In eleifend quam a odio.', 7, '2019-03-03 00:26:57');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('ut', 'In tempor, turpis nec euismod scelerisque, quam turpis adipiscing lorem, vitae mattis nibh ligula nec sem.', 'Morbi vel lectus in quam fringilla rhoncus.', 27, '2018-11-12 00:54:14');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('at', 'Donec semper sapien a libero.', 'Duis consequat dui nec nisi volutpat eleifend.', 15, '2019-03-30 03:56:31');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('vel augue', 'In hac habitasse platea dictumst.', 'Suspendisse potenti.', 10, '2019-08-28 04:33:15');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('nulla sed', 'Aenean fermentum.', 'Donec posuere metus vitae ipsum.', 19, '2019-02-26 09:48:08');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('sem sed', 'Proin interdum mauris non ligula pellentesque ultrices.', 'Nam congue, risus semper porta volutpat, quam pede lobortis ligula, sit amet eleifend pede libero quis orci.', 25, '2019-08-04 21:37:46');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('ac est', 'Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Donec pharetra, magna vestibulum aliquet ultrices, erat tortor sollicitudin mi, sit amet lobortis sapien sapien non mi.', 'Etiam vel augue.', 23, '2019-12-03 14:12:31');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('hac', 'Cras mi pede, malesuada in, imperdiet et, commodo vulputate, justo.', 'Nulla ut erat id mauris vulputate elementum.', 23, '2019-10-22 03:14:41');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('non mauris', 'Suspendisse ornare consequat lectus.', 'Fusce posuere felis sed lacus.', 16, '2019-03-08 15:56:27');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('mauris ullamcorper', 'Proin leo odio, porttitor id, consequat in, consequat ut, nulla.', 'Aenean auctor gravida sem.', 12, '2019-04-20 07:19:12');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('non mauris', 'Curabitur convallis.', 'Fusce consequat.', 9, '2019-01-05 00:13:42');

INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('libero', 'Mauris enim leo, rhoncus sed, vestibulum sit amet, cursus id, turpis.', 'Donec quis orci eget orci vehicula condimentum.', 1, '2021-03-30 13:57:07');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('orci pede', 'Aenean auctor gravida sem.', 'Nulla ac enim.', 2, '2020-12-23 01:54:24');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('lobortis convallis', 'Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Mauris viverra diam vitae quam.', 'Suspendisse potenti.', 3, '2020-04-14 16:20:41');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('facilisi cras', 'Nulla tempus.', 'Duis bibendum, felis sed interdum venenatis, turpis enim blandit mi, in porttitor pede justo eu massa.', 4, '2020-12-29 15:22:44');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('a', 'Cras mi pede, malesuada in, imperdiet et, commodo vulputate, justo.', 'Donec semper sapien a libero.', 5, '2020-06-22 01:29:42');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('sapien non', 'Vivamus metus arcu, adipiscing molestie, hendrerit at, vulputate vitae, nisl.', 'In hac habitasse platea dictumst.', 6, '2020-07-19 14:02:45');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('luctus nec', 'Phasellus in felis.', 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit.', 7, '2021-04-15 00:20:03');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('feugiat et', 'Nam congue, risus semper porta volutpat, quam pede lobortis ligula, sit amet eleifend pede libero quis orci.', 'Donec semper sapien a libero.', 8, '2020-06-09 14:03:14');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('quis', 'Vivamus in felis eu sapien cursus vestibulum.', 'In hac habitasse platea dictumst.', 9, '2020-10-19 00:26:59');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('mauris', 'Donec ut mauris eget massa tempor convallis.', 'In hac habitasse platea dictumst.', 10, '2020-05-31 07:09:50');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('erat id', 'Nunc nisl.', 'Nam dui.', 11, '2020-08-13 02:50:48');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('pellentesque', 'Duis ac nibh.', 'Quisque ut erat.', 12, '2020-01-02 03:41:41');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('ut', 'Vestibulum sed magna at nunc commodo placerat.', 'Ut at dolor quis odio consequat varius.', 13, '2020-09-19 07:12:00');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('nulla', 'Ut at dolor quis odio consequat varius.', 'Vestibulum ac est lacinia nisi venenatis tristique.', 14, '2021-04-26 22:17:55');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('sapien', 'Praesent blandit.', 'Proin leo odio, porttitor id, consequat in, consequat ut, nulla.', 15, '2021-01-13 18:20:41');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('interdum mauris', 'Proin at turpis a pede posuere nonummy.', 'Nulla ut erat id mauris vulputate elementum.', 16, '2020-04-29 21:10:46');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('purus phasellus', 'Nulla suscipit ligula in lacus.', 'Sed sagittis.', 17, '2020-01-12 07:20:51');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('at', 'Donec odio justo, sollicitudin ut, suscipit a, feugiat et, eros.', 'Integer pede justo, lacinia eget, tincidunt eget, tempus vel, pede.', 18, '2020-02-11 13:49:28');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('sit', 'Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Donec pharetra, magna vestibulum aliquet ultrices, erat tortor sollicitudin mi, sit amet lobortis sapien sapien non mi.', 'Vivamus in felis eu sapien cursus vestibulum.', 19, '2021-04-15 16:01:40');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('odio', 'Donec dapibus.', 'Nulla mollis molestie lorem.', 20, '2020-09-08 18:15:12');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('egestas metus', 'Vestibulum sed magna at nunc commodo placerat.', 'Etiam pretium iaculis justo.', 21, '2020-06-02 23:25:33');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('metus', 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit.', 'Nulla justo.', 22, '2021-01-18 04:16:18');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('sapien', 'Morbi sem mauris, laoreet ut, rhoncus aliquet, pulvinar sed, nisl.', 'Nullam varius.', 23, '2021-05-24 04:21:00');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('mattis', 'Fusce lacus purus, aliquet at, feugiat non, pretium quis, lectus.', 'Morbi non lectus.', 24, '2021-02-07 11:09:28');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('morbi odio', 'Suspendisse potenti.', 'Proin risus.', 25, '2021-03-23 15:23:11');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('placerat', 'Aliquam augue quam, sollicitudin vitae, consectetuer eget, rutrum at, lorem.', 'Maecenas ut massa quis augue luctus tincidunt.', 26, '2020-10-09 15:20:45');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('elementum ligula', 'Maecenas ut massa quis augue luctus tincidunt.', 'In est risus, auctor sed, tristique in, tempus sit amet, sem.', 27, '2020-08-08 22:03:59');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('sollicitudin vitae', 'Nam congue, risus semper porta volutpat, quam pede lobortis ligula, sit amet eleifend pede libero quis orci.', 'Vestibulum ac est lacinia nisi venenatis tristique.', 28, '2020-12-29 07:13:46');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('potenti', 'Cras pellentesque volutpat dui.', 'Donec diam neque, vestibulum eget, vulputate ut, ultrices vel, augue.', 29, '2021-04-03 10:24:27');
INSERT INTO information (title, item_description, auction_description, auction_id, time_date) VALUES ('aliquam sit', 'Nulla justo.', 'Vivamus metus arcu, adipiscing molestie, hendrerit at, vulputate vitae, nisl.', 30, '2021-01-03 03:08:37');

----------------------------------------------------------------  Licitations ------------------------------------------------------------------------------------


INSERT INTO licitation (price, auction_id, person_id) VALUES (181.37, 25, 13);
INSERT INTO licitation (price, auction_id, person_id) VALUES (177.12, 22, 4);
INSERT INTO licitation (price, auction_id, person_id) VALUES (183.32, 28, 25);
INSERT INTO licitation (price, auction_id, person_id) VALUES (154.74, 14, 9);
INSERT INTO licitation (price, auction_id, person_id) VALUES (183.29, 12, 17);
INSERT INTO licitation (price, auction_id, person_id) VALUES (164.95, 22, 23);
INSERT INTO licitation (price, auction_id, person_id) VALUES (158.04, 19, 14);
INSERT INTO licitation (price, auction_id, person_id) VALUES (143.55, 16, 22);
INSERT INTO licitation (price, auction_id, person_id) VALUES (148.25, 13, 9);
INSERT INTO licitation (price, auction_id, person_id) VALUES (106.33, 23, 17);
INSERT INTO licitation (price, auction_id, person_id) VALUES (125.41, 28, 1);
INSERT INTO licitation (price, auction_id, person_id) VALUES (185.19, 25, 3);
INSERT INTO licitation (price, auction_id, person_id) VALUES (101.15, 20, 7);
INSERT INTO licitation (price, auction_id, person_id) VALUES (168.32, 10, 8);
INSERT INTO licitation (price, auction_id, person_id) VALUES (158.19, 22, 1);
INSERT INTO licitation (price, auction_id, person_id) VALUES (165.81, 6, 20);
INSERT INTO licitation (price, auction_id, person_id) VALUES (115.52, 9, 22);
INSERT INTO licitation (price, auction_id, person_id) VALUES (198.52, 22, 9);
INSERT INTO licitation (price, auction_id, person_id) VALUES (108.57, 13, 30);
INSERT INTO licitation (price, auction_id, person_id) VALUES (158.53, 28, 5);
INSERT INTO licitation (price, auction_id, person_id) VALUES (147.8, 17, 6);
INSERT INTO licitation (price, auction_id, person_id) VALUES (100.01, 22, 8);
INSERT INTO licitation (price, auction_id, person_id) VALUES (111.24, 6, 14);
INSERT INTO licitation (price, auction_id, person_id) VALUES (193.32, 4, 24);
INSERT INTO licitation (price, auction_id, person_id) VALUES (122.29, 14, 13);
INSERT INTO licitation (price, auction_id, person_id) VALUES (178.68, 29, 15);
INSERT INTO licitation (price, auction_id, person_id) VALUES (101.67, 3, 19);
INSERT INTO licitation (price, auction_id, person_id) VALUES (133.97, 8, 3);
INSERT INTO licitation (price, auction_id, person_id) VALUES (171.85, 5, 6);
INSERT INTO licitation (price, auction_id, person_id) VALUES (106.74, 30, 30);

-- Message --
INSERT INTO message (content, person_id, auction_id) VALUES ('Ut at dolor quis odio consequat varius.', 2, 20);
INSERT INTO message (content, person_id, auction_id) VALUES ('Maecenas tristique, est et tempus semper, est quam pharetra magna, ac consequat metus sapien ut nunc.', 14, 9);
INSERT INTO message (content, person_id, auction_id) VALUES ('In congue.', 29, 17);
INSERT INTO message (content, person_id, auction_id) VALUES ('Vestibulum rutrum rutrum neque.', 23, 22);
INSERT INTO message (content, person_id, auction_id) VALUES ('Vivamus tortor.', 30, 13);
INSERT INTO message (content, person_id, auction_id) VALUES ('Maecenas leo odio, condimentum id, luctus nec, molestie sed, justo.', 28, 9);
INSERT INTO message (content, person_id, auction_id) VALUES ('Vivamus metus arcu, adipiscing molestie, hendrerit at, vulputate vitae, nisl.', 26, 26);
INSERT INTO message (content, person_id, auction_id) VALUES ('Aliquam erat volutpat.', 3, 25);
INSERT INTO message (content, person_id, auction_id) VALUES ('Vestibulum quam sapien, varius ut, blandit non, interdum in, ante.', 12, 20);
INSERT INTO message (content, person_id, auction_id) VALUES ('Nam ultrices, libero non mattis pulvinar, nulla pede ullamcorper augue, a suscipit nulla elit ac nulla.', 28, 19);
INSERT INTO message (content, person_id, auction_id) VALUES ('Aliquam sit amet diam in magna bibendum imperdiet.', 11, 20);
INSERT INTO message (content, person_id, auction_id) VALUES ('Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis.', 2, 14);
INSERT INTO message (content, person_id, auction_id) VALUES ('Mauris lacinia sapien quis libero.', 8, 12);
INSERT INTO message (content, person_id, auction_id) VALUES ('In eleifend quam a odio.', 13, 10);
INSERT INTO message (content, person_id, auction_id) VALUES ('Nam tristique tortor eu pede.', 19, 9);
INSERT INTO message (content, person_id, auction_id) VALUES ('Proin interdum mauris non ligula pellentesque ultrices.', 5, 13);
INSERT INTO message (content, person_id, auction_id) VALUES ('Lorem ipsum dolor sit amet, consectetuer adipiscing elit.', 2, 25);
INSERT INTO message (content, person_id, auction_id) VALUES ('Suspendisse potenti.', 28, 15);
INSERT INTO message (content, person_id, auction_id) VALUES ('Donec posuere metus vitae ipsum.', 17, 10);
INSERT INTO message (content, person_id, auction_id) VALUES ('Nulla nisl.', 4, 25);
INSERT INTO message (content, person_id, auction_id) VALUES ('Nullam varius.', 25, 8);
INSERT INTO message (content, person_id, auction_id) VALUES ('Vivamus tortor.', 14, 2);
INSERT INTO message (content, person_id, auction_id) VALUES ('Maecenas rhoncus aliquam lacus.', 25, 2);
INSERT INTO message (content, person_id, auction_id) VALUES ('Integer aliquet, massa id lobortis convallis, tortor risus dapibus augue, vel accumsan tellus nisi eu orci.', 7, 23);
INSERT INTO message (content, person_id, auction_id) VALUES ('In eleifend quam a odio.', 19, 2);
INSERT INTO message (content, person_id, auction_id) VALUES ('Suspendisse potenti.', 22, 16);
INSERT INTO message (content, person_id, auction_id) VALUES ('Nulla suscipit ligula in lacus.', 25, 3);
INSERT INTO message (content, person_id, auction_id) VALUES ('Nam congue, risus semper porta volutpat, quam pede lobortis ligula, sit amet eleifend pede libero quis orci.', 7, 14);
INSERT INTO message (content, person_id, auction_id) VALUES ('Maecenas leo odio, condimentum id, luctus nec, molestie sed, justo.', 3, 8);
INSERT INTO message (content, person_id, auction_id) VALUES ('Fusce congue, diam id ornare imperdiet, sapien urna pretium nisl, ut volutpat sapien arcu sed augue.', 13, 18);