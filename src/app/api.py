from os import error
from flask import Flask, json, jsonify, request
from datetime import datetime, timedelta
from functools import wraps

import psycopg2 as pg
import logging
import sys
import time
import argparse
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'it\xb5u\xc3\xaf\xc1Q\xb9\n\x92W\tB\xe4\xfe__\x87\x8c}\xe9\x1e\xb8\x0f'
auth = None

'''     Error   Codes      '''
BAD_REQUEST_CODE = 400
UNAUTHORIZED_CODE = 401
FORBIDDEN_CODE = 403
NOT_FOUND_CODE = 404
INTERNAL_SERVER_CODE = 500

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


'''     Endpoints       '''

# Root Endpoint
@app.route('/')
def hello():
    return "Well, the description has was too big, but it is working"


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
            # This is a bad bad security flaw, should be fixed in the future
            'is_admin': False,
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


# Database Connection Establishment
def create_connection():
    return pg.connect(user=auth.db_username,
                      password=auth.db_password,
                      host=auth.db_hostname,
                      port=auth.db_port,
                      database=auth.db_database)


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
