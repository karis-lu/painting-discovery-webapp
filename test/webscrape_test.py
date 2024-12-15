# this is the test file for the webscraping.py file

import pytest
import pandas as pd
import requests
from bs4 import BeautifulSoup
from notebook.webscrape import get_direct_image_url, get_wikipedia_image_url

def test_get_direct_image_url():
    search_term = "Starry Night Vincent Van Gogh"
    image_url = get_direct_image_url(search_term)
    print(image_url)
    assert image_url.startswith("http")

def test_get_wikipedia_image_url():
    search_term = "Starry Night Vincent Van Gogh"
    image_url = get_wikipedia_image_url(search_term)
    print(image_url)
    assert image_url.startswith("http")