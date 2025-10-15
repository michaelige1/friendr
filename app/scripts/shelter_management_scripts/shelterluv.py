import requests
import os
import re
import csv
import json
import logging
from types import SimpleNamespace
from logging.handlers import RotatingFileHandler

shelterluv_base_url='https://api.shelterluv.com'
shelterluv_api_url = "{}/api/v1".format(shelterluv_base_url)

limit = 100
logger = None

csv_keys = [
    'type', 
    'name', 
    'age', 
    'breed', 
    'size', 
    'weight', 
    'dogs', 
    'cats', 
    'kids', 
    'energy', 
    'affection', 
    'new_people',
    'training', 
    'image_url'
]

def create_logger():
    global logger

    log_level = 'INFO'
    log_file = 'logs/shelterluv_data_pull.log'
    logger = logging.getLogger('SHELTERLUV_DATA_PULL_LOG')
    rotatingHandler = RotatingFileHandler(log_file, maxBytes=10000000, backupCount=10)
    logger.addHandler(rotatingHandler)
    logging.basicConfig(
        filename=log_file, 
        filemode='a', 
        level=log_level, 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def transform_data(data):
    # Placeholder for data transformation logic
    transformed_data = []
    counter = 0
    for animal in data:
        # Example transformation: convert names to uppercase
        # type,name,age,breed,size,weight,dogs,cats,kids,energy,affection,training,image_url
        if (animal.Type in ['Rabbit, Domestic', 'Ferret']): # Skip rabbits for now
            continue

        transformed_animal = {}
        transformed_animal['type'] = animal.Type
        transformed_animal['name'] = animal.Name
        transformed_animal['age'] = animal.Age
        transformed_animal['breed'] = animal.Breed
        transformed_animal['size'] = animal.Size
        transformed_animal['weight'] = animal.CurrentWeightPounds
        transformed_animal['image_url'] = animal.CoverPhoto

        get_attributes(animal, transformed_animal)
        counter += 1
        transformed_data.append(transformed_animal)

    return transformed_data

def write_csv(config, data):
    if not data:
        print("No data to write.")
        return

    output_file = "data/{}_shelterluv_animals.csv".format(config.get("SHELTER_NAME", "shelter"))
    # Get all unique keys for CSV header

    with open(output_file, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_keys)
        writer.writeheader()
        for row in data:
            filtered_row = {key: row.get(key, 3) for key in csv_keys}
            writer.writerow(filtered_row)
    print(f"Wrote {len(data)} records to {output_file}")

def pull_data(config):
    print("Pulling data from Shelterluv...")
    shelterluv_headers = {
        'X-Api-Key': config.get("API_KEY"),
    }
    
    counter = 0
    has_more = True
    total_animals = 0
    animals = []

    while has_more:
        print("Pulling offset: {}".format(counter * limit))
        request_url = "{}/animals?status_type=in%20custody&limit={}&offset={}".format(shelterluv_api_url, limit, counter * limit)
        logger.info("Pulling offset: {} with url: {}".format(counter * limit, request_url))
        r = requests.get(request_url, headers=shelterluv_headers)
        pet_posts = json.loads(r.text, object_hook=lambda d: SimpleNamespace(**d))
        # print(pet_posts)
        total_animals = pet_posts.total_count

        for animal in pet_posts.animals:
            animals.append(animal)
            
        counter += 1
        has_more = pet_posts.has_more
    return animals
        # print(pet_posts)
        # has_more = False

def get_attributes(animal, transformed_animal):
    attributes = animal.Attributes
    for attribute in attributes:
        if m := re.match(r"-Kids: ([0-9])\).*", attribute.AttributeName):
            transformed_animal['kids'] = m.group(1)
        elif m := re.match(r"-Dogs: ([0-9])\).*", attribute.AttributeName):
            transformed_animal['dogs'] = m.group(1)
        elif m := re.match(r"-Cats: ([0-9])\).*", attribute.AttributeName):
            transformed_animal['cats'] = m.group(1)
        elif m := re.match(r"-Energy Level: ([0-9])\).*", attribute.AttributeName):
            transformed_animal['energy'] = m.group(1)
        elif m := re.match(r"-Affection Level: ([0-9])\).*", attribute.AttributeName):
            transformed_animal['affection'] = m.group(1)
        elif m := re.match(r"-New people: ([0-9])\).*", attribute.AttributeName):
            transformed_animal['new_people'] = m.group(1)
        
    # print("Transformed animal: {}".format(transformed_animal))
    
    transformed_animal['training'] = 3  # Default to 3

def collect_data(config):
    create_logger()
    api_key = config.get("API_KEY")
    if not api_key:
        print("API_KEY is missing in the configuration.")
        return
    
    data = pull_data(config)
    print(f"Pulled {len(data)} records from Shelterluv.")
    transformed_data = transform_data(data)
    print(f"Transformed {len(transformed_data)} records.")
    write_csv(config, transformed_data)