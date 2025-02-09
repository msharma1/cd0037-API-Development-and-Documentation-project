# Trivia API Documentation

## Endpoints

**1. GET /categories**

Fetches a dictionary of categories in which the keys are the IDs and the values are the corresponding category names.

**Request Arguments:** None

**Returns:** An object with a single key, categories, that contains a dictionary of id: category_string key-value pairs.

```json
{
  "success": true,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```
**2. GET /questions**

Fetches a list of questions, paginated in groups of 10. Also returns the total number of questions and all available categories.

**Request Arguments:**

*   `page` (optional): The page number of questions to return (default: 1).

**Returns:** An object containing:

*   `success`: Boolean indicating if the request was successful.
*   `questions`: A list of question objects, each containing id, question, answer, category, and difficulty.
*   `total_questions`: The total number of questions in the database.
*   `categories`: A dictionary of id: category_string key-value pairs.
*   `current_category`: The category of the returned questions (currently always null).

```json
{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What is the capital of France?",
      "answer": "Paris",
      "category": "3",
      "difficulty": 1
    }
  ],
  "total_questions": 100,
  "categories": {
    "1": "Science"
  },
  "current_category": null
}
```
**3. DELETE /questions/<int:question_id>**

Deletes a question by ID.

**Request Arguments:** None

**Returns:**

*   `success`: Boolean indicating if the request was successful.
*   `deleted`: The ID of the deleted question.

```json
{
  "success": true,
  "deleted": 12
}
```
**4. POST /questions**

Creates a new question.

**Request Body:**

*   `question`: The text of the question.
*   `answer`: The answer to the question.
*   `category`: The ID of the category for the question.
*   `difficulty`: The difficulty level of the question (1-5).

**Returns:**

*   `success`: Boolean indicating if the request was successful.
*   `created`: The ID of the created question.

```json
{
  "success": true,
  "created": 123
}
```
**5. POST /questions/search**

Searches for questions based on a search term.

**Request Body:**

*   `searchTerm`: The term to search for in the questions.

**Returns:**

*   `success`: Boolean indicating if the request was successful.
*   `questions`: A list of question objects matching the search term.
*   `total_questions`: The total number of questions matching the search term.

```json
{
  "success": true,
  "questions":,
  "total_questions": 5
}
```
**6. GET /categories/<int:category_id>/questions**

Fetches questions for a given category.

**Request Arguments:** None

**Returns:**

*   `success`: Boolean indicating if the request was successful.
*   `questions`: A list of question objects for the given category.
*   `total_questions`: The total number of questions for the given category.
*   `current_category`: The category of the returned questions.

```json
{
  "success": true,
  "questions":,
  "total_questions": 25,
  "current_category": "Science"
}
```
**7. POST /quizzes**

Fetches a random question for a quiz, based on a category and previous questions.

**Request Body:**

*   `previous_questions`: A list of IDs of previous questions (to avoid repetition).
*   `quiz_category`: An object with the ID of the category to fetch questions from, or 0 for all categories.

**Returns:**

*   `success`: Boolean indicating if the request was successful.
*   `question`: A random question object (or null if there are no more questions).

```json
{
  "success": true,
  "question": {}
}
```
## Error Handlers

The API includes error handlers for the following status codes:

*   **400 Bad Request:** Returned when a required parameter is missing or invalid.
*   **404 Not Found:** Returned when a resource is not found (e.g., a non-existent question or category).
*   **422 Unprocessable Entity:** Returned when a request is well-formed but cannot be processed due to semantic errors.
