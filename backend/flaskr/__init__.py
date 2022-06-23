import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response


    def paginate(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = selection[start:end]
        formatted_questions = [question.format() for question in questions]

        return formatted_questions


    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        formatted_categories = [
            category.format() for category in categories]

        dic = {}       # is used to store the category id and category type
        for item in formatted_categories:
            id = item['id']
            type = item['type']

            dic[str(id)] = type

        return jsonify({
            "categories": dic,
            "success": True
        })


    @app.route('/questions')
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        questions = paginate(request, selection)

        if len(questions) == 0:
            abort(404)

        categories = Category.query.all()
        formatted_categories = [
            category.format() for category in categories]

        dic = {}       # is used to store the category id and category type
        for item in formatted_categories:
            id = item['id']
            type = item['type']

            dic[str(id)] = type

        if len(questions) == 0:
            current_category_name = None
            questions = None
        else:
            category_id = int(questions[0]["category"])
            current_category = Category.query.get(category_id)
            current_category_name = current_category.type

        return jsonify({
            "success": True,
            "questions": questions,
            "total_questions": len(selection),
            "categories": dic,
            "current_category": current_category_name,
        })


    @app.route('/questions/<question_id>', methods=["DELETE"])
    def delete_book(question_id):
        question = Question.query.get(question_id)

        try:
            question.delete()

            return jsonify({
                "success": True,
                "deleted": question_id
            })
        except BaseException:
            return abort(422)


    @app.route('/questions', methods=["POST"])
    def post_question():
        data = request.get_json()
        search_term = data.get('searchTerm', None)
        question = data.get('question', None)
        answer = data.get('answer', None)
        difficulty = data.get('difficulty', None)
        category = data.get('category', None)

        try:
            if search_term:
                questions = Question.query.filter(Question.question.ilike(
                    '%{}%'.format(search_term))).all()  
                # the questions for the search term
                # the search term questions formatted
                formatted_questions = paginate(request, questions)

                if len(formatted_questions) == 0:
                    return abort(422)
                else:
                    category_id = int(formatted_questions[0]["category"])
                    current_category = Category.query.get(category_id)
                    current_category_name = current_category.type

                return jsonify({
                    "success": True,
                    "questions": formatted_questions,
                    "total_questions": len(formatted_questions),
                    "current_category": current_category_name
                })

            else:
                if answer == "" or question == "":
                    return abort(422)
                if answer is None or question is None:
                    return abort(422)
                new_question = Question(
                    question=question,
                    answer=answer,
                    category=category,
                    difficulty=difficulty
                )

                new_question.insert()

                return jsonify({
                    "success": True,
                })
        except BaseException:
            return abort(422)


    @app.route('/categories/<id>/questions')
    def get_questions_by_category(id):
        try:
            selections = Question.query.filter_by(category=id).all()
            questions = paginate(request, selections)   # paginated questions
            all_questions = Question.query.all()   # all questions
            current_category = Category.query.get(id)   # current category

            return jsonify({
                "success": True,
                "questions": questions,
                "total_questions": len(all_questions),
                "current_category": current_category.type
            })
        except BaseException:
            return abort(422)

    @app.route('/quizzes', methods=["POST"])
    def quiz():
        data = request.get_json()
        if data is None:
            return abort(400)
        print(data)
        previous_questions = data.get("previous_questions", None)
        quiz_category = data.get("quiz_category", None)

        if quiz_category is None or previous_questions is None:
            return abort(400)
        try:
            if quiz_category['id'] == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter_by(
                    category=quiz_category['id']).all()

            question_ids = [question.id for question in questions]
            new_questions = []

            for id in question_ids:
                if id not in previous_questions:
                    new_questions.append(id)
            random_question_id = random.choice(new_questions)

            question = Question.query.get(random_question_id)
            return jsonify({
                "success": True,
                "question": question.format()
            })
        except:
            return abort(422)


# ----------------------------------
# Error handler section
# ----------------------------------

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "message": "bad request",
            "error": 400,
            "success": False
        }), 400

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "message": "resource not found",
            "error": 404,
            "success": False
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "message": "method not allowed",
            "error": 405,
            "success": False
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "message": "unprocessable",
            "error": 422,
            "success": False
        }), 422

    return app