# cache.py
from flask_caching import Cache
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize cache - SimpleCache for dev, use Redis/Memcached for prod
cache = Cache(config={
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 3600 # Default 1 hour (overridden in set)
})

def init_cache(app):
  """Initializes the cache with the Flask app instance."""
  try:
      cache.init_app(app)
      logging.info("Flask-Caching initialized successfully.")
  except Exception as e:
      logging.error(f"Failed to initialize Flask-Caching: {e}")