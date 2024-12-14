# Some version of this code was used to transform paintings.csv into paintings_with_links.csv
# This is the team's recommended code but did not follow it exactly. The team scraped first with Bing, 
# but Bing has less consistent results than Wikipedia. The team then scraped with Wikipedia, which was more consistent.
# The team incrementally ran the code in a Google Colab notebook in the background which took around 1-2 hours total to webscrape the entire paintings.csv

import requests
import pandas as pd
from bs4 import BeautifulSoup

# Reference: ChatGPT
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

# Reference: ChatGPT
def get_wikipedia_image_url(search_term):
    """
    Scrapes the first full-resolution image URL from a Wikimedia Commons search page.

    Args:
        search_term (str): The search term to use on Wikimedia Commons.

    Returns:
        str: The URL of the full-resolution image, or None if no image is found.
    """
    try:
        # Construct the search URL
        search_url = (
            "https://commons.wikimedia.org/w/index.php?"
            f"search={search_term.replace(' ', '+')}&title=Special:MediaSearch&go=Go&type=image"
        )
        #print("Search URL:", search_url)  # Debugging URL

        # Set headers and timeout
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content of the search page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the first search result link
        first_result = soup.find('a', {'class': 'sdms-image-result'})
        if first_result and 'href' in first_result.attrs:
            # Extract the link to the image's page
            result_url = first_result['href']
            print("First result URL:", result_url)  # Debugging URL

            # Fetch the image's page
            result_response = requests.get(result_url, headers=headers, timeout=10)
            result_response.raise_for_status()

            # Parse the image's page
            result_soup = BeautifulSoup(result_response.text, 'html.parser')

            # Find the main image on the image's page
            main_image = result_soup.find('a', {'class': 'internal'})

            if main_image and 'href' in main_image.attrs:
                # Extract the full-resolution image URL
                image_url = main_image['href']

                # Prepend https if needed
                if image_url.startswith("//"):
                    image_url = "https:" + image_url

                return image_url
            else:
                print("No image found on the image's page.")
                return None
        else:
            print("No search result found.")
            return None

    except requests.RequestException as e:
        print(f"An error occurred while fetching the URL: {e}")
        return None

def fetch_image_url(row):
    search_term = f"{row['name']} painting by {row['full_name']}"
    return get_direct_image_url(search_term)

def fetch_wikipedia_image_url(row):
    search_term = f"{row['full_name']} {row['name']}"
    return get_wikipedia_image_url(search_term)

# Example usage
search_term = "bennecourt claude monet"
image_url = get_wikipedia_image_url(search_term)
print("Full-resolution image URL:", image_url)

# Load the data
paintings_df = pd.read_csv("paintings.csv")
#paintings_df = pd.read_csv("data/paintings_with_links.csv")

paintings_df['image_url'] = ""

# Comment out lines depending on how many sessions to scrape
paintings_df.loc[0:2000, 'image_url'] = paintings_df.iloc[0:2000].apply(get_wikipedia_image_url, axis=1)
#paintings_df.to_csv("paintings_with_links.csv", index=False)

paintings_df.loc[2000:4000, 'image_url'] = paintings_df.iloc[2000:4000].apply(get_wikipedia_image_url, axis=1)
#paintings_df.to_csv("paintings_with_links.csv", index=False)

paintings_df.loc[4000:8000, 'image_url'] = paintings_df.iloc[4000:8000].apply(get_wikipedia_image_url, axis=1)
#paintings_df.to_csv("paintings_with_links.csv", index=False)

paintings_df.loc[8000:12000, 'image_url'] = paintings_df.iloc[8000:12000].apply(get_wikipedia_image_url, axis=1)
#paintings_df.to_csv("paintings_with_links.csv", index=False)

paintings_df.loc[12000:, 'image_url'] = paintings_df.iloc[12000:].apply(get_wikipedia_image_url, axis=1)
#paintings_df.to_csv("paintings_with_links.csv", index=False)

# Run with bing if wikipedia has no results
paintings_df.loc[paintings_df['image_url'].isna(), 'image_url'] = paintings_df.loc[paintings_df['image_url'].isna()].apply(fetch_image_url, axis=1)
paintings_df.to_csv("paintings_with_links.csv", index=False)
