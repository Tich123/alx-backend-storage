#!/usr/bin/env python3
"""
Web cache and tracker
"""
import requests
import redis
from functools import wraps

# Initialize Redis connection
store = redis.Redis()

def count_url_access(method):
    """Decorator counting how many times a URL is accessed"""
    @wraps(method)
    def wrapper(url):
        cached_key = "cached:" + url
        cached_data = store.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        count_key = "count:" + url
        try:
            html = method(url)
            store.incr(count_key)
            store.set(cached_key, html)
            store.expire(cached_key, 10)
            return html
        except Exception as e:
            return f"An error occurred: {e}"

    return wrapper

def fetch_url_content(url):
    """Fetches HTML content of a URL using requests"""
    response = requests.get(url)
    return response.text

@count_url_access
def get_page(url: str) -> str:
    """Returns HTML content of a URL with caching and tracking"""
    return fetch_url_content(url)

# Test the function
sample_url = 'http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.google.co.uk'
print(get_page(sample_url))
