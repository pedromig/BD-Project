# BD-Project

![APM](https://img.shields.io/apm/l/vim-mode)
![BUILD](https://img.shields.io/badge/build-passing-green)

## About the project

Project for the Databases subject of the Informatics Engineering course @University of Coimbra

The aim of this project is to provide students with experience in developing database systems. The project
is oriented by the industry’s best practices for software development; thus, students will experience all the
main stages of a common software development project, from the very beginning to delivery.

This project consists of developing a typical auction system, supported by a
database management system. An auction is initiated by a seller who defines
an item, indicates the minimum price you are willing to receive, and decides when
that the auction will end (date, hour and minute). Buyers place bids that
successively increase the price until the end of the auction. Wins the
buyer who bids the highest amount.

The system must be made available through a REST API that allows the user to access the system
through HTTP requests (when content is needed, JSON should be used). The figure represents a
simplified view of the system to be developed. As we can see, the user interacts with the web
server through the exchange of REST request / response and in turn the web server interacts with the
database through an SQL interface.

## Index

- [BD-Project](#bd-project)
  - [About the project](#about-the-project)
  - [Index](#index)
  - [Technologies Used](#technologies-used)
  - [Project Structure](#project-structure)
  - [Native Installation](#native-installation)
    - [Tools Installation](#tools-installation)
    - [Database Setup](#database-setup)
    - [Running the Application](#running-the-application)
  - [Docker Support](#docker-support)
    - [Docker and docker-compose Installation](#docker-and-docker-compose-installation)
    - [Image Installation and Container Creation](#image-installation-and-container-creation)
      - [Using docker-compose](#using-docker-compose)
      - [Manually](#manually)
    - [Interacting with The REST API and Database Containers](#interacting-with-the-rest-api-and-database-containers)
      - [Database Container](#database-container)
      - [Web Server (REST API) Container](#web-server--rest-api--container)
    - [Useful Docker Commands](#useful-docker-commands)
  - [Dragon Server](#dragon-server)
  - [Project Features](#project-features)
    - [Database Design](#database-design)
    - [REST API Specification](#rest-api-specification)
    - [User Endpoints](#user-endpoints)
      - [User Registration](#user-registration)
      - [User Authentication](#user-authentication)
      - [User Listing](#user-listing)
      - [User Activity](#user-activity)
      - [User Inbox](#user-inbox)
      - [User Licitation](#user-licitation)
      - [User Message Posting](#user-message-posting)
      - [User Message Listing](#user-message-listing)
      - [User Auction Editing](#user-auction-editing)
    - [Auction Endpoints](#auction-endpoints)
      - [Auction Creation](#auction-creation)
      - [Auction Listing](#auction-listing)
      - [Auction Searching](#auction-searching)
      - [Auction Details](#auction-details)
    - [Administrator Endpoints](#administrator-endpoints)
      - [User Ban](#user-ban)
      - [Auction Cancellation](#auction-cancellation)
      - [Application Statistics](#application-statistics)
  - [Authors](#authors)

## Technologies Used

1. Programming Languages
   - Python
   - SQL and PL/pgSQL
2. Database Management System
   - PostgreSQL
3. Python Libraries
   - Flask
   - Psycopg2
4. Other Technologies
   - [Curl](https://curl.se/)
   - [Onda](http://onda.dei.uc.pt/v3/)
   - [Docker](https://www.docker.com/)
   - [Postman](https://postman.com/)

## Project Structure

```txt
.
├── docs
│  ├── deliverables
│  │  ├── meta1.zip
│  │  └── meta2.zip
│  ├── db_project.pdf
│  └── README.pdf
├── scripts
│  ├── clean.sh
│  ├── compose.sh
│  ├── compose.yml
│  └── unittester.py
├── src
│  ├── app
│  │  ├── templates
│  │  │  ├── ERD_conceptual.png
│  │  │  ├── ERD_physical.png
│  │  │  └── index.md
│  │  ├── api.py
│  │  └── Dockerfile
│  └── db
│     ├── clear.sql
│     ├── data.sql
│     ├── Dockerfile
│     ├── schema.sql
│     └── triggers.sql
├── LICENSE
├── README.md
└── REQUIREMENTS.txt
```

## Native Installation

If you choose to install and run the application and all its tools natively please follow these instructions.

`NOTE:` The native installation allows you to have more control over the application and database configurations but if you are looking to try the application and you don't want to worry about all the small configuration details, this project has docker support allowing you build pre-configured images and create containers that will run this application components with little or no configuration. To know how you use them check the [Docker Support](#docker-support) chapter.

### Tools Installation

In order to run this project it is required to have an installation of a python interpreter `python3` or `pypy3` the python package installer `pip` and the `curl` or `postman` tool which provides the same functionality as curl but is being more GUI oriented.
In our project we are opting to use the python3 interpreter and the curl tool. These programs can be installed using your operating system package manager as shown bellow for some Linux distributions and MacOS.

```bash
# MacOS:
brew install python3 curl

# CentOS:
sudo yum install python3 python3-pip curl

# Ubuntu/Debian
sudo apt install python3 python3-pip curl

# Fedora:
sudo dnf install python3 python3-pip curl

# OpenSUSE:
sudo zypper install python3 python3-pip curl

# Arch Linux:
sudo pacman -S python python-pip curl
```

In case of Windows/MacOS machines it is possible to install the software via a graphical installer. For more information about the download installation of python3, pip, curl and postman check the following websites:

- [Python](https://www.python.org/downloads/)
- [Pip](https://pip.pypa.io/en/stable/installing/)
- [Curl](https://curl.se/download.html)
- [Postman](https://postman.com/)

To store information this project uses the PostgreSQL Database management system. This DBMS can be installed using your operating system package manager as shown bellow for a debian based Linux distributions.

```bash
# Create the file repository configuration:
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

# Import the repository signing key:
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# Update the package lists:
sudo apt-get update

# Install the latest version of PostgreSQL.
# If you want a specific version, use 'postgresql-12' or similar instead of 'postgresql':

# In this case we are installing it on a debian based distro,
sudo apt-get -y install postgresql psql
```

If you have a machine running any other linux distributions, check the postgreSQL website to see how you can install this software in your machine. In the case MacOS or Windows you can find graphical based installers. To to know more about the installation process and options of this DBMS this link will point you to the postgreSQL official installation page.

- [PostgreSQL](https://www.postgresql.org/download/)

In the project implementation a few python libraries are used, namely: Flask to set up a REST web service and Psycogp2 in order to interact with a postgreSQL database. To see more about them check the links bellow:

- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [Psycogp2](https://www.psycopg.org/)

To install all the python libraries described above run the following command on the [REQUIREMENTS.txt](REQUIREMENTS.txt) file:

```bash
python3 -m pip install -r REQUIREMENTS.txt
```

### Database Setup

After the native installation of all the tools you are almost ready to begin using the application's REST API. Before that you will need to create and setup your native postgreSQL installation and the web server where the REST service will run.
To setup de database you need to access your postgreSQL DMBS with a client like `psql` or `pgadmin4` in order to create a new user and database to host all the application's data. The following instructions show you how you can do this using the `psql` client (that was installed along with postgreSQL).

```bash
# Use psql to login to the default superuser account on your DBMS.
# This information can be changed after should you wish to make
# the native installation more secure

# Default superuser account information
# Username: postgres
# Password: postgres

psql -h localhost -p 5432 -U postgres
```

```sql
-- Create a database to be used by the application
-- As an example we are going to create a database called dbauction

CREATE DATABASE dbauction;

-- We will also create a example user with regular privileges so we
-- don't have to access our database with only the root user.

CREATE USER example PASSWORD '123';
EXIT
```

```bash
# Now to configure the database just access it with your recently created user.

# Database: dbauction

# Example user account information
# Username: example
# Password: 123

psql -h localhost -p 5432 -U example -d dbauction

\i src/db/schema.sql       # The database table schema
\i src/db/data.sql         # Some example data
```

`IMPORTANT: Add all the SQL files that we are still going to make as the project grows bigger`

### Running the Application

After all the configuration of the database is time to run our web server making the REST API accessible to the outside world. To do that just run the [api.py](src/app/api.py) file providing it the required arguments .The arguments consist of a database name, host and port we want to connect to, where we can store and retrieve information and a the user credentials (username and password) necessary to access it. To see which arguments to pass check the help text of the program by executing it with no arguments.

```bash
# To see the usage help text

python3 api.py

# Example usage (using the database and user created for demonstration)

# Username: example
# Password: 123
# Database Name: dbauction
# Machine Hostname: localhost
# Database Port: 5432

python3 api.py -u example -p 123 -D dbauction -H localhost -P 5432
```

Once we execute the [api.py](src/app/api.py) after all this setup the web server that will provide the REST service will be started and will run in the host machine until the program is stopped. By default a flask web server will run on port 5000, in order to interact with it we can use a web browser or make curl/postman calls to the following URL or other URLs derived from this one and described in the REST API endpoint specification.

```http
http://localhost:5000/
```

## Docker Support

Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly. With Docker, you can manage your infrastructure in the same ways you manage your applications. By taking advantage of Docker’s methodologies for shipping, testing, and deploying code quickly, you can significantly reduce the delay between writing code and running it in production.

The components of this project such as the PostgreSQL database and REST API service (that will be provided via flask web server/application) can be ran in docker containers instead natively in your machine. The docker images are already pre-configured saving you the trouble of installing all the software natively in your machine.

### Docker and docker-compose Installation

The docker and docker-compose can be installed using your operating system package manager as shown bellow for a debian based Linux distribution (for other distributions the process is similar).

```bash
## INSTALL DOCKER (debian based distro)

sudo apt-get update

sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
    | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
```

In case of Windows/MacOS machines it is possible to install the software
via a graphical installer. For more information about the download installation of docker and docker-compose tools check the following links.

- [docker](https://docs.docker.com/engine/install/)
- [docker-compose](https://docs.docker.com/compose/install/)

### Image Installation and Container Creation

In order to install the images, create containers and run them in your machine you have multiple ways to do it:

#### Using docker-compose

You can use the docker-compose tool to automate the build process of docker images. This docker file follows a list of recipes specified in .yml file and that tells docker how should the images be built which images depend on which, the volumes to mount, the ports to expose, etc... For this project a docker-compose configuration file ([compose.yml](scripts/compose.yml)) has already been made. You can add more information to it should you wish to configure it even more so it fits your needs. The following examples show example usage of the script

In order to build this particular project you can issue the following commands.

```bash
   mkdir -p ../src/app/logs
   docker-compose -f compose.yml up --build
```

These commands will create a "logs" file where the REST API server logs will be placed and will assemble the app and db images (downloading the necessary components) create containers for both of them and run them (in foreground) until you issue a SIGINT and stop the process. For ease of use we added the script [compose.sh](scripts/compose.sh) which allows you to execute these commands and add more options

```bash
   # Give the user permission to execute this script
   chmod u+x compose.sh

    # Executes the commands shown above (default behaviour)
   ./compose.sh

   # Use the --no-start option to compose the images only
   # This command installs the images only
   ./compose.sh --no-start


   # Use the -d option to compose the images and run
   # containers from those images in the background
   ./compose.sh -d
```

`NOTE:` After you run the docker-compose command or script the db and auction-web-app images and will be installed in your system and the containers from those images will be created too. The next time you want to run a container from those images please consider using `docker start -ai {container_name}` to avoid the creation of a new image/container equal to the already installed/created. Just keep in mind that the database container must be started before the auction-rest-api. Use `docker stop {container_name}` to stop the containers.

#### Manually

You can build the images and run the containers manually should you although it might be error prone since something can go wrong with the configuration. We highly discourage this usage since its safer to build the images and run containers by following the instructions in the docker compose file. The examples bellow show a the same configuration that you get when using docker-compose but executed manually.

```bash
   # Build docker images
   docker build -t  auction-rest-api:latest  /src/app
   docker build -t  db:latest  /src/db

   # Create a logs folder
   mkdir -p logs

   # Run docker images
   docker run --name db -p 6000:5432 db:latest
   docker run --name auction-rest-api -p 8080:5000
               \ -v logs:/app/logs auction-rest-api:latest
```

### Interacting with The REST API and Database Containers

Once you get the containers running the REST API and database will be accessible through an exposed port in your systems localhost. Assuming that you followed these instructions you can access the containers like this:

`ǸOTE:` Always Keep in mind that the database container must be started before the auction-rest-api

#### Database Container

The database is exposed by the docker container in the port 6000 of your host machine to access it use psql, pgadmin4 or any other postgreSQL client

```bash
# Example: Accessing the database with the superuser

# Database Name: dbauction
# Database Exposed port: 6000

# Example user account information
# Username: admin
# Password: admin

psql -h localhost -p 6000 -U admin -d dbauction
```

#### Web Server (REST API) Container

The REST API exposed by the docker container in the port 8080 of your host machine, in order to interact with it we can use a web browser or make curl/postman calls to the following URL or other URLs derived from this one and described in the REST API endpoint specification.

```http
http://localhost:8080/
```

### Useful Docker Commands

Here is a list of docker commands that might be useful

```bash
   # To see all the available commands do
   docker --help

   # To start a container do
   docker start {container}

   # To stop a container
   docker stop {container}

   # To run a container from an image
   docker run {image}

   # To list all running containers do
   docker ps

   # To list all running and stopped containers do
   docker ps -a

   # To see all the images installed in your system do
   docker images

   # To remove a image do
   docker rmi {image_name}

   # To forcefully remove all images do
   docker image prune -f

   # To remove a docker container do
   docker rm {container_name}

   # To forcefully remove all containers do
   docker container prune

   # To start a container and attach to STDIN && STDOUT
   docker start -ai {container}
```

## Dragon Server

The project will be available in our server. To access the REST API access the following link:

```http
http://dragonserver.ddns.net:8080/
```

## Project Features

### Database Design

- Conceptual Diagram (Onda)

![conceptual-erd](./src/app/templates/ERD_conceptual.png)

- Physical Diagram (Onda)

![physical-erd](./src/app/templates/ERD_physical.png)

### REST API Specification

---

---

### User Endpoints

---

#### User Registration

**Description**: Registration of a new user in the application's database.  
**URL** : `/user`  
**Method** : `POST`  
**Authentication required** : `NO`  
**Permissions required** : `None`

##### Request Parameters

- username
- password
- email

##### Success Response

**Content** : The id of the user that was inserted in the application's database.  
**Code**: `201 Created`

```json
{
  "code": 201,
  "id": 12829371
}
```

##### Error Responses

**Condition** : An internal server error  
**Code** : `500 Internal Server Error`  
**Content** : An error message with the error code and error details

```json
{
  "error": " ***Error details*** ",
  "code": 500
}
```

**or**  
**Condition** : Missing parameters  
**Code** : `400 Bad Request`  
**Content** : An error message with the error code and error details

```json
{
  "error": "Invalid Parameters in call",
  "code": 400
}
```

##### Curl Query Example

```bash
curl -X POST http://localhost:8080/user
     -H "Content-Type: application/json"
     -d '{ "username": "example", "password": "123",
     "email":"example@gmail.com"}'
```

---

#### User Authentication

**Description**: User authentication with username and password.  
**URL** : `/user`  
**Method** : `PUT`  
**Authentication required** : `NO`  
**Permissions required** : `None`

##### Request Parameters

- username
- password

##### Success Response

**Content** : An authentication token at that must be included in subsequent calls to REST API methods/resources that require a prior user authentication.  
**Code**: `200 OK`

```json
{
  "code": 200,
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9 (...)"
}
```

##### Error Responses

**Condition** : User not found in the database  
**Code** : `404 Not Found`  
**Content** : An error message with the error code and error details

```json
{
  "error": "User not Found ",
  "code": 404
}
```

**or**

**Condition** : Missing parameters  
**Code** : `400 Bad Request`  
**Content** : An error message with the error code and error details

```json
{
  "error": "Invalid Parameters in call",
  "code": 400
}
```

**or**

**Condition** : User was already banned  
**Code** : `403 Not Forbidden`  
**Content** : An error message with the error code and error details

```json
{
  "error": "This user is banned",
  "code": 404
}
```

##### Curl Query Example

```bash
curl -X PUT http://localhost:8080/user \
     -H "Content-Type: application/json" \
     -d '{"username": "example", "password": "123"}'
```

---

#### User Listing

**Description**: Lists all the users that are registered in the application's database  
**URL** : `/users`  
**Method** : `GET`  
**Authentication required** : `YES`  
**Permissions required** : `None`

##### Request Parameters

- token

##### Success Response

**Content** : A json with all users data recorded in the database.  
**Code**: `200 OK`

```json
[
  {
    "banned": false,
    "email": "admin@gmail.com",
    "id": 1,
    "username": "admin"
  },
  {
    "banned": false,
    "email": "tdelgardo0@de.vu",
    "id": 2,
    "username": "dalliband0"
  },
  {
    "banned": false,
    "email": "dfrizzell1@elegantthemes.com",
    "id": 3,
    "username": "cmonshall1"
  },
  {
    "code": 200
  }
]
```

##### Error Responses

**Condition** : Missing token parameter  
**Code** : `401 Unauthorized`  
**Content** : An error message with the error code and error details

```json
{
  "code": 401,
  "error": "Token is missing!"
}
```

**or**

**Condition** : Invalid or malformed token was provided  
**Code** : `403 Forbidden`  
**Content** : An error message with the error code and error details

```json
{
  "code": 403,
  "error": "Invalid token"
}
```

**or**

**Condition** : An internal server error  
**Code** : `500 Internal Server Error`  
**Content** : An error message with the error code and error details

```json
{
  "error": "Could not fetch users data/message (dependant on type of internal error)",
  "code": 500
}
```

##### Curl Query Example

```bash
curl -X GET "http://localhost:8080/users"  \
     -H "Content-Type: application/json"   \
     -d '{ "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9 (...)" }'
```

---

#### User Activity

**URL** : `/user/activity`  
**Description**: List auctions where a user had any activity, either as creator of the auction or as a bidder. This listing summarizes the details of each auction (auction id and auction description).  
**Method** : `GET`  
**Authentication required** : `YES`  
**Permissions required** : `None`

##### Request Parameters

- token

##### Success Response

**Content** : The list of auction ids and descriptions of the auctions where the user has bid or has created.  
**Code**: `200 OK`

```json
[
  {
    "description": "Donec quis orci eget orci vehicula condimentum.",
    "id": 1
  },
  {
    "description": "Nulla ac enim.",
    "id": 2
  },
  {
    "description": "Vestibulum ac est lacinia nisi venenatis tristique.",
    "id": 14
  },
  {
    "code": 200
  }
]
```

##### Error Responses

**Condition** : Missing token parameter  
**Code** : `401 Unauthorized`  
**Content** : An error message with the error code and error details

```json
{
  "code": 401,
  "error": "Token is missing!"
}
```

**or**

**Condition** : Invalid or malformed token was provided  
**Code** : `403 Forbidden`  
**Content** : An error message with the error code and error details

```json
{
  "code": 403,
  "error": "Invalid token"
}
```

**or**

**Condition** : The query to the database for the user activity failed  
**Code** : `500 Internal Server Error`  
**Content** : An error message with the error code and error details

```json
{
  "error": "Error message (dependant on type of internal error)",
  "code": 500
}
```

##### Curl Query Example

```bash
curl -X GET "http://localhost:8080/user/activity" \
     -H "Content-Type: application/json" \
     -d '{ "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9 (...)" }'
```

---

#### User Inbox

**URL** : `/user/inbox`  
**Description**: List all the messages/notifications that a given user has in its inbox.  
**Method** : `GET`  
**Authentication required** : `YES`  
**Permissions required** : `None`

##### Request Parameters

- token

##### Success Response

**Content** : All the messages in the user inbox  
**Code**: `200 OK`

```json
[
  {
    "date": "Sun, 30 May 2021 23:34:48 GMT",
    "message": "hello",
    "was_read": true
  },
  {
    "date": "Sun, 30 May 2021 23:34:48 GMT",
    "message": "again",
    "was_read": false
  },
  {
    "date": "Sun, 30 May 2021 23:34:48 GMT",
    "message": "world",
    "was_read": false
  },
  {
    "code": 200
  }
]
```

##### Error Responses

**Condition** : Missing token parameter  
**Code** : `401 Unauthorized`  
**Content** : An error message with the error code and error details

```json
{
  "code": 401,
  "error": "Token is missing!"
}
```

**or**

**Condition** : Invalid or malformed token was provided  
**Code** : `403 Forbidden`  
**Content** : An error message with the error code and error details

```json
{
  "code": 403,
  "error": "Invalid token"
}
```

**or**

**Condition** : The query to the database for the user inbox failed  
**Code** : `500 Internal Server Error`  
**Content** : An error message with the error code and error details

```json
{
  "error": "Error message (dependant on type of internal error)",
  "code": 500
}
```

##### Curl Query Example

```bash
curl -X GET "http://localhost:8080/user/inbox" \
     -H "Content-Type: application/json" \
     -d '{ "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9 (...)"}'
```

---

#### User Licitation

**URL** : `/licitation/<auctionID>`  
**Description**: A user can bid with a higher price on a particular
auction, as long as the auction has not ended and there is no higher bid.
to do and is at least higher than the minimum price.  
**Method** : `PUT`  
**Authentication required** : `YES`  
**Permissions required** : `None`

##### Request Parameters

- token
- price

##### Success Response

**Code** : `201 Created`  
**Content** : A message indication a successful operation

```json
{
  "code": 201,
  "response": "Successful"
}
```

##### Error Responses

**Condition** : Missing parameters  
**Code** : `400 Bad Request`  
**Content** : An error message with the error code and error details

```json
{
  "error": "Missing Parameters in call",
  "code": 400
}
```

**or**

**Condition** : Invalid parameters (such has non-float amount, non-int auction, not existant auction)  
**Code** : `400 Bad Request`  
**Content** : An error message with the error code and error details

```json
{
  "error": "Invalid Parameters in call",
  "code": 400
}
```

**or**

**Condition** : Amount Lower Than Allowed  
**Code** : `400 Bad Request`  
**Content** : An error message with the error code and error details

```json
{
  "error": "Invalid Amount (Lower Than Allowed)",
  "code": 400
}
```

**Condition** : Missing token parameter  
**Code** : `401 Unauthorized`  
**Content** : An error message with the error code and error details

```json
{
  "code": 401,
  "error": "Token is missing!"
}
```

**or**

**Condition** : Invalid or malformed token was provided  
**Code** : `403 Forbidden`  
**Content** : An error message with the error code and error details

```json
{
  "code": 403,
  "error": "Invalid token"
}
```

**or**

**Condition** : Something went wrong when accessing the database.  
**Code** : `500 Internal Server Error`  
**Content** : An error message with the error code and error details

```json
{
  "error": "Error message (dependant on type of internal error)",
  "code": 500
}
```

##### Curl Query Example

```bash
curl -X PUT http://localhost:8080/licitation/5 \
     -H "Content-Type: application/json" \
     -d '{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9 (...)", "price": '252'}'
```

---

#### User Message Posting

**URL** : `/auction/<auctionID>/mural`  
**Description**: The auction's mural on which is to be written comments, questions and clarifications regarding the auction.  
**Method** : `POST`  
**Authentication required** : `YES`  
**Permissions required** : `None`

##### Request Parameters

- message
- token

##### Success Response

**Code** : `201 Created`  
**Content** : String saying Success

```json
{
  "code": 201,
  "response": "Successful"
}
```

##### Error Responses

**Condition** : Non-int auctionID  
**Code** : 404  
**Content** : String message response with error

```json
{
  "code": 404,
  "error": "Invalid auctionID"
}
```

**or**

**Condition** : Missing parameters  
**Code** : `400 Bad Request`  
**Content** : An error message with the error code and error details

```json
{
  "error": "Invalid Parameters in call",
  "code": 400
}
```

**Condition** : Missing token parameter  
**Code** : `401 Unauthorized`  
**Content** : An error message with the error code and error details

```json
{
  "code": 401,
  "error": "Token is missing!"
}
```

**or**

**Condition** : Invalid or malformed token was provided  
**Code** : `403 Forbidden`  
**Content** : An error message with the error code and error details

```json
{
  "code": 403,
  "error": "Invalid token"
}
```

**or**

**Condition** : Something went wrong when accessing the database.  
**Code** : `500 Internal Server Error`  
**Content** : An error message with the error code and error details

```json
{
  "error": "Error message (dependant on type of internal error)",
  "code": 500
}
```

##### Curl Query Example

```bash
curl -X POST http://localhost:8080/2/mural \
     -H "Content-Type: application/json" \
     -d '{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9 (...)", "message": "One ring to rule them all"}'

```

---

#### User Message Listing

**URL** : `/auction/<auctionID>/mural`  
**Description**: Lists all Messages in the message board.  
**Method** : `GET`  
**Authentication required** : `YES`  
**Permissions required** : `None`

##### Request Parameters

- token

##### Success Response

**Code** : `200 OK`  
**Content** : List of all messages in the message board

```json
[
  {
    "message": "Vivamus tortor.",
    "time_date": "Sun, 30 May 2021 18:53:52 GMT",
    "username": "kpelchatc"
  },
  {
    "message": "Maecenas rhoncus aliquam lacus.",
    "time_date": "Sun, 30 May 2021 18:53:52 GMT",
    "username": "trudledgen"
  },
  {
    "message": "In eleifend quam a odio.",
    "time_date": "Sun, 30 May 2021 18:53:52 GMT",
    "username": "sshenleyh"
  },
  {
    "code": 200
  }
]
```

##### Error Responses

**Condition** : Non-int auctionID  
**Code** : `404 Not Found`  
**Content** : String message response with error

```json
{
  "code": 404,
  "error": "Invalid auctionID"
}
```

**or**

**Condition** : Int-valid but non-existant auction or internal server error.  
**Code** : `500 Internal Server Error`  
**Content** : An error message with the error code and error details

```json
{
  "code": 500,
  "error": "Error message (dependant on type of internal error)"
}
```

**or**

**Condition** : Missing parameters  
**Code** : `400 Bad Request`  
**Content** : An error message with the error code and error details

```json
{
  "error": "Invalid Parameters in call",
  "code": 400
}
```

**Condition** : Missing token parameter  
**Code** : `401 Unauthorized`  
**Content** :

```json
{
  "code": 401,
  "error": "Token is missing!"
}
```

**or**

**Condition** : Invalid or malformed token was provided  
**Code** : `403 Forbidden`  
**Content** :

```json
{
  "code": 403,
  "error": "Invalid token"
}
```

**or**

**Condition** : Something went wrong when accessing the database.  
**Code** : `500 Internal Server Error`  
**Content** : An error message with the error code and error details

```json
{
  "error": "Error message (dependant on type of internal error)",
  "code": 500
}
```

##### Curl Query Example

```bash
curl -X GET http://localhost:8080/2/mural \
     -H "Content-Type: application/json" \
     -d '{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9 (...)" }'

```

---

#### User Auction Editing

**URL** : `/auction/<auctionID>`  
**Description**: The auction's owner can adjust all textual descriptions related to a
auction. All previous versions must be kept and can be consulted later for reference  
**Method** : `PUT`  
**Authentication required** : `YES`  
**Permissions required** : `Auction Ownership`

##### Request Parameters

- token
- title (optional)
- item_description (optional)
- auction_description (optional)

##### Success Response

**Code** : `201 Created`  
**Content** : String saying Success

```json
{
  "code": 201,
  "response": "Successful"
}
```

##### Error Responses

**Condition** : The user does not have permissions to edit the auction.  
**Code** : `401 Unauthorized`  
**Content** : An error message with the error code and error details

```json
{
  "code": 401,
  "error": "The user is not the auction's owner"
}
```

**or**

**Condition** : Missing token parameter  
**Code** : `401 Unauthorized`  
**Content** : An error message with the error code and error details

```json
{
  "code": 401,
  "error": "Token is missing!"
}
```

**or**

**Condition** : Invalid or malformed token was provided  
**Code** : `403 Forbidden`  
**Content** : An error message with the error code and error details

```json
{
  "code": 403,
  "error": "Invalid token"
}
```

**or**

**Condition** : Something went wrong when accessing the database.  
**Code** : `500 Internal Server Error`  
**Content** : An error message with the error code and error details

```json
{
  "error": "Error message (dependant on type of internal error)",
  "code": 500
}
```

##### Curl Query Example

```bash
curl -X PUT http://localhost:8080/auction/2 \
     -H "Content-Type: application/json" \
     -d '{ "title": "hello", "item_description": "world", "auction_description": "again", "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9 (...)"}'
```

---

---

### Auction Endpoints

---

#### Auction Creation

**URL** : `/auction`  
**Description**: Creation of a new auction in the application's database.  
**Method** : `POST`  
**Authentication required** : `YES`  
**Permissions required** : `None`

##### Request Parameters

- token

##### Success Response

**Code** : `201 Created`  
**Content** : The id of the newly created auction and the success http response code.

```json
{
  "code": 201,
  "id": 34
}
```

##### Error Responses

**Condition** : The textual descriptions of the auction are invalid  
**Code** : `400 Bad Request`  
**Content** : An error message with the error code and error details

```json
{
  "code": 400,
  "error": "Invalid textual arguments"
}
```

**or**

**Condition** : The starting price of the auction is invalid  
**Code** : `400 Bad Request`  
**Content** : An error message with the error code and error details

```json
{
  "code": 400,
  "error": "Invalid starting price"
}
```

**or**

**Condition** : The starting price of the auction is valid but it's negative.  
**Code** : `400 Bad Request`  
**Content** : An error message with the error code and error details

```json
{
  "code": 400,
  "error": "Invalid starting price"
}
```

**or**

**Condition** : Missing token parameter  
**Code** : `401 Unauthorized`  
**Content** : An error message with the error code and error details

```json
{
  "code": 401,
  "error": "Token is missing!"
}
```

**or**

**Condition** : Invalid or malformed token was provided  
**Code** : `403 Forbidden`  
**Content** : An error message with the error code and error details

```json
{
  "code": 403,
  "error": "Invalid token"
}
```

##### Curl Query Example

```bash
curl -X POST http://localhost:8080/auction/2 \
     -H "Content-Type: application/json" \
     -d '{ "item": "1234123", "min_price": "23", "end_date": "2021-10-12 04:05:04", "title": "Items sale", "item_description": "Itemizer", "auction_description": "Many items",  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9 (...)"}'
```

---

#### Auction Listing

**URL** : `/auctions`  
**Description**: List all auctions that are present in the application's database.  
**Method** : `GET`  
**Authentication required** : `YES`  
**Permissions required** : `None`

##### Request Parameters

- token

##### Success Response

**Code** : `200 OK`  
**Content** : The list of existing and running auctions in the database

```json
[
  {
    "code": 200
  },
  {
    "description": "Donec quis orci eget orci vehicula condimentum.",
    "id": 1
  },
  {
    "description": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.",
    "id": 7
  },
  {
    "description": "In hac habitasse platea dictumst.",
    "id": 9
  },
  {
    "description": "In hac habitasse platea dictumst.",
    "id": 10
  },
  {
    "description": "Etiam pretium iaculis justo.",
    "id": 21
  },
  {
    "description": "Maecenas ut massa quis augue luctus tincidunt.",
    "id": 26
  }
]
```

##### Error Responses

**Condition** : Invalid or malformed token was provided  
**Code** : `403 Forbidden`  
**Content** : An error message with the error code and error details

```json
{
  "code": 403,
  "error": "Invalid token"
}
```

**or**

**Condition** : Missing token parameter  
**Code** : `401 Unauthorized`  
**Content** : An error message with the error code and error details

```json
{
  "code": 401,
  "error": "Token is missing!"
}
```

**or**

**Condition** : Something went wrong when accessing the database.  
**Code** : `500 Internal Server Error`  
**Content** : An error message with the error code and error details

```json
{
  "error": "Error message (dependant on type of internal error)",
  "code": 500
}
```

##### Curl Query Example

```bash
curl -X GET "http://localhost:8080/auctions" \
     -H "Content-Type: application/json" \
     -d '{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9 (...)"}'
```

---

#### Auction Searching

**URL** : `/auctions/<filter>`  
**Description**: List ongoing auctions by code EAN / ISBN or by the auction's description. This listing presents the identifier and description of each auction.
that meets the search criteria.  
**Method** : `GET`  
**Authentication required** : `YES`  
**Permissions required** : `None`

##### Request Parameters

- token

##### Success Response

**Code** : `200 OK`  
**Content** : The list of auctions that meet the search filter criteria

```json
[
  {
    "code": 200
  },
  {
    "description": "In hac habitasse platea dictumst.",
    "id": 9
  },
  {
    "description": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.",
    "id": 7
  },
  {
    "description": "In hac habitasse platea dictumst.",
    "id": 10
  },
  {
    "description": "Maecenas ut massa quis augue luctus tincidunt.",
    "id": 26
  },
  {
    "description": "Etiam pretium iaculis justo.",
    "id": 21
  },
  {
    "description": "Donec quis orci eget orci vehicula condimentum.",
    "id": 1
  }
]
```

##### Error Responses

**Condition** : Missing token parameter  
**Code** : `401 Unauthorized`  
**Content** : An error message with the error code and error details

```json
{
  "code": 401,
  "error": "Token is missing!"
}
```

**or**

**Condition** : Invalid or malformed token was provided  
**Code** : `403 Forbidden`  
**Content** : An error message with the error code and error details

```json
{
  "code": 403,
  "error": "Invalid token"
}
```

**or**

**Condition** : Something went wrong when accessing the database.  
**Code** : `500 Internal Server Error`  
**Content** : An error message with the error code and error details

```json
{
  "error": "Error message (dependant on type of internal error)",
  "code": 500
}
```

##### Curl Query Example

```bash
curl -X GET "http://localhost:8080/auctions/a" \
     -H "Content-Type: application/json" \
     -d '{ "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9 (...)"}'

```

---

#### Auction Details

**URL** : `/auction/<auctionID>`  
**Description**: Obtain all details regarding the item description, the end of the auction, the messages exchanged and the history of bids made.  
**Method** : `GET`  
**Authentication required** : `YES`  
**Permissions required** : `None`

##### Request Parameters

- token

##### Success Response

**Code** : `200 OK`  
**Content** : All the details of the running auction.

```json
{
  "code": 200,
  "auction_description": "Donec quis orci eget orci vehicula condimentum",
  "canceled": false,
  "creator": "dalliband0",
  "end_date": "Sat, 12 Jun 2021 04:05:06 GMT",
  "id": 1,
  "item": 1234,
  "item_description": "Mauris enim leo, rhoncus sed, vestibulum sit amet",
  "opening_price": 32.3,
  "title": "libero",
  "messages": [],
  "licitation": []
}
```

##### Error Responses

**Condition** : Missing token parameter  
**Code** : `401 Unauthorized`  
**Content** : An error message with the error code and error details

```json
{
  "code": 401,
  "error": "Token is missing!"
}
```

**or**

**Condition** : Invalid or malformed token was provided  
**Code** : `403 Forbidden`  
**Content** : An error message with the error code and error details

```json
{
  "code": 403,
  "error": "Invalid token"
}
```

**or**

**Condition** : Something went wrong when accessing the database.  
**Code** : `500 Internal Server Error`  
**Content** : An error message with the error code and error details

```json
{
  "error": "Error message (dependant on type of internal error)",
  "code": 500
}
```

##### Curl Query Example

```bash
curl -X GET "http://localhost:8080/auction/123" \
     -H "Content-Type: application/json" \
     -d '{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9 (...)"}'
```

---

---

### Administrator Endpoints

---

#### User Ban

**URL** : `/admin/ban`  
**Description**: Ban a user. All auctions created by that
user are cancelled. All bids placed by that user should be invalidated (even
yet kept in the logs). When invalidating a bid in an auction, any higher bids
shall also be dropped except for the best one, whose value becomes equal to the value of the one that is invalidated. A message is automatically created on the wall of the affected auctions regretting the inconvenience.  
**Method** : `POST`  
**Authentication required** : `YES`  
**Permissions required** : `Administrator Privileges`

##### Request Parameters

- Administrator Login Token
- User ID

##### Success Response

**Code** : `201 Created`  
**Content** : A json with the following structure

```json
{
  "code": 200,
  "response": "Successful"
}
```

##### Error Responses

**Condition** : An internal Server Error  
**Code** : `500 Internal Server Error`  
**Content** : An error message with the error code and error details

```json
{
  "error": " ***Error Details*** ",
  "code": 500
}
```

##### Curl Query Example

```bash
curl -X POST http://localhost:8080/admin/ban \
     -H "Content-Type: application/json" \
     -d '{"id": 2, "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9 (...)"}'
```

---

#### Auction Cancellation

**URL** : `/admin/cancel`  
**Description**:
Cancel an auction. The auction can still be viewed by users, but is declared closed and no bids can be placed. All interested users receive a notification.  
**Method** : `POST`  
**Authentication required** : `YES`  
**Permissions required** : `Administrator Privileges`

##### Request Parameters

- Administrator Login Token
- Auction ID

##### Success Response

**Code** : `201 Created`  
**Content** : A json with the following structure

```json
{
  "code": 200,
  "response": "Successful"
}
```

##### Error Responses

**Condition** : An internal Server Error  
**Code** : `500 Internal Server Error`  
**Content** : An error message with the error code and error details

```json
{
  "error": " ***Error Details*** ",
  "code": 500
}
```

##### Curl Query Example

```bash
curl -X POST http://localhost:8080/admin/cancel \
     -H "Content-Type: application/json" \
     -d '{"id": 2, "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9 (...)"}'
```

---

#### Application Statistics

**URL** : `/admin/stats`  
**Description**:

- Top 10 users with the most auctions created.
- Total number of created auctions in the last 10 days.
- Top 10 users who won the most auctions.

**Method** : `GET`  
**Authentication required** : `YES`  
**Permissions required** : `Administrator Privileges`

##### Request Parameters

- Administrator Login Token

##### Success Response

**Code** : `201 Created`  
**Content** : A json with the following format

```json
{
  "more_auctions_created": [
    {
      "created": 2,
      "person_id": 2
    },
    {
      "created": 1,
      "person_id": 3
    }
  ],
  "total_created_auctions_last_10_days": 2,
  "winners": [
    {
      "person_id": 2,
      "won": 1
    },
    {
      "person_id": 3,
      "won": 1
    }
  ]
}
```

##### Error Responses

**Condition** : An internal Server Error  
**Code** : `500 Internal Server Error`  
**Content** : An error message with the error code and error details

```json
{
  "error": " ***Error Details*** ",
  "code": 500
}
```

##### Curl Query Example

```bash
curl -X GET http://localhost:5000/admin/stats \
     -H "Content-Type: application/json" \
     -d '{ "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9 (...)"}'
```

---

---

## Authors

- [Duarte Dias](https://github.com/TLDart)
- [Miguel Rabuge](https://github.com/MikeLrUC)
- [Pedro Rodrigues](https://github.com/pedromig)
