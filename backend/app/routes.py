import os
import requests
from flask import Blueprint, render_template, request, jsonify, current_app
from time import sleep
from app.menu_to_json import process_menu_text
from app.generate_for_restaurant import generate_for_restaurant
from scraper.scrape import scraper
from app.vector_db.vector_db import RestaurantVectorDB
from langchain_community.document_loaders import PDFMinerPDFasHTMLLoader
from bs4 import BeautifulSoup


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

            #Check if result['menu'] is empty
            if result['menu'] == None:
                result['menu'] = generate_for_restaurant(result)['menu']
                print(f"Generated menu for {result['name']}")
                print(f"Menu: {result['menu']}")

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
        # TODO: send the links of pdfs also to langchain
        result = scraper(website_url)
    except Exception as e:
        print(f"Error running scraper: {e}")
        return jsonify({'error': 'Failed to scrape menu data'}), 500
    
    if result == None:        
        return jsonify({'error': 'Failed to scrape menu data'}), 500
    else:
        menu_text, links = result
        # TODO logic
        # Download the pdfs in the links into a "downloads" folder

        # Create the downloads folder if it doesn't exist
        downloads_folder = os.path.join(os.getcwd(), 'downloads')
        os.makedirs(downloads_folder, exist_ok=True)

        # Download each PDF link
        for link in links[:5]:  # Restrict to the first 5 links
            try:
                response = requests.get(link)
                response.raise_for_status()  # Check if the request was successful
                pdf_filename = os.path.join(downloads_folder, os.path.basename(link))
                with open(pdf_filename, 'wb') as pdf_file:
                    pdf_file.write(response.content)
                print(f"Downloaded {link} to {pdf_filename}")
            except Exception as e:
                print(f"Failed to download {link}: {e}")
        

        #Loop through the pdfs and load them into PDFMinerPDFasHTMLLoader
        pdf_files = [f for f in os.listdir(downloads_folder) if f.endswith('.pdf')]
        for pdf_file in pdf_files:
            pdf_path = os.path.join(downloads_folder, pdf_file)
            loader = PDFMinerPDFasHTMLLoader(pdf_path)
            data = loader.load()[0]  # entire PDF is loaded as a single Document

            # Extract HTML content
            html_content = data.page_content

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract text content that is not inside a span
            content = ''.join(soup.stripped_strings)

            if any(word in content.lower() for word in ['menu', 'speise', 'karte', 'menü']):
                print(f"Loaded PDF: {pdf_path}")
                menu_text += content
                print(f"Added text from PDF: {pdf_path}")
                print(f"Menu text: {menu_text}")
                break
        # Delete all pdfs in downloads
        
        for pdf_file in os.listdir(downloads_folder):
            if pdf_file.endswith('.pdf'):
                pdf_path = os.path.join(downloads_folder, pdf_file)
                os.remove(pdf_path)
                print(f"Deleted PDF: {pdf_path}")


    #Check if menu_text is None
    if menu_text is None:
        return jsonify({'error': 'Failed to scrape menu data'}), 500

    # The result is then passed to the menu_to_json.py script
    # The result is a json with the structured menu
    print(f"Menu text\n\n\n: {menu_text}\n\n\n")
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