# painting-discovery-webapp

Our app provides a centralized platform that simplifies access to and exploration of famous painting data—offering an intuitive and educational experience.

_Disclaimer: This project was developed as a practice exercise in building a user-friendly web app. While it aims to provide a comprehensive overview of famous paintings, some information and images may not be entirely accurate. For a detailed explanation of data constraints and considerations, refer to the appendix._

Our Render link: https://painting-discovery-webapp.onrender.com 

## Setup

Create and activate a virtual environment (first time only):
```sh
conda create -n painting-discovery-env-2024 python=3.10
```

Activate the environment (whenever you come back to this project):
```sh
conda activate painting-discovery-env-2024
```

Install packages:
```sh
pip install -r requirements.txt
```


Create a ".env" file and add the following content (also mentioned below under Usage):

```sh
# this is the ".env" file:
FLASK_APP=web_app
```

## Usage

Run the paintings script:

```sh
python app/paintings.py
```

Run the web app (then view in the browser at http://localhost:5000/):

```sh
# Mac OS:
FLASK_APP=web_app flask run

# Windows OS:
# ... if `export` doesn't work for you, try `set` instead
# ... or set FLASK_APP variable via ".env" file
export FLASK_APP=web_app
flask run
```

## Testing

Run tests:

```sh
pytest
```

## Appendix

#### Original Dataset
The dataset used for this project is sourced from [Kaggle Famous Paintings Dataset](https://www.kaggle.com/datasets/mexwell/famous-paintings). This dataset provides information about notable artworks, their artists, and the museums where they are displayed.

#### Data Preparation
To create a consolidated dataset, three individual files from the original dataset—`artist.csv`, `work.csv`, and `museum.csv`—were joined together to produce `paintings.csv`. 

The image URLs in the original dataset were not functional. To address this, web scraping was used to populate a new column with updated image URLs. (see `webscraping.py`)

#### Data Limitations
- **Image Accuracy**: Some images may not accurately represent the referenced artwork. They might depict unrelated or generic content due to basic web scraping implementation.

- **Image Display Issues**: Images may fail to load or display properly because of hotlinking restrictions or CORS (Cross-Origin Resource Sharing) issues.

- **Inaccurate Style Information**: The original dataset associates artists with a single style, which does not account for the fact that many artists worked across multiple styles throughout their careers. As a result, some style classifications are incorrect. 

This app was developed as a final project for OPAN-3244 and should not be relied upon for precise scholarly or professional use.