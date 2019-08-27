# Football Statistics Project
This project is a web application for comparing statistical data for football (soccer) players, teams, etc.
While primarily focused on FC Barcelona the project is generic and can be applied to any or multiple teams.

The project is currently being developed in the `dev` branch until proper testing is done for base version features. You can see the progress in the projects page.

The application is built using Python as the core language and the [Django](https://www.djangoproject.com/) framework for the front-end and back-end. [Bootstrap](https://getbootstrap.com/) and a bit of Javascript are used for the front-end. At the moment testing is done through unit and integration tests and are run using [TravisCI](https://travis-ci.org/). System testing through [Selenium](https://www.seleniumhq.org/) is planned for a later time. [Codecov](https://codecov.io/) is used to monitor code coverage from the written tests.

A live version of the application is hosted on [Heroku](https://www.heroku.com/) and is available to demo:
https://soccerstatistics.herokuapp.com

Master branch stats:

<a href="https://travis-ci.org/santoyoalfredo/barca">
  <img src="https://travis-ci.org/santoyoalfredo/barca.svg?branch=master">
</a>
<a href="https://codecov.io/gh/santoyoalfredo/barca">
  <img src="https://codecov.io/gh/santoyoalfredo/barca/branch/master/graph/badge.svg">
</a>

Dev branch stats (latest build):

<a href="https://travis-ci.org/santoyoalfredo/barca">
  <img src="https://travis-ci.org/santoyoalfredo/barca.svg?branch=dev">
</a>
<a href="https://codecov.io/gh/santoyoalfredo/barca">
  <img src="https://codecov.io/gh/santoyoalfredo/barca/branch/dev/graph/badge.svg">
</a>

## Motivations
I decided to work on this project since I was able to combine my interests in sports and software development. Building this application will allow me to further enhance my current knowledge and add to my skillset as I work with more technologies. In the end I would also like to involve statistical and correlation analysis and possibly generate predictions based on existing data sets.

## Installation
- Clone the repository
- Install Python with pip
- Install virtualenv and create a virtual environment (suggested)
- `pip install requirements.txt`

## Usage
- Create user and database using PostgreSQL
- `python manage.py migrate`
- `python manage.py runserver`

## Features
### Competitions
Competitions can be browsed and a season can be selected for more information.
<img src="https://i.imgur.com/by3Uig0.jpg">

### Seasons
The Seasons page offers a view of the standings as well as the ability to see detailed information about fixtures for the selected season.

<img src="https://i.imgur.com/erE8TLS.jpg">
<img src="https://i.imgur.com/9eyuEhx.jpg">

### Fixtures
Selecting a fixture will allow you to see detailed information about the fixture as well as available statistics* for players of the teams involved.
_Feature still in development_

<img src="https://i.imgur.com/POUghHU.jpg">

### Players
The Players page shows a general overview of various players with more detailed information to be aggregated in their respective pages*.
_Feature still in development_

<img src="https://i.imgur.com/e3iwJWI.jpg">
<img src="https://i.imgur.com/488gIzH.jpg">

### Statistics
_Feature still in development_

## Credits
- Country flags obtained from Wikipedia: https://www.wikipedia.org/
- Elevation information obtained from Google Earth Pro: https://www.google.com/earth/
- FIFA Country Codes obtained from FIFA: https://www.fifa.com/associations/
- Fixture information obtained form WhoScored: https://www.whoscored.com/
- La Liga player information, stadium information and team names from La Liga: https://www.laliga.com/en-US/
- Weather information obtained from WeatherUnderground: https://www.wunderground.com

Images seen in the above demo screenshots are used only for demonstrational purposes and are not distributed in the source code. Any competition logos, club emblems or crests, stadium pictures, and player portraits belong to their respective owners.

## License
To-do
