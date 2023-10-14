import csv
import datetime
import urllib
import uuid

from flask import current_app
from flask import redirect, render_template, session, jsonify
from functools import wraps
import requests
    
def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        #TODO: check if the user exists in database?
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

#ebird API lookup nearby sightings
#TODO: move to a separate API python file
def lookupNearbyAPI(latitude, longitude):
    print("lookupNearbyAPI")
    
    # Prepare API request
    serverName = current_app.config['EBIRD_SERVER']
    contextRoot = current_app.config['EBIRD_CONTEXT']
    token = current_app.config['EBIRD_TOKEN']

    # eBird v2 API: https://{{serverName}}/{{contextRoot}}/data/obs/geo/recent?lat={{lat}}&lng={{lng}}
    url = (
        f"https://{serverName}/{contextRoot}/data/obs/geo/recent/notable"
        f"?lat={urllib.parse.quote_plus(latitude)}"
        f"&lng={urllib.parse.quote_plus(longitude)}"
        f"&maxResults=4"
        f"&back=1"
    )
    
    # Query API
    try:
        response = requests.get(
            url, headers={"x-ebirdapitoken": token},
        )
        response.raise_for_status()
        return response.json()
        
    except requests.RequestException as e:
        print("RequestException: " + str(e))
        return None

#ebird API lookup bird details
#TODO: move to a separate API python file    
def lookupBirdDetails(species_code):
    print("lookupBirdDetails")
      
    # Prepare API request
    serverName = current_app.config['EBIRD_SERVER']
    contextRoot = current_app.config['EBIRD_CONTEXT']
    token = current_app.config['EBIRD_TOKEN']

    # eBird v2 API: https://{{serverName}}/{{contextRoot}}/ref/taxonomy/ebird?species={{species}}&fmt=json
    url = (
        f"https://{serverName}/{contextRoot}/ref/taxonomy/ebird"
        f"?species={urllib.parse.quote_plus(species_code)}"
        f"&fmt=json"
    )
    
    # Query API
    try:
        response = requests.get(
            url, headers={"x-ebirdapitoken": token},
        )
        response.raise_for_status()
        return response.json()
        
    except requests.RequestException as e:
        print("RequestException: " + str(e))
        return None

#openCage API lookup location
#TODO: move to a separate API python file    
def getOpenCageLocation(latitude, longitude):
    print("getOpenCageLocation")
      
    # Prepare API request
    serverName = current_app.config['OPENCAGE_SERVER']
    contextRoot = current_app.config['OPENCAGE_CONTEXT']
    key = current_app.config['OPENCAGE_KEY']
    
    # Make a request to OpenCage API
    url = f"https://{serverName}/{contextRoot}/json?q={latitude}+{longitude}&key={key}"
    response = requests.get(url)
    
    # Query API
    try:
        response = requests.get(url)
        response.raise_for_status()
        location_data = response.json()
        formatted_location = location_data['results'][0]['formatted']
        return formatted_location
        #return jsonify({'location': formatted_location}) 
    except requests.RequestException as e:
        print("RequestException: " + str(e))
        #return jsonify({'error': 'Unable to retrieve location data'}), 500
        return "n/a"
