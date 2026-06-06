# CLAUDE.md — Arkanoid

## Présentation

Jeu Arkanoid développé en Python avec pygame. Projet d'exploration / apprentissage.

## Structure

```
arkanoid/
├── CLAUDE.md
├── pyproject.toml
├── docs/
│   └── journal.md        # journal de bord du projet
└── src/
    └── game/             # package Python du jeu
        ├── __init__.py
        └── arkadoid.py   # fichier unique du jeu
```

## Lancer le jeu

```bash
poetry run play        # fond diag_scroll (défaut)
poetry run play-grid   # fond grille
```

## Configuration

La constante `BACKGROUND` dans [src/game/arkadoid.py](src/game/arkadoid.py) contrôle le fond par défaut :

```python
BACKGROUND = "diag_scroll"  # "diag_scroll" | "grid"
```

Les fonctions de fond ont toutes la même signature `(r1, g1, b1, r2, g2, b2, v_scroll, h_scroll)` — en ajouter une nouvelle suffit à l'enregistrer dans le dict `BACKGROUNDS`.

Dépendance : `pygame` (géré par Poetry)

## Architecture

### Classes principales

| Classe | Rôle |
|---|---|
| `Ball` | Balle : position, vitesse, détection de collision, état anti-doublon |
| `Paddle` | Raquette : rendu dégradé, suivi de la balle |
| `Brick` | Brique individuelle : rendu dégradé + animation de disparition |
| `BrickGroup` | Groupe de briques, gère la collision et le nettoyage |
| `BrickWall(BrickGroup)` | Mur complet généré en grille |

### Boucle principale

Tourne à 60 fps (`clock.tick(60)`). Ordre d'exécution par frame :
1. Événements pygame
2. Regen du mur si vide
3. Fond animé (glow + défilement)
4. `brick_group.draw()`
5. `ball.update()` puis `ball.draw()`
6. `paddle.update()` puis `paddle.draw()`
7. `brick_group.update()` (nettoyage des briques détruites)
8. `pygame.display.flip()`

### Particularités notables

- La raquette suit automatiquement la balle (pas de contrôle joueur pour l'instant)
- L'état `_collisionState` de la balle empêche les collisions multiples sur une même brique
- Les briques disparaissent progressivement via `_vanishingStep` (animation sur ~30 frames)
- `arkadoid_diag_scroll.py` calcule un effet de perspective via `1 / sin(angle)` pour le défilement du fond

## Conventions

- Pas de commentaires sauf pour les invariants non évidents ou les TODO actifs
- Pas de gestion d'erreur sur les chemins internes (faire confiance à pygame)
- **Aucun module ne dépasse 200 lignes** — indicateur de bonne conception, pas de seuil d'alerte ; la séparation des responsabilités et le faible couplage se pensent dès la conception, pas en réaction à la taille
- **Mettre à jour `docs/journal.md` à chaque session de travail significative** — résumé des changements, décisions prises, points ouverts
- **Mettre à jour `docs/todo.md`** quand une tâche est ajoutée, commencée ou terminée
- **Mettre à jour `README.md`** si la structure, les commandes ou les fonctionnalités changent

## Directives graphiques

Tous les graphismes sont **100% procéduraux** : formes, couleurs, animations et effets sont calculés et dessinés par le code à chaque frame via pygame.

- Aucun fichier image externe (PNG, JPG, SVG, sprite sheet…)
- Aucune police bitmap chargée depuis un fichier
- Aucun asset graphique versionné dans le dépôt

Si un rendu visuel est nécessaire pour documenter ou tester, le décrire textuellement ou le reproduire par du code, jamais par une capture figée.
