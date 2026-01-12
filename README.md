🗺️ DQ9 Treasure Picker

DQ9 Treasure Picker est un outil PC dédié à Dragon Quest IX – Les Sentinelles du Firmament, pensé pour aider les joueurs à identifier et parcourir les cartes au trésor du jeu.

Le projet se compose actuellement de deux fonctionnalités distinctes :
un picker manuel fonctionnel et un système de détection automatique expérimental.

✨ Fonctionnalités
🖱️ 1. Treasure Picker (fonctionnel)

Le picker permet de parcourir manuellement les cartes au trésor, classées par zones / régions, à partir d’images locales.

📁 Navigation par dossiers (zones)

🖼️ Aperçu clair des cartes

🖱️ Sélection simple à la souris

⚡ Rapide, léger et hors ligne

👉 Idéal pour consulter, comparer et identifier des cartes sans effort.

🤖 2. find.py – Détection automatique (expérimental / non finalisé)

Le script find.py est une fonctionnalité expérimentale, pas encore totalement fonctionnelle, dont le but est de :

🔍 Détecter automatiquement une carte au trésor

📸 À partir d’un screenshot in-game

🧠 Comparer l’image avec la base de données de cartes

📌 Fonctionnement prévu

Faire un screenshot en jeu de la carte au trésor

Placer l’image dans le dossier query

Renommer l’image en treasure.png

Lancer le script find.py

➡️ Le résultat est généré dans le dossier out, avec :

🗺️ la carte correspondante

🌍 la région / zone associée

⚠️ Cette partie est encore en cours de développement et peut donner des résultats incomplets ou imprécis.

🎯 Objectif du projet

Proposer un outil communautaire pratique pour :

l’identification des cartes au trésor

le confort de recherche

le theorycraft autour de Dragon Quest IX

Le projet évolue progressivement et reste ouvert aux améliorations.

🛠️ Technologies utilisées

Python

Tkinter (interface graphique)

Traitement d’images (basique / expérimental)

Fonctionne hors ligne

📜 Disclaimer

Ce projet est un outil non officiel à but communautaire.
Dragon Quest IX – Les Sentinelles du Firmament et tous les assets associés sont la propriété de Square Enix.
