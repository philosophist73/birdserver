import argparse
import shutil
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
import csv
import re
import requests
from bs4 import BeautifulSoup

from app.models import Base
from app.models import Bird

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--images', action='store_true', help='Flag indicating whether to download images')
    parser.add_argument('--update', action='store_true', help='Flag indicating whether to update birdserver-preloaded.db, which is checked into git')
    args = parser.parse_args()
    
    # download fresh images. This will take 20+ minutes
    if args.images:
        load_images()
    
    # re-create the database. This instance is checked into git
    if args.update:
        engine = create_engine('sqlite:///birdserver-preloaded.db', echo=True)
        create_schema(engine)
        load_birds(engine)
        
    #copy this to the instance folder so the app can use it. This only needs to be done once.
    shutil.copy2('birdserver-preloaded.db', '../instance/birdserver.db')
    print("Updated the application database at ../instance/birdserver.db")
    
    
def create_schema(engine):
    # Drop all existing tables
    Base.metadata.drop_all(engine)
    # Create the tables
    Base.metadata.create_all(engine)

def load_birds(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    # Delete all rows from the 'bird' table
    session.query(Bird).delete()

    # Step 1: Read bird rows from CSV File
    import csv
    with open('birds.csv', 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        rows = list(csv_reader)
        
    count = 0

    # Step 2: Insert bird rows into the database
    for row in rows:
        bird = Bird(species_code=row['species_code'], common_name=row['american_english_name'], scientific_name=row['scientific_name'], image_url=row['image_url'], small_image_url=row['small_image_url'])
        session.add(bird)
        count += 1

    # Step 3: Commit the changes
    session.commit()

    print(f"Added {count} birds to the database.")


def load_images():
    # Input and output CSV files
    input_csv = 'PFW_spp_translation_table_May2023.csv'
    output_csv = 'birds.csv'

    # Define fieldnames including an additional column 'image_url' that we're adding
    fieldnames = ["species_code", "alt_full_spp_code", "n_locations", "scientific_name",
                  "american_english_name", "taxonomy_version", "taxonomic_sort_order", "image_url", "small_image_url"]

    # Read in the birds and add the image_url
    data = []
    with open(input_csv, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['image_url'], row['small_image_url'] = get_image_url(row['species_code'])
            data.append(row)


    # Write the modified data back to a birds.csv file. This will be used by a subsequent step, load_birds.py
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


# Function to crawl ebird.org website to parse an image url out of the HTML. This code worked as of 11/12/2023.
# If the HTML changes, this code will need to be updated.
def get_image_url(species_code):

    url = f'https://ebird.org/species/{species_code}'
    # defaults are Red-tailed Hawk (solitudinis), species code = rethaw3
    image_url = 'https://cdn.download.ams.birds.cornell.edu/api/v1/asset/223764621/1800'
    image_url_320w = 'https://cdn.download.ams.birds.cornell.edu/api/v1/asset/223764621/320'
    
    #retry 5 times case of connection error
    for i in range(5):
        try:
            with requests.get(url) as response:
                if response.status_code == 200:
                    html_content = response.content
                    soup = BeautifulSoup(html_content, 'html.parser')

                    # Find the div with class "MediaFeed-carousel"
                    div_with_images = soup.find('div', class_='Media-content')

                    # Find the img tag within the div
                    img_tag = div_with_images.find('img')
                    image_url = img_tag['src']

                    # Use regular expression to find the URL that ends with '320' (without the second 320w)
                    srcset = img_tag['srcset']
                    match = re.search(r'https://[^ ]+320(?!\w)', srcset)
                    if match: 
                        image_url_320w = match.group()
                    break
        except (Exception) as error:
            print(f"Failed to retrieve image URL for {species_code} due to {error}")

    print(f"{species_code}: {image_url} and {image_url_320w}")
    return image_url, image_url_320w


if __name__ == '__main__':
    main()