import mysql.connector
import sys
from geopy.distance import distance
import banner
import random
from colorama import Fore, Back, Style

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
    print("Please select a number from 1 to 4 to make your choice.")
    print("1. Login")
    print("2. Registration")
    print("3. Exit")
    print("4. Statistics")

    while True:
        choice = input("Enter your choice: ")
        if choice == "1":
            # login()
            break
        elif choice == "2":
            register_user()
            break
        elif choice == "3":
            print("You've chosen to exit the game. We hope to see you again soon!")
            sys.exit(1)
        elif choice == "4":
            # statistics()
            break
        else:
            print(f"Incorrect! Select the number from 1 to 4, please try again!")
            continue
        
        
# Reads user input for the airport. Returns ICAO code of the selected airport.
def airport_input() -> str:
    # Get all available continent from the database
    continents = database_query("SELECT DISTINCT continent FROM country ORDER BY continent")
    continent_options = [continent[0].lower() for continent in continents]

    while True:

        # Selection of continent
        print("\nAvailable continents:")
        for continent in continents:
            print(continent[0])

        print("\nEnter the continent you want to fly to.\n")

        selected_continent = select_option(continent_options, "Select continent: ", "The continent doesn't exist.")

        # Selection of country
        countries = database_query(f"SELECT iso_country, name FROM country WHERE continent = '{selected_continent}'")

        print("\nAvailable countries in the selected continent:")
        for country in countries:
            print(f"{country[1]} (ISO code: {country[0]})")

        print("\nEnter the country you want to fly to. Use the ISO code of the country.")
        print("Enter 0 if you want to go back to entering continent.\n")

        country_options = [country[0].lower() for country in countries]
        country_options.append("0")
        selected_country = select_option(country_options, "Select country: ", "The country doesn't exist.")

        if selected_country == "0":
            continue

        # Selection of airport
        airports = database_query(f"SELECT ident, name FROM airport WHERE iso_country = '{selected_country}' AND type = 'large_airport'")

        print("\nAvailable airports in the selected country:")
        for airport in airports:
            print(f"{airport[1]} (ICAO code: {airport[0]})")

        print("\nEnter the airport you want to fly to. Use the ICAO code of the airport.")
        print("Enter 0 if you want to go back to entering continent.\n")

        airport_options = [airport[0].lower() for airport in airports]
        airport_options.append("0")
        selected_airport = select_option(airport_options, "Select airport: ", "The airport doesn't exist.")

        if selected_airport == "0":
            continue

        return selected_airport


# Reads user input.
# If the input in lower case is not in the options list, the function reads input again and displays the error message.
# Returns the input when it is in the options list.
def select_option(options: list, input_message: str, error_message: str) -> str:
    while True:
        selected_country = input(input_message)
        if selected_country.lower() in options:
            return selected_country

        print(error_message)


# Executes SQL in the database.
# Returns the result of the SQL.
def database_query(sql: str) -> list:
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
    except mysql.connector.Error as error:
        print(f"Error while executing query in database: {error}")
        sys.exit(1)

    cursor.close()
    return result

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


# example ICAOs: EGSS, VHHH
# print(distance_calcs("EGSS", "VHHH"))  # comment later

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
    print("\n"+Back.LIGHTGREEN_EX + Fore.BLACK + " NEW USER REGISTRATION " + Style.RESET_ALL)

    while True:
        user_name = input("Enter your name: ")
        # Check if user_name length is less than 6 or greater than 20, prompt until valid input is provided
        if len(user_name) < 4 or len(user_name) > 20: # changed 6 to 4 minimum because 6 is too long
            print("Username must be between 4 and 20 characters long.")
            continue

        # Check if the username already exists in the database
        cursor = connection.cursor()
        select_name_query = f"""SELECT name FROM player WHERE name = "{user_name}";"""
        cursor.execute(select_name_query)
        existing_user = cursor.fetchone()
        if existing_user:
            print(f"Username \"{user_name}\" already exists. Please choose another username.")
            continue  # Restart the registration process
        else:
            break

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
    print(f"User {user_name} successfully registered (your password is: {password}).")
    cursor.close()


def main_game():    # main game flow
    #banner.printBanner()  # to print banner (code is in the file "banner")
    #menu()
    airports = start_locations()
    print(f"You are in {airports[0]}. The distance to the suitcase is {distance_calcs(airports[0], airports[1]):.2f} km")
    airport_input()

main_game()