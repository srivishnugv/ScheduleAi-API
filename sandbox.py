import mysql.connector
from flask import jsonify
import json
import datetime

# mydb = mysql.connector.connect(
#         host="us-cdbr-east-04.cleardb.com",
#         user="bf74b446fb93c2",
#         password="a599fa14"
#     )
#
# cur = mydb.cursor()
# cur.execute("use heroku_99fce871dfe74ee;")
#
#
# username = "gokay"
# cur = mydb.cursor()
# cur.execute("use heroku_99fce871dfe74ee;")
# select_stmt = "Select * from commitments where username = %(username)s"
# cur.execute(select_stmt, {'username': username})
# #fetchdata = cur.fetchall()
# row_headers=[x[0] for x in cur.description] #this will extract row headers
# rv = cur.fetchall()
# json_data=[]
# for result in rv:
#     json_data.append(dict(zip(row_headers,result)))
# cur.close()
# mydb.close()
# print(json_data)


#response.headers.add('Access-Control-Allow-Origin', '*')
#print(fetchdata)

#
# row_headers=[x[0] for x in cur.description] #this will extract row headers
# rv = cur.fetchall()
# json_data=[]
# for result in rv:
#     json_data.append(dict(zip(row_headers,result)))
# print(json.dumps(json_data))


#
# username = "apiman21"
#
# # select_stmt = "Select exists(Select * from login where username = %(username)s)"
# select_stmt = "Select * from login where username = %(username)s"
# cur.execute(select_stmt, { 'username': username })
# #cur.execute("Select * from login")
# data = cur.fetchall()
# for i in data:
#     print(i)
# print(data)
#
# print(data[0][1])
# if(data[0] == (0,)):
#     print(False)
# else:
#     print(True)
# #print(cur)
# cur.close()
# mydb.close()
#
#
# returnMessage = {
#     'success': False,
#     'username': "apiman21"
# }
#
# print(returnMessage)

def closeTask():
    mydb = mysql.connector.connect(
        host="us-cdbr-east-04.cleardb.com",
        user="bf74b446fb93c2",
        password="a599fa14"
    )

    cur = mydb.cursor()
    cur.execute("use heroku_99fce871dfe74ee;")

    taskId = 15

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
        #cur.execute('update tasks set status="complete" where taskId=%s',taskId)
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

print(closeTask())

# @app.route('/api/v1/fetchTaskCountForCommitment', methods=['POST'])
# def closeTask():
#     mydb = mysql.connector.connect(
#         host="us-cdbr-east-04.cleardb.com",
#         user="bf74b446fb93c2",
#         password="a599fa14"
#     )
#
#     cur = mydb.cursor()
#     cur.execute("use heroku_99fce871dfe74ee;")
#
#     taskId = request.json['taskId']
#     username = request.json['username']
#
#     select_stmt = "Select exists(Select * from tasks where taskId = %(taskId)s)"
#     cur.execute(select_stmt, {'taskId': taskId})
#     data = cur.fetchall()
#     taskFlag = True
#
#     if (data[0] == (0,)):
#         taskFlag = False
#
#     select_stmt = "Select exists(Select * from login where username = %(username)s)"
#     cur.execute(select_stmt, {'username': username})
#     data = cur.fetchall()
#     taskFlag = True
#
#     if (data[0] == (0,)):
#         taskFlag = False
#     else:
#
#         returnMessage = {
#             'success': False,
#             'taskId': taskId,
#             'error': "Task doesn't exist!"
#         }
#         select_stmt = 'update tasks set status="complete" where taskId=%(taskId)s'
#         cur.execute(select_stmt, {'taskId': taskId})
#         mydb.commit()
#
#
#         returnMessage = {
#             'taskId': taskId,
#             'success':True
#         }
#     cur.close()
#     mydb.close()
#     return returnMessage