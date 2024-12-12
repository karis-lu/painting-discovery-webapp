# this is the "web_app/routes/unemployment_routes.py" file...
import pandas as pd
from flask import Blueprint, request, render_template, redirect, flash, Flask, jsonify, request

from app.paintings import search_by_style

style_routes = Blueprint("style_routes", __name__)

@style_routes.route("/style/")
def style_form():
    print("SEARCH BY STYLE FORM...")
    paintings_df = pd.read_csv("data/paintings.csv")

    # Get unique values of style column
    art_styles = paintings_df["style"].unique()
    art_styles = [style for style in art_styles if pd.notna(style)]

    return render_template("style_form.html", styles = art_styles)


@style_routes.route("/style/results", methods=["POST", "GET"])
def artist_results():
    print("SEARCH BY STYLE RESULTS...")

    if request.method == "POST":
        # for data sent via POST request, form inputs are in request.form:
        request_data = dict(request.form)
        print("FORM DATA:", request_data)
    else:
        # for data sent via GET request, url params are in request.args
        request_data = dict(request.args)
        print("URL PARAMS:", request_data)

    style = request_data.get("style")
    print(style)

    try:
        results = search_by_style(style)
        
        flash(f"Search for '{style}' returned {len(results)} results.", "info")
        return render_template("style_results.html", style=style, results=results)
    except Exception as err:
        print('OOPS', err)

        flash("Style Not Found. Please try again!", "danger")
        return redirect("/style/")

