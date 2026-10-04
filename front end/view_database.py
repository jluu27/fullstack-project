import sqlite3
import os

print("Database:", os.path.abspath("database.db"))

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

print("Users:", users)

cursor.execute("SELECT * FROM characters")
characters = cursor.fetchall()

print("characters:", characters)
connection.close()  