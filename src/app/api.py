from flask import Flask, jsonify, request
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
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Error: Token is missing!', 'code': UNAUTHORIZED_CODE})
        try:
            logger.debug(token)
            jwt.decode(token, app.config['SECRET_KEY'])
        except Exception as e:
            logger.debug(e)
            return jsonify({'message': 'Error: Invalid token', 'code': FORBIDDEN_CODE})
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
    cur = conn.cursor()

    if "username" not in content or "password" not in content:
        return jsonify({"Error": 'Invalid Parameters in call'})
    logger.info(f'Request Content: {content}')

    statement1 = """
                SELECT person_id
                FROM users
                WHERE person_username = %s AND person_password = %s
                """
    statement2 = """
                SELECT person_id
                FROM administrator
                WHERE person_username = %s AND person_password = %s
                """

    values = (content["username"], content["password"])

    try:
        res = cur.execute(statement1, values)
        rows = cur.fetchall()
        if(len(rows) != 0):
            row = rows[0]
            token = jwt.encode({
                'person_id': row[0],
                'is_admin': False,  # This is a bad bad security flaw, should be fixed in the future
                # Defaulting for a 24 hr token
                'expiration': str(datetime.utcnow() + timedelta(hours=24))
            }, app.config['SECRET_KEY'])
            logger.info(token)
            return {'token': token.decode('utf-8')}
    except (Exception, pg.DatabaseError) as error:
        logger.error("Request not found in user database, checking admin")
        logger.error(error)
    finally:
        if conn is not None:
            conn.close()

    try:
        res = cur.execute(statement2, values)
        rows = cur.fetchall()
        if(len(rows) != 0):
            row = rows[0]
            token = jwt.encode({
                'person_id': row[0],
                'is_admin': True,  # This is a bad bad security flaw, should be fixed in the future
                # Defaulting for a 24 hr token
                'expiration': str(datetime.utcnow() + timedelta(hours=24))
            }, app.config['SECRET_KEY'])
            logger.info(token)
            return jsonify({'token': token.decode('utf-8')})
    except (Exception, pg.DatabaseError) as error:
        logger.error("Request not found in user database, checking admin")
        return jsonify({"Error": 'User not Found'}, 404)

    finally:
        if conn is not None:
            conn.close()

@app.route("/user", methods = ['GET'])
def print_users():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password, email, banned FROM person;")
        rows = cursor.fetchall()
        return "<h2>Users</h2>" + str(rows).strip("[()]").replace("), (","<br/>")
    except:
        return "Not Found :("
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
        return jsonify({'message': 'Error: Invalid Parameters in call', 'code': BAD_REQUEST_CODE})


    logger.info(f'Request Content: {content}')

    put_person_stmt = """
                INSERT INTO
                person (username, password, email)
                VALUES
                (%s, %s, %s); 
                """
    get_person_id_stmt = """
                SELECT person_id
                FROM users
                WHERE person_username = %s
                """

    put_user_stmt = " INSERT INTO users(person_id) VALUES (%s);"

    values = [content["username"], content["password"], content["email"]]

    try:
        # Put Person in person table
        cursor.execute(put_person_stmt, values)
        
        # Get system-assigned personID
        cursor.execute(get_person_id_stmt, [values[0]])
        rows = cursor.fetchall()
        logger.info("rows: "+ rows) #remove
        
        # Put User in users table
        cursor.execute(put_user_stmt, [rows[0][0]])
        
        # Make Changes Permanent
        conn.commit()
        
        logger.info("Insert user successfully into the database Username: %s , Password: %s, email: %s, is_Admin : false", *values)
        return jsonify({"userId": str(rows[0][0])})

    except (Exception, pg.DatabaseError) as error:
        logger.error("There was an error : %s", error)
        return jsonify({"error": str(error)})
    finally:
        if conn is not None:
            conn.close()

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
                        help="the database username")

    parser.add_argument("-p", "--db-password", type=str,
                        help="the user password")

    parser.add_argument("-D", "--db-database", type=str,
                        help="the database to connect to")

    parser.add_argument("-P", "--db-port", type=int,
                        help="the port where the DBMS is running")

    parser.add_argument("-H", "--db-hostname", type=str,
                        help="the hostname where the DBMS is running")

    if len(sys.argv) == 1:
        parser.print_help()
        parser.exit()

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
