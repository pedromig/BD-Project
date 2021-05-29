from os import error
from flask import Flask, json, jsonify, request
from datetime import datetime, timedelta
from functools import wraps
from flask.json.tag import PassDict

import psycopg2 as pg
import logging
import sys
import time
import argparse
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'it\xb5u\xc3\xaf\xc1Q\xb9\n\x92W\tB\xe4\xfe__\x87\x8c}\xe9\x1e\xb8\x0f'
auth = None

'''     Codes      '''
SUCCESS_CODE = 201

BAD_REQUEST_CODE = 400
UNAUTHORIZED_CODE = 401
FORBIDDEN_CODE = 403
NOT_FOUND_CODE = 404
INTERNAL_SERVER_CODE = 500
SUCCESS_CODE = 201

######################################################################################
#####################################    UTILS    ####################################
######################################################################################

# Token Interceptor


def auth_user(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            token = request.get_json()["token"]
            if not token:
                return jsonify({'error': 'Token is missing!', 'code': UNAUTHORIZED_CODE})
            logger.info(f'Token Content, {token}')
            jwt.decode(token, app.config['SECRET_KEY'])
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
def hello():
    return "Well, the description has was too big, but it is working"


######################################################################################
################################    SIGN UP / LOGIN    ###############################
######################################################################################

# Login Endpoint
@app.route("/user", methods=['PUT'])
def login():
    logger.info("Authenticating a user")
    content = request.get_json()

    conn = create_connection()
    cursor = conn.cursor()

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
        cursor.execute(get_person_id_stmt, values)
        rows = cursor.fetchall()
        token = jwt.encode({
            'person_id': rows[0][0],
            # This is a bad bad security flaw, should be fixed in the future and the is_admin is hardcoded
            'is_admin': True if rows[0][0] == 1 else False,
            # Defaulting for a 24 hr token
            'expiration': str(datetime.utcnow() + timedelta(hours=24))
        }, app.config['SECRET_KEY'])
        logger.info(token)
        return {'token': token.decode('utf-8')}
    except (Exception, pg.DatabaseError) as error:
        logger.error("Request not found in person table")
        logger.error(error)
        return jsonify({"code": NOT_FOUND_CODE, "error": "User not Found"})
    finally:
        if conn is not None:
            conn.close()

# User Listing Endpoint
@app.route("/users", methods=['GET'])
def print_users():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, password, email, banned FROM person;")
        rows = cursor.fetchall()
        return jsonify({"users": rows})
    except:
        return jsonify({"code": INTERNAL_SERVER_CODE, "error": "Could not fetch users data"})
    finally:
        if conn is not None:
            conn.close()

# Sign up Endpoint
@app.route("/user", methods=['POST'])
def create_user():
    logger.info("Signing up a User")

    content = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()

    if "username" not in content or "password" not in content or "email" not in content:
        return jsonify({'code': BAD_REQUEST_CODE, "error": 'Invalid Parameters in call'})

    logger.info(f'Request Content: {content}')

    put_person_stmt = """
                INSERT INTO
                person (username, password, email)
                VALUES
                (%s, %s, %s);
                """
    get_person_id_stmt = """
                SELECT id
                FROM person
                WHERE username = %s;
                """

    put_user_stmt = " INSERT INTO users(person_id) VALUES (%s);"

    values = [content["username"], content["password"], content["email"]]

    try:
        # Put Person in person table
        cursor.execute(put_person_stmt, values)

        # Get system-assigned personID
        cursor.execute(get_person_id_stmt, [values[0]])
        rows = cursor.fetchall()

        # Put User in users table
        cursor.execute(put_user_stmt, [rows[0][0]])

        # Make Changes Permanent
        conn.commit()
        logger.info(
            "Insert user successfully into the database Username: %s , Password: %s, email: %s, is_Admin : false", *values)
        return jsonify({"id": str(rows[0][0])})

    except (Exception, pg.DatabaseError) as error:
        logger.error("There was an error : %s", error)
        return jsonify({"code": INTERNAL_SERVER_CODE, "error": str(error)})
    finally:
        if conn is not None:
            conn.close()


######################################################################################
##############################    AUCTION OPERATIONS    ##############################
######################################################################################

@app.route("/auction", methods=['POST'])
@auth_user
def create_auction():
    logger.info("Creating an auction!")

    content = request.get_json()
    token = jwt.decode(content["token"], app.config['SECRET_KEY'])

    logger.info(f'Request Content: {content}')
    if not {"item", "min_price", "end_date", "title", "description"}.issubset(content):
        return jsonify({'error': 'Invalid Parameters in call', 'code': BAD_REQUEST_CODE})

    # SQL queriesd
    auction_create_stmt = """
            INSERT INTO auction (item, min_price, end_date, person_id)
            VALUES (%s, %s, TIMESTAMP %s, %s);
            """

    auction_add_info_stmt = """
            INSERT INTO information (title, description, auction_id)
            VALUES (%s, %s, %s);
            """

    get_auction_id_stmt = """
                SELECT id
                FROM auction
                WHERE item = %s;
                """
    try:
        with create_connection() as conn:
            with conn.cursor() as cursor:
                # Insert auction into the database
                auction_values = [content["item"], content["min_price"],
                                  content["end_date"], token["person_id"]]
                cursor.execute(auction_create_stmt, auction_values)

                # Query ID of the inserted auction
                cursor.execute(get_auction_id_stmt, [content["item"]])
                id = cursor.fetchone()[0]

                # Add information to the newly created auction
                info_values = [content["title"], content["description"], id]
                cursor.execute(auction_add_info_stmt, info_values)
        conn.close()

    except (Exception, pg.DatabaseError) as error:
        logger.error("There was an error : %s", error)
        return jsonify({"error": str(error), "code": INTERNAL_SERVER_CODE})

    return jsonify({"id": id})

# Auction Listing Endpoint
# TODO: I am not finished yet
@app.route("/auctions", methods=['GET'])
def list_auctions():

    auction_list_stmt = """ 
                        SELECT id 
                        FROM auction;
                        """
    auction_description_stmt = """
                            SELECT description 
                            FROM auction
                            WHERE auction_id = %s
                            """

    with create_connection() as conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute(auction_list_stmt)
                rows = cursor.fetchall()
                return jsonify(rows)

        except (Exception, pg.DatabaseError) as error:
            logger.error("There was an error : %s", error)
            return jsonify({"error": str(error), "code": INTERNAL_SERVER_CODE})


# Inserting a message into the mural
@app.route("/<auctionID>/mural", methods=['PUT'])
@auth_user
def write_msg(auctionID):
    content = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    if not {"message"}.issubset(content):
        return jsonify({'error': 'Invalid Parameters in call', 'code': BAD_REQUEST_CODE})

    token = content["token"]
    decoded = jwt.decode(token, app.config['SECRET_KEY'])
    author = decoded['person_id']
    message = content['message']

    try:
        int(auctionID)
    except Exception as error:
        return jsonify({"error": "Invalid auctionID", "code": NOT_FOUND_CODE})

    # We could verify is auction exists in the database before running this command

    write_msg_stmt = """
               INSERT INTO message (person_id, auction_id, content, time_date)
               VALUES (%s, %s, %s , TIMESTAMP %s)
                """
    tmstp = datetime.utcnow()  # just because this is used in the logger later
    values = (author, auctionID, message, str(tmstp))
    try:
        # Put Person in person table
        cursor.execute(write_msg_stmt, values)

        # Make Changes Permanent
        conn.commit()

        logger.info(
            "Inserted Message successfully into election's %s Mural , Content : %s, Author : %s , TimeStamp: %s", auctionID, message, author, str(tmstp))
        return jsonify({"response": "Successful", "code": SUCCESS_CODE})

    except (Exception, pg.DatabaseError) as error:
        logger.error("There was an error : %s", error)
        return jsonify({"code": INTERNAL_SERVER_CODE, "error": str(error)})
    finally:
        if conn is not None:
            conn.close()

# List all messages in message board
@app.route("/<auctionID>/mural", methods=['GET'])
# @auth_user Use this later?
def list_msg(auctionID):
    conn = create_connection()
    cursor = conn.cursor()
    list_msg_stmt = """
               SELECT * from message where auction_id = %s
                """
    values = (auctionID)
    try:
        with conn.cursor() as cursor:
            cursor.execute(list_msg_stmt, values)
            rows = cursor.fetchall()
            logger.info(
                "Successfully fetched %d rows from Message Board from auction %s", len(rows), auctionID)
            return jsonify(rows)

    except (Exception, pg.DatabaseError) as error:
        logger.error("There was an error : %s", error)
        return jsonify({"code": INTERNAL_SERVER_CODE, "error": str(error)})
    finally:
        if conn is not None:
            conn.close()

######################################################################################
###############################    ADMIN OPERATIONS    ###############################
######################################################################################

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
    put_notification_stmt = "INSERT INTO notification(content, time_date) VALUES (%s, %s);"
    get_notification_id_stmt = "SELECT MAX(id) FROM notification;"
    associate_notification_stmt = "INSERT INTO inbox_messages(notification_id, person_id) VALUES (%s, %s);"

    with create_connection() as conn:
        try:
            # Create a view over the database
            with conn.cursor() as cursor:
                # Cancel Auction
                cursor.execute(cancel_auction_stmt, [content["id"]])

                # Create Notification
                logger.info("Creating notification")
                cursor.execute(put_notification_stmt, [
                               "The auction was cancelled by the application administrator", datetime.now()])

                # Get notification ID
                cursor.execute(get_notification_id_stmt)
                notification_id = cursor.fetchall()[0][0]

                # Notify all auction-related users
                logger.info("Notifying users")
                cursor.execute(get_auction_people_ids_stmt, [content["id"]])
                people_ids = cursor.fetchall()

                for entry in people_ids:
                    cursor.execute(associate_notification_stmt,
                                   [notification_id, entry[0]])

                # Make Changes Permanent
                conn.commit()

                # return response
                logger.info("Auction cancel operation successful")
                return jsonify({"response": "Successful", "code": SUCCESS_CODE})

        except (Exception, pg.DatabaseError) as error:
            logger.error("There was an error : %s", error)
            return jsonify({"error": str(error), "code": INTERNAL_SERVER_CODE})

# Ban User Endpoint
@app.route("/admin/ban", methods=['POST'])
@auth_user
def ban_user():
    return

# App Statistics Endpoint
@app.route("/admin/stats", methods=['GET'])
@auth_user
def statistics():
    return


########################################################################################
##################################### MAIN #############################################
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

    # create formatter
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s]:  %(message)s', '%H:%M:%S'
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    time.sleep(1)
    logger.info("\n-------- Everything seems to be working ----------\n"
                "-------- Docker: http://localhost:8080/ ----------\n"
                "-------- Native: http://localhost:5000/ ----------\n"
                )
    app.run(host="0.0.0.0",  debug=True, threaded=True)
