# this is the app/paintings.py file

import pandas as pd
import requests
import unicodedata
import re
from IPython.display import display, Image
from bs4 import BeautifulSoup

# MAIN METHODS
def search_by_artist(input_artist):
    """
    Returns a list of dictionaries containing information about paintings by a given artist.
    """

    if not input_artist: # Empty string
        raise ValueError("Please enter an artist name.")
    
    # Load the data
    paintings_df = pd.read_csv("data/paintings_with_links.csv")
    artist_df = pd.read_csv("data/artist.csv")

    # Remove accents and replace hyphens or extra characters with a space
    artist_df['normalized_name'] = artist_df['full_name'].apply(remove_accents).str.lower()
    artist_df['normalized_name'] = artist_df['normalized_name'].str.replace(r"[-.\']", ' ', regex=True)

    normalized_input_artist = re.sub(r"[-.\']", ' ', remove_accents(input_artist)).lower()

    # Match using the contains_word function, reference ChatGPT
    search_terms = normalized_input_artist.split()
    matching_artist = artist_df[
        artist_df['normalized_name'].apply(
            lambda name: all(contains_word(term, name) for term in search_terms)
        )
    ]

    if matching_artist.empty:
        raise ValueError(f"No records found for artist: {input_artist}")

    # Store artist id, name, nationality
    artist_id = matching_artist['artist_id'].iloc[0]
    artist_name = matching_artist['full_name'].iloc[0]
    print(f"Displaying results for {artist_name}")

    # Loop through paintings csv to find artist's works
    matching_works = paintings_df[paintings_df['artist_id'] == artist_id].copy()
    print(f"Found {len(matching_works)} records for artist: {input_artist}")

    # Create a list of dictionary of results
    results = [
        {
            "work_title": row['title'],
            "artist_name": row['full_name'],
            "nationality": row['nationality'],
            "style": row['style'],
            "museum_name": row['museum_name'] if not pd.isna(row['museum_name']) else None,
            "city": row['city'],
            "country": row['country'],
            "image_url": row['image_url']
        }
        for _, row in matching_works.iterrows()
    ]

    return results

def search_by_style(input_style):
    """
    Returns a list of dictionaries containing information about paintings of a given style.
    """
        
    if not input_style: # Empty string
        raise ValueError("Please enter an art style.")
    
    # Load the data
    paintings_df = pd.read_csv("data/paintings_with_links.csv")

    # Loop through works csv to find works of that style
    matching_styles = paintings_df[paintings_df['style'] == input_style]

    if matching_styles.empty:
        raise ValueError(f"No records found for style: {input_style}")
    
    print(f"Found {len(matching_styles)} records for style: {input_style}")

    # Create a list of dictionary of results
    results = [
        {
            "work_title": row['title'],
            "artist_name": row['full_name'],
            "nationality": row['nationality'],
            "style": row['style'],
            "museum_name": row['museum_name'] if not pd.isna(row['museum_name']) else None,
            "city": row['city'],
            "country": row['country'],
            "image_url": row['image_url']
        }
        for _, row in matching_styles.iterrows()
    ]

    # To scatter artists, sort by last word of title
    results = sorted(results, key=lambda x: x.get('work_title').split()[-1] or '')

    return results

# HELPER METHODS
def remove_accents(input_str): #Reference ChatGPT
    """Remove accents from a given string."""

    # Normalize the string to decompose accents (NFD form)
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    # Filter out combining characters (accents)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def contains_word(word, text):
    # Example "Frank Ocean" contains "Frank" but not "rank"

    # Create a regex pattern with word boundaries
    pattern = rf'\b{re.escape(word)}\b'
    return re.search(pattern, text) is not None

# (Not used in web app only used when running script in terminal )
def display_first_ten(matching_works_df):
    for work in matching_works_df[:10]:
        print(f"Title: {work['work_title']}")
        print(f"Artist Name: {work['artist_name']}")

        if not pd.isna(work['style']):
            print(f"Style: {work['style']}")
        if not pd.isna(work['museum_name']):
            print(f"Museum Name: {work['museum_name']}")
        if not pd.isna(work['city']):
            print(f"City: {work['city']}")
        if not pd.isna(work['country']):
            print(f"Country: {work['country']}")
        if not pd.isna(work['image_url']):
            print(f"Image URL: {work['image_url']}")
        print("-----------------------------------")
        print("\n")


if __name__ == "__main__":
    while True:
        try:
            input_artist = input("Please enter artist name: ")
            matching_works = search_by_artist(input_artist)
     
            break
        except ValueError as e:
            # Handle the error and prompt the user to try again
            print(f"Error: {e}. Please enter a valid artist name.")

    # Print first 10 results
    print("\n")
    display_first_ten(matching_works)
    
    while True:
        try:
            input_style = input("Please enter art style: ").title()
            matching_works = search_by_style(input_style)
     
            break
        except ValueError as e:
            # Handle the error and prompt the user to try again
            print(f"Error: {e}. Please enter a valid style name.")

    # Print first 10 results
    print("\n")
    display_first_ten(matching_works)

    print("\nDone!")
    