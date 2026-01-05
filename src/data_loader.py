import requests
from src import config

def fetch_posts_data():
    try:
        response = requests.get(config.API_URL, timeout=config.API_TIMEOUT)
        response.raise_for_status()
        return response.json()[:config.POST_LIMIT]
    except:
        return [
            {
                "id": i, 
                "title": f"Offline Backup Post {i}", 
                "body": "Automation continuing in offline mode."
            }
            for i in range(1, config.POST_LIMIT + 1)
        ]
