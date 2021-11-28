# from flask import render_template, request, abort, jsonify
# from app import app
#
# import mysql.connector
#
# mydb = mysql.connector.connect(
#     host="localhost",
#     port="3306",
#     user="root",
#     password="Goonies#1068"
# )
#
# @app.route('/')
# @app.route('/index')
# def index():
#     cur = mydb.cursor()
#     cur.execute("use schedule_ai")
#     cur.execute("SELECT * FROM login")
#     fetchdata = cur.fetchall()
#     cur.close()
#     return render_template('index.html',data=fetchdata)
#
# @app.route('/signup', methods=['POST'])
# def sign_up():
#     if not request.json or not 'title' in request.json:
#         abort(400)
#     #cur = mydb.cursor()
#     #cur.execute("use schedule_ai")
#     #cur.execute("SELECT * FROM login")
#     #check password == repeated password:
#     if(request.json['password'] == request.json['repeatPassword']):
#         #verify new username, then add to database and return success message
#         task = {
#             'username': request.json['username'],
#             'password': request.json['password']
#         }
#
#         returnMessage = {
#             'success': True,
#             'username': request.json['username'],
#             'isUserSignedIn': True
#         }
#     else:
#         returnMessage = {
#             'success': False,
#             'username': request.json['username'],
#             'isUserSignedIn': False
#         }
#     return jsonify({'returnMessage': returnMessage}), 201
#
# @app.route('/signup2')
# def sign_up_test():
#     param = {
#       "username": "vishnu2",
#       "password": "pass1",
#       "repeatPassword": "pass2"
#     }
#     return render_template('index.html',data=param)