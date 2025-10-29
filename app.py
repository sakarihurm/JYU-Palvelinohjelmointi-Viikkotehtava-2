#Toteuta sovellus tähän tiedostoon
# -*- coding: utf-8 -*-
from flask import Flask, request, Response, render_template, url_for, redirect
import urllib.request, json
from urllib.parse import urlencode

import os
app = Flask(__name__)


# @app.route('/')
# def peli():
#     return Response("Game begins", content_type="text/plain; charset=UTF-8")

@app.route('/vt2.cgi', methods=['GET'])
@app.route('/', methods=['POST', 'GET'])
def lauta():

    virhe = False

    try:
        with urllib.request.urlopen("https://europe-west1-ties4080.cloudfunctions.net/vt2_taso1") as response:
            data = json.load(response)
    except Exception as e:
        print("Virhe haettaessa dataa:", e)
        data = {"min": 8, "max": 16, "first": "white", "balls": "top-to-bottom"}

    koko = request.values.get("koko", data["min"])
    pelaaja1 = request.values.get("p1", "")
    pelaaja2 = request.values.get("p2", "")


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


    return Response(render_template('pohja.xhtml', koko=koko, virhe=virhe, pelaaja1=pelaaja1, pelaaja2=pelaaja2, haku="", first=data["first"], balls=data["balls"], piilotetut=[], palautetut=[]), content_type="application/xhtml+xml; charset=utf-8")

def tarkistaNimet(pelaaja1, pelaaja2):
    try: 
        if len(pelaaja1.strip()) == 0:
            return True
        if len(pelaaja2.strip()) == 0:
            return True
    except Exception as e:
        return True
    return False


@app.route('/piilota', methods=['POST'])
def piilota():
    data = {}
    try:
        with urllib.request.urlopen("https://europe-west1-ties4080.cloudfunctions.net/vt2_taso1") as response:
            data = json.load(response)
    except Exception as e:
        print("Virhe haettaessa dataa:", e)
        data = {"min": 8, "max": 16, "first": "white", "balls": "top-to-bottom"}
    
    rivi = int(request.values.get("rivi"))
    sarake = int(request.values.get("sarake"))
    koko = int(request.form.get("koko", data["min"]))
    p1 = request.form.get("_p1", "")
    p2 = request.form.get("_p2", "")
    piilotetut = request.form.get("piilotetut", [])
    palautetut = request.form.get("palautetut", [])

    try:
        piilotetut = json.loads(piilotetut)
    except Exception as e:
        piilotetut = []
    try:
        palautetut = json.loads(palautetut)
    except Exception as e:
        palautetut = []
        
    piilotetut.append([rivi, sarake])
    piilotetut_str = json.dumps(piilotetut)
    palautetut_str = json.dumps(palautetut)

    tiedot = {
        "koko": koko,
        "p1": p1,
        "p2": p2,
        "rivi": str(rivi),
        "sarake": str(sarake),
        "piilotetut": piilotetut_str,
        "palautetut": palautetut_str
    }

    haku = request.base_url.replace("/piilota", "/palauta") + "?" + urlencode(tiedot)

    # except Exception as e:
    #     print("piilotus virhe:", e)
    #     haku = ""
    
    return Response(render_template(
        'pohja.xhtml',
        koko=koko, virhe=False, pelaaja1=p1, pelaaja2=p2,
        haku=haku, first=data["first"], balls=data["balls"],
        piilotetut=piilotetut, palautetut=palautetut, piilotetut_str=piilotetut_str, palautetut_str=palautetut_str
    ), content_type="application/xhtml+xml; charset=utf-8")


@app.route('/palauta', methods=['GET'])
def palauta():
    try:
        with urllib.request.urlopen("https://europe-west1-ties4080.cloudfunctions.net/vt2_taso1") as response:
            data = json.load(response)
    except Exception as e:
        print("Virhe haettaessa dataa:", e)
        data = {"min": 8, "max": 16, "first": "white", "balls": "top-to-bottom"}
    
    rivi = int(request.args.get("rivi"))
    sarake = int(request.args.get("sarake"))
    koko = int(request.args.get("koko"))
    p1 = request.args.get("p1", "")
    p2 = request.args.get("p2", "")
    piilotetut = request.args.get("piilotetut", [])
    palautetut = request.args.get("palautetut", [])

    try:
        piilotetut = json.loads(piilotetut)
    except Exception as e:
        piilotetut = []
    try:
        palautetut = json.loads(palautetut)
    except Exception as e:
        palautetut = []

    piilotetut.remove([rivi, sarake])
    palautetut.append([rivi, sarake])

    piilotetut_str = json.dumps(piilotetut)
    palautetut_str = json.dumps(palautetut)

    return Response(render_template(
        'pohja.xhtml',
        koko=koko, virhe=False, pelaaja1=p1, pelaaja2=p2,
        haku="", first=data["first"], balls=data["balls"],
        piilotetut=piilotetut, palautetut=palautetut, piilotetut_str=piilotetut_str, palautetut_str=palautetut_str
    ), content_type="application/xhtml+xml; charset=utf-8")
