# coding: utf-8
from grab import Grab
from grab.spider import Spider, Task
import logging
import sys
import mymodel
import db
from flask import Flask, jsonify, request
import urllib

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/api/v1/artists', methods=['GET'])
def get_artists():
    artists = db.session.query(mymodel.Artist).filter(mymodel.Artist.lang == 'kz')
    if(request.args.get('q', '')):
        q = request.args.get('q', '')
        q = '%' + q + '%'
        artists = artists.filter(mymodel.Artist.fullname.ilike(q)).all()
    return jsonify(data=[i.serialize for i in artists])

@app.route('/api/v1/songs', methods=['GET'])
def get_songs():
    songs = db.session.query(mymodel.Song)
    if(request.args.get('artist_id', '')):
        id = request.args.get('artist_id', '')
        songs = songs.filter(mymodel.Song.artist_id == id)
    if(request.args.get('title', '')):
        title = request.args.get('title', '')
        title = '%' + title + '%'
        songs = songs.filter(mymodel.Song.title.ilike(title))
    return jsonify(data=[i.serialize for i in songs.all()])


if __name__ == '__main__':
    app.run(debug=True)
