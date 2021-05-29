CREATE OR REPLACE FUNCTION notify_users()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
DECLARE
    f BIGINT;
    d BIGINT;

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

DROP trigger IF EXISTS t1 ON licitation;

CREATE TRIGGER t1
AFTER INSERT ON licitation
FOR EACH ROW
EXECUTE PROCEDURE notify_users();