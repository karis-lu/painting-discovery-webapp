# this is the test file for the paintings.py module

import pytest
import pandas as pd
from numpy import nan
from app.paintings import search_by_artist, search_by_style

def test_csv():
    paintings_df = pd.read_csv("data/paintings_with_links.csv")
    assert isinstance(paintings_df, pd.DataFrame)
    assert len(paintings_df) > 10000
    assert paintings_df.columns.tolist() == ['work_id','title','artist_id','style',
                                            'museum_id','full_name','first_name',
                                            'middle_names','last_name','nationality',
                                            'birth','death','museum_name','city',
                                            'state','country','url','image_url']
    
    artist_df = pd.read_csv("data/artist.csv")
    assert isinstance(artist_df, pd.DataFrame)
    assert len(artist_df) > 100
    assert artist_df.columns.tolist() == ['artist_id','full_name','first_name',
                                          'middle_names','last_name','nationality', 'style',
                                          'birth','death']


def test_search_by_artist():
    columns = ['work_title','artist_name','nationality','style','museum_name','city','country','image_url']
    
    results = search_by_artist("John Singer Sargent") # Full name
    assert len(results) > 0 and list(results[0].keys()) == columns
       
    results = search_by_artist("Van Gogh") # Last name
    assert len(results) > 0 and list(results[0].keys()) == columns
    
    results = search_by_artist("monet") # Lowercase
    assert len(results) > 0 and list(results[0].keys()) == columns
    
    results = search_by_artist("Paul Cézanne") # Accented name
    assert len(results) > 0 and list(results[0].keys()) == columns
    results = search_by_artist("paul cezanne")
    assert len(results) > 0 and list(results[0].keys()) == columns
    
    results = search_by_artist("François Drouais") # Hyphenated name
    assert len(results) > 0 and list(results[0].keys()) == columns
    results = search_by_artist("francois-hubert drouais")
    assert len(results) > 0 and list(results[0].keys()) == columns
    
    # Incomplete/Misspelled name
    with pytest.raises(ValueError, match="No records found for artist: Van Gog"):
        search_by_artist("Van Gog")

    # Artist that does not exist
    with pytest.raises(ValueError, match="No records found for artist: random guy"):
        search_by_artist("random guy")

def test_style_form():
    paintings_df = pd.read_csv("data/paintings.csv")

    art_styles = paintings_df["style"].unique()
    art_styles = [style for style in art_styles if pd.notna(style)]
    assert len(art_styles) == 23

def test_search_by_style():
    # Drop down menu in web form eliminates the possibility of misspelling a style or inputting one that does not exist
    results = search_by_style("Impressionism")
    assert len(results) > 0
    assert isinstance(results, list)
    assert isinstance(results[0], dict)
    assert list(results[0].keys()) == ['work_title','artist_name','nationality','style','museum_name','city','country','image_url']

    # Test with a style that does not exist
    with pytest.raises(ValueError, match="No records found for style: random style"):
        search_by_style("random style")