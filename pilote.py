from parametres import *
import requests    # A installer avec : python -m pip install requests




class PiloteAfficheur:
    """Classe pour piloter l'affichage du MML16CN"""
    
    def __init__(self, url_base: str):
        """Initialise le pilotage de l'afficheur"""
        # Paramètres de base de l'afficheur
        self.url_base = url_base
        self.ligne = "<L1>"
        self.page = "<PA>"
        self.effet_ouverture = "<FE>"
        self.mode_affichage = "<MA>"
        self.pause = "<WC>"
        self.effet_fermeture = "<FA>"
        self.couleur = "<CA>"
        self.message = "Hello world"


    def envoyer(self) -> int:
        """Met à jour l'afficheur en envoyant une trame complète"""
        # Préparation de la sous-trame pour configurer l'afffichage du MML16CN
        config_afficheur = ""
        config_afficheur += f"{self.ligne}"
        config_afficheur += f"{self.page}"
        config_afficheur += f"{self.effet_ouverture}"
        config_afficheur += f"{self.mode_affichage}"
        config_afficheur += f"{self.pause}"
        config_afficheur += f"{self.effet_fermeture}"
        config_afficheur += f"{self.couleur}"
        config_afficheur += f"{self.message}"

        # Préparation des 3 sous-trames
        trame = f"<ID00><BE>05<E>"
        trame += "<ID00>"
        trame += config_afficheur
        trame += f"{self.calculer_checksum(config_afficheur)}"
        trame += "<E>"
        trame += "<ID00><BF>06<E>"
        donnees = {"trame": trame}
        print(donnees)
        reponse = requests.post(self.url_base, donnees)
        return reponse.status_code


    def calculer_checksum(self, donnees: str) -> str:
        """Calcule la somme de contrôle (checksum) d'une trame de données"""
        checksum = 0x00                     # Initialisation de la somme de contrôle
        for caractere in donnees:           # Pour chaque caractère de la trame
            checksum ^= ord(caractere)      # XOR du code ASCII du caractère
        return  f"{checksum:02X}"           # Mise en forme sur 2 digits en majuscules
    

    def set_message(self, nouveau_message: str) -> bool:
        """Change le message à afficher"""
        if len(nouveau_message) <= 16:
            self.message = nouveau_message        
            return True
        else:
            return False
        

    def set_couleur(self, nouvelle_couleur: str) -> bool:
        """Change la couleur du message"""
        if nouvelle_couleur in COULEURS:
            self.couleur = f"<C{COULEURS[nouvelle_couleur]}>"
            return True 
        else:
            return False
        

    def set_pause(self, nouvelle_duree: float) -> bool:
        """Change la durée de pause du message"""
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if nouvelle_duree == 0.5:
            self.pause = "<WA>"
        elif nouvelle_duree <= 25.0:
            indice_temporisation = int(nouvelle_duree)
            self.pause = f"<W{alphabet[indice_temporisation]}>"


    def set_effet_ouverture(self, nouvel_effet: str) -> bool:
        """Change l'effet d'ouverture du message"""
        if nouvel_effet in EFFETS_OUVERTURE:
            self.effet_ouverture = f"<F{EFFETS_OUVERTURE[nouvel_effet]}>"
            return True 
        else:
            return False


    def set_effet_fermeture(self, nouvel_effet: str) -> bool:
        """Change l'effet d'ouverture du message"""
        if nouvel_effet in EFFETS_FERMETURE:
            self.effet_fermeture = f"<F{EFFETS_FERMETURE[nouvel_effet]}>"
            return True 
        else:
            return False


if __name__ == "__main__":
    p = PiloteAfficheur("http://192.168.1.29:5000/api")
    p.set_message("Bienvenue")
    p.set_couleur("DIM_GREEN")
    p.set_pause(3.0)
    p.set_effet_ouverture("SCROLL_LEFT")
    p.set_effet_fermeture("SCROLL_RIGHT")
    p.envoyer()