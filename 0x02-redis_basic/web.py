#!/usr/bin/env python3

import requests
import time
import redis

# Initialize Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_page(url: str) -> str:
    cache_key = f'page:{url}'
    count_key = f'count:{url}'

    # Check if the page is cached
    cached_page = redis_client.get(cache_key)
    if cached_page:
        # Increment the access count
        redis_client.incr(count_key)
        return cached_page

    # Fetch the page content
    response = requests.get(url)
    page_content = response.text

    # Cache the page with expiration time of 10 seconds
    redis_client.setex(cache_key, 10, page_content)

    # Track the access count
    redis_client.incr(count_key)

    return page_content

# Test the function
sample_url = 'http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.google.co.uk'
print(get_page(sample_url))
