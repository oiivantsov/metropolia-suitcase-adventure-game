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