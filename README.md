# Birdserver
### Video Demo: https://youtu.be/H2qSsxp02Aw
### Description: 
A personal website to log bird sightings and favorite birds and add a watch list of birds you want to see. This application connects with Cornell Labs eBird API for detailed bird information and OpenCage to translate GPS location to an address

### Github: 
https://github.com/philosophist73/birdserver.git

### Goals:
    This was my CS50x final project. In the final, week 9 assignment, CS Finance, I was introduced to Flask and basic web development. I decided i wanted to expand and go deep into learning how to do web development with Flask.
    Project Goals (completed):
        - Document requirements using basic use cases
        - Create a high level software architecture and database design before implementation
        - Organize my work with Jira
        - expand my knowledge of coding with Python by creating a moderate-sized web application
        - setup a full development environment outside of CS50
        - learn VS Code and dev container integration with Docker to make it easy to share my code with others
        - learn Github for my source code repository
        - expand knowledge of Flask by building a moderate sized application with multiple modules and directories
        - learn more about HTML, CSS, and javascript by adding some dynamic features to the site
        - Learn SQLAclhemy for database access and convenient database scheme creation with the ORM framework
        - Learn and integrate PostgreSQL and pgadmin for database
        - Learn how to integrate with APIs including ebird API for bird information and OpenCage to translate browser GPS coordinates to a nearby address. 
        - Learn how to use Postman to test APIs before coding in the application
        - learn how to leverage LLMs like github copilot, chatgpt, and bard for software development
    Future goals:
        - polish up the UI and fix bugs
        - ensure the application is fully thread safe for multiple users
        - all upload of photos and audio files for bird sightings
        - implement collaboration features so users can see each other favorites and watch lists
        - display photos for all birds in the database
        - create a web application so this can be used on mobile devices
        - package the application in a docker container that i can deploy
        - create an automated test framework
        - create a CI/CD pipeline
        - deploy the app to public cloud (likely GCP cloud run and CloudSQL)
        - integrate with AI APIs like Cornell Labs Merlin to identify birds by photo or audio
    What the app does:
        The application provides a simplistic web application for logging bird sightings, seeing a history of bird sightings, flagging birds as a favorite so you can see all the birds you like, and flagging birds to watch so you can see all the birds that you'd like to find. I started with the framework provided by CS50 finance, but quickly overhauled 95% of it, with only the Login feature and the apology feature remaining. 

### Features:
        - Account management: the user can register for an account, login, and logout. The account saves all of their bird sighting information and persists from session to session. The user won't see any of the other app features until they log in
        - Bird ticker: at the bottom of every page is a streaming ticker of notable bird sightings in the user's area in the last 5 days. These sightings are pulled from eBird API
        - Bird Search: the user can search for birds by common name, scientific name, or species code (a cornell labs ebird code). The results are returned in a sortable and searchable tabled
        - Bird Sighting: from the bird search results, the user can select a bird to log a bird sighting. The bird sighting automatically captures location and timestamp. It also allows the user to enter notes. The location is translated to nearby address using the OpenCage API
        - History: the user will see a list of all bird sightings in a sortable and searchable table. The user is able to edit the notes or time of a bird sighting, but not the bird (future feature)
        - Favorites: the user is able to "heart" a bird to add it to the favorites list. The favorites list displays all the birds the user has previous "hearted"
        - Watch List: the user is able to "eye" a bird to add it to the watch list. The watch list displays all the birds the user has previous "eyed" 
### HOW TO SETUP:
    **Clone Repo**
    - https://github.com/philosophist73/birdserver.git

    **Setup Local Workstation**
    Two options:   
    1. dev container (recommended)
        - this is preferred way to run this app. When you clone the repo into vscode, it will automatically ask you if you want to connect to the dev container.
        - requires VS Code (I am using 1.83.1) and Docker Desktop (I am using 4.24.1) installed
            - https://code.visualstudio.com/docs/devcontainers/containers
            - https://www.docker.com/products/docker-desktop/
        - dev container extension installed for VS Code. 
            - My version is 0.315.1
            - VSCode extension id is: ms-vscode-remote.remote-containers

    2. directly configuring python environment
        - Windows requires WSL in VS Code for windows
        - VSCode on WSL (With with WSL extension)
            - install WSL2: https://learn.microsoft.com/en-us/windows/wsl/install
            - verify it's ubuntu or debian bullseye (debian is what the dev container uses, but ubuntu should be fine)
            - connect VS Code to WSL (bottom left you can open up and select "connect to WSL")
            - clone repo: https://github.com/philosophist73/birdserver.git
        - set VSCode version of python
            - CTRL-SHIFT-P: python 3.10.12 (other versions might work, but this is what i am using)
            - my dev container environment used python 3.11.5
        - set up python venv (these are the linux commands)
            - make sure to do this in the birdserver directory
            - python3 -m venv .venv
            - source .venv/bin/activate
        - BUG: set this is .flaskenv with actual path: SQLALCHEMY_DATABASE_URI="sqlite:////home/philosophist/birdserver/sqlite/birdserver.db"
        - install python modules from birdserver with 'pip install -r requirements.txt'
        - Optional install sqlite3 CLI
            - update apt: sudo apt update
            - sudo apt install sqlite3
            
    **Set up Secrets**
    - .env
        - create an .env file in birdserver directory (~/birdserver/.env)
    - Flask SECRET_KEY
        - generate a Flask secret key with this command in the python command line: python -c 'import secrets; print(secrets.token_hex())'
        - add an entry to the .env file for SECRET_KEY and copy/paste the output of that as the value (SECRET_KEY="")
    - EBIRD API 
        - create a ebird API account to generate an API token. Token can be generated from https://ebird.org/api/keygen
        - add an EBIRD_TOKEN entry with that value in the .env file (EBIRD_TOKEN="")
        - Alternatively contact me directly and I will provide
    - OPENCAGE API 
        - create a opencage API account to generate an API key. Key can be generated from https://opencagedata.com/dashboard#geocoding
        - add an OPENCAGE_KEY entry with that value in the .env file (OPENCAGE_KEY="")
        - Alternatively contact me directly and I will provide
    
    **Setup Database if NOT running in dev container**
    - from birdserver directory: 'python db_setup.py'. This will set up your sqlite tables
    - from birdserver directory: 'python load_birds.py'. This will load all the birds from the migrations/birds.csv
    - **BUG**: if you are in a dev container, my original implementation of this uses PostgreSQL. in fact, the dev container has two containers one for flask and one for the database. to use this:
        - 'pip install psycopg2'
        - in .flaskenv change SQLALCHEMY_DATABASE_URI to use "postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/postgres"
        - if you want to see what's in the database, you can install pgAdmin at https://www.pgadmin.org/ and connect to this database on port 5432

### HOW TO RUN:
    - Launch application: from birdserver directory: 'flask run'
    - IMPORTANT: make sure you click "yes" when the browser ask for your location

### Code Details:
    - This is a python flask application with bootstrap CSS and javascript front end and a postgresql backend, plus API integration
    - /birdserver
        - /.devcontainer directory: setup for a vs code dev container integration with docker desktop dev enviroments. This makes it easy for me to share my code in a full working environment
        - /.vscode: configuration for my vscode environment. i didnt modify this
        - .flaskenv: configuration settings for the application
        - .env: secret config settings
        - .gitignore: files to ignore such as __pycache__ executables
        - config.py: reads in .flaskenv and makes ready for use by the application. Will be helpful in future when i build a test framework
        - db_setup.py: using SQLAlchemy ORM, creates the database schema
        - load_birds.py: using SQLAlchemy ORM, loads in birds.csv file to load basic bird information (common name, species code, and scientific name). Any other bird information i lookup at ebird API using the species code
        - README.md: this file!
        - requirements: all the python modules used by this app. I made sure to add to the .devcontainer/devconatiner.json to make sure these are installed when the dev container is created
        - run.py: no longer used. i settled on always running 'flask run' for my application
            - /app
                - __init__py: launches the app and configures Flask, Flask-Caching, Flask-Session, and SQLAlchemy db
                - helpers.py: adapting from cs50 finance app. reuses apology (although i changed the gif to gandalf) and login_required method used as a decorator. Contains methods that make calls to eBird and OpenCage APIs
                - routes.py: all of the "Views" for my flask application. Sets up one blueprint, but i dont use it in any useful way.
                - /models
                    - __init__.py sets up all my SQLAlchemy ORM Base classes
                    - account.py: model for Account table. Also encapsulates methods for interacting with an Account like login and logout
                    - bird.py: model for Bird table. Also encapsulates methods for interacting with a Bird like search
                    - birdsighting.py: model for Bird table. Also encapsulates methods for interacting with a Bird like create and update. Has FKs to account and history (this is a bug, just realized it needs to be added).
                    - favorite.py: model for Favorite table. Also encapsulates methods for interacting with a FAvorite like setting favorite, getting all favorites, and checking if a bird is a favorite. FKs to account and bird
                    - history.py: model for History table. Also encapsulates methors for interacting with History including creating a new entry. FK to account and bird
                    - watch.py: model for Watch table. Also encapsulates methods for interacting with a Watch like setting watch, getting all watches, and checking if a bird is a each. FKs to account and bird
                - /static
                    - /favicon: bird icon for navbar, browser tab, and bookmarks
                    - birdserver.js: all the javascript used for this app. needs to be refactored to consolidate the event handling in one place and fire only for appropriate pages
                    - bootstrap.min.css: bootswatch css override. not currently used
                    - styles.css: custom css. used for my search bar and the bird ticker (this was hard and took a lot of hunting and pecking on internet and querying LLMs. need to optimize the performance)
                - /templates: all my HTML pages
            - /migrations:
                - birds.csv: i used a really handy VSCode extension called Rainbow CSV to trim this down to just 3 fields for my database. the rest of the data i go to the ebird API when i need it
            - /sqlite: directory for birdserver.db, which will be created by db_setup.py
            - /tests: not yet used
                
