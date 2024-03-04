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

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    sql = "SELECT * FROM player WHERE name=%s AND password=%s"
    val = (username, password)

    cursor = yhteys.cursor()
    cursor.execute(sql, val)
    result = cursor.fetchall()

    if result:
        print("Welcome to play game")
        
    else:
        print("Sorry, wrong username or password. Try again.")

def start_option():
    print("1. Start the game")
    print("2. Continue the game")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        #new_game()
    elif choice == 2:
        #continue_game()
    else:
        print("invalid choice")




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


# Prints the location of the player and the distance from the player to the target.
# The value of the game_id parameter should be the id of the current game.
def print_game_state(game_id: int) -> None:
    # Get data for the player location in the current game
    player_location = database_query(f"SELECT airport.ident, airport.name, country.name, country.continent FROM airport INNER JOIN country ON airport.iso_country = country.iso_country INNER JOIN game ON game.current_location = airport.ident WHERE game.id = {game_id}")
    if len(player_location) != 1:
        print("Error while loading your current airport data.")
        sys.exit(1)

    # Get data for the target location in the current game
    target_location = database_query(f"SELECT airport.ident FROM airport INNER JOIN game ON airport.ident = game.target_location WHERE game.id = {game_id}")
    if len(target_location) != 1:
        print("Error while loading your target airport data.")
        sys.exit(1)

    # Print the current game state
    print(f"\nYou are currently at {player_location[0][1]}, located in {player_location[0][2]} ({player_location[0][3]}).")
    print(f"The distance to your owner is {distance_calcs(player_location[0][0], target_location[0][0]):.0f} km.")


# Requests game statistics from the database and prints them.
def statistics() -> None:
    result = database_query("SELECT AVG(co2_consumed), AVG(flights_num), COUNT(*) FROM game WHERE completed = 1")
    co2_average, flights_average, game_count = result[0]

    if game_count == 0 or co2_average is None or flights_average is None:
        print("\nNo statistics available.\n")
        return

    print(f"\nStatistics for all {game_count} completed games:")
    print(f"Average co2 consumption: {co2_average:.1f}")
    print(f"Average flight amount: {flights_average:.1f}\n")
    cursor.close()
