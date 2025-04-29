#viikkotehtävä 2:n testit
import json
from xml.dom.minidom import parseString

def test_vt2(client):
    response = client.get("/")
    assert 200 == response.status_code, 'Sovelluksen aloitussivu ei toimi'


def test_vt2_params(client):
    reqdata = {
        "lauta": "10",
        "p1": "testipelaaja1",
        "p2": "testipelaaja2"
    }
    response = client.get("/", query_string=reqdata)
    data = response.data.decode("UTF-8")

    assert 200 == response.status_code, 'Sovellus ei toimi get-metodin parametreilla'
    doc = parseString( data )
    td = doc.getElementsByTagName("td")
    assert td.length == 10*10, 'Ei tunnista annettua laudan kokoa' + data
    assert all(nimi in data for nimi in ["testipelaaja1", "testipelaaja2"]), 'Ei tunnista annettuja nimiä ' 

def test_invalid_x(client):
    reqdata = {
        "lauta": "foo",
        "p1": "testipelaaja1",
        "p2": "testipelaaja2"
    }
    response = client.get("/", query_string=reqdata)
    assert 200 == response.status_code, 'Sovellus kaatuu epävalidilla laudan koolla'


def test_puuttuvat_nimet(client):
    reqdata = {
        "lauta": "foo",
    }
    response = client.get("/", query_string=reqdata)
    assert 200 == response.status_code, 'Sovellus kaatuu, jos pelaajien nimet puuttuvat'


def test_puuttuvat_nimet(client):
    reqdata = {
        "lauta": "-5",
    }
    response = client.get("/", query_string=reqdata)
    assert 200 == response.status_code, 'Sovellus kaatuu, jos x on negatiivinen'


