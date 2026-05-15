# Todo — Arkanoid

## En cours

_(rien)_

## À faire

- [ ] **Fichier de config** — externaliser les paramètres de jeu dans un fichier de configuration (type de background, vitesse balle, dimensions fenêtre…). Pour l'instant la constante `BACKGROUND` dans `arkadoid.py` est le seul point de config.

- [ ] **Contrôle joueur** — la raquette suit automatiquement la balle (mode démo). Ajouter le contrôle souris ou clavier.

- [ ] **Collisions latérales des briques** — TODO dans le code, seules les collisions verticales sont gérées.

- [ ] **Condition de régénération du mur** — le mur se régénère uniquement quand toutes les briques sont détruites **et** que la balle est en bas (`yLoc > 600`). Comportement à revoir.

## Fait

- [x] **Séparation logique métier / affichage / input** — `domain/`, `graphics/`, `input/` ; `domain/entities.py` sans pygame, `_vanishingStep` géré dans `update()` et non dans `draw()`
- [x] **Musique procédurale** — boucle synthwave générée par code (numpy), Am→F→C→G 110 BPM, pause synchronisée avec le jeu
