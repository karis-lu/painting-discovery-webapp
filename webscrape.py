import pandas as pd
from IPython.display import display, Image
import requests
from bs4 import BeautifulSoup

def get_direct_image_url(search_query):
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


paintings_df = pd.read_csv("data/paintings.csv")

paintings_df.head()

# add a column of image urls to paintings_df
paintings_df['image_url'] = ""

for index, row in paintings_df.iterrows():
    # store variables
    work_title = row['name']
    artist_name = row['full_name']

    # get image url
    search_term = f"{work_title} painting by {artist_name}"
    image_url = get_direct_image_url(search_term)
    row['image_url'] = image_url

print(paintings_df.head())

# save the updated dataframe to a new csv file
paintings_df.to_csv("paintings_with_images.csv", index=False)
