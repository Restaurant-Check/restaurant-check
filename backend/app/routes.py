import os
import requests
from flask import Blueprint, render_template, request, jsonify, current_app

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
