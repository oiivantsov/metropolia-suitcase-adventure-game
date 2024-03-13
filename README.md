# 🎒 Welcome to Suitcase Adventure! 🌍

Embark on a journey like no other as you explore the world while learning about the impact of your travels on the environment! 🌱✈️

## :video_game: About the game

Suitcase Adventure is a game that combines entertainment with environmental education. Players travel the world, learning about carbon footprints of air travel and aiming to minimize their impact. The game features diverse airports and provides feedback on players' travel emissions.

Airports on the map: https://viktoriia-code.github.io/map-airport/

📅 February - March, 2024

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
