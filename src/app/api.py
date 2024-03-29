from os import error
from flask import Flask, jsonify, request
from datetime import datetime, timedelta
from functools import wraps

import psycopg2 as pg
import markdown as md
import logging
import time
import argparse
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'it\xb5u\xc3\xaf\xc1Q\xb9\n\x92W\tB\xe4\xfe__\x87\x8c}\xe9\x1e\xb8\x0f'
auth = None

ADMIN_ID = 1

'''     Codes      '''
OK_CODE = 200
SUCCESS_CODE = 201
BAD_REQUEST_CODE = 400
UNAUTHORIZED_CODE = 401
FORBIDDEN_CODE = 403
NOT_FOUND_CODE = 404
INTERNAL_SERVER_CODE = 500

######################################################################################
#####################################    UTILS    ####################################
######################################################################################


# Logging formater
class APILogFormatter(logging.Formatter):

    RED = "\x1B[31m"
    GREEN = "\x1B[32m"
    YELLOW = "\x1b[33;21m"
    RESET = "\x1B[0m"
    BLUE = "\x1B[34m"
    FORMAT = "%(asctime)s [%(levelname)s]:  %(message)s"

    FORMATS = {
        logging.DEBUG: FORMAT,
        logging.INFO: BLUE + FORMAT + RESET,
        logging.WARNING: YELLOW + FORMAT + RESET,
        logging.ERROR: RED + FORMAT + RESET,
    }

    def format(self, record):
        fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(fmt, "%H:%M:%S")
        return formatter.format(record)


# Token Interceptor
def auth_user(func):
    @wraps(func)
    def decorated(*args, **kwargs):

        content = request.get_json()
        if content is None or "token" not in content or not content["token"]:
            return jsonify({'error': 'Token is missing!', 'code': UNAUTHORIZED_CODE})

        check_ban_stmt = """
            SELECT *
            FROM person
            WHERE banned = true AND id = %s; 
        """

        try:
            token = content["token"]
            logger.info(f'Token Content, {token}')
            data = jwt.decode(token, app.config['SECRET_KEY'])

            try:
                with create_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(check_ban_stmt, [data["person_id"]])
                        rows = cursor.fetchall()
                        logger.info(rows)
                        if rows != []:
                            return jsonify({"code": FORBIDDEN_CODE, "error": "This user is banned"})

                conn.close()
            except (Exception, pg.DatabaseError) as error:
                logger.error(error)
                return jsonify({"code": INTERNAL_SERVER_CODE, "error": error})

        except Exception as e:
            logger.debug(e)
            return jsonify({'error': 'Invalid token', 'code': FORBIDDEN_CODE})
        return func(*args, **kwargs)
    return decorated

# Database Connection Establishment


def create_connection():
    return pg.connect(user=auth.db_username,
                      password=auth.db_password,
                      host=auth.db_hostname,
                      port=auth.db_port,
                      database=auth.db_database)


######################################################################################
#####################################    ROOT    #####################################
######################################################################################

# Root Endpoint
@app.route('/')
def index():
    readme_file = open("./templates/index.md", "r")
    md_template_string = md.markdown(
        readme_file.read(), extensions=["fenced_code"]
    )
    return md_template_string


######################################################################################
################################    SIGN UP / LOGIN    ###############################
######################################################################################

# Login Endpoint
@app.route("/user", methods=['PUT'])
def login():
    logger.info("Authenticating a user")
    content = request.get_json()

    if "username" not in content or "password" not in content:
        return jsonify({"code": BAD_REQUEST_CODE, "error": "Invalid Parameters in call"})

    logger.info(f'Request Content: {content}')

    get_person_id_stmt = """
                SELECT id
                FROM person
                WHERE username = %s AND password = %s
                """

    values = [content["username"], content["password"]]

    try:
        with create_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(get_person_id_stmt, values)
                rows = cursor.fetchall()
                token = jwt.encode({
                    'person_id': rows[0][0],
                    'is_admin': True if rows[0][0] == ADMIN_ID else False,
                    'expiration': str(datetime.utcnow() + timedelta(hours=24))
                }, app.config['SECRET_KEY'])
                logger.info(token)
        conn.close()
    except (Exception, pg.DatabaseError) as error:
        logger.error(error)
        return jsonify({"code": NOT_FOUND_CODE, "error": "User not Found"})
    return {"code": OK_CODE, 'token': token.decode('utf-8')}


def user_list_response_builder(rows):
    users = [{"code": OK_CODE}]
    for id, username, email, banned in rows:
        users.append({
            "id": id,
            "username": username,
            "email": email,
            "banned": banned
        })
    return users

# User Listing Endpoint
@app.route("/users", methods=['GET'])
@auth_user
def print_users():
    get_people_stmt = """
                    SELECT id, username, email, banned
                    FROM person;
                    """
    try:
        with create_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(get_people_stmt)
                rows = cursor.fetchall()
                users = user_list_response_builder(rows)
        conn.close()
    except (Exception, pg.DatabaseError) as error:
        logger.error(error)
        return jsonify({"code": INTERNAL_SERVER_CODE, "error": "Could not fetch users data"})
    return jsonify(users)

# Sign up Endpoint
@app.route("/user", methods=['POST'])
def create_user():
    logger.info("Signing up a User")

    content = request.get_json()

    if "username" not in content or "password" not in content or "email" not in content:
        return jsonify({'code': BAD_REQUEST_CODE, "error": 'Invalid Parameters in call'})

    logger.info(f'Request Content: {content}')

    put_person_stmt = """
                INSERT INTO person
                (username, password, email)
                VALUES
                (%s, %s, %s);
                """
    get_person_id_stmt = """
                SELECT id
                FROM person
                WHERE username = %s;
                """

    put_user_stmt = """
                    INSERT INTO users
                    (person_id)
                    VALUES
                    (%s);
                    """

    values = [content["username"], content["password"], content["email"]]

    try:
        with create_connection() as conn:
            with conn.cursor() as cursor:
                # Put Person in person table
                cursor.execute(put_person_stmt, values)

                # Get system-assigned personID
                cursor.execute(get_person_id_stmt, [values[0]])
                rows = cursor.fetchall()

                # Put User in users table
                cursor.execute(put_user_stmt, [rows[0][0]])

                logger.info(
                    "Insert user successfully into the database Username: %s , Password: %s, email: %s, is_Admin : false", *values)
        conn.close()
    except (Exception, pg.DatabaseError) as error:
        logger.error(error)
        return jsonify({"code": INTERNAL_SERVER_CODE, "error": str(error)})
    return jsonify({"code": SUCCESS_CODE, "id": str(rows[0][0])})


@app.route("/licitation/<auctionID>", methods=['PUT'])
@auth_user
def user_licitation(auctionID):
    content = request.get_json()

    if "price" not in content:
        return jsonify({'code': BAD_REQUEST_CODE, "error": 'Invalid Parameters in call'})

    token = content["token"]
    decoded = jwt.decode(token, app.config['SECRET_KEY'])
    author = decoded['person_id']
    price = content['price']

    logger.info(f'Request Content: {content}')

    try:
        int(auctionID)
        float(price)
        logger.debug(f"AuctionID: {auctionID}, bid: {price}")
    except Exception as error:
        return jsonify({'code': BAD_REQUEST_CODE, "error": 'Invalid Parameters in call'})

    validate_auction_stmt = """
                        SELECT 1
                        FROM auction 
                        WHERE id = %s AND cancelled = %s AND CURRENT_TIMESTAMP < end_date;
    """

    list_max_bid_auction_stmt = """
                        SELECT MAX(price)
                        FROM licitation
                        WHERE auction_id = %s AND valid = %s;
                         """

    list_min_price_stmt = """
               SELECT min_price 
               FROM auction 
               WHERE auction.id = %s;
                """
    insert_bid_stmt = """
               INSERT INTO licitation (price, auction_id, person_id) VALUES (%s, %s ,%s)
                """

    values_validate_auction = [auctionID, "false"]
    values_max_bid = [auctionID, "true"]
    values_min_price = [auctionID]
    values_insert_bid = [price, auctionID, author]

    try:
        with create_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(validate_auction_stmt, values_validate_auction)
                rows = cursor.fetchall()
                logger.info(rows)
                if(rows == []):
                    return jsonify({"error": "Either not existant or terminated/cancelled auction", "code": BAD_REQUEST_CODE})

                # stmt 2
                cursor.execute(list_max_bid_auction_stmt, values_max_bid)
                rows = cursor.fetchall()
                max_bid = 0 if rows[0][0] == None else float(rows[0][0])

                # stmt 3
                cursor.execute(list_min_price_stmt, values_min_price)
                rows = cursor.fetchall()
                logger.info(rows)
                min_amt = None if rows == [] else rows[0][0]
                if min_amt == None:
                    return jsonify({'code': BAD_REQUEST_CODE, "error": 'Invalid Parameters in call'})

                if float(price) <= max(max_bid, min_amt):
                    return jsonify({"error": "Invalid Amount (Lower Than Allowed)", "code": BAD_REQUEST_CODE})

                # stmt 4
                cursor.execute(insert_bid_stmt, values_insert_bid)
        conn.close()
    except (Exception, pg.DatabaseError) as error:
        logger.error(error)
        return jsonify({"code": INTERNAL_SERVER_CODE, "error": str(error)})
    return jsonify({"response": "Successful", "code": SUCCESS_CODE})


def inbox_messages_list_response_builder(rows):
    inbox = [{"code": OK_CODE}]
    for date, content, was_read in rows:
        inbox.append({
            "date": date,
            "message": content,
            "was_read": was_read
        })
    return inbox


@app.route("/user/inbox", methods=["GET"])
@auth_user
def list_user_inbox():
    content = request.get_json()
    token = content["token"]
    decoded = jwt.decode(token, app.config['SECRET_KEY'])
    author = decoded['person_id']

    # SQL queries
    list_user_inbox_stmt = """
        SELECT time_date,
            content,
            was_read
        FROM inbox_messages,
            notification
        WHERE inbox_messages.notification_id = notification.id
            AND inbox_messages.person_id = %s;
    """

    mark_read_stmt = """
        UPDATE inbox_messages
        SET was_read = true
        WHERE person_id = %s;
    """

    try:
        with create_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(list_user_inbox_stmt, [author])
                rows = cursor.fetchall()
                cursor.execute(mark_read_stmt, [author])

                logger.info(
                    "Successfully fetched %d rows from user %s inbox", len(rows), author)
                inbox = inbox_messages_list_response_builder(rows)

        conn.close()
    except (Exception, pg.DatabaseError) as error:
        logger.error(error)
        return jsonify({"code": INTERNAL_SERVER_CODE, "error": str(error)})
    return jsonify(inbox)

# Fetch auction description for each given ID


def auction_list_response_builder(rows):
    auctions = [{"code": OK_CODE}]
    for id, description in rows:
        # Append Auction to the response
        logger.info(
            f"""Adding auction to the response (id: {id}, description: {description})""")
        auctions.append({
            "id": id,
            "description": description
        })
    return auctions


@app.route("/user/activity", methods=["GET"])
@auth_user
def user_activity():
    content = request.get_json()
    token = jwt.decode(content["token"], app.config['SECRET_KEY'])

    # SQL query
    user_activity_stmt = """
        SELECT id,
            auction_description
        FROM (
                SELECT id
                FROM auction
                WHERE person_id = %s
                UNION
                SELECT auction_id
                FROM licitation
                WHERE person_id = %s
            ) AS activity
            JOIN (
                SELECT auction_id,
                    auction_description
                FROM information
                    JOIN (
                        SELECT MAX(reference) as ref,
                            auction_id as aid
                        FROM information
                        GROUP BY aid
                    ) AS ref_id ON reference = ref_id.ref
            ) AS info ON activity.id = info.auction_id;
    """

    logger.info("Making the database query...")
    try:
        with create_connection() as conn:
            with conn.cursor() as cursor:
                # Get user activity
                cursor.execute(user_activity_stmt, [token["person_id"]] * 2)
                logger.info(f"Successfully fetched user activity!")

                auctions = auction_list_response_builder(cursor.fetchall())

        conn.close()
    except (Exception, pg.DatabaseError) as error:
        logger.error(error)
        return jsonify({"error": str(error), "code": INTERNAL_SERVER_CODE})

    return jsonify(auctions)


######################################################################################
##############################    AUCTION OPERATIONS    ##############################
######################################################################################

@app.route("/auction", methods=['POST'])
@auth_user
def create_auction():
    logger.info("Creating an auction!")

    args = {"item", "min_price", "end_date", "title",
            "auction_description", "item_description"}
    content = request.get_json()
    token = jwt.decode(content["token"], app.config['SECRET_KEY'])

    if not args.issubset(content):
        return jsonify({'error': 'Invalid Parameters in call', 'code': BAD_REQUEST_CODE})

    # Check if arguments are valid

    if content["title"] is None or content["item_description"] is None or content["auction_description"] is None:
        return jsonify({'error': 'Invalid textual arguments', 'code': BAD_REQUEST_CODE})

    if content["item"] is None or not content["item"].isdigit():
        return jsonify({'error': 'Invalid item EAN/ISBN', 'code': BAD_REQUEST_CODE})

    if content["min_price"] is None or not content["min_price"].isdigit():
        return jsonify({'error': 'Invalid starting price', 'code': BAD_REQUEST_CODE})

    try:
        float(content["min_price"])
    except ValueError:
        return jsonify({'error': 'Starting price may not be negative', 'code': BAD_REQUEST_CODE})

    logger.info(f'Request Content: {content}')

    # SQL queries
    auction_create_stmt = """
            INSERT INTO auction
            (item, min_price, end_date, person_id)
            VALUES
            (%s, %s, TIMESTAMP %s, %s);
            """

    auction_add_info_stmt = """
            INSERT INTO information
            (title, item_description, auction_description, auction_id)
            VALUES
            (%s, %s, %s, %s);
            """

    get_auction_id_stmt = """
                SELECT MAX(id)
                FROM auction
                """

    logger.info("Making the database query...")
    try:
        with create_connection() as conn:
            with conn.cursor() as cursor:
                # Insert auction into the database
                auction_values = [content["item"], content["min_price"],
                                  content["end_date"], token["person_id"]]
                cursor.execute(auction_create_stmt, auction_values)
                logger.info(f"Auction Properties Inserted: {auction_values}")

                # Query ID of the inserted auction
                cursor.execute(get_auction_id_stmt)
                id = cursor.fetchone()[0]
                logger.info(f"Created Auction ID: {id}")

                # Add information to the newly created auction
                info_values = [content["title"], content["item_description"],
                               content["auction_description"], id]
                cursor.execute(auction_add_info_stmt, info_values)
                logger.info(f" Auction Information Inserted: {info_values}")

        conn.close()
    except (Exception, pg.DatabaseError) as error:
        logger.error(error)
        return jsonify({"error": str(error), "code": INTERNAL_SERVER_CODE})

    return jsonify({"id": id, "code": SUCCESS_CODE})


# Auction Listing Endpoint
@app.route("/auctions", methods=['GET'])
@auth_user
def list_auctions():
    logger.info("Listing auctions!")

    # SQL query
    running_auction_list_stmt = """
                        SELECT id,
                            auction_description
                        FROM auction
                            JOIN (
                                SELECT auction_id,
                                    auction_description
                                FROM information
                                    JOIN (
                                        SELECT MAX(reference) as ref,
                                            auction_id as aid
                                        FROM information
                                        GROUP BY aid
                                    ) AS ref_id ON reference = ref_id.ref
                            ) AS info ON id = info.auction_id
                        WHERE end_date > TIMESTAMP %s
                        """

    logger.info("Making the database query...")
    try:
        with create_connection() as conn:
            with conn.cursor() as cursor:
                # Get current time and fetch all running auctions IDs
                current_time = str(datetime.utcnow())
                cursor.execute(running_auction_list_stmt, [current_time])
                logger.info(f"Successfully fetched running auctions!")

                auctions = auction_list_response_builder(cursor.fetchall())

        conn.close()
    except (Exception, pg.DatabaseError) as error:
        logger.error("There was an error : %s", error)
        return jsonify({"error": str(error), "code": INTERNAL_SERVER_CODE})

    return jsonify(auctions)


@app.route("/auctions/<filter>", methods=["GET"])
@auth_user
def search_auctions(filter: str):
    logger.info("Searching auctions!")

    # Select SQL search query accourding to filter type
    id_filter_stmt = ""
    if filter.isdigit():
        id_filter_stmt = f"item = {filter} OR"

    # SQL query
    auction_search_stmt = """
                SELECT id,
                    item_description
                FROM auction
                    JOIN (
                        SELECT auction_id,
                            item_description
                        FROM information
                            JOIN (
                                SELECT MAX(reference) as ref,
                                    auction_id as aid
                                FROM information
                                GROUP BY aid
                            ) AS ref_id ON reference = ref_id.ref
                    ) AS info ON id = info.auction_id
                WHERE end_date > TIMESTAMP %s
                    AND {} item_description LIKE %s;
                """.format(id_filter_stmt)

    logger.info("Making the database query...")
    try:
        with create_connection() as conn:
            auctions = []
            with conn.cursor() as cursor:
                # Get current time and fetch all running auctions IDs
                current_time = str(datetime.utcnow())
                cursor.execute(auction_search_stmt, [
                               current_time, f"%{filter}%"])
                logger.info(
                    f"Successfully filtered and fetched running auctions!")

                auctions = auction_list_response_builder(cursor.fetchall())

        conn.close()
    except (Exception, pg.DatabaseError) as error:
        logger.error(error)
        return jsonify({"error": str(error), "code": INTERNAL_SERVER_CODE})

    return jsonify(auctions)


@app.route("/auction/<auctionID>", methods=["GET"])
@auth_user
def auction_details(auctionID: str):
    logger.info(f"Details for auction with ID {auctionID}!")

    if not auctionID.isdigit():
        logger.error("Invalid auction ID!")
        return jsonify({
            'error': 'A invalid auction ID was provided',
            'code': BAD_REQUEST_CODE
        })

    # SQL queries
    auction_properties_stmt = """
        SELECT auction_id, username, title,
            item, item_description, auction_description,
            min_price, end_date, cancelled
        FROM auction
        JOIN (
            SELECT *
            FROM information
                JOIN (
                    SELECT MAX(reference) as ref,
                        auction_id as aid
                    FROM information
                    WHERE auction_id = %s
                    GROUP BY auction_id
                ) AS ref_id ON reference = ref_id.ref
        ) AS info ON id = info.auction_id
        JOIN (
            SELECT id,
                username
            FROM person
        ) AS names ON names.id = person_id;
        """
    auction_message_list_stmt = """
        SELECT username, content, time_date
        FROM message
            JOIN (
                SELECT id,
                    username
                FROM person
            ) AS names ON names.id = person_id
        WHERE auction_id = %s
        ORDER BY time_date ASC;
    """

    licitation_message_list_stmt = """
        SELECT username, price
        FROM licitation
            JOIN (
                SELECT id,
                    username
                FROM person
            ) AS names ON names.id = person_id
        WHERE auction_id = %s
        ORDER BY price ASC;
    """

    # Response JSON Keys
    response_properties_keys = [
        "id",
        "creator",
        "title",
        "item",
        "item_description",
        "auction_description",
        "opening_price",
        "end_date",
        "canceled"
    ]

    response_message_keys = [
        "author",
        "content",
        "time_date"
    ]

    response_licitation_keys = [
        "bidder",
        "bid"
    ]

    logger.info("Making the database query...")
    try:
        with create_connection() as conn:
            payload = {"code": OK_CODE}
            with conn.cursor() as cursor:

                # Auction properties query
                logger.info("Adding properties to the response payload!")
                cursor.execute(auction_properties_stmt, [auctionID])
                rows = cursor.fetchall()
                logger.debug(rows)
                # Add auction properties to the payload
                if len(rows) > 0:
                    payload.update(
                        list(zip(response_properties_keys, rows[0]))
                    )

                # Auction mural messages query
                logger.info("Adding mural messages to the response payload!")
                cursor.execute(auction_message_list_stmt, [auctionID])
                rows = cursor.fetchall()

                # Add auction mural messages to the payload
                if len(rows) > 0:
                    payload["messages"] = []
                    for message in rows:
                        payload["messages"].append(
                            dict(zip(response_message_keys, message))
                        )

                # Auction licitations query
                logger.info("Adding licitations to the response payload!")
                cursor.execute(licitation_message_list_stmt, [auctionID])
                rows = cursor.fetchall()

                # Add auction licitations to the payload
                if len(rows) > 0:
                    payload["licitations"] = []
                    for licitation in rows:
                        payload["licitations"].append(
                            dict(zip(response_licitation_keys, licitation))
                        )
        conn.close()
    except (Exception, pg.DatabaseError) as error:
        logger.error(error)
        return jsonify({"error": str(error), "code": INTERNAL_SERVER_CODE})

    return jsonify(payload)


def message_list_response_builder(rows):
    messages = [{"code": OK_CODE}]
    for username, content, time_date in rows:
        messages.append({
            "username": username,
            "message": content,
            "time_date": time_date
        })
    return messages


def write_msg_core(auctionID, author, message):
    # We could verify is auction exists in the database before running this command
    write_msg_stmt = """
               INSERT INTO message (person_id, auction_id, content, time_date)
               VALUES (%s, %s, %s , TIMESTAMP %s)
                """
    tmstp = datetime.utcnow()  # just because this is used in the logger later
    values = (author, auctionID, message, str(tmstp))
    try:
        with create_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(write_msg_stmt, values)
                logger.info(
                    "Inserted Message successfully into election's %s Mural , Content : %s, Author : %s , TimeStamp: %s", auctionID, message, author, str(tmstp))
        conn.close()
    except (Exception, pg.DatabaseError) as error:
        logger.error("There was an error : %s", error)
        return jsonify({"code": INTERNAL_SERVER_CODE, "error": str(error)})

    return jsonify({"response": "Successful", "code": SUCCESS_CODE})

# Inserting a message into the mural
@app.route("/auction/<auctionID>/mural", methods=['POST'])
@auth_user
def write_msg(auctionID):
    content = request.get_json()
    if not {"message"}.issubset(content):
        return jsonify({'error': 'Invalid Parameters in call', 'code': BAD_REQUEST_CODE})

    if not auctionID.isdigit():
        return jsonify({"error": "Invalid auctionID", "code": NOT_FOUND_CODE})

    token = content["token"]
    decoded = jwt.decode(token, app.config['SECRET_KEY'])
    author = decoded['person_id']
    message = content['message']

    return write_msg_core(auctionID, author, message)

# List all messages in message board
@app.route("/auction/<auctionID>/mural", methods=["GET"])
@auth_user
def list_msg(auctionID):

    if not auctionID.isdigit():
        return jsonify({"error": "Invalid auctionID", "code": NOT_FOUND_CODE})

    # SQL queries
    list_msg_stmt = """
        SELECT username,
            content,
            time_date
        FROM message
            JOIN (
                SELECT id,
                    username
                FROM person
            ) AS info ON info.id = person_id
        WHERE auction_id = %s;
    """

    try:
        with create_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(list_msg_stmt, [auctionID])
                rows = cursor.fetchall()

                logger.info("Successfully fetched %d rows from Message Board from auction %s", len(
                    rows), auctionID)
                messages = message_list_response_builder(rows)

        conn.close()
    except (Exception, pg.DatabaseError) as error:
        logger.error("There was an error : %s", error)
        return jsonify({"code": INTERNAL_SERVER_CODE, "error": str(error)})
    return jsonify(messages)


@app.route("/auction/<auctionID>", methods=["PUT"])
def edit_auction(auctionID: str):

    content = request.get_json()
    token = jwt.decode(content["token"], app.config['SECRET_KEY'])

    logger.info(f'Request Content: {content}')

    # Editable information
    edit_args = ["title", "item_description",
                 "auction_description"]

    # SQL queries
    auction_information_by_id_stmt = """
        SELECT title,
            item_description,
            auction_description,
            time_date,
            person_id
        FROM auction
            JOIN (
                SELECT *
                FROM information
                    JOIN (
                        SELECT MAX(reference) as ref,
                            auction_id as aid
                        FROM information
                        WHERE auction_id = %s
                        GROUP BY auction_id
                    ) AS ref_id ON reference = ref_id.ref
            ) AS info ON id = info.auction_id;
    """

    auction_add_info_stmt = """
            INSERT INTO information
            (title, item_description, auction_description, auction_id)
            VALUES
            (%s, %s, %s, %s);
            """

    try:
        with create_connection() as conn:
            with conn.cursor() as cursor:
                # Getting most recent auction information details
                cursor.execute(auction_information_by_id_stmt, [auctionID])
                rows = cursor.fetchone()

                if rows[-1] != token["person_id"]:
                    return jsonify({"error": "The user is not the auction's owner", "code": UNAUTHORIZED_CODE})

                edit = dict(zip(edit_args, rows[:-1]))
                logger.info(f"Existing Information Values: {edit}")

                # Update information details
                for arg in edit_args:
                    if arg in content:
                        edit[arg] = content[arg]

                cursor.execute(auction_add_info_stmt, list(
                    edit.values()) + [auctionID])
                logger.info(f"Auction Information Updated with values: {edit}")

        conn.close()
    except (Exception, pg.DatabaseError) as error:
        logger.error("There was an error : %s", error)
        return jsonify({"code": INTERNAL_SERVER_CODE, "error": str(error)})

    return jsonify({"response": "Successfull", "code": SUCCESS_CODE})


######################################################################################
###############################    ADMIN OPERATIONS    ###############################
######################################################################################

def cancel_auction_core(auction_id):

    # SQL queries
    cancel_auction_stmt = """
                        UPDATE auction 
                        SET cancelled = true 
                        WHERE id = %s;
                        """

    get_auction_people_ids_stmt = """
                            SELECT DISTINCT person_id 
                            FROM licitation 
                            WHERE auction_id = %s;
                            """
    put_notification_stmt = """
                        INSERT INTO notification
                        (content, time_date)
                        VALUES
                        (%s, %s);
                        """
    get_notification_id_stmt = """
                            SELECT MAX(id)
                            FROM notification;
                            """
    associate_notification_stmt = """
                            INSERT INTO inbox_messages
                            (notification_id, person_id)
                            VALUES 
                            (%s, %s);
                            """
    get_creator_id_stmt = """
                            SELECT person_id
                            FROM auction
                            WHERE id = %s;
                        """

    with create_connection() as conn:
        # Create a view over the database
        with conn.cursor() as cursor:
            # Cancel Auction
            cursor.execute(cancel_auction_stmt, [auction_id])

            logger.info("Creating notifications")

            # Create Notification for bidders
            cursor.execute(put_notification_stmt, [
                           "The auction was cancelled by the application administrator", datetime.utcnow()])
            # Get bidder's notification ID
            cursor.execute(get_notification_id_stmt)
            bidders_notification_id = cursor.fetchall()[0][0]

            # Create Notification for creator
            cursor.execute(put_notification_stmt, [
                "Your auction was cancelled by the application administrator", datetime.utcnow()])
            # Get creator's notification ID
            cursor.execute(get_notification_id_stmt)
            creator_notification_id = cursor.fetchall()[0][0]

            # Get Creator ID
            cursor.execute(get_creator_id_stmt, [auction_id])
            creator_id = cursor.fetchall()[0][0]

            # Get auction-related users IDS
            logger.info("Notifying users")
            cursor.execute(get_auction_people_ids_stmt, [auction_id])
            people_ids = cursor.fetchall()

            # Notify all auction-related users
            cursor.execute(associate_notification_stmt, [
                           creator_notification_id, creator_id])
            for entry in people_ids:
                cursor.execute(associate_notification_stmt,
                               [bidders_notification_id, entry[0]])
    conn.close()

# Cancel auction Endpoint
@app.route("/admin/cancel", methods=['POST'])
@auth_user
def cancel_auction():
    logger.info("Cancelling Auction")

    content = request.get_json()

    # Checking Form Parameters
    if not {"id", "token"}.issubset(content):
        return jsonify({'error': 'Invalid Parameters in call', 'code': BAD_REQUEST_CODE})

    logger.info(f'Request Content: {content}')

    # Checking if user in admin
    decoded_token = jwt.decode(content['token'], app.config['SECRET_KEY'])
    if(not decoded_token['is_admin']):
        return jsonify({"error": "The user does not have admin privileges", "code": FORBIDDEN_CODE})

    try:
        cancel_auction_core(content['id'])
    except (Exception, pg.DatabaseError) as error:
        logger.error("There was an error : %s", error)
        return jsonify({"error": str(error), "code": INTERNAL_SERVER_CODE})
    # Return response
    logger.info("Auction cancel operation successful")
    return jsonify({"response": "Successful", "code": SUCCESS_CODE})


# Ban User Endpoint
@app.route("/admin/ban", methods=['POST'])
@auth_user
def ban_user():
    logger.info("Banning User")

    content = request.get_json()

    # Checking Form Parameters
    if not {"id", "token"}.issubset(content):
        return jsonify({'error': 'Invalid Parameters in call', 'code': BAD_REQUEST_CODE})

    logger.info(f'Request Content: {content}')

    # Checking if user in admin
    decoded_token = jwt.decode(content['token'], app.config['SECRET_KEY'])
    if(not decoded_token['is_admin']):
        return jsonify({"error": "The user does not have admin privileges", "code": FORBIDDEN_CODE})

    # SQL queries
    ban_user_stmt = """
                    UPDATE person
                    SET banned = true
                    WHERE id = %s;
                    """
    get_user_created_auctions_ids_stmt = """
                                        SELECT id
                                        FROM auction
                                        WHERE person_id = %s;
                                        """

    update_user_licitations_stmt = """
                                UPDATE licitation
                                SET valid = false
                                WHERE person_id = %s;
                                """

    get_auction_min_max_bid_stmt = """
                                    SELECT auction.id, table_min.min, table_max.max
                                    FROM auction
                                    JOIN (
                                        SELECT auction_id, MIN(price) AS "min"
                                        FROM licitation
                                        WHERE person_id = %s
                                        GROUP BY auction_id
                                    ) AS table_min
                                    ON auction.id = table_min.auction_id
                                    JOIN (
                                        SELECT auction_id, MAX(price) AS "max"
                                        FROM licitation
                                        WHERE valid = true
                                        GROUP BY auction_id
                                    ) AS table_max
                                    ON auction.id = table_max.auction_id;
                                """

    update_licitations_price_stmt = """
                            UPDATE licitation
                            SET valid = false
                            WHERE (auction_id = %s AND price >= %s AND price < %s);
                            """

    update_max_stmt = """
                    UPDATE licitation
                    SET price = '%s'
                    WHERE price = '%s';
                    """

    try:
        with create_connection() as conn:
            # Create a view over the database
            with conn.cursor() as cursor:
                # Ban User
                cursor.execute(ban_user_stmt, [content['id']])

                # Get user created auctions IDS
                cursor.execute(
                    get_user_created_auctions_ids_stmt, [content['id']])
                auctions_ids = cursor.fetchall()

                for entry in auctions_ids:
                    # Cancel Auctions and notify Related users
                    cancel_auction_core(entry[0])
                    # Create Message on Auction's mural
                    write_msg_core(
                        entry[0], ADMIN_ID, "We're sorry to inform that this auction has been cancelled.")

                logger.info("Invalidating User Licitations")
                # Invalidate User licitations
                cursor.execute(update_user_licitations_stmt, [content['id']])

                # Get minimum user bidded and max valid bidded licitations for all related auctions
                cursor.execute(get_auction_min_max_bid_stmt, [content['id']])
                info = cursor.fetchall()

                logger.info("Updating Bidded Prices")
                for auction_id, min_user_bid, max_valid_bid in info:
                    # All licitations above the minimum banned user licitation price are cancelled, except the maximum valid licitation
                    cursor.execute(update_licitations_price_stmt, [
                                   auction_id, min_user_bid, max_valid_bid])

                    # All licitations maximum price are updated to minimum banned user licitation price if
                    if (min_user_bid < max_valid_bid):
                        cursor.execute(update_max_stmt, [
                            min_user_bid, max_valid_bid])

        conn.close()
    except (Exception, pg.DatabaseError) as error:
        logger.error("There was an error : %s", error)
        return jsonify({"error": str(error), "code": INTERNAL_SERVER_CODE})

    logger.info("Person ban operation successful")
    return jsonify({"response": "Successful", "code": SUCCESS_CODE})

# App Statistics Endpoint
@app.route("/admin/stats", methods=['GET'])
@auth_user
def statistics():
    logger.info("Showing Statistics")

    content = request.get_json()

    # Checking Form Parameters
    if not {"token"}.issubset(content):
        return jsonify({'error': 'Invalid Parameters in call', 'code': BAD_REQUEST_CODE})

    logger.info(f'Request Content: {content}')

    # Checking if user in admin
    decoded_token = jwt.decode(content['token'], app.config['SECRET_KEY'])
    if(not decoded_token['is_admin']):
        return jsonify({"error": "The user does not have admin privileges", "code": FORBIDDEN_CODE})

    # SQL queries
    get_top_10_users_with_more_auctions_created_stmt = """
        SELECT person_id, count(*) as "auctions"
        FROM auction
        GROUP BY person_id
        ORDER BY "auctions" DESC
        LIMIT 10;
        """

    get_top_10_winners_stmt = """
        SELECT person_id, count(ended_valid_auction_winners.person_id) AS "counter"
        FROM (
            SELECT ended_valid_auctions.id, winners.person_id
            FROM (
                SELECT id 
                FROM auction 
                WHERE (end_date < %s)
                AND cancelled = false
            ) AS ended_valid_auctions
            JOIN (
                SELECT person_id, auction_id, price
                FROM licitation
                WHERE (auction_id, price) IN (
                    SELECT auction_id, MAX(price)
                    FROM licitation
                    WHERE valid = true
                    GROUP BY auction_id
                ) AND valid = true
            ) AS winners 
            ON ended_valid_auctions.id = winners.auction_id
        ) AS ended_valid_auction_winners
        GROUP BY person_id
        ORDER BY "counter" DESC
        LIMIT 10;
        """

    get_total_auction_n_last_10_days_stmt = """
        SELECT COUNT(time_date)
        FROM information
        WHERE (auction_id, reference) IN (
            SELECT auction_id, MIN(reference)
            FROM information
            GROUP BY auction_id
        )  AND time_date > %s - INTERVAL '10' DAY ;
    """

    try:
        with create_connection() as conn:
            # Create a view over the database
            with conn.cursor() as cursor:
                cursor.execute(
                    get_top_10_users_with_more_auctions_created_stmt)
                more_auctions_created = cursor.fetchall()

                cursor.execute(get_top_10_winners_stmt, [datetime.utcnow()])
                winners = cursor.fetchall()

                cursor.execute(get_total_auction_n_last_10_days_stmt, [
                               datetime.utcnow()])
                total_10_days = cursor.fetchall()[0][0]

        conn.close()
    except (Exception, pg.DatabaseError) as error:
        logger.error("There was an error : %s", error)
        return jsonify({"error": str(error), "code": INTERNAL_SERVER_CODE})

    logger.info("Statistics operation successful")
    return jsonify(
        {
            "more_auctions_created": [{"person_id": person_id, "created": counter} for person_id, counter in more_auctions_created],
            "winners": [{"person_id": person_id, "won": won} for person_id, won in winners],
            "total_created_auctions_last_10_days": total_10_days
        }
    )

########################################################################################
#################################     MAIN     #########################################
########################################################################################


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="DB-Project Auction REST API - Flask Web Server"
    )
    parser.add_argument("-u", "--db-username", type=str,
                        help="the database username",
                        default="admin")

    parser.add_argument("-p", "--db-password", type=str,
                        help="the user password",
                        default="admin")

    parser.add_argument("-D", "--db-database", type=str,
                        help="the database to connect to",
                        default="dbauction")

    parser.add_argument("-P", "--db-port", type=int,
                        help="the port where the DBMS is running",
                        default="5432")

    parser.add_argument("-H", "--db-hostname", type=str,
                        help="the hostname where the DBMS is running",
                        default="localhost")
    auth = parser.parse_args()

    # Set up the logging
    logging.basicConfig(filename="logs/log_file.log")
    logger = logging.getLogger('logger')

    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(APILogFormatter())
    logger.addHandler(ch)

    time.sleep(1)
    logger.info("\n-------- Everything seems to be working ----------\n"
                "-------- Docker: http://localhost:8080/ ----------\n"
                "-------- Native: http://localhost:5000/ ----------\n"
                )
    app.run(host="0.0.0.0",  debug=False, threaded=True)
