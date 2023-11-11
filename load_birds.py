from dotenv import load_dotenv
load_dotenv('.flaskenv')

import requests
from bs4 import BeautifulSoup
from config import Config
from sqlalchemy import create_engine

config = Config()
#TODO: hard coded to directory for now (./sqlite)
engine = create_engine("sqlite:///./sqlite/birdserver.db", echo=True)

# Now you can create tables based on your models
from app.models import Base

from app.models import Bird
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

# Delete all rows from the 'bird' table
#session.query(Bird).delete()

# Step 1: Read CSV File
import csv
with open('migrations/birds.csv', 'r', encoding='utf-8-sig') as file:
    csv_reader = csv.DictReader(file)
    rows = list(csv_reader)
    
count = 0

# Step 2: Get the image URL for each bird and write it to the database    
for row in rows:
    # URL of the webpage you want to scrape
    speciesCode = row['species_code']
    print(f"{speciesCode}:")
    url = f'https://ebird.org/species/{speciesCode}'
    

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Get the HTML content of the page
        html_content = response.content

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the div with class "MediaFeed-carousel"
        div_with_images = soup.find('div', class_='Media-content')

        # Find the img tag within the div
        img_tag = div_with_images.find('img')

        # Extract the value of the 'src' attribute (which contains the image URL)
        try:
            image_url = img_tag['src']
        except:
            print(f"Failed to retrieve image URL for {speciesCode}")

        print(f"{image_url}")
        
    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")
        
    bird = Bird(species_code=row['species_code'], common_name=row['common_name'], scientific_name=row['scientific_name'], image_url=image_url)
    session.add(bird)
    count += 1

# Step 3: Commit the changes
session.commit()

print(f"Added {count} images to the database.")