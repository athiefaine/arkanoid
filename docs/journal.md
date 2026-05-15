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

### État du projet

Deux variantes du jeu coexistent :

- `arkadoid.py` (`poetry run play-base`) — fond diagonal expérimental avec effet de perspective (`math.sin`), logique de collision simple
- `arkadoid_diag_scroll.py` (`poetry run play`) — fond grille avec défilement horizontal lié à la raquette, logique de collision améliorée (`_collisionState` anti-doublon)

**Attention** : le nommage est contre-intuitif — c'est `arkadoid.py` qui contient l'effet diagonal, pas `arkadoid_diag_scroll.py`.

### Incident — inversion des fichiers par Claude

Lors de la refactorisation pour ajouter `main()`, Claude a réécrit les deux fichiers entièrement (`Write`) et a **interverti leur contenu** en faisant une inférence sur les noms de fichiers plutôt qu'en restant fidèle aux sources lues.

Cause : quand un LLM réécrit un fichier en entier, il peut laisser ses suppositions prendre le dessus sur ce qu'il a effectivement lu. Un `Edit` ciblé laisse un diff visible et limite ce risque.

**La vigilance de l'humain reste indispensable** — en particulier lors des réécritures complètes de fichiers, des renommages ou de toute opération sans diff partiel facilement vérifiable.

### Points ouverts

- Collisions latérales des briques non gérées (TODO dans le code)
- La raquette suit automatiquement la balle (mode démo) — pas encore de contrôle joueur
- Le mur se régénère uniquement quand toutes les briques sont détruites **et** que la balle est en bas (`yLoc > 600`) — comportement à revoir
- `self.__screen` stocké dans chaque `__init__` mais jamais utilisé (le dessin passe par le global `screen`) — à nettoyer
