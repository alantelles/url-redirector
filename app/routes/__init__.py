from flask import render_template, request, redirect, url_for

import app.helpers.templates as tp
import app.services.shortener as shortener
from app import app

@app.route('/', methods=["GET"])
def index():
    context = {'base_template': tp.get_layout_path('base')}
    return tp.get_page('index', context)

@app.route('/check', methods=["GET"])
def new_short_url():
    context = {
        'base_template': tp.get_layout_path('base')
    }
    url = request.args.get('short')
    if url:
        context['short'] = url
        valid_url =  shortener.check_short_url(url)
        if valid_url:
            context['destination'] = valid_url
            return tp.get_page('result', context)

        return tp.get_page('url_not_found', context)
    

@app.route('/new', methods=["POST"])
def save_short_url():
    
    short_url = shortener.create_short_url()
    return redirect(url_for('new_short_url', short=short_url))