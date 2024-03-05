import mysql.connector
import sys
from geopy.distance import distance
import banner
import random

try:
    connection = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        database='suitcase_game',
        user='root',  # change it to your username
        password='metro0',  # change it to your password
        autocommit=True
    )
    # print("Database connected successfully!")  # we can comment this line later
except mysql.connector.Error as error:
    print("Error while connecting to MySQL:", error)
    sys.exit(1)  # Exit the program with a non-zero status code indicating an error

banner.printBanner()  # to print banner (code is in the file "banner")

# pause
input("\033[32mPress [Enter] to continue...\033[0m")

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
# Reads user input for the airport. Returns ICAO code of the selected airport.
def airport_input(game_id: int) -> str:
    # Get all available continent from the database
    continents = database_query(f"SELECT country.continent FROM airport INNER JOIN country ON airport.iso_country = country.iso_country WHERE airport.type = 'large_airport' AND airport.ident NOT IN (SELECT current_location FROM game WHERE id = {game_id}) GROUP BY country.continent")
    continent_options = [str(i) for i in range(1, len(continents) + 1)]

    while True:

        # Selection of continent
        print("\nAvailable continents:")
        for i in range(0, len(continents)):
            continent = continents[i]
            print(f"{i + 1}: {continent[0]}")

        print("\nEnter the continent you want to fly to. Use the number of the continent.\n")

        selected_continent_number = select_option(continent_options, "Select continent: ", "The continent doesn't exist or can't be selected.")
        selected_continent = continents[int(selected_continent_number) - 1][0]

        # Selection of country
        countries = database_query(f"SELECT country.iso_country, country.name FROM airport INNER JOIN country ON airport.iso_country = country.iso_country WHERE airport.type = 'large_airport' AND airport.ident NOT IN (SELECT current_location FROM game WHERE id = {game_id}) AND country.continent = '{selected_continent}' GROUP BY country.iso_country")

        print("\nAvailable countries in the selected continent:")
        for i in range(0, len(countries)):
            country = countries[i]
            print(f"{i + 1}: {country[1]}")

        print("\nEnter the country you want to fly to. Use the number of the country.")
        print("Enter 0 if you want to go back to entering continent.\n")

        country_options = [str(i) for i in range(0, len(countries) + 1)]
        selected_country_number = select_option(country_options, "Select country: ", "The country doesn't exist or can't be selected.")

        if selected_country_number == "0":
            continue

        selected_country = countries[int(selected_country_number) - 1][0]

        # Selection of airport
        airports = database_query(f"SELECT ident, name, municipality FROM airport WHERE iso_country = '{selected_country}' AND type = 'large_airport' AND ident NOT IN (SELECT current_location FROM game WHERE id = {game_id})")

        print("\nAvailable airports in the selected country:")
        for i in range(0, len(airports)):
            airport = airports[i]
            print(f"{i + 1}: {airport[1]} ({airport[2]})")

        print("\nEnter the airport you want to fly to. Use the number of the airport.")
        print("Enter 0 if you want to go back to entering continent.\n")

        airport_options = [str(i) for i in range(0, len(airports) + 1)]
        selected_airport_number = select_option(airport_options, "Select airport: ", "The airport doesn't exist or can't be selected.")

        if selected_airport_number == "0":
            continue

        selected_airport = airports[int(selected_airport_number) - 1][0]
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


def distance_calcs(icao1: str, icao2: str) -> float:
    """
    returns the distance between two airports in kilometers (float number)
    """
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


def fetch_all_large() -> list:
    """
    returns the list of 451 airports' ICAO-codes
    """
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


def random_location(airports) -> str:
    """
    returns a random ICAO code from the current list of airports, and also reduces the list by 1
    """
    new_icao = airports.pop(random.choice(range(len(airports))))
    return new_icao


def flights_divisible_by_5(flights_num) -> bool:
    """
    checks if the number of flights is divisible by 5
    """
    if flights_num > 0 and flights_num % 5 == 0:
        return True


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
    cursor.close()