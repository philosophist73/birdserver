birdserver

*HOW TO SETUP*

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
        - Optional install sqlite3 CLI
            - update apt: sudo apt update
            - sudo apt install sqlite3

    DATABASE
    - from birdserver directory: 'python3
    
    Launch application
    from birdserver directory (app is a subdirectory): 'flask run'

