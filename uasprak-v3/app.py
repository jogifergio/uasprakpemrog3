from flask import Flask, request, jsonify, render_template
import requests
import random  # Import the random module

app = Flask(__name__)

# Replace with your OMDb API key
OMDB_API_KEY = "b7b324b6"
OMDB_BASE_URL = "http://www.omdbapi.com/"

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

    return jsonify(response.json())

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
    # Example list of popular movie IDs
    all_movie_ids = [
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

    # Randomly select 5 movie IDs from the list
    recommended_movie_ids = random.sample(all_movie_ids, 5)

    recommendations = []
    for movie_id in recommended_movie_ids:
        params = {
            'apikey': OMDB_API_KEY,
            'i': movie_id,
        }
        response = requests.get(OMDB_BASE_URL, params=params)
        if response.status_code == 200:
            recommendations.append(response.json())

    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)