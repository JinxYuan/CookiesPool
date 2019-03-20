from flask import Flask, g
from .config import *
from .db import RedisClient
import json

__all__ = ['app']
app = Flask(__name__)


def get_coon():
    for website in GENERATOR_MAP:
        print(website)
        if not hasattr(g, website):
            setattr(g, website + '_cookies',
                    eval('RedisClient("cookies","' + website + '")'))
            setattr(g, website + '_accounts',
                    eval('RedisClient("accounts","' + website + '")'))
        return g


@app.route('/')
def index():
    return '<h2>Welcome to Cookies Pool System</h2'


@app.route('/<website>/add/<username>/<password>')
def add(website, username, password):
    fg = get_coon()
    getattr(fg, website + '_accounts').set(username, password)
    return json.dumps({'status': '1'})


@app.route('/<website>/count')
def count(website):
    fg = get_coon()
    counts = getattr(fg, website + '_cookies').count()
    return json.dumps({'status': '1', 'count': counts})


@app.route('/<website>/random')
def random(website):
    fg = get_coon()
    cookies = getattr(fg, website + '_cookies').random()
    return cookies
