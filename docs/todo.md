# Todo — Arkanoid

## En cours

_(rien)_

## À faire

- [ ] **Fichier de config** — externaliser les paramètres de jeu dans un fichier de configuration (type de background, vitesse balle, dimensions fenêtre…). Pour l'instant la constante `BACKGROUND` dans `arkadoid.py` est le seul point de config.

- [ ] **Séparation logique métier / affichage / input** — le code mélange actuellement les trois dans les mêmes classes. Pistes :
  - Extraire la logique de mise à jour (positions, collisions) des méthodes `draw()`
  - Centraliser la gestion des événements clavier/souris hors de la boucle principale
  - Permettre de tester la logique sans lancer pygame

## Fait

_(rien)_
