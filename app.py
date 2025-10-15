#Toteuta sovellus tähän tiedostoon
# -*- coding: utf-8 -*-
from flask import Flask, request, Response, render_template, url_for, redirect
import os
app = Flask(__name__)

@app.route('/')
def peli():
    return Response("Game begins", content_type="text/plain; charset=UTF-8")

@app.route('/vt2/vt2.cgi', methods=['GET'])
@app.route('/vt2', methods=['POST', 'GET'])
def lauta():
    virhe = False
    try:
        koko = request.args.get('lauta')
        pelaaja1 = request.args.get('p1')
        pelaaja2 = request.args.get('p2')
    except Exception as e:
        pass

    if not (koko or pelaaja1 or pelaaja2):
        koko = request.values.get("lauta", 8)
        pelaaja1 = request.values.get("p1", "")
        pelaaja2 = request.values.get("p2", "")
    else:
        virhe = tarkistaNimet(pelaaja1, pelaaja2)

    try:
        koko = int(koko)
    except Exception as e:
        koko = 8
        virhe = True

    if koko > 16 or koko < 8:
        koko = 8
        virhe = True

    if request.method == "POST" and not virhe:
        virhe = tarkistaNimet(pelaaja1, pelaaja2)

    return Response(render_template('pohja.xhtml', koko=koko, virhe=virhe, pelaaja1=pelaaja1, pelaaja2=pelaaja2), content_type="application/xhtml+xml; charset=utf-8")

def tarkistaNimet(pelaaja1, pelaaja2):
    try: 
        if len(pelaaja1.strip()) == 0:
            return True
        if len(pelaaja2.strip()) == 0:
            return True
    except Exception as e:
        return True
    return False