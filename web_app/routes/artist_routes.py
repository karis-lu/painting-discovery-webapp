# this is the "web_app/routes/unemployment_routes.py" file...

from flask import Blueprint, request, render_template, redirect, flash, Flask, jsonify, request

from app.paintings import search_by_artist

artist_routes = Blueprint("artist_routes", __name__)

@artist_routes.route("/artist/")
def artist_form():
    print("SEARCH BY ARTIST FORM...")
    return render_template("artist_form.html")

@artist_routes.route("/artist/results", methods=["POST", "GET"])
def artist_results():
    print("SEARCH BY ARTIST RESULTS...")

    if request.method == "POST":
        # for data sent via POST request, form inputs are in request.form:
        request_data = dict(request.form)
        print("FORM DATA:", request_data)
    else:
        # for data sent via GET request, url params are in request.args
        request_data = dict(request.args)
        print("URL PARAMS:", request_data)

    artist_name = request_data.get("artist")
    print(artist_name)

    try:
        results = search_by_artist(artist_name)
        # get the artist name from the results dictionary
        artist = results[0]['artist_name']
        
        flash(f"Search for '{artist_name}' returned {len(results)} results. Showing results for {artist}.", "info")
        return render_template("artist_results.html", artist_name=artist, results=results)
    except Exception as err:
        print('OOPS', err)

        flash("Artist Not Found. Please try again!", "danger")
        return redirect("/artist/")
