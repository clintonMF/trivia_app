import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

from dotenv import load_dotenv
import os

load_dotenv()


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = os.getenv("database_test_name")
        self.database_password = os.getenv("database_password")
        self.database_username = os.getenv("database_username")
        self.database_path = "postgresql://{}:{}@{}/{}".format(self.database_username,self.database_password ,'localhost:5432',self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        
    def test_404_resource_not_found(self):
        res = self.client().get('/categories/5')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(data["success"], False)
        
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        
        question = Question.query.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["categories"])
        self.assertEqual(data["total_questions"], len(question))
        
    def test_404_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"],False)
        self.assertEqual(data["message"], "resource not found")
        
    # def test_delete_question(self):
    #     res= self.client().delete('/questions/5')
    #     data = json.loads(res.data)
        
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["deleted"],5)
        
    def test_422_if_question_does_not_exist(self):
        res= self.client().delete('/questions/1000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
        
    def test_post_question(self):
        res = self.client().post('/questions', json={
            "question":"testing question",
            "answer":"testing",
            "difficulty": 1,
            "category": 3,
        })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        
    def test_405_method_not_allowed(self):
        res = self.client().post('/questions/4', json={
            "question":"testing question",
            "answer":"testing",
            "difficulty": 1,
            "category": 3,
        })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["message"],"method not allowed")
        self.assertEqual(data["success"], False)
        
    def test_search_for_a_question_with_result(self):
        res = self.client().post('/questions', json={"search_term":"who discovered"})
        data = json.loads(res.data)
        
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["questions"])
        
    def test_422_search_for_a_question_without_result(self):
        res = self.client().post('/questions', json={"search_term":"whofdasjkl;jkfdk"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"],"unprocessable")
        
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        
        questions = Question.query.all()
        current_category = Category.query.get(1)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["total_questions"],len(questions))
        self.assertEqual(data["current_category"],current_category.type)
        
    def test_422_if_category_does_not_exist(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)       
 
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
        
    def test_quizzes(self):
        res = self.client().post('/quizzes', json={"previous_questions":[9,2,11],"quiz_category":5})       
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])
        
    def test_400_bad_request_for_quizzes(self):
        res = self.client().post('/quizzes', json={"previous_questions":[9,2,11]})       
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")
    
    def test_422_if_category_does_not_exist(self):
        res = self.client().post('/quizzes', json={"previous_questions":[9,2,11],"quiz_category":100})       
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"],False)
        self.assertEqual(data["message"],"unprocessable")      
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()