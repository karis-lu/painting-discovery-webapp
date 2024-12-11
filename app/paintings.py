# this is the app/paintings.py file

import pandas as pd
import requests
from IPython.display import display, Image
from bs4 import BeautifulSoup

def get_direct_image_url(search_query):
    """
    Fetches image url from the first result of a search query on bing.

    Param search_query (str) : The search query to look for

    Returns (str) of the image url
    """
    # Encode the search query
    query = search_query.replace(" ", "+")
    url = f"https://www.bing.com/images/search?q={query}"

    # Add headers to mimic a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    # Perform the HTTP request
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch the page")
        return None

    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Look for the direct image link in the metadata
    # Bing often includes it in "m" attribute of <a> or in <img>
    first_image_link = soup.find("a", {"class": "iusc"})
    if first_image_link and "m" in first_image_link.attrs:
        # The "m" attribute contains a JSON-like string with the direct image URL
        import json
        metadata = json.loads(first_image_link["m"])
        if "murl" in metadata:
            return metadata["murl"]
    else:
        print("No direct image link found")
        return None


def search_by_artist(input_artist):
    # Load the data
    paintings_df = pd.read_csv("data/paintings.csv")
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

    # Loop through matching_works dataframe and append image url to a new column
    matching_works['image_url'] = matching_works.apply(
        lambda row: get_direct_image_url(f"{row['name']} painting by {artist_name}"), axis=1)

    # Create a dictionary of results
    results = [
        {
            "work_title": row['name'],
            "artist_name": row['full_name'],
            "nationality": row['nationality'],
            "style": row['style'],
            "museum_name": row['museum_name'],
            "city": row['city'],
            "country": row['country'],
            "image_url": row['image_url']
        }
        for _, row in matching_works.iterrows()
    ]

    return results

def search_by_style():
    # Load the data
    paintings_df = pd.read_csv("data/paintings.csv")
    artist_df = pd.read_csv("data/artist.csv")

    # Get unique values of style column
    art_styles = paintings_df["style"].unique()
    art_styles = [style for style in art_styles if pd.notna(style)]
    print(art_styles)
    
    # search by art style; this will be a drop-down menu in web app
    correct = False

    while not correct:
        style = input("Please enter art style: ").strip().title()

        if style in art_styles:
            print(f"Displaying results for {style}")
            correct = True
        else:
            print(f"No records found for style: {style}")
            print(f"Check spelling and try again.")

    # loop through works csv to find works of that style
    matching_styles = paintings_df[paintings_df['style'] == style]
    print(f"Found {len(matching_styles)} records for style: {style}")

    # loop through matching_works dataframe to display first 20 results
    counter = 0

    for index, row in matching_styles.iterrows():
        if counter >= 20:
            break

        counter += 1
        # store variables
        work_title = row['name']
        artist_name = row['full_name']
        artist_nationality = row['nationality']
        style = row['style'] if not pd.isna(row['style']) else None
        museum_name = row['museum_name'] if not pd.isna(row['museum_name']) else None
        city = row['city'] if not pd.isna(row['city']) else None
        country = row['country'] if not pd.isna(row['country']) else None

        # get image url
        search_term = f"{work_title} painting by {artist_name}"
        image_url = get_direct_image_url(search_term)
        #print("Direct image URL:", image_url)

        #display output
        print(f"Work Title: {work_title}")
        print(f"Artist: {artist_name} Nationality: {artist_nationality}")
        if style is not None:
            print(f"Style: {style}")
        if museum_name is not None:
            print(f"Location: {museum_name} ({city}, {country})")
        print(f"Image:")
        display(Image(url=image_url, height=200))
        print("-----------------------------------\n")

if __name__ == "__main__":
    search_by_artist()
    search_by_style()