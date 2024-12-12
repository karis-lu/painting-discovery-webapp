# this is the app/paintings.py file

import pandas as pd
import requests
from IPython.display import display, Image
from bs4 import BeautifulSoup

def search_by_artist(input_artist):
    # Load the data
    paintings_df = pd.read_csv("data/paintings_with_links.csv")
    artist_df = pd.read_csv("data/artist.csv")

    matching_artist = artist_df[artist_df['full_name'].str.contains(input_artist, case=False, na=False)]
    
    if matching_artist.empty:
        raise ValueError(f"No records found for artist: {input_artist}")

    # Store artist id, name, nationality
    artist_id = matching_artist['artist_id'].iloc[0]
    artist_name = matching_artist['full_name'].iloc[0]
    print(f"Displaying results for {artist_name}")

    # Loop through paintings csv to find artist's works
    matching_works = paintings_df[paintings_df['artist_id'] == artist_id].copy()
    print(f"Found {len(matching_works)} records for artist: {input_artist}")

    # Create a dictionary of results
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
    # Load the data
    paintings_df = pd.read_csv("data/paintings_with_links.csv")

    # Loop through works csv to find works of that style
    matching_styles = paintings_df[paintings_df['style'] == input_style]

    if matching_styles.empty:
        raise ValueError(f"No records found for style: {input_style}")
    
    print(f"Found {len(matching_styles)} records for style: {input_style}")

    # Create a dictionary of results
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

if __name__ == "__main__":
    input_artist = input("Please enter artist name: ")
    search_by_artist(input_artist)

    input_style = input("Please enter art style: ")
    search_by_style(input_style)