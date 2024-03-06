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

FROM_EACH_CONTINENT = 5  # max 17 as just 17 airports in OC continent

def menu():
    print(Back.LIGHTGREEN_EX + Fore.BLACK + " MENU " + Style.RESET_ALL)
    print("Please select a number from 1 to 4 to make your choice.")
    print("1. Login")
    print("2. Registration")
    print("3. Exit")
    print("4. Statistics")

    while True:
        choice = input("Enter your choice: ")
        if choice == "1":
            login()
            break
        elif choice == "2":
            register_user()
            break
        elif choice == "3":
            print("You've chosen to exit the game. We hope to see you again soon!")
            sys.exit(1)
        elif choice == "4":
            statistics()
            input("Press [ENTER] to continue...")
            menu()
        else:
            print(Fore.LIGHTRED_EX + f"Incorrect! Select the number from 1 to 4, please try again!" + Style.RESET_ALL)
            continue


def login():      # login user
    print("\n"+Back.LIGHTGREEN_EX + Fore.BLACK + " LOGIN USER " + Style.RESET_ALL)
    while True:
        username = input("Enter your username: ")
        cursor = connection.cursor()
        username_check_sql = f"SELECT * FROM player WHERE name='{username}'"
        cursor.execute(username_check_sql)
        username_check_result = cursor.fetchall()
        if len(username_check_result) == 0:
            choice = input("Sorry, wrong username! Do you want to register instead? (y/n)")
            if choice == "y":
                register_user()
                break
            elif choice == "n":
                continue
            else:
                print("Sorry, wrong choice. Enter correct username to login.")
                continue

        password = input("Enter your password: ")

        sql = "SELECT * FROM player WHERE name=%s AND password=%s"
        val = (username, password)

        cursor.execute(sql, val)
        result = cursor.fetchall()

        if result:
            print(Fore.LIGHTGREEN_EX + f"User {username} successfully logged in!" + Style.RESET_ALL + "\n")
            break

        else:
            print(Fore.LIGHTRED_EX + "Sorry, wrong username or password. Try again." + Style.RESET_ALL)


def register_user():     # register new user
    print("\n"+Back.LIGHTGREEN_EX + Fore.BLACK + " NEW USER REGISTRATION " + Style.RESET_ALL)

    while True:
        user_name = input("Enter your name: ")
        # Check if user_name length is less than 6 or greater than 20, prompt until valid input is provided
        if len(user_name) < 4 or len(user_name) > 20: # changed 6 to 4 minimum because 6 is too long
            print(Fore.LIGHTRED_EX + "Username must be between 4 and 20 characters long." + Style.RESET_ALL)
            continue

        # Check if the username already exists in the database
        cursor = connection.cursor()
        select_name_query = f"""SELECT name FROM player WHERE name = "{user_name}";"""
        cursor.execute(select_name_query)
        existing_user = cursor.fetchone()
        if existing_user:
            print(Fore.LIGHTRED_EX + f"Username \"{user_name}\" already exists. Please choose another username." + Style.RESET_ALL)
            continue  # Restart the registration process
        else:
            break

    password = input("Enter your password: ")
    # Check if password length is less than 4, prompt until valid input is provided
    while len(password) < 4:
        print("Password must be at least 4 characters long.")
        password = input("Enter your password: ")

    # Find the maximum id value currently in use
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(id) FROM player")
    max_id_result = cursor.fetchone()
    max_id = max_id_result[0] if max_id_result[0] is not None else 0

    # Insert the airport into the MySQL database with a new id
    new_id = max_id + 1
    # Insert the airport into the MySQL database
    insert_query = "INSERT INTO player (id, name, password) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (new_id, user_name, password))
    print(Fore.LIGHTYELLOW_EX + f"User {user_name} successfully registered (your password is: {password})." + Style.RESET_ALL)
    cursor.close()


def statistics() -> None:        # Requests game statistics from the database and prints them.
    result = database_query("SELECT AVG(co2_consumed), AVG(flights_num), COUNT(*) FROM game WHERE completed = 1")
    co2_average, flights_average, game_count = result[0]
    print(Back.LIGHTGREEN_EX + Fore.BLACK + "STATISTICS" + Style.RESET_ALL)
    if game_count == 0 or co2_average is None or flights_average is None:
        print("\nNo statistics available.\n")
        return

    print(f"\nStatistics for all {game_count} completed games:")
    print(f"Average co2 consumption: {co2_average:.1f}")
    print(f"Average flight amount: {flights_average:.1f}\n")


"""def start_option():
    print("1. Start the game")
    print("2. Continue the game")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        pass
        #new_game()
    elif choice == 2:
        pass
        #continue_game()
    else:
        print("invalid choice")"""


# Reads user input for the airport. Returns ICAO code of the selected airport.
def airport_input(game_id: int) -> str:
    # Get all available continent from the database
    continents = database_query(f"SELECT country.continent FROM airport INNER JOIN country ON airport.iso_country = country.iso_country WHERE airport.ident IN (SELECT airport_ident FROM available_airport WHERE game_id = {game_id}) AND airport.ident NOT IN (SELECT current_location FROM game WHERE id = {game_id}) GROUP BY country.continent")
    continent_options = [str(i) for i in range(1, len(continents) + 1)]
    continent_names = {"AF": "Africa", "AS": "Asia", "EU": "Europe", "NA": "North America", "OC": "Oceania", "SA": "South America"}

    while True:

        # Selection of continent
        print("\nAvailable continents:")
        for i in range(0, len(continents)):
            continent = continents[i]
            continent_name = continent_names[continent[0]] if continent[0] in continent_names else continent[0]
            print(f"{i + 1}. {continent_name}")

        #print("\nEnter the continent you want to fly to. Use the number of the continent.\n")
        print("")

        selected_continent_number = select_option(continent_options, "Select continent: ", "The continent doesn't exist or can't be selected.")
        selected_continent = continents[int(selected_continent_number) - 1][0]

        # Selection of country
        countries = database_query(f"SELECT country.iso_country, country.name FROM airport INNER JOIN country ON airport.iso_country = country.iso_country WHERE airport.ident IN (SELECT airport_ident FROM available_airport WHERE game_id = {game_id}) AND airport.ident NOT IN (SELECT current_location FROM game WHERE id = {game_id}) AND country.continent = '{selected_continent}' GROUP BY country.iso_country")

        print("\nAvailable countries in the selected continent:")
        for i in range(0, len(countries)):
            country = countries[i]
            print(f"{i + 1}. {country[1]}")

        #print("\nEnter the country you want to fly to. Use the number of the country.")
        print("")
        #print("Enter 0 if you want to go back to entering continent.\n")

        country_options = [str(i) for i in range(0, len(countries) + 1)]
        selected_country_number = select_option(country_options, "Select country: ", "The country doesn't exist or can't be selected.")

        if selected_country_number == "0":
            continue

        selected_country = countries[int(selected_country_number) - 1][0]

        # Selection of airport
        airports = database_query(f"SELECT ident, name, municipality FROM airport WHERE iso_country = '{selected_country}' AND ident IN (SELECT airport_ident FROM available_airport WHERE game_id = {game_id}) AND ident NOT IN (SELECT current_location FROM game WHERE id = {game_id})")

        print("\nAvailable airports in the selected country:")
        for i in range(0, len(airports)):
            airport = airports[i]
            print(f"{i + 1}. {airport[1]} ({airport[2]})")

        #print("\nEnter the airport you want to fly to. Use the number of the airport.")
        #print("Enter 0 if you want to go back to entering continent.\n")
        print("")

        airport_options = [str(i) for i in range(0, len(airports) + 1)]
        selected_airport_number = select_option(airport_options, "Select airport: ", "The airport doesn't exist or can't be selected.")

        print("")
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


def fetch_random_large() -> list:
    """
    returns the list of airports, 5 from each continent' ICAO-codes
    """
    continents = ["AF", "AS", "EU", "NA", "OC", "SA"]

    try:
        available_airports = []
        for _ in continents:
            with connection.cursor() as mycursor:
                sql = f""" 
                SELECT airport.ident FROM airport
                LEFT JOIN country
                ON airport.iso_country = country.iso_country
                WHERE airport.type = "large_airport"
                AND country.continent = "{_}";
                """

                mycursor.execute(sql)
                myresult = mycursor.fetchall()

                larges_from_continent = [i[0] for i in myresult]
                random.shuffle(larges_from_continent) # to random
                available_airports.extend(larges_from_continent[:FROM_EACH_CONTINENT])

        random.shuffle(available_airports)
        return available_airports

    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return []


def flights_divisible_by_5(flights_num: int) -> bool:     # checks if the number of flights is divisible by 5
    if flights_num > 0 and flights_num % 5 == 0:
        return True


def emission_calcs(distance_in_km: float) -> float:
    """
    :param distance_in_km:
    :return: CO2 emissions in kg (float)
    Calculate after each flight \n
    source1: https://ourworldindata.org/travel-carbon-footprint \n
    source2: https://www.statista.com/statistics/1185559/carbon-footprint-of-travel-per-kilometer-by-mode-of-transport/ \n
    source3: https://dbpedia.org/page/Flight_length
    """
    if distance_in_km < 1100:
        return distance_in_km * 0.245
    elif 1100 <= distance_in_km < 2000:
        return distance_in_km * 0.151
    else:
        return distance_in_km * 0.148


# Prints the location of the player and the distance from the player to the target.
# The value of the game_id parameter should be the id of the current game.
def print_game_state(game_id: int) -> None:
    # Get data for the player location in the current game
    player_location = database_query(f"SELECT airport.ident, airport.name, country.name, country.continent, airport.municipality FROM airport INNER JOIN country ON airport.iso_country = country.iso_country INNER JOIN game ON game.current_location = airport.ident WHERE game.id = {game_id}")
    if len(player_location) != 1:
        print("Error while loading your current airport data.")
        sys.exit(1)

    # Get data for the target location in the current game
    target_location = database_query(f"SELECT airport.ident FROM airport INNER JOIN game ON airport.ident = game.target_location WHERE game.id = {game_id}")
    if len(target_location) != 1:
        print("Error while loading your target airport data.")
        sys.exit(1)

    # Print the current game state
    print(Back.WHITE + Fore.LIGHTWHITE_EX + f" You are currently at {player_location[0][1]}, located in {player_location[0][4]}, {player_location[0][2]} ({player_location[0][3]}). " + Style.RESET_ALL)
    print(Back.WHITE + Fore.LIGHTWHITE_EX + " The distance to your owner is " + Fore.BLACK + Back.LIGHTYELLOW_EX + f" {distance_calcs(player_location[0][0], target_location[0][0]):.0f} "+Back.WHITE + Fore.LIGHTWHITE_EX + " km. " + Style.RESET_ALL)


# Creates a new game for a player.
# Returns the id of the created game.
def create_game(player_id: int) -> int:
    cursor = connection.cursor()

    # Find the maximum id value currently in use
    cursor.execute("SELECT MAX(id) FROM game")
    max_id_result = cursor.fetchone()
    max_id = max_id_result[0] if max_id_result[0] is not None else 0
    game_id = max_id + 1                          # create id for the game

    airports = fetch_random_large()                  # get list of the airports

    current_location = random.choice(airports)  # get start/current location
    target_location = random.choice(airports)   # get goal location
    while current_location == target_location:  # check that target and player are not in the same location
        target_location = random.choice(airports)

    distance = distance_calcs(current_location, target_location)
    flights_num = 0                               # set flights_num as 0 at the beginning
    emissions = 0                               # set emissions as 0 at the beginning

    insert_query = """
    INSERT INTO game (id, player_id, current_location, target_location, co2_consumed, flights_num, distance_to_target) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (game_id, player_id, current_location, target_location, emissions, flights_num, distance))

    for icao in airports:
        insert_query = """
        INSERT INTO available_airport (game_id, airport_ident) 
        VALUES (%s, %s)
        """
        cursor.execute(insert_query, (game_id, icao))

    cursor.close()

    return game_id


def game(game_id: int) -> None:
    cursor = connection.cursor()

    # Get the target location from the database
    cursor.execute(f"SELECT target_location FROM game WHERE id = {game_id}")
    target_location_result = cursor.fetchall()

    if len(target_location_result) != 1:
        print("Error while loading your target airport data.")
        sys.exit(1)

    target_location = target_location_result[0][0]

    print(Back.LIGHTGREEN_EX + Fore.BLACK + " GAME START " + Style.RESET_ALL)

    # Game loop
    while True:
        print_game_state(game_id)
        current_location = airport_input(game_id)

        distance = distance_calcs(current_location, target_location)
        emissions = emission_calcs(distance)

        update_query = """
        UPDATE game 
        SET current_location = %s, target_location = %s, co2_consumed = co2_consumed + %s, flights_num = flights_num + %s, distance_to_target = %s 
        WHERE id = %s;"""
        cursor.execute(update_query, (current_location, target_location, emissions, 1, distance, game_id))

        if current_location == target_location:
            print("You won!")
            update_query = """
            UPDATE game SET completed = %s WHERE id = %s;
            """
            cursor.execute(update_query, (1, game_id))
            break
        #if flights_divisible_by_5(flights_num):
            #goal_location = random_location(airports)

    cursor.close()


def main_game():    # main game flow
    banner.printBanner()  # to print banner (code is in the file "banner") (commented during testing)
    #menu()
    database_query("INSERT IGNORE INTO player VALUES (1, 'Test User', '1')") # Delete this row later. This row makes sure that there is a user with id 1 in the database so that the game is currently playable.
    game(create_game(1))


main_game()
