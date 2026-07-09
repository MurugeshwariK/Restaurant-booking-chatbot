import mysql.connector


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="darshini@2005",
    database="restaurant_bot"
)


cursor = db.cursor(dictionary=True)

print("Database connected successfully")
