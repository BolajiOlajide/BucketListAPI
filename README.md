[![Coverage Status](https://coveralls.io/repos/github/andela-bolajide/BucketListAPI/badge.svg?branch=develop)](https://coveralls.io/github/andela-bolajide/BucketListAPI?branch=develop) [![Build Status](https://travis-ci.org/andela-bolajide/BucketListAPI.svg?branch=develop)](https://travis-ci.org/andela-bolajide/BucketListAPI) [![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/andela-bolajide/BucketListAPI/badges/quality-score.png?b=develop)](https://scrutinizer-ci.com/g/andela-bolajide/BucketListAPI/?branch=develop) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Code Climate](https://codeclimate.com/github/andela-bolajide/BucketListAPI/badges/gpa.svg)](https://codeclimate.com/github/andela-bolajide/BucketListAPI) [![Issue Count](https://codeclimate.com/github/andela-bolajide/BucketListAPI/badges/issue_count.svg)](https://codeclimate.com/github/andela-bolajide/BucketListAPI)

# BucketListAPI
This repository contains a fully working API project that communicates seamlessly with the BucketList service. This API accepts only `JSON` objects as input. The API service requires authentication for easy access to the resources provided.

## Installation
* Start up your terminal (or Command Prompt on Windows OS).
* Clone the repository by entering the command `git clone https://github.com/andela-bolajide/BucketListAPI` in the terminal - this clones the project to your PC.
* Navigate to the project folder using `cd BucketListAPI` on your terminal (or command prompt)
* After cloning, install the requirements with the command:
`pip install requirements/requirements.txt` or `pip install requirements/requirements_devel.txt` if you wish to contribute to the project as a developer.
* After this, you'll need to migrate data to the database so the schema can be built with the command `python manage.py db migrate -m "initial migration"`.
* Once migration is done, you then upgrade the database with the command `python manage.py db upgrade`
* A customized interactive python shell can be accessed by passing the command `python manage.py shell` on your terminal.


## Usage
* Before accessing most of the resources accessible with this API, you'll need to have an account created. This endpoint is available via the route: `/auth/register/`
`curl -u sample_token:unused -i -X GET http://127.0.0.1:5000/api/v1/bucketlists/`

## Testing
To ensure that your installation is successful you'll need to run tests.
Enter the command `python manage.py test` in your terminal (or command prompt) to run test.

### API Resource Endpoints
URL Prefix = `http://sample_domain/api/v1` where sample domain is the root URL of the server HOST.
-------------------------------------------------------------------------------------------
| EndPoint                                 | Functionality                 | Public Access|
| -----------------------------------------|:-----------------------------:|-------------:|
| **POST** /auth/register                  | Register a user               |    TRUE      |
| **POST** /auth/login                     | Logs a user in                |    TRUE      |
| **POST** /bucketlists/                   | Create a new bucket list      |    FALSE     |
| **GET** /bucketlists/                    | List all created bucket lists |    FALSE     |
| **GET** /bucketlists/id                  | Get single bucket list        |    FALSE     |
| **PUT** /bucketlists/id                  | Update a bucket list          |    FALSE     |
| **DELETE** /bucketlists/id               | Delete a bucket list          |    FALSE     |
| *POST* /bucketlists/id                   | Create a new item bucket list |    FALSE     |
| *PUT* /bucketlists/id/items/item_id      | Update a bucket list item     |    FALSE     |
| *DELETE* /bucketlists/id/items/item_id   | Delete an item in bucket list |    FALSE     |
-------------------------------------------------------------------------------------------

### Screenshots
![alt text][ScreenShot1]

[ScreenShot1]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "User trying to access his saved BucketList with the use of token."

## Authors

**Olajide Bolaji E.** - Software Developer at Andela

## Acknowledgments

Thanks to my facilitator **Njira Perci** and my wonderful **Pygo Teammates**