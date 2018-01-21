import os, json

from flask import Flask, request, Response, jsonify, json
from flask import render_template, url_for, redirect, send_from_directory
from flask import make_response, abort, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

from project import app
from project.core import db
from project.models import *

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from mining.mining import read_stopword, tokenizing, textmining

# Web Profile
@app.route('/')
def index():
    return redirect(url_for('sepatumu'))

# SepatuMu
@app.route('/sepatumu/')
def sepatumu():
    return render_template('sepatumu/index.html', title="Home")

@app.route('/sepatumu/data/', methods=['GET', 'POST'])
def data():
    articles = None
    if request.form:
        try:
            article = Artikel(judul=request.form.get("judul"), url=request.form.get("url"), isi=request.form.get("isi"), isMining=False)
            db.session.add(article)
            db.session.commit()
        except Exception as e:
            print("Failed to data")
            print(e)
    articles = Artikel.query.all()
    return render_template('sepatumu/data.html', title="Data Artikel", articles=articles)

@app.route('/sepatumu/data/delete/', methods=['POST'])
def delete():
    try:
        id_article = request.form.get("id_article")
        article = Artikel.query.filter_by(id_article=id_article).first()
        db.session.delete(article)
        db.session.commit()
    except Exception as e:
        print("Couldn't delete")
        print(e)
    return redirect('/sepatumu/data/')

@app.route('/sepatumu/textmining/')
def mining():
    articles = None
    articles = Artikel.query.all()
    return render_template('sepatumu/mining.html', title="Mining", articles=articles)

@app.route('/sepatumu/process_mining/', methods=['POST'])
def process_mining():
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    keywords = None
    result = dict()

    if request.form:
        try:
            id = request.form.get("id")
            judul = request.form.get("judul")
            url = request.form.get("url")
            isi = request.form.get("isi")
        except Exception as e:
            print("Failed to process keyword")
            print(e)

    stop_word = read_stopword()
    data, data_stopword, data_judul = tokenizing(isi, stop_word, judul)
    result = textmining(data, data_stopword, data_judul, result, stemmer)
    print(result)

    for key, value in result.items():
        try:
            keywords = Keyword(judul=judul, url=url, isi=isi, keyword=key, jumlah=value)
            db.session.add(keywords)
            db.session.commit()
        except Exception as e:
            print("Failed")
            print(e)

    try:
        article = Artikel.query.filter_by(id_artikel=id).first()
        article.isMining = True
        db.session.commit()
    except Exception as e:
        print("Couldn't update isMining")
        print(e)

    return redirect('/sepatumu/textmining/')

@app.route('/sepatumu/result/', methods=['GET', 'POST'])
def result():
    result = []
    if request.form:
        text = request.form.get("search")
        text = text.lower()
        split_txt = text.split()

        words = ""
        for value in split_txt:
            words = words + '"' + value + '",'
        words = words.rstrip(', ')

        try:
            query = db.engine.execute("SELECT DISTINCT judul, url, isi FROM keyword WHERE keyword in (" + words + ") ORDER BY jumlah DESC")
            for i in query:
                result.append(i)
        except Exception as e:
            print("Couldn't update isMining")
            print(e)

        if result:
            results = result
        else:
            results = None

    return render_template('sepatumu/result.html', title=text, text=text, results=results)