from flask import Flask, request, jsonify
from flask_cors import CORS
import json
app = Flask(__name__)
CORS(app)

import mysql.connector

@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

@app.route('/api/v1/test')
def testApi():
    response = jsonify({'some': 'data'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/v1/getLoginInfo')
def getLoginInfo():
    mydb = mysql.connector.connect(
        host="us-cdbr-east-04.cleardb.com",
        user="bf74b446fb93c2",
        password="a599fa14"
    )

    cur = mydb.cursor()
    cur.execute("use heroku_99fce871dfe74ee;")
    cur.execute("SELECT * FROM login")
    fetchdata = cur.fetchall()
    cur.close()
    mydb.close()
    response = jsonify(fetchdata)
    #response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/v1/signup', methods=['POST'])
def signup():
    mydb = mysql.connector.connect(
        host="us-cdbr-east-04.cleardb.com",
        user="bf74b446fb93c2",
        password="a599fa14"
    )

    cur = mydb.cursor()
    cur.execute("use heroku_99fce871dfe74ee;")

    username = request.json['username']

    select_stmt = "Select exists(Select * from login where username = %(username)s)"
    cur.execute(select_stmt, {'username': username})
    data = cur.fetchall()

    if (data[0] == (0,)):
        flag = 'empty'
    else:
        flag = 'full'

    if flag == 'empty' and (request.json['password'] == request.json['repeatPassword']):
        password = request.json['password']

        cur.execute("INSERT INTO login VALUES (%s, %s)", (username, password))

        mydb.commit()

        returnMessage = {
            'success': True,
            'username': request.json['username'],
        }
    else:
        returnMessage = {
            'success': False,
            'username': request.json['username'],
        }
    cur.close()
    mydb.close()
    #return jsonify({'returnMessage': returnMessage})
    return returnMessage

@app.route('/api/v1/login', methods=['POST'])
def login():
    mydb = mysql.connector.connect(
        host="us-cdbr-east-04.cleardb.com",
        user="bf74b446fb93c2",
        password="a599fa14"
    )

    cur = mydb.cursor()
    cur.execute("use heroku_99fce871dfe74ee;")

    username = request.json['username']
    password = request.json['password']

    select_stmt = "Select exists(Select * from login where username = %(username)s)"
    cur.execute(select_stmt, {'username': username})
    data = cur.fetchall()

    if (data[0] == (0,)):
        returnMessage = {
            'success': False,
            'username': username
        }
    else:
        flag = 'full'
        select_stmt = "Select * from login where username = %(username)s"
        cur.execute(select_stmt, {'username': username})
        data = cur.fetchall()
        if(password == data[0][1]):
            returnMessage = {
                'success': True,
                'username': username
            }
        else:
            returnMessage = {
                'success': False,
                'username': username
            }
    cur.close()
    mydb.close()
    return returnMessage


@app.route('/api/v1/fetchCommitments', methods=['POST'])
def fetchCommitments():
    mydb = mysql.connector.connect(
        host="us-cdbr-east-04.cleardb.com",
        user="bf74b446fb93c2",
        password="a599fa14"
    )
    username = request.json['username']
    cur = mydb.cursor()
    cur.execute("use heroku_99fce871dfe74ee;")

    select_stmt = "Select exists(Select * from login where username = %(username)s)"
    cur.execute(select_stmt, {'username': username})
    data = cur.fetchall()

    if (data[0] == (0,)):
        returnMessage = {
            'success': False,
            'username': username
        }
    else:
        select_stmt = "Select * from commitments where username = %(username)s"
        cur.execute(select_stmt, {'username': username})
        rv = cur.fetchall()
        row_headers = []
        for x in cur.description:
            row_headers.append(x[0])
        returnMessage = []
        for result in rv:
            returnMessage.append(dict(zip(row_headers, result)))
        returnMessage = json.dumps(returnMessage)
    cur.close()
    mydb.close()
    return returnMessage

@app.route('/api/v1/addCommitment', methods=['POST'])
def addCommitment():
    mydb = mysql.connector.connect(
        host="us-cdbr-east-04.cleardb.com",
        user="bf74b446fb93c2",
        password="a599fa14"
    )

    cur = mydb.cursor()
    cur.execute("use heroku_99fce871dfe74ee;")

    username = request.json['username']

    select_stmt = "Select exists(Select * from login where username = %(username)s)"
    cur.execute(select_stmt, {'username': username})
    data = cur.fetchall()

    if (data[0] == (0,)):
        returnMessage = {
            'success': False,
            'username': username,
            'error': "User doesn't exist!"
        }
    else:
        commitmentName = request.json['commitmentName']
        colorScheme = request.json['colorScheme']

        cur.execute("INSERT INTO commitments(commitmentName,colorScheme,username) VALUES (%s, %s, %s)", (commitmentName, colorScheme, username))

        mydb.commit()

        cur.execute("SELECT LAST_INSERT_ID();")
        data = cur.fetchall()

        returnMessage = {
            'commitmentId': data[0][0],
            'commitmentName': request.json['commitmentName'],
            'colorScheme': request.json['colorScheme']
        }

    cur.close()
    mydb.close()
    return returnMessage

@app.route('/api/v1/addTask', methods=['POST'])
def addTask():
    mydb = mysql.connector.connect(
        host="us-cdbr-east-04.cleardb.com",
        user="bf74b446fb93c2",
        password="a599fa14"
    )

    cur = mydb.cursor()
    cur.execute("use heroku_99fce871dfe74ee;")

    username = request.json['username']

    select_stmt = "Select exists(Select * from login where username = %(username)s)"
    cur.execute(select_stmt, {'username': username})
    data = cur.fetchall()

    if (data[0] == (0,)):
        returnMessage = {
            'success': False,
            'username': username,
            'error': "User doesn't exist!"
        }
    else:
        commitmentId = request.json['commitmentId']
        taskName = request.json['taskName']
        status = request.json['status']
        dueDateTime = request.json['dueDateTime']
        scheduleDateTime = request.json['scheduleDateTime']
        estTimeOfCompletion = request.json['estimatedTimeOfCompletion']

        cur.execute("INSERT INTO tasks(username,commitmentId,taskName,status,dueDateTime,scheduleDateTime,estTimeOfCompletion) VALUES (%s, %s, %s, %s, %s, %s, %s)",(username, commitmentId, taskName, status, dueDateTime, scheduleDateTime, estTimeOfCompletion))

        mydb.commit()

        cur.execute("SELECT LAST_INSERT_ID();")
        data = cur.fetchall()

        select_stmt = ("select colorScheme from commitments where commitmentId = %(commitmentId)s")
        cur.execute(select_stmt, {'commitmentId': commitmentId})
        data2 = cur.fetchall()

        returnMessage = {
            'taskId': data[0][0],
            'commitmentId': commitmentId,
            'taskName': taskName,
            'status':status,
            'dueDateTime': dueDateTime,
            'scheduleDateTime':scheduleDateTime,
            'estimatedTimeOfCompletion': estTimeOfCompletion,
            'colorScheme': data2[0][0]
        }
    cur.close()
    mydb.close()
    return returnMessage

@app.route('/api/v1/fetchPendingTasks', methods=['POST'])
def fetchPendingTasks():
    mydb = mysql.connector.connect(
        host="us-cdbr-east-04.cleardb.com",
        user="bf74b446fb93c2",
        password="a599fa14"
    )
    username = request.json['username']
    cur = mydb.cursor()
    cur.execute("use heroku_99fce871dfe74ee;")

    select_stmt = "Select exists(Select * from login where username = %(username)s)"
    cur.execute(select_stmt, {'username': username})
    data = cur.fetchall()

    if (data[0] == (0,)):
        returnMessage = {
            'success': False,
            'username': username
        }
    else:
        select_stmt = 'SELECT * FROM tasks where username=%(username)s and status="pending";'
        cur.execute(select_stmt, {'username': username})
        rv = cur.fetchall()
        row_headers = []
        for x in cur.description:
            row_headers.append(x[0])
        returnMessage = []
        for result in rv:
            returnMessage.append(dict(zip(row_headers, result)))
        returnMessage = json.dumps(returnMessage,default=str)
    cur.close()
    mydb.close()
    return returnMessage

@app.route('/api/v1/editTask', methods=['POST'])
def editTask():
    mydb = mysql.connector.connect(
        host="us-cdbr-east-04.cleardb.com",
        user="bf74b446fb93c2",
        password="a599fa14"
    )

    cur = mydb.cursor()
    cur.execute("use heroku_99fce871dfe74ee;")

    username = request.json['username']

    select_stmt = "Select exists(Select * from login where username = %(username)s)"
    cur.execute(select_stmt, {'username': username})
    data = cur.fetchall()

    if (data[0] == (0,)):
        returnMessage = {
            'success': False,
            'username': username,
            'error': "User doesn't exist!"
        }
    else:
        taskId = request.json['taskId']
        commitmentId = request.json['commitmentId']
        taskName = request.json['taskName']
        #status = request.json['status']
        #dueDateTime = request.json['dueDateTime']
        #scheduleDateTime = request.json['scheduleDateTime']
        #estTimeOfCompletion = request.json['estimatedTimeOfCompletion']

        #query = ("update tasks set commitmentId=%s,taskName=%s,status=%s,dueDateTime=%s,scheduleDateTime=%s,estTimeOfCompletion=%s where taskId=%s;")
        #values = (commitmentId, taskName, status, dueDateTime, scheduleDateTime, estTimeOfCompletion, taskId)
        query = ("update tasks set commitmentId=%s,taskName=%s where taskId=%s;")
        values = (commitmentId, taskName, taskId)
        cur.execute(query, values)
        mydb.commit()

        select_stmt = ("select colorScheme from commitments where commitmentId = %(commitmentId)s")
        cur.execute(select_stmt, {'commitmentId': commitmentId})
        data2 = cur.fetchall()

        # returnMessage = {
        #     'taskId': taskId,
        #     'commitmentId': commitmentId,
        #     'taskName': taskName,
        #     'status':status,
        #     'dueDateTime': dueDateTime,
        #     'scheduleDateTime':scheduleDateTime,
        #     'estimatedTimeOfCompletion': estTimeOfCompletion,
        #     'colorScheme': data2[0][0]
        # }
        returnMessage = {
            'taskId': taskId,
            'commitmentId': commitmentId,
            'taskName': taskName,
            'colorScheme': data2[0][0]
        }
    cur.close()
    mydb.close()
    return returnMessage

@app.route('/api/v1/closeTask', methods=['POST'])
def closeTask():
    mydb = mysql.connector.connect(
        host="us-cdbr-east-04.cleardb.com",
        user="bf74b446fb93c2",
        password="a599fa14"
    )

    cur = mydb.cursor()
    cur.execute("use heroku_99fce871dfe74ee;")

    taskId = request.json['taskId']

    select_stmt = "Select exists(Select * from tasks where taskId = %(taskId)s)"
    cur.execute(select_stmt, {'taskId': taskId})
    data = cur.fetchall()

    if (data[0] == (0,)):
        returnMessage = {
            'success': False,
            'taskId': taskId,
            'error': "Task doesn't exist!"
        }
    else:
        select_stmt = 'update tasks set status="complete" where taskId=%(taskId)s'
        cur.execute(select_stmt, {'taskId': taskId})
        mydb.commit()


        returnMessage = {
            'taskId': taskId,
            'success':True
        }
    cur.close()
    mydb.close()
    return returnMessage