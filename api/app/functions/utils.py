import os
import re
import requests
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

env = os.getenv('APP_ENV', 'dev')
load_dotenv(f".env.{env}")

def get_doppler_secret(key, default=None):
    """Get secret from Doppler API"""
    token = os.environ.get('DOPPLER_TOKEN')
    if not token:
        return default
    
    try:
        response = requests.get(
            'https://api.doppler.com/v3/configs/config/secrets/download',
            headers={'Authorization': f'Bearer {token}'},
            params={'format': 'json'}
        )
        response.raise_for_status()
        secrets = response.json()
        return secrets.get(key, default)
    except Exception as e:
        logging.exception(f"Error getting Doppler secret {key}: {e}")
        return default
    

def parse_name(name: str) -> str:
    name = name.replace('_', ' ')
    clean_name = ''.join(e for e in name if e.isalnum() or e.isspace())
    return ' '.join(clean_name.split()).title()
