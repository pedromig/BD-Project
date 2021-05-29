CREATE TABLE person (
	id	 BIGSERIAL,
	username VARCHAR(512) UNIQUE NOT NULL,
	password VARCHAR(512) NOT NULL,
	email	 VARCHAR(512) NOT NULL,
	banned	 BOOL NOT NULL DEFAULT false,
	PRIMARY KEY(id)
);

CREATE TABLE licitation (
	id	 BIGSERIAL,
	price	 FLOAT(8) NOT NULL,
	valid	 BOOL NOT NULL DEFAULT true,
	auction_id BIGINT NOT NULL,
	person_id	 BIGINT NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE auction (
	id	 BIGSERIAL,
	item	 BIGINT NOT NULL,
	min_price FLOAT(8) NOT NULL DEFAULT 0,
	end_date	 TIMESTAMP NOT NULL,
	cancelled BOOL NOT NULL DEFAULT false,
	person_id BIGINT NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE users (
	person_id BIGINT,
	PRIMARY KEY(person_id)
);

CREATE TABLE administrator (
	person_id BIGINT,
	PRIMARY KEY(person_id)
);

CREATE TABLE message (
	id	 BIGSERIAL,
	content	 VARCHAR(512) NOT NULL,
	time_date	 TIMESTAMP NOT NULL,
	person_id	 BIGINT NOT NULL,
	auction_id BIGINT NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE information (
	reference	 BIGSERIAL,
	title	 VARCHAR(512) NOT NULL,
	item_description VARCHAR(512) NOT NULL,
	auction_description VARCHAR(512) NOT NULL,
	time_date	 TIMESTAMP NOT NULL,
	auction_id	 BIGINT NOT NULL,
	PRIMARY KEY(reference)
);

CREATE TABLE notification (
	id	 BIGSERIAL,
	content	 VARCHAR(512) NOT NULL,
	time_date TIMESTAMP NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE inbox_messages (
	was_read	 BOOL NOT NULL DEFAULT false,
	notification_id BIGINT,
	person_id	 BIGINT,
	PRIMARY KEY(notification_id,person_id)
);

ALTER TABLE licitation ADD CONSTRAINT licitation_fk1 FOREIGN KEY (auction_id) REFERENCES auction(id);
ALTER TABLE licitation ADD CONSTRAINT licitation_fk2 FOREIGN KEY (person_id) REFERENCES person(id);
ALTER TABLE auction ADD CONSTRAINT auction_fk1 FOREIGN KEY (person_id) REFERENCES person(id);
ALTER TABLE users ADD CONSTRAINT users_fk1 FOREIGN KEY (person_id) REFERENCES person(id);
ALTER TABLE administrator ADD CONSTRAINT administrator_fk1 FOREIGN KEY (person_id) REFERENCES person(id);
ALTER TABLE message ADD CONSTRAINT message_fk1 FOREIGN KEY (person_id) REFERENCES person(id);
ALTER TABLE message ADD CONSTRAINT message_fk2 FOREIGN KEY (auction_id) REFERENCES auction(id);
ALTER TABLE information ADD CONSTRAINT information_fk1 FOREIGN KEY (auction_id) REFERENCES auction(id);
ALTER TABLE inbox_messages ADD CONSTRAINT inbox_messages_fk1 FOREIGN KEY (notification_id) REFERENCES notification(id);
ALTER TABLE inbox_messages ADD CONSTRAINT inbox_messages_fk2 FOREIGN KEY (person_id) REFERENCES person(id);

