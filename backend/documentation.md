# TRIVIA API Documentation 
The Trivia app is an application that is used for quizzing. The application is capable of performing the functions stated below.

1. Display questions - both all questions and by category. Questions shows the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## Getting started

- base url : this application is ran locally so the base url is `http://127.0.0.1:5000/` .
-Authentication: this version of the application does not require authentication or API keys.


## Error Handling
conventional error codes are used in this application.

Errors are returned as JSON object in the following format:
'''
{
    "success": False,
    "error":404,
    "message": " resource not found"
}
'''
The API would return these errors when request fails:
- error 404: Resource not found
- error 405: method not allowed
- error 4o2: unprocessable 
- error 400: bad request


## Endpoint Library
-There are various endpoints in this API which provides various functions. 
-A comprehensive summary of the properties and functionality of each end point is given below
-All endpoints return a success value of True when successful.


#### GET /categories
- General 
   - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
   - Request Arguments: None
   - Returns: An object with categories, that contains an object of id: category_string key:value pairs and a success value of true.

- Sample: `curl http://127.0.0.1:5000/categories`

"""
{
    "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}

"""
#### GET /questions 

-General 
    - Fetches a paginated set of questions, a total number of questions, all categories and current category string.
    - Request Arguments: page - integer
    - Returns: An object with 10 paginated questions, total questions, object including all categories, current category string  and a success value of true.

-Sample: `curl http://127.0.0.1:5000/questions`

"""
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "Entertainment",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": "5",
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": "5",
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": "5",
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": "4",
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": "6",
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": "6",
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": "4",
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": "3",
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": "3",
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": "2",
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ],
  "success": true,
  "total_questions": 13
}

"""
#### GET '/categories/{id}/questions'

-General
    - Fetches questions for a cateogry specified by id request argument
    - Request Arguments: id - integer
    - Returns: An object with questions for the specified category, total questions, and current category string.

-Sample: `curl http://127.0.0.1:5000/categories/2/questions`

"""
{
  "current_category": "Art",
  "questions": [
    {
      "answer": "Escher",
      "category": "2",
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ],
  "success": true,
  "total_questions": 13
}

"""

#### DELETE '/questions/{id}'
- General
    - Deletes a specified question using the id of the question
    - Request Arguments: id - integer
    - Returns: it returns success value of true and the deleted id of the question. 

-Sample: `curl -X DELETE http://127.0.0.1:5000/questions/62`

"""
{
  "deleted": "62",
  "success": true
}

"""

#### POST '/questions'   -To create a new question
- General
    - Sends a post request as json object in order to add a new question
    - Request Body: `{"question":"testing","answer":"test","difficulty":3,"category":4}`
    - Returns: it returns success value of true.

-Sample: `curl -H "Content-Type: application/json" -d '{"question":"testing","answer":"test","difficulty":3,"category":4}' -X POST http://127.0.0.1:5000/questions`

"""
{
  "success": true
}

"""
#### POST '/questions'   -To search for a question
- General
    -Sends a post request as json object in order to search for a specific question
    - Request Body: `{"search_term": "who is the current"}`
    - Returns:  it returns success value of true,an array of questions, a number of totalQuestions that met the search term and the current category string.

-Sample: `curl -H "Content-Type: application/json" -d '{"search_term": "who is the current"}' -X POST http://127.0.0.1:5000/questions`

"""
{
  "current_category": "History",
  "questions": [
    {
      "answer": "buhari",
      "category": "4",
      "difficulty": 2,
      "id": 63,
      "question": "who is the current president of nigeria"
    }
  ],
  "success": true,
  "total_questions": 1
}

"""

#### POST '/quizzes'
-General
    - Sends a post request in order to get the next question
    - Request Body: `{"previous_questions":[9,2,11],"quiz_category":5}`
    - Returns: success value of true and a single new question.

-Sample: `curl -H "Content-Type: application/json" -d '{"previous_questions":[9,2,11],"quiz_category":5}' -X POST http://127.0.0.1:5000/quizzes`


"""
{
  "question": {
    "answer": "Edward Scissorhands",
    "category": "5",
    "difficulty": 3,
    "id": 6,
    "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
  },
  "success": true
}

"""
