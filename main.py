import mysql.connector
import sys

try:
    connection = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        database='flight_game',
        user='root',
        password='MetroSuomi2024',  # change it to your password
        autocommit=True
    )
    print("Database connected successfully!")   # we can comment this line later
except mysql.connector.Error as error:
    print("Error while connecting to MySQL:", error)
    sys.exit(1)  # Exit the program with a non-zero status code indicating an error
