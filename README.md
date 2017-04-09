[![Coverage Status](https://coveralls.io/repos/github/andela-bolajide/BucketListAPI/badge.svg?branch=develop)](https://coveralls.io/github/andela-bolajide/BucketListAPI?branch=develop) [![Build Status](https://travis-ci.org/andela-bolajide/BucketListAPI.svg?branch=develop)](https://travis-ci.org/andela-bolajide/BucketListAPI) [![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/andela-bolajide/BucketListAPI/badges/quality-score.png?b=develop)](https://scrutinizer-ci.com/g/andela-bolajide/BucketListAPI/?branch=develop) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# BucketListAPI
This repository contains a fully working API project that communicates seamlessly with the BucketList service. This API accepts only `JSON` objects as input. The API service requires authentication for easy access to the resources provided.

## Development
This application was developed using [Flask](http://flask.pocoo.org/). Postgres was used for persisting data with [SQLAlchemy](https://www.sqlalchemy.org/) as [ORM](https://en.wikipedia.org/wiki/Object-relational_mapping).

## Application Features
###### User Authentication
Users are authenticated and validated using an `itsdangerous` token. Generating tokens on login ensures each account is unique to a user and can't be accessed by an authenticated user.

## Installation
* Start up your terminal (or Command Prompt on Windows OS).
* Ensure that you've `python` installed on your PC.
* Clone the repository by entering the command `git clone https://github.com/andela-bolajide/BucketListAPI` in the terminal.
* Navigate to the project folder using `cd BucketListAPI` on your terminal (or command prompt)
* After cloning, create a virtual environment then install the requirements with the command:
`pip install -r requirements.txt`.
* Create a `.env` file in your root directory as described in `.env.sample` file. Variables such as DATABASE_URL and config are defined in the .env file and it is essential you create this file before running the application.
```
FLASK_CONFIG='default'
DATABASE_URI='database connection to be used'
SECRET_KEY='random string used for generating token'
TEST_DB='database to be used for testing'
```
* After this, you'll need to migrate data schema to the database using the command: `python manage.py create_db`.

## Testing
To ensure that your installation is successful you'll need to run tests.
Enter the command `python manage.py test` in your terminal (or command prompt) to run test.

## Usage
* A customized interactive python shell can be accessed by passing the command `python manage.py shell` on your terminal.
* Once this is done, the application can be started using `python manage.py runserver` and by default the application can be accessed at `http://127.0.0.1:5000`. The application starts using the configuration settings defined in your .env file.

## Configuration
The API currently has 4 different configuration which can be defined in the .env file.
- `production`: this configuration starts the app ready for production to be deployed on any cloud application platform such as Heroku, AWS etc.
- `development`: this configuration starts the application in the development mode.
- `testing`: this configuration starts the application in a testing mode.
- `default`: this is the same as the development configuration.

## API Documentation
-----
The API has routes, each dedicated to a single task that uses HTTP response codes to indicate API status and errors.

#### API Features

The following features make up the BucketList API:

###### Authentication
-   It uses itsdangerous-Serializer token for authentication.

-   It generates a token on successful login and returns it to the user.

-   It verifies the token to ensures a user is authenticated to access protected endpoints.

###### Users

-   It allows users to be created.

-   It allows users to login and obtain a token

-   It allows authenticated users to retrieve and update their information.

###### BucketLists

-   It allows new bucketlists to be created by authenticated users.

-   It ensures all bucketlist are accessible based on the permission specified.

-   It allows the users to create, retrieve, modify, and delete bucketlists and bucketlist items.

### API Resource Endpoints

URL Prefix = `http://sample_domain/api/v1` where sample domain is the root URL of the server HOST.


| EndPoint                                 | Functionality                 | Public Access|
| -----------------------------------------|:-----------------------------:|-------------:|
| **POST** /auth/register                  | Register a user               |    TRUE      |
| **POST** /auth/login                     | Logs a user in                |    TRUE      |
| **POST** /bucketlists/                   | Create a new bucket list      |    FALSE     |
| **GET** /bucketlists/                    | List all created bucket lists |    FALSE     |
| **GET** /bucketlists/id                  | Get single bucket list        |    FALSE     |
| **PUT** /bucketlists/id                  | Update a bucket list          |    FALSE     |
| **DELETE** /bucketlists/id               | Delete a bucket list          |    FALSE     |
| **POST** /bucketlists/id/items           | Create a new item bucket list |    FALSE     |
| **PUT** /bucketlists/id/items/item_id    | Update a bucket list item     |    FALSE     |
| **DELETE** /bucketlists/id/items/item_id | Delete an item in bucket list |    FALSE     |

#### Authentication
###### POST HTTP Request
-   `POST /auth/login`
-   INPUT:
```json
{
  "username":"username",
  "password":"password"
}
```
    ###### HTTP Response
-   HTTP Status: `200: created`
-   JSON data
```json
{
  "token": "eyJhbGciOiJIUImV4cCI6MTQ5MTM1MDk5MCwiaWF0pZCI6MX0.sPajMqbJwGtnb8xEcR4Ardmd9G9OFPIHr-_oEM"
}
```

###### POST HTTP Request
-   `POST /auth/register`
-   INPUT:
```json
{
  "username":"username",
  "password":"password"
}
```
    ###### HTTP Response
-   HTTP Status: `201: created`
-   JSON data
```json
{
  "username": "test_user"
}
```

#### BucketLists
###### GET HTTP Request
-   `GET /api/v1/bucketlists`
-   Requires: User Authentication
    ###### HTTP Response
-   HTTP Status: `200: OK`
-   JSON data
```json
{
      "bucketlist_url": "http://localhost:5000/api/v1/bucketlists/10",
      "created_by": 2,
      "date_created": "Sun, 26 Mar 2017 19:11:06 GMT",
      "date_modified": "Sun, 26 Mar 2017 19:11:06 GMT",
      "id": 10,
      "items": [
        {
          "date_created": "Sun, 26 Mar 2017 19:41:48 GMT",
          "date_modified": "Sun, 26 Mar 2017 19:41:48 GMT",
          "done": false,
          "id": 11,
          "name": "I want to be an OAP"
        },
        {
          "date_created": "Sun, 26 Mar 2017 19:41:48 GMT",
          "date_modified": "Sun, 26 Mar 2017 19:41:48 GMT",
          "done": false,
          "id": 12,
          "name": "I want to be a presenter..."
        }
      ],
      "name": "Adepeju's BucketList"
    }
```

###### POST HTTP Request
-   `POST /api/v1/bucketlists`
```json
{
  "name":"BucketList1"
}
```
-   Requires: User Authentication
    ###### HTTP Response
-   HTTP Status: `200: OK`
-   JSON data
```json
{
      "bucketlist_url": "http://localhost:5000/api/v1/bucketlists/10",
      "created_by": 2,
      "date_created": "Sun, 26 Mar 2017 19:11:06 GMT",
      "date_modified": "Sun, 26 Mar 2017 19:11:06 GMT",
      "id": 10,
      "items": [],
      "name": "BucketList"
    }
```

###### POST HTTP Request
-   `POST /api/v1/bucketlists/<bucketlist_id>/items`
```json
{
  "name":"Item 1",
  "done":"false"
}
```
-   Requires: User Authentication
    ###### HTTP Response
-   HTTP Status: `200: OK`
-   JSON data
```json
{
      "bucketlist_url": "http://localhost:5000/api/v1/bucketlists/10",
      "created_by": 2,
      "date_created": "Sun, 26 Mar 2017 19:11:06 GMT",
      "date_modified": "Sun, 26 Mar 2017 19:11:06 GMT",
      "id": 10,
      "items": [
          {
          "date_created": "Sun, 26 Mar 2017 19:41:48 GMT",
          "date_modified": "Sun, 26 Mar 2017 19:41:48 GMT",
          "done": false,
          "id": 12,
          "name": "Item 1"
          }
      ],
      "name": "BucketList1"
    }
```

###### PUT HTTP Request
-   `POST /api/v1/bucketlists/<bucketlist_id>`
```json
{
  "name":"John Doe's BucketList"
}
```
-   Requires: User Authentication
    ###### HTTP Response
-   HTTP Status: `200: OK`
-   JSON data
```json
{
      "bucketlist_url": "http://localhost:5000/api/v1/bucketlists/10",
      "created_by": 2,
      "date_created": "Sun, 26 Mar 2017 19:11:06 GMT",
      "date_modified": "Sun, 26 Mar 2017 19:11:06 GMT",
      "id": 10,
      "items": [
          {
          "date_created": "Sun, 26 Mar 2017 19:41:48 GMT",
          "date_modified": "Sun, 26 Mar 2017 19:41:48 GMT",
          "done": false,
          "id": 12,
          "name": "Item 1"
          }
      ],
      "name": "John Doe's BucketList"
    }
```

###### DELETE HTTP Request
-   `DELETE /api/v1/bucketlists/<bucketlist_id>`
-   Requires: User Authentication
    ###### HTTP Response
-   HTTP Status: `200: OK`
-   JSON data
```json
{
    "Delete":"true"
}
```

## Authors

**Olajide Bolaji E.** - Software Developer at Andela

## Acknowledgments

Thanks to my facilitator **Njira Perci** and my wonderful **Pygo Teammates**
