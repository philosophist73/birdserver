from sqlalchemy.sql import text

from datetime import datetime
from flask import Blueprint, jsonify, Flask, flash, redirect, render_template, request, session, url_for
from flask_caching import Cache
from flask import session

from app import cache
from app.helpers import apology, login_required, lookupNearbyAPI, lookupBirdDetails, getOpenCageLocation
from app.models.account import Account, AccountException
from app.models.bird import Bird, BirdException
from app.models.birdsighting import BirdSighting, BirdSightingException
from app.models.favorite import Favorite, FavoriteException
from app.models.watch import Watch, WatchException

#TODO: move this to __init__.py
birdserver = Blueprint('birdserver', __name__)

@birdserver.route('/test')
def test_page():
    return '<h1>Testing the birdserver app</h1>'

@birdserver.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@birdserver.route("/")
@login_required
def index():
    return render_template("index.html")

@birdserver.get("/register")
def register_get():
    return render_template("register.html")

@birdserver.post("/register")
def register_post():
    print("VIEW: register")
    if not request.form.get("username"):
        return apology("must provide username", 400)

    # Ensure password was submitted
    if not request.form.get("password"):
        return apology("must provide password", 400)

    # Ensure password and confirmation match
    if request.form.get("password") != request.form.get("confirmation"):
        return apology("passwords must match", 400)
    
    try:
        account = Account.create(request.form.get("username"), request.form.get("password"))
    except AccountException as e:
        return apology(str(e), 400)

    # Redirect user to home page
    return redirect("/")

@birdserver.get('/login')
def login_get():
    return render_template("login.html")

@birdserver.post('/login')
def login_post():
    print("VIEW: login")
    # Ensure username was submitted
    if not request.form.get("username"):
        return apology("must provide username", 403)

    # Ensure password was submitted
    elif not request.form.get("password"):
        return apology("must provide password", 403)
    
    try:
        Account.login(request.form.get("username"), request.form.get("password"))
    except AccountException as e:
        return apology(str(e), 400)
    
    return redirect("/")

@birdserver.route("/logout")
def logout():

    Account.logout()
    
    # Redirect user to login form
    return redirect("/")

@birdserver.get('/search')
@login_required
def search_get():
    print("VIEW: search")

    birdname = request.args.get('bird')
    attr = request.args.get('attr')
    birds = Bird.search(attr, birdname)
    
    return render_template("birdresults.html", birds=birds)

@birdserver.get("/birdticker")
@cache.cached()
def birdticker_get():
    print("VIEW: birdticker")
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    response = lookupNearbyAPI(latitude, longitude)
    
    birds = [r['comName'] + ' sighted at ' + r['locName'] for r in response]
  
    return jsonify(birds)

#TODO: why didnt the default cache key work?
def species_cache_key():
    species_code = request.args.get('species_code')
    return f'custom_cache_key_{species_code}'

#TODO: caching also caches the login
@birdserver.get("/bird")
@login_required
#@cache.cached(key_prefix=species_cache_key)
def birddetails_get():
    print("VIEW: bird")
    species_code = request.args.get('species_code')
    bird_id = request.args.get('bird_id')
    
    if (species_code):
        bird = Bird.get_bird_by_species_code(species_code)
        bird_details = lookupBirdDetails(species_code)
    elif (bird_id):
        bird = Bird.getBirdbyID(bird_id)
        bird_details = lookupBirdDetails(bird.species_code)
    
    favorite = Favorite.isFavorite(session["user_id"], bird.id)
    watch = Watch.isWatched(session["user_id"], bird.id)
    
    image_url = bird.image_url
    
    return render_template("bird.html", bird_details=bird_details, bird_id=bird.id, favorite=favorite, watch=watch, image_url=image_url)

@birdserver.post("/create_sighting")
@login_required
def create_sighting_post():
    print("VIEW: create_sighting")
    speciesCode = request.form.get("speciesCode")
    notes = request.form.get("notes")
    timestamp = datetime.fromisoformat(request.form.get("timestamp"))
    latitude = float(request.form.get("latitude"))
    longitude = float(request.form.get("longitude"))
    
    #use OpenCage to get location
    location = "n/a"
    if latitude and longitude:    
        location = getOpenCageLocation(latitude, longitude)    
    
    #lookup bird
    birds = Bird.search_by_species_code(speciesCode)
    
    #create bird_sighting
    bird_sighting = BirdSighting.create(session["user_id"], birds[0].id, timestamp, notes, location)
    
    return redirect(url_for('birdserver.history_get'))

@birdserver.get("/history")
@login_required
def history_get():
    print("VIEW: history")
    bird_sightings = BirdSighting.getHistory(session["user_id"])
    history_list = []
    
    #merge bird and birdsighting info. Feels hackish
    for bird_sighting in bird_sightings:
        bird = Bird.getBirdbyID(bird_sighting.bird_id)
        
        history_item = {
            'common_name': bird.common_name,
            'bird_id': bird.id,
            'timestamp': bird_sighting.timestamp,
            'notes': bird_sighting.notes,
            'location': bird_sighting.location,
            'sighting_id': bird_sighting.id            
        }
        history_list.append(history_item)        
        
    return render_template("history.html", history_list=history_list)

@birdserver.get("/favorites")
@login_required
def favorites_get():
    print("VIEW: favorites")
    
    birds = Favorite.getFavoriteBirds()
    return render_template("favorites.html", birds=birds)

@birdserver.get("/watch")
@login_required
def watch_get():
    print("VIEW: watch")
    
    birds = Watch.getWatchedBirds()
    return render_template("watch.html", birds=birds)

#TODO: cache
@birdserver.post("/translate_location")
def process_location():
    print("VIEW: translate location")
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    return getOpenCageLocation(latitude, longitude)

@birdserver.post("/add_favorite")
def add_favorite():
    print("VIEW: add favorite")
    data = request.get_json()
    bird_id = data.get('id')
    account_id = session["user_id"]
    
    Favorite.add(account_id, bird_id)

    #no response needed
    return '', 200

@birdserver.post("/remove_favorite")
def remove_favorite():
    print("VIEW: remove favorite")
    data = request.get_json()
    bird_id = data.get('id')
    account_id = session["user_id"]
    
    Favorite.remove(account_id, bird_id)

    #no response needed
    return '', 200

#TODO: is this used anywhere?
@birdserver.post("/is_favorite")
def is_favorite():
    print("VIEW: is favorite")
    data = request.get_json()
    print(data)
    bird_id = data.get('bird_id')
    account_id = session["user_id"]
    
    #True or false
    response = Favorite.isFavorite(account_id, bird_id)
    response_data = {'favorite': response}
    return jsonify(response_data)

    #no response needed
    return '', 200

@birdserver.post("/edit_sighting")
def edit_sighting():
    print("VIEW: edit sighting")
    data = request.get_json()
    timestamp = data.get('timestamp')
    notes = data.get('notes')
    location = data.get('location')
    id = data.get('id')
    updatedSighting = BirdSighting.update(id, timestamp, notes, location)
    #return jsonify(updatedSighting)

    #no response needed
    return '', 200

@birdserver.post("/add_watch")
def add_watch():
    print("VIEW: add watch")
    data = request.get_json()
    print(data)
    bird_id = data.get('id')
    account_id = session["user_id"]
    
    Watch.add(account_id, bird_id)

    #no response needed
    return '', 200

@birdserver.post("/remove_watch")
def remove_watch():
    print("VIEW: remove watch")
    data = request.get_json()
    print(data)
    bird_id = data.get('id')
    account_id = session["user_id"]
    
    Watch.remove(account_id, bird_id)

    #no response needed
    return '', 200
