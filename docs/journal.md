# Journal de bord — Arkanoid

## 2026-05-15

- Création du projet, commit initial (`arkadoid.py`, `arkadoid_diag_scroll.py`)
- Installation de `pygame` (via `pip3 install pygame --break-system-packages`)
- Réorganisation de la structure : déplacement des modules dans `src/game/` avec `__init__.py`
- Ajout du répertoire `docs/` et du fichier `CLAUDE.md`

- Mise en place de Poetry (2.4.1) : `pyproject.toml`, `poetry.lock`, venv isolé
- Ajout des commandes `poetry run play` et `poetry run play-base`
- Restructuration des deux fichiers : extraction du code d'initialisation et de la boucle dans `main()`, ajout de `if __name__ == '__main__': main()`
- Correction du bug latent `Paddle` (majuscule) vs `paddle` dans `Ball.update()` — le paramètre référençait l'ancienne variable globale
- Suppression du `print()` de debug dans la boucle de rendu de `arkadoid.py`

### Incident — inversion des fichiers par Claude

Lors de la refactorisation pour ajouter `main()`, Claude a réécrit les deux fichiers entièrement (`Write`) et a **interverti leur contenu** en faisant une inférence sur les noms de fichiers plutôt qu'en restant fidèle aux sources lues.

Cause : quand un LLM réécrit un fichier en entier, il peut laisser ses suppositions prendre le dessus sur ce qu'il a effectivement lu. Un `Edit` ciblé laisse un diff visible et limite ce risque.

**La vigilance de l'humain reste indispensable** — en particulier lors des réécritures complètes de fichiers, des renommages ou de toute opération sans diff partiel facilement vérifiable.

---

- Fusion des deux fichiers en un seul `arkadoid.py` avec background configurable
- Backgrounds renommés : `"grid"` (défaut) et `"trench"` (ex-`diag_scroll`)
- Commandes : `poetry run play` (grid) et `poetry run play-trench`
- Pause toggle sur la touche espace
- Raquette redessinée : forme capsule, effet métallique (gradient + arête + reflet)
- Création du `.gitignore` et nettoyage des `__pycache__`
- Séparation logique métier / affichage / input :
  - `domain/entities.py` — Ball, Paddle, Brick, BrickGroup, BrickWall — zéro import pygame
  - `graphics/renderer.py` — Renderer, méthodes draw_*, backgrounds, BRICK_COLORS
  - `input/handler.py` — InputHandler
  - `arkadoid.py` — boucle principale ~50 lignes
- `BRICK_COLORS` déplacé de `domain` vers `graphics` (décision d'affichage, pas métier)
- `_vanishingStep` incrémenté dans `Brick.update()` au lieu de `draw()` (logique découplée du rendu)

- Ajout du système audio procédural (`audio/`) : `synth.py` (oscillateurs + ADSR + FM + overdrive), boucle seamless, pause synchronisée avec le jeu — cohérence UX notée positivement
- Dépendance `numpy` ajoutée
- Refonte musicale style Thunderforce 3 (Mega Drive) : FM synthesis 2 opérateurs, overdrive, kick + hihat procéduraux, 160 BPM, Ré mineur
- Architecture profiles : `audio/profiles/synth_profiles.py` (comment ça sonne) et `audio/profiles/compose_profiles.py` (ce qui est joué) — deux axes orthogonaux configurables indépendamment
- Profiles disponibles : synth `"megadrive"` / `"synthwave"`, compose `"thunderforce"` / `"ambient"` (Am→F→C→G 110 BPM)

### État du projet

Fichier unique `src/game/arkadoid.py` orchestrant trois packages :

```
domain/entities.py              ← logique pure, pas de pygame
graphics/renderer.py            ← tout le rendu
input/handler.py                ← événements clavier
audio/synth.py                  ← oscillateurs + ADSR + FM (numpy pur)
audio/composer.py               ← moteur générique de composition
audio/player.py                 ← AudioPlayer(synth=, compose=)
audio/profiles/synth_profiles.py   ← HOW : megadrive, synthwave
audio/profiles/compose_profiles.py ← WHAT : thunderforce, ambient
```

### Points ouverts

- Collisions latérales des briques non gérées (TODO dans le code)
- La raquette suit automatiquement la balle (mode démo) — pas encore de contrôle joueur
- Le mur se régénère uniquement quand toutes les briques sont détruites **et** que la balle est en bas (`yLoc > 600`) — comportement à revoir
