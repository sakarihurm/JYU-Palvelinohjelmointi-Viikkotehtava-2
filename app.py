#Toteuta sovellus tähän tiedostoon
# -*- coding: utf-8 -*-
from flask import Flask, request, Response, render_template, url_for, redirect
import urllib.request, json
import os
app = Flask(__name__)


piilotetut = set()
url = ""

@app.route('/')
def peli():
    return Response("Game begins", content_type="text/plain; charset=UTF-8")

@app.route('/vt2/vt2.cgi', methods=['GET'])
@app.route('/vt2', methods=['POST', 'GET'])
def lauta():
    global url
    virhe = False

    with urllib.request.urlopen("https://europe-west1-ties4080.cloudfunctions.net/vt2_taso1") as response:
        data = json.load(response)
    print(data)

    try:
        koko = request.args.get('lauta')
        pelaaja1 = request.args.get('p1')
        pelaaja2 = request.args.get('p2')
    except Exception as e:
        pass

    if not (koko or pelaaja1 or pelaaja2):
        koko = request.values.get("lauta", data["min"])
        pelaaja1 = request.values.get("p1", "")
        pelaaja2 = request.values.get("p2", "")
    else:
        virhe = tarkistaNimet(pelaaja1, pelaaja2)

    try:
        koko = int(koko)
    except Exception as e:
        koko = data["min"]
        virhe = True

    if koko > data["max"] or koko < data["min"]:
        koko = data["min"]
        virhe = True

    if request.method == "POST" and not virhe:
        virhe = tarkistaNimet(pelaaja1, pelaaja2)

    haku = request.base_url + url

    return Response(render_template('pohja.xhtml', koko=koko, virhe=virhe, pelaaja1=pelaaja1, pelaaja2=pelaaja2, haku=haku, first=data["first"], balls="bottom-to-top", piilotetut=piilotetut), content_type="application/xhtml+xml; charset=utf-8")

def tarkistaNimet(pelaaja1, pelaaja2):
    try: 
        if len(pelaaja1.strip()) == 0:
            return True
        if len(pelaaja2.strip()) == 0:
            return True
    except Exception as e:
        return True
    return False

@app.route('/vt2/piilota', methods=['POST'])
def piilota():
    global url
    try:
        rivi = int(request.values.get("rivi"))
        sarake = int(request.values.get("sarake"))
        piilotetut.add((rivi, sarake))
        url = "/palauta?rivi="+ str(rivi) +"&sarake=" + str(sarake)
    except Exception as e:
        print("piilotus virhe", e)
    return redirect('/vt2')

@app.route('/vt2/palauta', methods=['GET'])
def palauta():
    global url
    try:
        rivi = request.args.get('rivi')
        sarake = request.args.get('sarake')
        piilotetut.remove((int(rivi), int(sarake)))
        url = "/palauta?rivi="+ str(rivi) +"&sarake=" + str(sarake)
    except Exception as e:
        print("palautus virhe", e)
    return redirect('/vt2')