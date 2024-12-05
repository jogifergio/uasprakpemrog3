from flask import Flask, request, jsonify, render_template
import requests
import random
import threading
import time
import json
from datetime import datetime

app = Flask(__name__)

# Replace with your OMDb API key
OMDB_API_KEY = "b7b324b6"
OMDB_BASE_URL = "http://www.omdbapi.com/"

# Path to store the movie recommendations
RECOMMENDATIONS_FILE = "recommendations.json"

# Example list of popular movie IDs
ALL_MOVIE_IDS = [
    "tt0111161",  # The Shawshank Redemption
    "tt0068646",  # The Godfather
    "tt0071562",  # The Godfather: Part II
    "tt0468569",  # The Dark Knight
    "tt0050083",  # 12 Angry Men
    "tt0108052",  # Schindler's List
    "tt0137523",  # Fight Club
    "tt0167260",  # The Lord of the Rings: The Return of the King
    "tt0133093",  # The Matrix
    "tt0372784",  # Batman Begins
]

# Function to fetch movie recommendations
def fetch_recommendations():
    recommended_movie_ids = random.sample(ALL_MOVIE_IDS, 4)
    recommendations = []

    for movie_id in recommended_movie_ids:
        params = {'apikey': OMDB_API_KEY, 'i': movie_id}
        response = requests.get(OMDB_BASE_URL, params=params)
        if response.status_code == 200:
            recommendations.append(response.json())

    # Save recommendations to a file
    with open(RECOMMENDATIONS_FILE, 'w') as file:
        json.dump(recommendations, file)
    
    print(f"Recommendations updated at {datetime.now()}")

# Function to run the scheduled task every 24 hours (86400 seconds)
def schedule_recommendations():
    while True:
        fetch_recommendations()
        time.sleep(5)  # Wait 24 hours before running again

# Start the background thread to fetch recommendations on schedule
threading.Thread(target=schedule_recommendations, daemon=True).start()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search_movies():
    query = request.args.get('query', '')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    params = {
        'apikey': OMDB_API_KEY,
        's': query,
        'type': 'movie',
    }
    response = requests.get(OMDB_BASE_URL, params=params)

    if response.status_code != 200 or 'Error' in response.json():
        return jsonify({'error': 'Failed to fetch data from OMDb API', 'details': response.json().get('Error')}), 500

    # Limit the results to 8
    data = response.json()
    if 'Search' in data:
        data['Search'] = data['Search'][:8]

    return jsonify(data)

@app.route('/movie/<movie_id>', methods=['GET'])
def get_movie_details(movie_id):
    params = {
        'apikey': OMDB_API_KEY,
        'i': movie_id,
        'plot': 'full',
    }
    response = requests.get(OMDB_BASE_URL, params=params)

    if response.status_code != 200 or 'Error' in response.json():
        return jsonify({'error': 'Failed to fetch data from OMDb API', 'details': response.json().get('Error')}), 500

    return jsonify(response.json())

@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    try:
        with open(RECOMMENDATIONS_FILE, 'r') as file:
            recommendations = json.load(file)
        return jsonify(recommendations)
    except FileNotFoundError:
        return jsonify({'error': 'Recommendations not available yet.'}), 500

if __name__ == '__main__':
    # Initially fetch recommendations when the app starts
    fetch_recommendations()
    app.run(debug=True)
