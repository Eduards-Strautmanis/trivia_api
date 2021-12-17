## Udacitrivia

This is an application for playing a quiz game. There are 6 categories: Science, Art, Geography, History, Entertainment, and Sports. You can add your own questions, and play the game with only one category or all categories at once. It features a React frontend, which is powered by the backend API. All data is stored on a PostgreSQL server, and any update made to the frontend is immediately synced with the server.

## Getting Started

# Prerequisites

To set up the project for local development for yourself, first clone this GitHub directory. As a prerequisite, Python3, Node, and pip must be installed on your computer.

First, start a virtual environment by navigating to the starter folder and running

```
python3 -m venv env
source env/bin/activate
```

If you don't have virtual environment, you can install it by running `python3 -m pip install --user virtualenv`

# Backend

To install the dependencies, navigate to the backend folder, then run

```
bash
pip install -r requirements.txt
```

To start the backend, in the backend folder, run these commands:

```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

The backend will by default be running on localhost:5000

To restore the database, with Postgres running, run

```
bash
psql trivia < trivia.psql
```

# Frontend

To install the dependencies and then start the frontend, run these commands:

```
bash
npm install
npm start
```

The frontend will by default be running on localhost:3000

## Tests

To run the tests, navigate to the backend folder and run the following commands:

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < books.psql
python test_flaskr.py
```

### API Reference

This is an API for returning questions, among other things, for a quiz game. It is linked to a PostgreSQL server, and can return questions by category, give a new random question among all questions or amongst a specific category, as well as create and delete questions in the database.

## Getting Started

This API currently only runs locally, and thus, is hosted on localhost:5000. This would be the url used to communicate to the frontend.
At present, this API does not have authentication or API keys.

## Error Handling

This API returns errors in a standardized JSON format:

```
{
  "success": False,
  "error": 400,
  "message": "Bad request"
}
```

This project is set to return the following errors:
400: Bad Request
404: Not Found
405: Method Not Allowed
422: Unprocessable

## Endpoints

#GET /categories
* General:
  + Returns all categories as a dictionary where the key is the id of the category, as well as a success value
* Sample: `curl http://127.0.0.1:5000/categories`

```
{
  "categories":
    {
      "1": "Science",
      "2": "Art",
      "3": "Geography",
      "4": "History",
      "5": "Entertainment",
      "6": "Sports"
    },
  "success": True
}
```

#GET /questions
* General:
  + Returns all questions, ordered by id, paginated by ten questions per page, as well as a success value, total number of questions, and all categories as a json dictionary.
* Sample: `curl http://127.0.0.1:5000/questions`

```
{
  "categories":
    {
      "1": "Science",
      "2": "Art",
      "3": "Geography",
      "4": "History",
      "5": "Entertainment",
      "6": "Sports"
    },
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },

    ...

    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```

#DELETE /questions/{question_id}
* General:
  + Deletes the question indicated by the provided id. Returns a success value.
* Sample: `curl http://127.0.0.1:5000/questions/15`

```
{
  "success": True
}
```

#POST /questions (searching for question)
* General:
  + If a JSON form is provided with a search term, this endpoint will return all questions that match the search term string in a case insensitive manner, as well as a success value and length of total questions.
* Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "who"}' `

```
{
  "questions":[
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    }
  ],
  "success": true,
  "totalQuestions": 3
}
```

#POST /questions (posting a question)
* General:
  + If a JSON form is provided with all the fields for creating a question, this endpoint will utilize Flask SQLAlchemy to add the new specified question to the database. It will return a success value
* Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d "{'question': 'What year was the first iPhone model released?','answer': '2007','category': 5,'difficulty': 2}"`

```
{
  "success": True
}
```

#GET /categories/{category_id}/questions
* General:
  + Returns all questions in the specified category, as well as a success value and length of total questions in that category.
* Sample: `curl http://127.0.0.1:5000/categories/6/questions`

```
{
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "success": true,
  "totalQuestions": 2
}
```

#POST /quizzes
* General:
  + This endpoint takes a JSON dictionary of all questions that have already been shown to the player and returns a new question, whether in a specific category if provided, or from the pool of all questions (specified by setting quiz_category to 0). If there are no more new questions to be shown, `{"question": None}` will be returned.
* Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category": 6, "previous_questions": [10]}' `

```
{
  "question":
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
  "success": true}
```

## Deployment N/A

## Authors

Coach Caryn: Frontend, most of the backend
Edward Strautmanis: The parts of the backend that had TODOs
