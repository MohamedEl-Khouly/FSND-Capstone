# FSND-CAPSTONE

This is the final project for the UDACITY FSND certification. The project aims to test all skills learned through out the nanodeagre.

## Project Description

The Casting Agency is a company that is responsible for movie production. The API holds a database of the movies produced by the company and actors playing roles in these movies. The API manages CRUD operations for the movies and actors data.

There is no frontend implementation for the API. It is a server only application at the moment.

## Hosted API Link

The API is hosted live on HEROKU. It can be accessed through the link
**https://fsndudacity-capstone.herokuapp.com/**

## Tech Stack

The Tech Stack used in API includes:

-   **Python3**: The [server language](https://www.python.org/downloads/)
-   **Flask**: [Server Framework](https://flask.palletsprojects.com/en/1.1.x/)
-   **PostgreSQL**: [Database](https://www.postgresql.org/) of choice
-   **SQLAlchemy**: [ORM of choice](https://www.sqlalchemy.org/) to communicate between the python server and the Postgres Database. [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) is directly used.
-   **Heroku**: [Deployment Platform](https://www.heroku.com/)
-   **[Postman](https://www.postman.com/)**: Testing the Application Endpoints

## Local development

### Installing Dependencies

#### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Environment Variables

In the project folder create `setup.sh` file to hold the environment variables

#### Create Local Database

Create a local database and export the database URI as an environment variable with the key `DATABASE_PATH`.

#### Run Database Migrations

```bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

### Run the application

To run the API run the following commands

```bash
export FLASK_APP=myapp
export FLASK_ENV=development
flask run
```

### Testing

There are two file included for testing the API.

#### test_app.py

This is a local testing file. To use this file
comment out the require_auth decorator in the app.py
and run the following command.

```bash
python test_app.py
```

### Postman testing

To test the endpoints with [Postman](https://getpostman.com).

-   Import the postman collection `./udacity-fsnd-capstone.postman_collection.json`
-   Run the collection and correct any errors.

## API

### Getting Started

-   Base URL: if the flask app is being run locally use `https://localhost:5000/`.
    As for the hosted version `herkou url`
-   Authentication: This version of the application requires Auth0 jwt that can acquired through /auth endpoint.

### Error Handling

Errors are returned in JSON objects in the following format:

```json
{
	"success": false,
	"error": 404,
	"message": "Resource Not Found"
}
```

When a request fails the API sends one of the following errors:

-   400: bad request
-   401: Unauthorized
-   403: Forbidden
-   404: Resource Not Found
-   422: Request unprocessable

### Endpoints

#### Base Endpoints

**GET** `/`

-   Confirms Api is running
-   Request Arguments: None
-   Returns the following object

```json
{
	"success": True,
	"App": "Casting Agency"
}
```

**GET** `/auth`

-   Confirms Api is running
-   Request Arguments: None
-   Returns the following object

```json
{
	"url": "https://se-fsnd.us.auth0.com/authorize?audience=agency&response_type=token&client_id=yKiu9F8JsUtKelZwtob4eQHGiicBQaSJ&redirect_uri=http://localhost:5000/"
}
```

#### Actors

**GET** `/actors?page=<page_number>`

-   Fetches a paginated list actors objects from the database.
-   Request Arguments: beerar token, (optional) page:int.
-   Returns an object with the format of the following example

```json
{
	"actors": [
		{
			"age": 23,
			"gender": "F",
			"id": 1,
			"movies": ["The New Mutants", "Game of Thrones"],
			"name": "Maisie Williams"
		},
		{
			"age": 24,
			"gender": "F",
			"id": 2,
			"movies": ["Game of Thrones"],
			"name": "Sophie Turner"
		},
		{
			"age": 37,
			"gender": "M",
			"id": 3,
			"movies": ["Justice League: Snyder Cut"],
			"name": "Henry Cavill"
		},
		{
			"age": 33,
			"gender": "F",
			"id": 4,
			"movies": [],
			"name": "Emilia Clarke"
		},
		{
			"age": 24,
			"gender": "F",
			"id": 5,
			"movies": [],
			"name": "Anya Chalotra"
		},
		{
			"age": 47,
			"gender": "M",
			"id": 6,
			"movies": ["Justice League: Snyder Cut"],
			"name": "Ben Affleck"
		},
		{
			"age": 40,
			"gender": "M",
			"id": 7,
			"movies": ["Justice League: Snyder Cut", "Aquaman", "See"],
			"name": "Jason Momoa"
		},
		{
			"age": 28,
			"gender": "F",
			"id": 8,
			"movies": [],
			"name": "Chloe Bennet"
		},
		{
			"age": 56,
			"gender": "F",
			"id": 9,
			"movies": [],
			"name": "Ming-Na Wen"
		},
		{
			"age": 44,
			"gender": "F",
			"id": 10,
			"movies": ["The Old Guard"],
			"name": "Charlize Theron"
		}
	],
	"success": true,
	"total_actors": 19
}
```

**POST** `/actors`

-   Adds a new actor to the table of actors storred in the APP Database
-   Requires a body of the following format

```json
{
	"name": "Tom Holland",
	"age": 24,
	"gender": "M"
}
```

-   Returns an object with the format of the following example

```json
{
	"actor": {
		"age": 24,
		"gender": "M",
		"id": 1,
		"movies": [],
		"name": "Tom Holland"
	},
	"success": true
}
```

**PATCH** `/actors/<int:actor_id>`

-   edits an existing actor of the table actors stored in the APP Database
-   Requires a body of the following format

```json
{
	"movies": 5
}
```

-   Returns an object with the format of the following example

````json
{
	"actor": {
		"age": 24,
		"gender": "M",
		"id": 1,
		"movies": ["Spider-man"],
		"name": "Tom Holland"
	},
	"success": true
}```

**DELETE** `/actors/<int:actor_id>`

-   Deletes an actor from the table of actors stored in the APP database
-   Request arguments: question_id:int
-   Returns an object with the format of the following example

```json
{
	"deleted": "2",
	"success": true
}
````

#### Movies

**GET** `/movies?page=<page_number>`

-   Fetches a paginated list of movies objects from the database.
-   Request Arguments: beerar token, (optional) page:int.
-   Returns an object with the format of the following example

```json
{
	"movies": [
		{
			"actors": [
				"Henry Cavill",
				"Ben Affleck",
				"Jason Momoa",
				"Gal Gadot"
			],
			"id": 1,
			"release_date": "Sat, 13 Mar 2021 00:00:00 GMT",
			"title": "Justice League: Snyder Cut"
		},
		{
			"actors": [],
			"id": 2,
			"release_date": "Fri, 12 Nov 2021 00:00:00 GMT",
			"title": "The Batman"
		},
		{
			"actors": ["Charlize Theron"],
			"id": 3,
			"release_date": "Sun, 23 Jan 2022 00:00:00 GMT",
			"title": "The Old Guard"
		},
		{
			"actors": [],
			"id": 4,
			"release_date": "Thu, 24 Mar 2022 00:00:00 GMT",
			"title": "Ready Player One"
		},
		{
			"actors": ["Jason Momoa", "Nicole Kidman"],
			"id": 5,
			"release_date": "Sun, 15 May 2022 00:00:00 GMT",
			"title": "Aquaman"
		},
		{
			"actors": ["Maisie Williams", "Anya Taylor"],
			"id": 6,
			"release_date": "Fri, 21 Aug 2020 00:00:00 GMT",
			"title": "The New Mutants"
		},
		{
			"actors": [],
			"id": 7,
			"release_date": "Mon, 21 Sep 2020 00:00:00 GMT",
			"title": "Tenet"
		},
		{
			"actors": [],
			"id": 8,
			"release_date": "Fri, 21 Aug 2020 00:00:00 GMT",
			"title": "His Dark Materials"
		},
		{
			"actors": ["Jason Momoa"],
			"id": 9,
			"release_date": "Mon, 19 Jul 2021 00:00:00 GMT",
			"title": "See"
		},
		{
			"actors": [],
			"id": 10,
			"release_date": "Sun, 07 May 2023 00:00:00 GMT",
			"title": "Enders Game:2"
		}
	],
	"success": true,
	"total_movies": 13
}
```

**POST** `/movies`

-   Adds a new movie to the table of movies stored in the APP Database
-   Requires a body of the following format

```json
{
	"title": "The Developer",
	"release_date": "20-5-2023"
}
```

-   Returns an object with the format of the following example

```json
{
	"movie": {
		"actors": [],
		"id": 1,
		"release_date": "Sat, 20 May 2023 00:00:00 GMT",
		"title": "The Developer"
	},
	"success": true
}
```

**PATCH** `/movies/<int:movie_id>`

-   edits an existing movie of the table movies stored in the APP Database
-   Requires a body of the following format

```json
{
	"release_date": "20-5-2025"
}
```

-   Returns an object with the format of the following example

```json
{
	"movie": {
		"actors": [],
		"id": 1,
		"release_date": "Sat, 20 May 2025 00:00:00 GMT",
		"title": "The Developer"
	},
	"success": true
}
```

**DELETE** `/movies/<int:movie_id>`

-   Deletes a movie from the table of movies stored in the APP database
-   Request arguments: question_id:int
-   Returns an object with the format of the following example

```
{
	"deleted": "2",
	"success": true
}
```
