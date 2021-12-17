import os
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

  cors = CORS(app, resources={r"/api/*/": {"origins": "*"}})

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response

  # Since this format needs to be called multiple times throughout the code,
  # I turned it into a function, to reduce code repetition
  def format_categories():
      categories = Category.query.all()
      categories_dict = {}
      for category in categories:
          categories_dict[category.id] = category.type
      return categories_dict

  # Another repeated multi-line code block. Checks if a provided id for a
  # category exists in the database, so that it is not hardcoded that only
  # 6 possible categories exist in the game
  def is_existing_category(id):
      categories = Category.query.all()
      ids = [category.id for category in categories]
      if id in ids:
          return True
      else:
          return False

  @app.route('/categories', methods=['GET'])
  def get_all_categories():
      all_categories = {
          "success": True,
          "categories": format_categories()
      }
      return jsonify(all_categories)

  @app.route('/questions', methods=['GET'])
  def get_questions():
      page = request.args.get('page', 1, type=int)
      start = (page - 1) * 10
      end = start + 10
      questions = Question.query.order_by(Question.id).all()
      formatted_questions = [question.format() for question in questions]
      if len(formatted_questions[start:end]) == 0:
          abort(404)
      output = {
          'success': True,
          'questions': formatted_questions[start:end],
          'total_questions': len(questions),
          'categories': format_categories()
      }
      return jsonify(output)

  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
      try:
          question = Question.query.filter(Question.id == id).one_or_none()
          if question is None:
              abort(404)
          question.delete()
          return jsonify({ 'success': True })
      except:
          abort(422)

  # Since the frontend only had one specified endpoint for POST for questions,
  # the code checks whether the user is looking to search for a question or
  # trying to post a new question with two try catch blocks.
  @app.route('/questions', methods=['POST'])
  def post_question():
      form = request.json
      try:
          if form['searchTerm']:
              questions = Question.query \
              .filter(Question.question.ilike('%'+form['searchTerm']+'%')).all()
              formatted_questions = [question.format() for question in questions]
              result = {
                  'success': True,
                  'questions': formatted_questions,
                  'totalQuestions': len(questions)
              }
              return jsonify(result)
      except:
          try:
              question = Question(
                  question=form['question'],
                  answer=form['answer'],
                  category=form['category'],
                  difficulty=form['difficulty']
              )
              question.insert()
              return jsonify({ 'success': True })
          except:
              abort(400)

  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def get_questions_by_category(id):
      if not is_existing_category(id):
          abort(404)
      questions = Question.query.filter(Question.category == id).all()
      formatted_questions = [question.format() for question in questions]
      result = {
          'success': True,
          'questions': formatted_questions,
          'totalQuestions': len(questions)
      }
      return jsonify(result)

  @app.route('/quizzes', methods=['POST'])
  def get_next_question():
      form = request.json
      category_id = form['quiz_category']
      if not is_existing_category(category_id):
          abort(404)
      if category_id == 0:
          questions = Question.query.all()
      else:
          questions = Question.query.filter(Question.category==category_id).all()
      formatted_questions = [question.format() for question in questions]
      new_question = False
      while new_question == False:
          length = len(formatted_questions)
          if length == 0:
              return jsonify({ 'question': None })
          selection = random.randint(0, length - 1)
          if len(form['previous_questions']) > 0:
              question_id = formatted_questions[selection]['id']
              if question_id in form['previous_questions']:
                  formatted_questions.pop(selection)
                  continue
              else:
                  new_question = True
          else:
              new_question = True
      result = {
          'success': True,
          'question': formatted_questions[selection]
      }
      return jsonify(result)

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "Bad request"
      }), 400

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "Not found"
      }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
      return jsonify({
          "success": False,
          "error": 405,
          "message": "Method not allowed"
      }), 405

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "Unprocessable"
      }), 422

  return app
