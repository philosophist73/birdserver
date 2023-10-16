# Birdserver
### Video Demo:  <URL HERE>
### Description: 
A personal website to log bird sightings and favorite birds and add a watch list of birds you want to see. This application connects with Cornell Labs eBird API for detailed bird information and OpenCage to translate GPS location to an address

### Details:
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
    Primary features: 
        - Account management: the user can register for an account, login, and logout. The account saves all of their bird sighting information and persists from session to session. The user won't see any of the other app features until they log in
        - Bird ticker: at the bottom of every page is a streaming ticker of notable bird sightings in the user's area in the last 5 days. These sightings are pulled from eBird API
        - Bird Search: the user can search for birds by common name, scientific name, or species code (a cornell labs ebird code). The results are returned in a sortable and searchable tabled
        - Bird Sighting: from the bird search results, the user can select a bird to log a bird sighting. The bird sighting automatically captures location and timestamp. It also allows the user to enter notes. The location is translated to nearby address using the OpenCage API
        - History: the user will see a list of all bird sightings in a sortable and searchable table. The user is able to edit the notes or time of a bird sighting, but not the bird (future feature)
        - Favorites: the user is able to "heart" a bird to add it to the favorites list. The favorites list displays all the birds the user has previous "hearted"
        - Watch List: the user is able to "eye" a bird to add it to the watch list. The watch list displays all the birds the user has previous "eyed" 
    

### Github: 
https://github.com/philosophist73/birdserver.git

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



