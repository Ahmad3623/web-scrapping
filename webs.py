import mysql.connector

cnx = mysql.connector.connect(user='MySQL80', password='Ahmad@04',
                              host='127.0.0.1',
                              database='employees')
cnx.close()