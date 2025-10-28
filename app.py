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
    piilotetut_arvot = request.values.get("piilotetut", "")
    palautetut_arvot = request.values.get("palautetut", "")

    piilotetut = pura_lista(piilotetut_arvot)
    palautetut = pura_lista(palautetut_arvot)

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
        piilotetut.clear()
        palautetut.clear()
    
    return Response(render_template('pohja.xhtml', koko=koko, virhe=virhe, pelaaja1=pelaaja1, pelaaja2=pelaaja2, haku="", first=data["first"], balls=data["balls"], piilotetut=piilotetut, palautetut=palautetut), content_type="application/xhtml+xml; charset=utf-8")

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
    try:
        data = {
            "rivi": int(request.values.get("rivi")),
            "sarake": int(request.values.get("sarake")),
            "koko": int(request.form.get("koko")),
            "p1": request.form.get("p1", ""),
            "p2": request.form.get("p2", ""),
            "piilotetut": request.form.get("piilotetut", ""),
            "palautetut": request.form.get("palautetut", "")
        }
        # --- Käsitellään piilotetut ---
        piilotetut = pura_lista(data["piilotetut"])
        piilotetut.add((data["rivi"], data["sarake"]))

        # --- Käsitellään palautetut ---
        palautetut = pura_lista(data["palautetut"])

        piilotetut_str = muunna(piilotetut)
        palautetut_str = muunna(palautetut)

        tiedot = {
            "koko": data["koko"],
            "p1": data["p1"],
            "p2": data["p2"],
            "piilotetut": piilotetut_str,
            "palautetut": palautetut_str
        }

        haku = request.base_url.replace("/piilota", "/palauta") + "?" + urlencode(tiedot)

    except Exception as e:
        print("piilotus virhe:", e)
        haku = ""

    return Response(render_template(
        'pohja.xhtml',
        koko=data["koko"], virhe=False, pelaaja1=data["p1"], pelaaja2=data["p2"],
        haku=haku, first="white", balls="top-to-bottom",
        piilotetut=piilotetut, palautetut=palautetut
    ), content_type="application/xhtml+xml; charset=utf-8")


@app.route('/palauta', methods=['GET'])
def palauta():
    try:
        rivi = int(request.args.get("rivi", 0))
        sarake = int(request.args.get("sarake", 0))
        koko = int(request.args.get("koko"))
        p1 = request.args.get("p1", "")
        p2 = request.args.get("p2", "")
        piilotetut_arvot = request.args.get("piilotetut", "")
        palautetut_arvot = request.args.get("palautetut", "")

        piilotetut = pura_lista(piilotetut_arvot)
        palautetut = pura_lista(palautetut_arvot)

        piilotetut.remove((rivi, sarake))
        palautetut.add((rivi, sarake))

    except Exception as e:
        print("palautus virhe", e)

    return Response(render_template(
        'pohja.xhtml',
        koko=koko, virhe=False, pelaaja1=p1, pelaaja2=p2,
        haku="", first="white", balls="top-to-bottom",
        piilotetut=piilotetut, palautetut=palautetut
    ), content_type="application/xhtml+xml; charset=utf-8")


def pura_lista(arvot):
    if not arvot:
        return set()

    tulos = set()
    try:
        osat = arvot.split(';')

        for item in osat:
            if not item.strip():
                continue

            luvut = item.split(',')
            if len(luvut) != 2:
                continue

            rivi = int(luvut[0])
            sarake = int(luvut[1])

            tulos.add((rivi, sarake))

    except Exception as e:
        print("Virhe listan purussa:", e)
        return set()
    return tulos


def muunna(joukko):
    tulos = []

    for (rivi, sarake) in joukko:
        tulos.append(f"{rivi},{sarake}")

    return ';'.join(tulos)