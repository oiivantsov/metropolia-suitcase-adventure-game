import mysql.connector
import sys
from geopy.distance import distance
import random

try:
    connection = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        database='suitcase_game',
        user='root',  # change it to your username
        password='MetroSuomi2024',  # change it to your password
        autocommit=True
    )
    # print("Database connected successfully!")  # we can comment this line later
except mysql.connector.Error as error:
    print("Error while connecting to MySQL:", error)
    sys.exit(1)  # Exit the program with a non-zero status code indicating an error

def menu():
    print("1. Login")
    print("2. Registration")
    print("3. Exit")
    print("4. Statistics")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        # login()
        pass

    elif choice == 2:
        # register()
        pass

    elif choice == 3:
        exit()

    elif choice == 4:
        # statistics()
        pass

    else:
        print("The input is incorrect, please try again")



def distance_calcs(icao1, icao2):  # returns km between two airports in kilometers (integer)

    locations = [icao1, icao2]
    coordinates = []

    for _ in locations:

        sql = f""" 
        SELECT airport.latitude_deg, airport.longitude_deg
        FROM airport
        LEFT JOIN country 
        ON airport.iso_country = country.iso_country
        WHERE ident = "{_}";
        """

        mycursor = connection.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchall()

        if mycursor.rowcount > 0:
            coordinates.append((myresult[0][0], myresult[0][1]))
        else:
            print("ICAO code is missing from database!")
            return False

    return distance(coordinates[0], coordinates[1]).km


def fetch_all_large():  # (technical function) return the list of 451 airports' ICAO-codes
    try:
        with connection.cursor() as mycursor:
            sql = """ 
            SELECT ident FROM airport
            WHERE airport.type = "large_airport";
            """

            mycursor.execute(sql)
            myresult = mycursor.fetchall()

            return [i[0] for i in myresult]

    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return []


def start_locations():  # returns the list of 2 random ICAO-codes from 451 airports
    all_locations = fetch_all_large()

    if len(all_locations) < 2:
        print("Error")
        return None

    icao1 = all_locations.pop(random.choice(range(len(all_locations))))
    icao2 = all_locations.pop(random.choice(range(len(all_locations))))

    return [icao1, icao2]

def register_user():
    user_name = input("Enter your name: ")
    # Check if user_name length is less than 6 or greater than 20, prompt until valid input is provided
    while len(user_name) < 4 or len(user_name) > 20:      # changed 6 to 4 minimum because 6 is too long
        print("Username must be between 4 and 20 characters long.")
        user_name = input("Enter your name: ")

    # Check if the username already exists in the database
    cursor = connection.cursor()
    select_name_query = f"""SELECT name FROM player WHERE name = "{user_name}";"""
    cursor.execute(select_name_query)
    existing_user = cursor.fetchone()
    if existing_user:
        print("Username already exists. Please choose another username.")
        register_user()  # Restart the registration process
        return

    password = input("Enter your password: ")
    # Check if password length is less than 4, prompt until valid input is provided
    while len(password) < 4:
        print("Password must be at least 4 characters long.")
        password = input("Enter your password: ")

    # Find the maximum id value currently in use
    cursor.execute("SELECT MAX(id) FROM player")
    max_id_result = cursor.fetchone()
    max_id = max_id_result[0] if max_id_result[0] is not None else 0

    # Insert the airport into the MySQL database with a new id
    new_id = max_id + 1
    # Insert the airport into the MySQL database
    insert_query = "INSERT INTO player (id, name, password) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (new_id, user_name, password))
    print(f"User {user_name} successfully registered.")
    connection.close()

register_user()