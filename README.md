# Birdserver
### Video Demo:  <URL HERE>
### Description: 
A personal website to log bird sightings and favorite birds and add a watch list of birds you want to see. This application connects with Cornell Labs eBird API for detailed bird information and
### Github: 
https://github.com/philosophist73/birdserver.git

#### HOW TO SETUP

    SECRETS
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

    LOCAL WORKSTATION

    Two options:   
    1. dev container (recommended)
        - this is preferred way to run this app
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

    DATABASE
    - from birdserver directory: 'python db_setup.py'. This will set up your sqlite tables
    - from birdserver directory: 'python load_birds.py'. This will load all the birds from the migrations/birds.csv
    - NOTE: if you are in a dev container, my original implementation of this uses PostgreSQL. in fact, the dev container has two containers one for flask and one for the database. to use this:
        - 'pip install psycopg2'
        - in .flaskenv change SQLALCHEMY_DATABASE_URI to use "postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/postgres"
        - if you want to see what's in the database, you can install pgAdmin at https://www.pgadmin.org/ and connect to this database on port 5432

*HOW TO RUN*
    - Launch application: from birdserver directory: 'flask run'
    - IMPORTANT: make sure you click "yes" when the browser ask for your location



