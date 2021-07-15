import traceback
from flask import render_template, request, redirect, url_for
from werkzeug.exceptions import NotFound

import app.helpers.templates as tp
import app.services.shortener as shortener
from app import app, front

@app.route('/', methods=["GET"])
def index():
    return redirect(front)

@app.route('/<url>', methods=["GET"])
def redirect_to_complete_url(url):
    complete_url = shortener.check_short_url(url)
    if complete_url:
        return redirect(complete_url, code=301)

    return redirect(f"{front}check?short={url}", code=301)

@app.errorhandler(NotFound)
def handle_not_found_exception(e):
    return redirect(f"{front}errors?type=page_not_found")

@app.errorhandler(Exception)
def handle_not_found_exception(e):
    traceback.print_exc()    
    return redirect(f"{front}errors")