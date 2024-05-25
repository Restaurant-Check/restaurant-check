import os
import requests
from flask import Blueprint, render_template, request, jsonify, current_app
from time import sleep
from app.menu_to_json import process_menu_text
from scraper.scrape import scraper
from app.vector_db.vector_db import RestaurantVectorDB

bp = Blueprint('main', __name__)

@bp.route('/api/openai', methods=['POST'])
def call_openai_api():
    data = request.json
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    api_key = current_app.config['OPENAI_API_KEY']
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': 'text-davinci-003',
        'prompt': prompt,
        'max_tokens': 100
    }

    response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=payload)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to get response from OpenAI'}), response.status_code

    return jsonify(response.json())

@bp.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    location = request.args.get('location', '48.137517,11.575897')  # Format: "latitude,longitude"
    radius = request.args.get('radius', 10000)  # Radius in meters
    type = 'restaurant'  # Restrict to only restaurants

    if not location:
        return jsonify({'error': 'Location is required'}), 400

    api_key = current_app.config['GOOGLE_MAPS_API_KEY']

    nearby_search_endpoint = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    place_details_endpoint = 'https://maps.googleapis.com/maps/api/place/details/json'
    nearby_search_params = {
        'location': location,
        'radius': radius,
        'type': type,
        'key': api_key
    }

    nearby_results = []
    next_page_token = None
    while True:
        if next_page_token:
            nearby_search_params['pagetoken'] = next_page_token

        nearby_search_response = requests.get(nearby_search_endpoint, params=nearby_search_params)

        if nearby_search_response.status_code != 200:
            return jsonify({'error': 'Failed to get response from Google Maps API'}), nearby_search_response.status_code

        nearby_results.extend(nearby_search_response.json().get('results', []))

        next_page_token = nearby_search_response.json().get('next_page_token')
        if not next_page_token:
            break  # No more results available

        sleep(2) # Delay to wait for next page token to become valid

    print(f'Found {len(nearby_results)} restaurants nearby')

    detailed_results = []
    for result in nearby_results[:5]: # TODO: Remove Limit
        place_id = result.get('place_id')
        if place_id:
            place_details_params = {
                'place_id': place_id,
                'fields': 'name,website,rating,types,user_ratings_total,vicinity,geometry',
                'key': api_key
            }
            place_details_response = requests.get(place_details_endpoint, params=place_details_params)
            if place_details_response.status_code == 200:
                place_details = place_details_response.json().get('result', {})
                filtered_result = {
                    'geometry': place_details.get('geometry'),
                    'name': place_details.get('name'),
                    'price_level': result.get('price_level'),
                    'rating': place_details.get('rating'),
                    'types': place_details.get('types'),
                    'user_ratings_total': place_details.get('user_ratings_total'),
                    'vicinity': place_details.get('vicinity'),
                    'website': place_details.get('website')
                }
                detailed_results.append(filtered_result)

    # Map price levels to descriptive words
    # This is done so we can use word similarity for the searching later on
    price_level_mapping = {
        1: 'very cheap',
        2: 'cheap',
        3: 'normal',
        4: 'pricey/expensive'
    }

    # Replace price_level with descriptive words
    for result in detailed_results:
        price_level = result.get('price_level')
        if price_level in price_level_mapping:
            result['price_level'] = price_level_mapping[price_level]

    return jsonify(detailed_results)



@bp.route('/api/menus', methods=['GET'])
def get_restaurants_with_menu():
    # Get the detailed restaurant results
    detailed_results = get_restaurants().json

    # Add the menu to each restaurant entry
    for result in detailed_results:
        website = result.get('website')
        if website:
            menu = get_menu(website)
            result['menu'] = menu
        else:
            result['menu'] = "No website available"

    print(f'Found {len(detailed_results)} restaurants with menu')
    print(f'Items: {detailed_results}')
    return jsonify(detailed_results)


@bp.route('/api/menu', methods=['GET'])
def get_menu(website_url=''):

    if (website_url == ''):
        #Check the request parameters
        website_url = request.args.get('website_url')
        if not website_url:
            return jsonify({'error': 'No website URL provided'}), 400

    # Here the website url gets passed to the parsing function
    try:
        menu_text = scraper(website_url)
    except Exception as e:
        print(f"Error running scraper: {e}")
        return jsonify({'error': 'Failed to scrape menu data'}), 500



    #Check if menu_text is None
    if menu_text is None:
        return jsonify({'error': 'Failed to scrape menu data'}), 500

    # The result is then passed to the menu_to_json.py script
    # The result is a json with the structured menu
    menu_json = process_menu_text(menu_text)

    #Check if menu_json is None
    if menu_json is None:
        return jsonify({'error': 'Failed to process menu data'}), 500

    return menu_json




database = RestaurantVectorDB("./app/vector_db/data")
assert not database.get_restaurants_db().is_empty()
print("loaded database")

@bp.route('/', methods=['GET'])
def index():
    return "hello there!"

@bp.route('/query', methods=['GET'])
def query():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    return jsonify(database.query(query))