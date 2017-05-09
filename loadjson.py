import json
import requests
import time


# Load Json and return it
def recup():
    with open('listeresident.json', 'r') as f:
        return json.load(f)


# # Session
def connection():

    # start = '2017-04-26'
    # end = '2017-04-27'

    IDI = 'ma'

    login_data_st = {'j_username': 'admin', 'j_password': 'Tarkett2014'}
    login_data_ma = {'j_username': 'MatAdmin2', 'j_password': 'T@rkett2014'}

    # Url pour les requetes
    urlbase = 'http://care.floorinmotion.com/api/'
    urllogin = urlbase + 'authentication'
    stream = urlbase + 'monitoring/I4.A.'

    # Ouverture de session et id
    s = requests.session()

    if IDI == 'ma':
        s.post(urllogin, login_data_ma)
    elif IDI == 'st':
        s.post(urllogin, login_data_st)

    # Initialisation du json interne qui gardera les données
    datatemporaire = recup()

    # Liste des event considere comme actif
    eventactif = ('BEDROOM', 'BATHROOM', 'FALL')
    eventinactif = ('ABSENCE', 'PRESENCE',)

    # # Boucle eternel qui se lance toutes les 60 secondes (a refaire)
    while True:

        # For each room
        for value in datatemporaire:
            n = value["n"]

            # get the live info
            r2 = s.get(stream + str(n))
            value["lastEvent"] = json.loads(r2.text)["room"]["lastEvent"]

            if value["lastEvent"] in eventactif:
                value["acti"] += "1"
            else:
                value["acti"] += "0"

            if "00000" in value["acti"] or "1" not in value["acti"]:
                value["tempsdemarche"] = 0
                value["acti"] = ""
            else:
                value["tempsdemarche"] = int(len(value["acti"]) / 5) * 5
            # update data
        with open('listeresident.json', 'w+') as f:
            json.dump(datatemporaire, f)

        time.sleep(60)

        # for key, value in data_old:
        #     data_new[key] = getdata(value)
        #     c = {key: value for (key, value) in (a.items() + b.items())}


# Lance la fonction
connection()
