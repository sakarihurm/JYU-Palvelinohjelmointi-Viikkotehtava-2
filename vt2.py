#Toteuta sovellus tähän tiedostoon
# -*- coding: utf-8 -*-
from flask import Flask, request, Response
import os
app = Flask(__name__)

@app.route('/')
def peli():
    return Response("Game begins", content_type="text/plain; charset=UTF-8")

