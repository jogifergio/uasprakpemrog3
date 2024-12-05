from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Replace with your OMDb API key
OMDB_API_KEY = "b7b324b6"
OMDB_BASE_URL = "http://www.omdbapi.com/"

@app.route('/')
def home():
    # Render the main HTML page
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search_movies():
    query = request.args.get('query', '')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    # Call OMDb API to search for movies
    params = {
        'apikey': OMDB_API_KEY,
        's': query,  # 's' is used to search for titles
        'type': 'movie',  # Optional: limit search to movies
    }
    response = requests.get(OMDB_BASE_URL, params=params)

    if response.status_code != 200 or 'Error' in response.json():
        return jsonify({'error': 'Failed to fetch data from OMDb API', 'details': response.json().get('Error')}), 500

    return jsonify(response.json())

@app.route('/movie/<movie_id>', methods=['GET'])
def get_movie_details(movie_id):
    # Call OMDb API to get movie details
    params = {
        'apikey': OMDB_API_KEY,
        'i': movie_id,  # 'i' is used to search by IMDb ID
        'plot': 'full',  # Optional: fetch full plot details
    }
    response = requests.get(OMDB_BASE_URL, params=params)

    if response.status_code != 200 or 'Error' in response.json():
        return jsonify({'error': 'Failed to fetch data from OMDb API', 'details': response.json().get('Error')}), 500

    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)