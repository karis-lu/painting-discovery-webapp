# painting-discovery-webapp

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

