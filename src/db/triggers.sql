CREATE OR REPLACE FUNCTION notify_users()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
DECLARE
    f BIGINT;
    d BIGINT;
    k BIGINT;

BEGIN
	FOR f IN SELECT DISTINCT person_id FROM licitation
            WHERE licitation.auction_id = NEW.auction_id AND licitation.person_id != NEW.person_id
    LOOP
        INSERT INTO notification (content) VALUES ('Value Updated') RETURNING notification.id INTO d;
        INSERT INTO inbox_messages (person_id, notification_id) VALUES (f, d);
    END LOOP;
	RETURN NEW;
END;
$$;


CREATE OR REPLACE FUNCTION notify_users_mural()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
DECLARE
    f BIGINT;
    d BIGINT;
    k BIGINT;

BEGIN
    SELECT person_id INTO k from auction WHERE id = NEW.auction_id;
	FOR f IN SELECT DISTINCT person_id FROM message
            WHERE message.auction_id = NEW.auction_id AND message.person_id != NEW.person_id AND NEW.person_id != k
    LOOP
        INSERT INTO notification (content) VALUES ('New Notification') RETURNING notification.id INTO d;
        INSERT INTO inbox_messages (person_id, notification_id) VALUES (f, d);
    END LOOP;
	RETURN NEW;
END;
$$;

CREATE OR REPLACE FUNCTION notify_creator()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
DECLARE
    f BIGINT;
    d BIGINT;

BEGIN
    SELECT person_id INTO f from auction WHERE id = NEW.auction_id;
        INSERT INTO notification (content) VALUES ('New Notification in Your Auction') RETURNING notification.id INTO d;
        INSERT INTO inbox_messages (person_id, notification_id) VALUES (f, d);
	RETURN NEW;
END;
$$;

DROP trigger IF EXISTS t1 ON licitation;
DROP trigger IF EXISTS t2 ON message;
DROP trigger IF EXISTS t3 ON message;

CREATE TRIGGER t1
AFTER INSERT ON licitation
FOR EACH ROW
EXECUTE PROCEDURE notify_users();

CREATE TRIGGER t2
AFTER INSERT ON message
FOR EACH ROW
EXECUTE PROCEDURE notify_users_mural();

CREATE TRIGGER t3
AFTER INSERT ON message
FOR EACH ROW
EXECUTE PROCEDURE notify_creator();