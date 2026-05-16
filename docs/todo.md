# Todo — Arkanoid

## En cours

_(rien)_

## À faire

- [ ] **Fichier de config** — externaliser les paramètres de jeu dans un fichier de configuration (type de background, vitesse balle, dimensions fenêtre…). Pour l'instant la constante `BACKGROUND` dans `arkadoid.py` est le seul point de config.

- [x] **Contrôle joueur** — flèches ←/→, espace pour lancer, p pour pause. Machine d'état idle/playing/paused. Balle perdue → reset paddle centre + idle.

- [x] **Collisions latérales des briques** — détection par minimum d'overlap (h/v), tri par distance pour les cas de coin, reversal xSpd+ySpd sur hit latéral pour éviter la pénétration du mur.

- [ ] **Condition de régénération du mur** — le mur se régénère uniquement quand toutes les briques sont détruites **et** que la balle est en bas (`yLoc > 600`). Comportement à revoir.

- [x] **[BUG] Balle coincée dans un couloir diagonal** — configuration reproductible :
  ```
  -vv
  vvv
  vv-
  ```
  Root cause : `Brick.collide()` ne vérifiait pas `_vanishingStep`. Une brique déjà touchée (en train de disparaître) pouvait être re-touchée, ce qui remettait `_vanishingStep = 1` et relançait son animation indéfiniment — la brique n'atteignait jamais 30 et n'était jamais supprimée. Fix : retourner `None` dans `collide()` si `self._vanishingStep > 0`.

- [ ] **Angle de lancement** — en état `idle`, les touches ←/→ orientent la trajectoire de lancement (ex. ±15° à ±75° par rapport à la verticale). Afficher un réticule (ligne ou flèche) depuis la balle pour visualiser l'angle courant. Le lancement sur espace tire dans la direction choisie.

- [ ] **Mode démo (attract mode)** — au démarrage, le jeu tourne en mode démo : raquette qui suit automatiquement la balle (comportement pré-contrôle joueur), pas de musique, texte "PRESS START" qui clignote à l'écran. Ajouter l'état `demo` à la machine d'état (`demo` → `idle` → `playing` → `paused`). La démo reprend si la balle tombe (reset silencieux, pas de punition).

- [ ] **Démarrage sur action joueur** — depuis l'état `demo`, appuyer sur espace, Start ou bouton 1 passe en `idle` et lance la musique. La transition `idle` → `playing` (lancement de la balle) reste inchangée.

- [ ] **Effets sonores** — sons courts procéduraux (via le synth existant ou un oscillateur dédié, sans fichier audio externe) pour : collision brique (clic court, pitch selon la rangée), collision raquette (bruit sourd grave), balle perdue dans le ravin (descente mélodique ou bruit de chute).

- [ ] **Rallonger la boucle musicale `hunger_desperate`** — 8 barres à 160 BPM ≈ 12 secondes, trop court. Ajouter des sections (ex. variation avec octave différente, section B sur E mineur ou B mineur, transition) pour atteindre ~30-40 secondes avant boucle.

- [ ] Permettre de toggle la musique via pression sur 'm'

- [ ] Ne pas crasher (et ne pas jouer de musique) lorsque le synth ou le compose ne sont pas trouvés. Afficher un message de warning dans les logs

- [x] **Accélération du jeu pour le debug** — `` ` `` pour accélérer, `ù` pour décélérer, cycles x1/x2/x4/x8/x16. N updates par frame, rendu toujours à 60fps. Multiplicateur affiché en jaune hors zone de jeu.


## Fait

- [x] **Séparation logique métier / affichage / input** — `domain/`, `graphics/`, `input/` ; `domain/entities.py` sans pygame, `_vanishingStep` géré dans `update()` et non dans `draw()`
- [x] **Musique procédurale** — boucle générée par code (numpy), pause synchronisée avec le jeu
- [x] **Profiles audio** — synth profiles (`megadrive`, `synthwave`) et compose profiles (`thunderforce`, `ambient`) configurables indépendamment
