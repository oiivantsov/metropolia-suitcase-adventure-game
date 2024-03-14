# 🎒 Welcome to Suitcase Adventure! 🌍

Embark on a journey like no other as you explore the world while learning about the impact of your travels on the environment! 🌱✈️

📅 February - March, 2024

## :video_game: About the game

Suitcase Adventure is a game that combines entertainment with environmental education. Players travel the world, learning about carbon footprints of air travel and aiming to minimize their impact. The game features diverse airports and provides feedback on players' travel emissions.
<p align="center">
  <img src="https://github.com/Viktoriia-code/suitcase-adventure-game/assets/43078402/488e28e3-5146-4497-b63f-b6f7c8c7dea5" alt="image" width="600">
</p>

## :floppy_disk: Technical stack overview
* Programming language: Python
* Database: SQL

## :wrench: Installation
1. Clone the Suitcase Adventure repository from GitHub:
```
git clone https://github.com/Viktoriia-code/suitcase-adventure-game.git
```
2. Navigate to the project directory:
```
cd suitcase-adventure-game
```
3. Install the required Python packages using pip:
```
pip install -r requirements.txt
```
4. Replace the password at the connection with your own database password
```
connection = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        database='suitcase_game',
        user='root',
        password='YOUR_DATABASE_PASSWORD_HERE',  # replace it with your database password
        autocommit=True
    )
```

## :electric_plug: Modules
* geopy
* mysql-connector-python
* wikipedia
* colorama
* pygame
* playsound

## :bulb: Airports Map
If you need assistance navigating through airports or want to explore the locations featured in Suitcase Adventure, you can use our interactive map of airports. This map provides visual information about large airports around the world.

https://viktoriia-code.github.io/map-airport/
