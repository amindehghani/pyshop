import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='shop',
    password='123'
)

print(mydb)