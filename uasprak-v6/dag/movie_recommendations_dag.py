from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
import random
import json

OMDB_API_KEY = "b7b324b6"
OMDB_BASE_URL = "http://www.omdbapi.com/"
RECOMMENDATIONS_FILE = "/app/recommendations.json"

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

def fetch_recommendations():
    recommended_movie_ids = random.sample(ALL_MOVIE_IDS, 4)
    recommendations = []

    for movie_id in recommended_movie_ids:
        params = {'apikey': OMDB_API_KEY, 'i': movie_id}
        response = requests.get(OMDB_BASE_URL, params=params)
        if response.status_code == 200:
            recommendations.append(response.json())

    with open(RECOMMENDATIONS_FILE, 'w') as file:
        json.dump(recommendations, file)

    print(f"Recommendations updated at {datetime.now()}")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 12, 5),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'movie_recommendations',
    default_args=default_args,
    description='A DAG for updating movie recommendations',
    schedule_interval=timedelta(minutes=1),  # Runs daily
)

fetch_task = PythonOperator(
    task_id='fetch_recommendations',
    python_callable=fetch_recommendations,
    dag=dag,
)
