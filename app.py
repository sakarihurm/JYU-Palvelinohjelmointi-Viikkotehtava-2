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
    virhe = ""
    koko = request.values.get("lauta", "")
    pelaaja1 = request.values.get("p1", "")
    pelaaja2 = request.values.get("p2", "")

    try:
        koko = int(koko)
    except:
        koko = 8
        virhe = "Epäkelpo laudan koko"

    if koko > 16:
        koko = 16
        virhe = "Maksimi koko on 16"

    if koko < 8:
        koko = 8
        virhe = "Minimi koko on 8"
        
    return render_template('pohja.xhtml', koko=koko, virhe=virhe, pelaaja1=pelaaja1, pelaaja2=pelaaja2)