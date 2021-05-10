# BD-Project

![APM](https://img.shields.io/apm/l/vim-mode)
![BUILD](https://img.shields.io/badge/build-passing-green)

## About The Project

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

## Native Installation

If you choose to run the application and all the tools natively please follow these instructions.

NOTE: The native installation allows you to have more control over the application and database configurations but if you are looking to try the application and you don't want to worry about all the small configuration details, this project has docker support allowing you build pre-configured images and create containers that will run this application components with little or no configuration. To know how you use them check the [Docker Support](#docker-support) chapter.

### Tools Installation

In order to run this project it is required to have an installation of a python interpreter `python3` or `pypy3` the python package installer `pip` and the `curl` or `postman` tool which provides the same functionality as curl but is being more GUI oriented.
In our project we are opting to use the python3 interpreter and the curl tool. These programs can be installed using your operating system package manager as shown bellow for a Linux/MacOS machine.

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

#Arch Linux:
sudo pacman -S python python-pip curl
```

In case ofWindows/MacOS machines it is possible to install the software
via a graphical installer. For more information about the download installation of python3, pip, curl and postman check the following websites:

- [Python](https://www.python.org/downloads/)
- [Pip](https://pip.pypa.io/en/stable/installing/)
- [Curl](https://curl.se/download.html)
- [Postman](https://postman.com/)

To store information this project uses the PostgreSQL Database management system. This DBMS can be installed using your operating system package manager as shown bellow for a debian based Linux distro.

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

### Project Setup

After the native installation of all the tools you are almost ready to begin using the REST API. Before that you will need to create and setup your native postgreSQL installation and the web server where the REST service will run.
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

Once we execute the [api.py](src/app/api.py) after all this setup the web server that will provide the REST service will be started and will run in the host machine until the program is stopped. By default a flask web server will run on port 5000, in order to interact with it we can use a web browser or make curl/postman calls to the following URL or other URLs derived from this one and described in the REST API specification.

```
http://localhost:5000/
```

## Docker Support

The components of this project such as the PostgreSQL database and REST service (that will be provided via web server) can be ran in docker containers instead natively in your machine. The docker images are already pre-configured saving you the trouble of installing all the software natively in your machine. In order to use install and run these images follow the instructions described bellow.

`TODO: docker support chapter`

## Dragon server

`TODO: Add here information about the interaction with our server`

## Project Features

### REST API

`TODO: Add here information relative to our API`

# Collaborators

- [Miguel Rabuge](https://github.com/MikeLrUC)
- [Duarte Dias](https://github.com/TLDart)
