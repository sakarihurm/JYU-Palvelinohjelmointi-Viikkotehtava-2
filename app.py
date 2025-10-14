#Toteuta sovellus tähän tiedostoon
# -*- coding: utf-8 -*-
from flask import Flask, request, Response, render_template, url_for, redirect
import os
app = Flask(__name__)

@app.route('/')
def peli():
    return Response("Game begins", content_type="text/plain; charset=UTF-8")

@app.route('/lauta/vt2.cgi', methods=['GET'])
@app.route('/lauta', methods=['POST', 'GET'])
def lauta():
    koko = request.args.get('lauta')
    pelaaja1 = request.args.get('p1')
    pelaaja2 = request.args.get('p2')

    # Jos yhtään ei ole annettu, ohjaa /lauta -reitille
    if not (koko or pelaaja1 or pelaaja2):
        koko = request.values.get("lauta", "")
        pelaaja1 = request.values.get("p1", "")
        pelaaja2 = request.values.get("p2", "")

    virhe = False
    try:
        koko = int(koko)
    except:
        koko = 8
        virhe = True

    if koko > 16 or koko < 8:
        koko = 8
        virhe = True

    if len(pelaaja1.strip()) == 0:
        virhe = True
    if len(pelaaja2.strip()) == 0:
        virhe = True
        
    return render_template('pohja.xhtml', koko=koko, virhe=virhe, pelaaja1=pelaaja1, pelaaja2=pelaaja2)