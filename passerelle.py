# Librairie(s) utilisée(s)
from flask import Flask, request
from afficheur import Afficheur
from threading import Lock


# Créations des objets
app = Flask(__name__)
aff = Afficheur("COM3")
verrou = Lock()


# Préparation des routes
@app.route("/api", methods=["POST"])
def envoyer_trame_brute():
    """Récupère une trame brute et la fait suivre vers l'afficheur via une liaison série"""
    #global aff
    with verrou:
        trame = request.form.get("trame")
        if trame is not None:
            reponse = aff.envoyer(trame)
            return "OK"
        else:
            return "NOK"


# Lancement
if __name__ == "__main__":
    #aff = Afficheur("COM3")
    app.run(host="0.0.0.0", debug=True, use_reloader=False)
