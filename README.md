birdserver

How to run: from birdserver directory (app is a subdirectory)

*local workstation setup*
0. both dev container and WSL in VS Code
- generate secret key and add to .flaskenv 
    - python -c 'import secrets; print(secrets.token_hex())'
    -copy paste the output of that to SECRET_KEY
    
1. dev container (recommended)
- this is preferred way to run this app
- requires VS Code and Docker Desktop installed
- dev container extension installed for VS Code

2. WSL in VS Code

    - VSCode on WSL (With extention)
        - install WSL2
        - verify it's ubuntu or debian bullseye (which is what the dev container uses)
        - connect "remote" to WSL
        - clone repo
    - set VSCode version of pythong
        - CTRL-SHIFT-P: python 3.10.12
    - set up venv
        - at workspace directory (~/birdserver)
        - python3 -m venv .venv
        - ACTIVATE IT: source .venv/bin/activate
    - version of python is 3.11.5
    - update apt: sudo apt update
    - install sqlite3 CLI: sudo apt install sqlite3