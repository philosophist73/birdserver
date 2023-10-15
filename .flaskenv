#valid configs: development, production
FLASK_ENV="development"

#TODO- why arent these needed anymore??
PYTHONPATH="/workspaces/birdserver"
FLASK_APP="app"

#HTTP SESSION
SESSION_PERMANENT="False"
SESSION_TYPE="filesystem"
#TODO: figure out why this doesnt work

#Flask
#NOTE: you need to create a .env file with SECRET_KEY. Key can be generated from python console with: python -c 'import secrets; print(secrets.token_hex())' 

#SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/postgres"
SQLALCHEMY_DATABASE_URI="sqlite:////home/philosophist/birdserver/sqlite/birdserver.db"

#FLASK_CACHING
CACHE_TYPE="SimpleCache"
CACHE_DEFAULT_TIMEOUT=300

#ebird API
#NOTE: you need to create a .env file with EBIRD_TOKEN. Token can be generated from https://ebird.org/api/keygen. 
#You will need to create an account. Alternatively contact me directly and I will provide
EBIRD_SERVER="api.ebird.org"
EBIRD_CONTEXT="v2"

#opencage API
#NOTE: you need to create a .env file with OPENCAGE_KEY. Key can be generated from https://opencagedata.com/dashboard#geocoding
#You will need to create an account. Alternatively contact me directly and I will provide
OPENCAGE_SERVER="api.opencagedata.com"
OPENCAGE_CONTEXT="geocode/v1"