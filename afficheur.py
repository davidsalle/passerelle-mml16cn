# Librairie(s) utilisée(s)
import time
import traceback
import serial


class Afficheur:
    """Classe pour gérer le journal lumineux MML16CN"""

    def __init__(self, port_serie="COM3"):
        """Initialisation de l'afficheur"""
        try:
            self.liaison = serial.Serial(
                port_serie,
                baudrate=9600,
                bytesize=8,
                parity="N",
                stopbits=1,            
                xonxoff=True,
                timeout=0.1           
            )
            print(self.liaison)
        except serial.SerialException as erreur:
            traceback.print_exc()
            self.liaison = None
        
    def __del__(self):
        """A la fermeture"""
        if self.liaison is not None:
            self.liaison.close()

    def preparer_trame(self, donnees) -> str:
        """Prépare une trame <IDxx>...yy<E>"""
        checksum = 0x00
        for caractere in donnees:
            checksum ^= ord(caractere)
        trame = f"<ID00>{donnees}{checksum:02X}<E>"
        return trame

    def envoyer(self, trame) -> str:
        """Envoi d'une trame sur le port serie"""
        print(f"Afficheur.envoyer() => {trame}")
        requete = trame.encode()
        self.liaison.write(requete)
        time.sleep(1)
        reponse = self.liaison.read()   # Pas de ACK si <ID00> utilisé
        return reponse.decode()
    
    def mettre_a_jour(self, parametres, texte) -> str:
        """Met à jour l'affichage sur l'afficheur"""
        trame = f"{parametres}{texte}"
        requete = f"<ID00><BE>05<E>{self.preparer_trame(trame)}<ID00><BF>06<E>"
        self.envoyer(requete)


if __name__ == "__main__":
    a = Afficheur("COM3")
    #message = [0x01, 0x03] + [ord(c) for c in "Bonjour"] + [0x0A]
    #message = "<ID00><BE>05<E><ID00><L1><PA><FE><MA><WC><FE>bonjour15<E><ID00><BF>06<E>"
    #message = "<ID01><BE>05<E><ID01><L1><PA><FE><MA><WC><FE>bonjour15<E><ID01><BF>06<E>"
    #message = "<ID00><L1><PA><FE><MA><WC><FE>bonkour14<E>"
    #message = "<ID00><BF>06<E>"
    #print(a.preparer_trame("<BE>"))
    #print(a.preparer_trame("<BF>"))
    #print(a.preparer_trame("<L1><PA><FE><MA><WC><FE>bonkour"))
    #message = "<ID00><BQ>11<E><ID00><L1><PA><FE><MA><WC><FE>bonjour15<E>"
    #print(a.envoyer(message))

    #a.envoyer(a.preparer_trame("Salut"))

    a.mettre_a_jour("<L1><PA><FE><MQ><WC><FA>", "<CA>Sortie <U26>")



