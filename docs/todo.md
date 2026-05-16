# Todo — Arkanoid

## En cours

_(rien)_

## À faire

- [ ] **Fichier de config** — externaliser les paramètres de jeu dans un fichier de configuration (type de background, vitesse balle, dimensions fenêtre…). Pour l'instant la constante `BACKGROUND` dans `arkadoid.py` est le seul point de config.

- [ ] **Contrôle joueur** — la raquette suit automatiquement la balle (mode démo). Ajouter le contrôle souris ou clavier.

- [x] **Collisions latérales des briques** — détection par minimum d'overlap (h/v), tri par distance pour les cas de coin, reversal xSpd+ySpd sur hit latéral pour éviter la pénétration du mur.

- [ ] **Condition de régénération du mur** — le mur se régénère uniquement quand toutes les briques sont détruites **et** que la balle est en bas (`yLoc > 600`). Comportement à revoir.

- [ ] **Rallonger la boucle musicale `hunger_desperate`** — 8 barres à 160 BPM ≈ 12 secondes, trop court. Ajouter des sections (ex. variation avec octave différente, section B sur E mineur ou B mineur, transition) pour atteindre ~30-40 secondes avant boucle.

- [ ] Permettre de toggle la musique via pression sur 'm'

- [ ] Ne pas crasher (et ne pas jouer de musique) lorsque le synth ou le compose ne sont pas trouvés. Afficher un message de warning dans les logs

- [x] **Accélération du jeu pour le debug** — `` ` `` pour accélérer, `ù` pour décélérer, cycles x1/x2/x4/x8/x16. N updates par frame, rendu toujours à 60fps. Multiplicateur affiché en jaune hors zone de jeu.


## Fait

- [x] **Séparation logique métier / affichage / input** — `domain/`, `graphics/`, `input/` ; `domain/entities.py` sans pygame, `_vanishingStep` géré dans `update()` et non dans `draw()`
- [x] **Musique procédurale** — boucle générée par code (numpy), pause synchronisée avec le jeu
- [x] **Profiles audio** — synth profiles (`megadrive`, `synthwave`) et compose profiles (`thunderforce`, `ambient`) configurables indépendamment
