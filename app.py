#Toteuta sovellus tähän tiedostoon
# -*- coding: utf-8 -*-
from flask import Flask, request, Response, render_template, url_for
import os
app = Flask(__name__)

@app.route('/')
def peli():
    return Response("Game begins", content_type="text/plain; charset=UTF-8")

@app.route('/lauta', methods=['POST', 'GET'])
def lauta():
    koko = request.values.get("lauta", "")
    koko = int(koko)
    hello = "asd"
    return render_template('pohja.xhtml', hello=hello, koko=koko)