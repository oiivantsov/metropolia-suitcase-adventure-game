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
        password='metro0',  # change it to your password
        autocommit=True
    )
    # print("Database connected successfully!")  # we can comment this line later
except mysql.connector.Error as error:
    print("Error while connecting to MySQL:", error)
    sys.exit(1)  # Exit the program with a non-zero status code indicating an error


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

