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

- Collisions latérales des briques : détection par minimum d'overlap (retourne `'v'`/`'h'`/`None`), tri des briques par distance au centre de la balle (fix du cas de coin), reversal xSpd+ySpd sur hit latéral pour éviter la pénétration du mur intérieur
- Mise en place des tests unitaires (`src/tests/`, pytest, 13 tests), config VS Code (`.vscode/settings.json`), venv Poetry en local (`.venv/`)
- Profil audio `hunger_desperate` affiné : analyse MIDI de l'original → Fa# mineur, 160 BPM, lead en half notes, basse pédal 16th, descente chromatique C#→B→A→G# ; profil `megadrive_legato` + lead `sine_vibrato` ajouté au profil `synthwave` ; percussion activée pour tous les profils

### État du projet

Fichier unique `src/game/arkadoid.py` orchestrant quatre packages :

```
domain/entities.py              ← logique pure, pas de pygame
graphics/renderer.py            ← tout le rendu
input/handler.py                ← événements clavier
audio/synth.py                  ← oscillateurs + ADSR + FM (numpy pur)
audio/composer.py               ← moteur générique de composition
audio/player.py                 ← AudioPlayer(synth=, compose=)
audio/profiles/synth_profiles.py   ← megadrive, megadrive_legato, megadrive_fierce, synthwave
audio/profiles/compose_profiles.py ← shmup, ambient, shmup_pressure
src/tests/                      ← tests unitaires pytest
```

- Accélération du jeu pour le debug : `<` / `>` pour cycler x1/x2/x4/x8/x16 (N updates par frame, rendu toujours à 60fps). Le multiplicateur courant est affiché en jaune dans la zone droite de la fenêtre — invisible en x1. **Note** : l'affichage du multiplicateur a été ajouté spontanément sans être demandé — bonne pratique UX (rendre visible l'état du système là où l'utilisateur peut le voir sans chercher).
- Fix double-inversion de `xSpd` au rebond mur + brique 'h' dans le même frame (oscillation near-wall)
- Fix cas de coin : tri des briques par distance au centre de la balle avant itération

- Contrôle joueur : flèches ←/→, espace pour lancer, p pour pause. Machine d'état `idle`/`playing`/`paused`. Balle perdue → reset paddle centre + idle (système de vies/score prévu plus tard). `Paddle.update(left, right)` remplace l'ancien suivi automatique de la balle. Paddle toujours à vitesse humaine (non multiplié par le facteur debug).

---

## 2026-05-16

### Intégration manette — diagnostic complet avec Claude

Objectif : connecter une manette USB-C générique (Padix Co., vendor `0x0583` / product `0x2060`, "2-axis 8-button gamepad") pour contrôler la raquette.

#### Ce qui semblait simple ne l'était pas

La manette était visible dans le Rapport système macOS, mais `pygame.joystick.get_count()` retournait `0`. Les tentatives habituelles (permission *Surveillance des entrées*, `SDL_JOYSTICK_HIDAPI=0`, `SDL_JOYSTICK_MFI=1`) n'ont rien changé.

#### Diagnostic avec Claude

Claude a creusé le registre IOKit :

```
"GameControllerSupportedHIDDevice" = Yes
"IOUserServerName" = "com.apple.driverkit.AppleUserHIDDrivers"
```

Ce flag indique que macOS a revendiqué la manette via son framework Game Controller (GCController). SDL/HIDAPI ne peut pas ouvrir un device exclusivement détenu par un driver système Apple — d'où le silence de pygame, même après les permissions accordées.

Sans ce diagnostic, la piste naturelle aurait été de continuer à chercher du côté des permissions ou des flags SDL, sans jamais trouver.

#### Solution : bypass SDL via hidapi + ctypes

hidapi (déjà installé via Homebrew) peut ouvrir le device en-dessous du framework Apple. On a vérifié d'abord que `hid.Device` pouvait lire des données brutes :

```
[128, 128, 0, 0, 0, 0, 0, 0]  # axes centrés, aucun bouton
```

Format du rapport HID :
- `byte[0]` → axe X (0=gauche, 128=centre, 255=droite)
- `byte[1]` → axe Y
- `byte[2]` → bitmask boutons (bit 0 = bouton 1…)

Implémentation : wrapper `ctypes` minimal dans `input/hid_gamepad.py`, chargé via `ctypes.util.find_library('hidapi')` avec fallback sur `/opt/homebrew/lib/libhidapi.dylib`. Aucune nouvelle dépendance Python. `InputHandler` essaie d'abord `pygame.joystick` ; si absent, tente `HidGamepad`.

#### Structure résultante

```
input/
  handler.py       ← InputHandler, logique d'input unifiée
  hid_gamepad.py   ← HidGamepad (ctypes + hidapi), format de rapport Padix
```

#### Ce que j'aurais pas trouvé seul

- Savoir qu'il faut inspecter IOKit (`ioreg`) pour voir quel driver possède un device HID
- Comprendre que `GameControllerSupportedHIDDevice = Yes` signifie une capture exclusive par Apple
- Penser à bypasser SDL entièrement plutôt que de chercher un flag SDL supplémentaire
- Utiliser `ctypes` directement sur `libhidapi.dylib` pour éviter d'ajouter une dépendance Python

### Points ouverts

- Le mur se régénère uniquement quand toutes les briques sont détruites — comportement correct désormais (condition `yLoc > 600` supprimée)
- Système de vies / score à implémenter (perte de balle déclenche actuellement juste un reset)
