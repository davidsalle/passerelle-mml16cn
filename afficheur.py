# Librairie(s) utilisée(s)
import time
import traceback
import serial


class Afficheur:
    """Classe pour gérer le journal lumineux MML16CN"""

    def __init__(self, port_serie="COM3", numero=0):
        """Initialisation de l'afficheur"""
        self.numero = numero
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

    def calculer_checksum(self, donnees: str) -> str:
        """Calcule la somme de contrôle (checksum) d'une trame de données"""
        checksum = 0x00                     # Initialisation de la somme de contrôle
        for caractere in donnees:           # Pour chaque caractère de la trame
            checksum ^= ord(caractere)      # XOR du code ASCII du caractère
        return  f"{checksum:02X}"           # Mise en forme sur 2 digits en majuscules
    
    def preparer_trame(self, donnees) -> str:
        """Prépare une trame <IDxx>...yy<E>"""
        checksum = self.calculer_checksum(donnees)       
        trame = f"<ID{self.numero:02d}>{donnees}{checksum}<E>"
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
        requete = f"{self.preparer_trame("<BE>")}{self.preparer_trame(trame)}{self.preparer_trame("<BF>")}"
        self.envoyer(requete)


if __name__ == "__main__":
    a = Afficheur("COM3", 0)
    #message = [0x01, 0x03] + [ord(c) for c in "Bonjour"] + [0x0A]
    #message = "<ID00><BE>05<E><ID00><L1><PA><FE><MA><WC><FE>bonjour15<E><ID00><BF>06<E>"
    #message = "<ID01><BE>05<E><ID01><L1><PA><FE><MA><WC><FE>bonjour15<E><ID01><BF>06<E>"
    #message = "<ID00><L1><PA><FE><MA><WC><FE>bonkour14<E>"
    #message = "<ID00><BF>06<E>"
    #print(a.preparer_trame("<BE>"))
    #print(a.preparer_trame("<BF>"))
    #print(a.preparer_trame("<L1><PA><FE><MA><WC><FE>bonkour"))
    #message = "<ID03><BE>05<E><ID03><L1><PA><FE><MQ><WC><FA><CA>Hello world60<E><ID03><BF>06<E>"
    #print(a.envoyer(message))

    #a.envoyer(a.preparer_trame("Salut"))

    #a.mettre_a_jour("<L1><PA><FE><MQ><WC><FA>", "<CA>Hello world")
    a.mettre_a_jour("<L1><PA><FL><MA><WB><FF>", "<CD>Johnny")



