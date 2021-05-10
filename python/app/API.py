from flask import Flask, jsonify, request
from datetime import datetime, timedelta
from functools import wraps
import logging
import psycopg2
import time
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'it\xb5u\xc3\xaf\xc1Q\xb9\n\x92W\tB\xe4\xfe__\x87\x8c}\xe9\x1e\xb8\x0f'


@app.route('/')
def hello():
    return """

    Hi there!<br/>
    <br/>
    How did you get here?<br/>
    <br/>
    Anyway, this is the home page, in the future, all the documentarion required to run this app will be listen in here<br/>
    <br/>
    """


def auth_user(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Error': 'Token is missing!'}), 401

        try:
            logger.debug(token)
            jwt.decode(token, app.config['SECRET_KEY'])
        except Exception as e:
            logger.debug(e)
            return jsonify({'Message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return decorated


# Authenticate a user
@app.route("/dbproj/user", methods=['PUT'])
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
                'is_admin': 'false',  # This is a bad bad security flaw, should be fixed in the future
                # Defaulting for a 24 hr token
                'expiration': str(datetime.utcnow() + timedelta(hours=24))
            },
                app.config['SECRET_KEY'])
            logger.info(token)
            return {'token': token.decode('utf-8')}
    except (Exception, psycopg2.DatabaseError) as error:
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
                'is_admin': true,  # This is a bad bad security flaw, should be fixed in the future
                # Defaulting for a 24 hr token
                'expiration': str(datetime.utcnow() + timedelta(hours=24))
            },
                app.config['SECRET_KEY'])
            logger.info(token)
            return jsonify({'token': token.decode('utf-8')})
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error("Request not found in user database, checking admin")
        return jsonify({"Error": 'User not Found'}, 404)

    finally:
        if conn is not None:
            conn.close()

# Register user (Can't register a user via webapp)


@app.route("/dbproj/user", methods=['POST'])
def create_user():
    logger.info("Authenticating a user")
    content = request.get_json()

    conn = create_connection()
    cursor = conn.cursor()

    if "username" not in content or "password" not in content or "email" not in content:
        return jsonify({"Error": 'Invalid Parameters in call'})

    logger.info(f'Request Content: {content}')

    statement = """
                INSERT INTO 
                users(person_username, person_password,person_email) 
                VALUES 
                (%s, %s, %s);
                """
    statement2 = """
                SELECT person_id
                FROM users
                WHERE person_username = %s
                """

    values = (content["username"], content["password"], content["email"])

    try:
        cursor.execute(statement, values)

        conn.commit()
        logger.info("Insert user successfully into the database Username : %s , Password : %s , email : %s , is_Admin : false" , values[0], values[1], values[2])
        cursor.execute(statement2, [values[0]])
        rows = cursor.fetchall()
        return jsonify({"userId": str(rows[0][0])})

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error("There was an error : %s", error)
        return jsonify({"Error": str(error)})
    finally:
        if conn is not None:
            conn.close()



def create_connection():
    db = psycopg2.connect(user="admin",
                          password="admin",
                          host="db",
                          port="5432",
                          database="project")
    return db


if __name__ == "__main__":

    # Set up the logging
    logging.basicConfig(filename="logs/log_file.log")
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]:  %(message)s',
                                  '%H:%M:%S')
    # "%Y-%m-%d %H:%M:%S") # not using DATE to simplify
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    time.sleep(1)  # just to let the DB start before this print :-)

    logger.info("\n------Everything seems to be working ----------\n" +
                "-----------http://localhost:8080/--------------\n")

    app.run(host="0.0.0.0", debug=True, threaded=True)
