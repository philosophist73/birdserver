import csv
import os
import requests
from bs4 import BeautifulSoup
import csv


def main():
    # Define the paths
    input_csv = './db-load/PFW_spp_translation_table_May2023.csv'
    output_csv = './db-load/birdseye.csv'

    # Define fieldnames including the additional column 'image_url'
    fieldnames = ["species_code", "alt_full_spp_code", "n_locations", "scientific_name",
                  "american_english_name", "taxonomy_version", "taxonomic_sort_order", "image_url"]

    # Read the CSV file and store its data
    data = []
    with open(input_csv, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)

    # Add image_url to the data
    for row in data:
        image_url = get_image_url(row['species_code'])
        row['image_url'] = image_url

    # Write the modified data back to the CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write the modified rows
        for row in data:
            writer.writerow(row)


# Function to perform the database lookup and return image_url
def get_image_url(species_code):

    print(f"{species_code}:")
    url = f'https://ebird.org/species/{species_code}'
    image_url = ""

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
            print(f"Failed to retrieve image URL for {species_code}")

        print(f"{image_url}")

    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")

    return image_url


if __name__ == '__main__':
    main()
