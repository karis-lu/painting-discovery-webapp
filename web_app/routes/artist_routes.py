# this is the "web_app/routes/unemployment_routes.py" file...

from flask import Blueprint, request, render_template, redirect, flash

from app.paintings import get_direct_image_url, search_by_artist

artist_routes = Blueprint("artist_routes", __name__)

@artist_routes.route("/artist/form")
def artist_form():
    print("SEARCH BY ARTIST FORM...")
    return render_template("artist_form.html")

@artist_routes.route("/artist/results", methods=["POST"])
def artist_results():
    print("SEARCH BY ARTIST RESULTS...")
    print("FORM DATA:", dict(request.form))

    artist_name = request.form["artist_name"]
    print(artist_name)

    try:
        results = search_by_artist(artist_name)
        
        flash(f"Search for {artist_name} returned {len(results)} results.", "info")
        return render_template("artist_results.html", artist_name=artist_name, results=results)
    except Exception as err:
        print('OOPS', err)

        flash("Artist Not Found. Please try again!", "danger")
        return redirect("/artist/form")