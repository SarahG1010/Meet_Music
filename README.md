Meet Music App
-----

## Introduction

Meet Music App is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.


## Overview

### 1. Backend Dependencies
Our tech stack will include the following:
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **PostgreSQL** as our database of choice
 * **Python3** and **Flask** as our server language and server framework
 * **Flask-Migrate** for creating and running schema migrations
You can download and install the dependencies mentioned above using `pip` as:
```
pip install virtualenv
pip install SQLAlchemy
pip install postgres
pip install Flask
pip install Flask-Migrate
```

### 2. Frontend Dependencies
You must have the **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for our website's frontend. Bootstrap can only be installed by Node Package Manager (NPM). Therefore, if not already, download and install the [Node.js](https://nodejs.org/en/download/). Windows users must run the executable as an Administrator, and restart the computer after installation. After successfully installing the Node, verify the installation as shown below.
```
node -v
npm -v
```
Install [Bootstrap 3](https://getbootstrap.com/docs/3.3/getting-started/) for the website's frontend:
```
npm init -y
npm install bootstrap@3
```


## Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. Includes your SQLAlchemy models.
                    "python app.py" to run after installing dependencies
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── error.log
  ├── forms.py *** Your forms
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```


## Data Models
There are 3 data models in this app.
* Venue: 

| Columns             | Description                               | Property           |
|---------------------|-------------------------------------------|--------------------|
| id                  | id for venues                             | integer,primary key |
| name                | name of the venues                        | string, not null   |
| genres              | genres played in this venue               | string, not nul    |
| city                | city of the venues                        | string, not null   |
| state               | state of the venues                       | string, not null   |
| address             | address of the venues                     | string, not null   |
| phone               | phone of the venues                       | string             |
| image_link          | image link of the venues                  | string             |
| facebook_link       | facebook link of the venues               | string             |
| website             | website of the venues                     | string             |
| seeking_talent      | whether a venues is seeking talent or not | bool               |
| seeking_description | details of the seeking                    | string             |


* Artist:

| Columns             | Description                               | Property           |
|---------------------|-------------------------------------------|--------------------|
| id                  | id for artist                             | integer,primary key |
| name                | name of the artist                        | string, not null   |
| genres              | genres played by the artist               | string, not nul    |
| city                | city of the artist                        | string, not null   |
| state               | state of the artist                       | string, not null   |
| phone               | phone of the artist                       | string             |
| website             | website of the artist                     | string             |
| facebook_link       | facebook link of the artist               | string             |
| seeking_venue       | whether a artist is seeking venues or not | bool               |
| seeking_description | details of the seeking                    | string             |
| image_link          | image link of the artist                  | string             |

* Show:

| Columns    | Description                   | Property                      |
|------------|-------------------------------|-------------------------------|
| id         | id for shows                  | integer,primary key           |
| venue_id   | id of the venue for the show  | integer, foreign key,not null |
| artist_id  | id of the artist for the show | integer, foreign key,not null |
| start_time | the start time of the show    | datetime, not null            |


## Run the App and trouble shooting

1.**Initialize and activate a virtualenv using:**
```
python -m virtualenv env
source env/bin/activate
```

2.**Install the dependencies:**
```
pip install -r requirements.txt
```

3.**Run the development server:**
```
export FLASK_APP=myapp
export FLASK_ENV=development # enables debug mode
python3 app.py
```

4.**Verify on the Browser**<br>
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000) 

## Troubleshooting:
- If you encounter any dependency errors, please ensure that you are using Python 3.9 or lower.
- If you are still facing the dependency errors, follow the given commands:
  - `using pip install --upgrade flask-moment`
  - `Using pip install Werkzeug==2.0.0`
  - `Using pip uninstall Flask and then pip install flask==2.0.3`
- **Additional trouble shooting:**
  - if you cannot use flask in the virtual environment, install it gloablly by `pip install -U flask`
  - add `app.app_context().push()` (after define the flask app) to the app.py if you are using python 3.11
  - use conda environment instead (especially if you use jupyter notebook)
