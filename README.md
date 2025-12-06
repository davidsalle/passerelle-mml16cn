# passerelle-mml16cn

## 1 - Introduction

Passerelle HTTP/RS232 pour piloter à distance le journal lumineux MML16CN


## 2 - Mise en oeuvre

### 2.1 - Câblage
- Connecter le câble RJ11/USB au PC
- Alimenter l'afficheur

### 2.2 - Pilotes
- Il faut télécharger les pilotes **CP210x Universal Windows Driver** de l'adaptateur USB/Serial depuis [https://www.silabs.com/software-and-tools/usb-to-uart-bridge-vcp-drivers?tab=downloads]. Sinon ils sont dans le dossier `pilotes` du dépôt.
- Faire une mise à jour manuelle des pilotes depuis le gestionnaire de périphériques par exemple.
- Il doit apparaître en `COM3`

### 2.3 - Protocole
Pas vraiment de docs officielles

Cette trame affiche "bonjour" en rouge sur l'afficheur `<ID00><BE>05<E><ID00><L1><PA><FE><MA><WC><FE>bonjour15<E><ID00><BF>06<E>`

Format trame : `<ID00>...XX<E>`
- `<ID00>` indique à la fois le début de trame et aussi le numéro de l'afficheur si plusieurs appareils
- `...` représente les données à envoyer
- ``XX` est le checksum, à savoir un XOR de tous les octets de `...` au format hexadécimal sur 2 digits
- `<E>` indique la fin d'un trame


- `<D*>` : reset de l'afficheur si besoin (à envoyer avant les autres trames)
- `<ID00><BE>05<E>`
    - `<BE>05` : début d'une mise à jour de l'affichage
- `<ID00><L1><PA><FE><MA><WC><FE><CA>bonjour15<E>`
    - `<L1>` : ligne d'affichage numéro 1
    - `<PA>` : page d'affichage A
    - `<FE>` : effet spéciaux à l'ouverture (E=scroll left)
    - `<MA>` : Mode d'affichage (A=normal, B=clignotement)
    - `<WC>` : temps de pause (Wait) (A=rapide, B=moyen1, C=moyen2, D=lent)
    - `<FE>` : effet spéciaux à la fermeture (F=scroll left)
    - `<CA>` : Couleur (A=rouge)
    - `Sortie <U26>` : message texte + caractère spécial européen
    - `25` : checksum en hexadécimal et majuscule de tous les caractères XORés entres <ID00> et <E>
- `<ID00><BF>06<E>`
     -`<BF>06` : fin de la mise à jour de l'affichage


## 3 - Webographie
- https://github.com/shackenberg/text2led.py
- https://github.com/schorschii/sixleds
