# TBO Treuhand — Demo-Landingpage

Mehrsprachige Demo-Landingpage (DE · FR · IT · EN) für TBO Treuhand AG.
Live: **https://tbo.arvut.ch** · Vorschau (GitHub Pages): **https://arvut.github.io/tbo-demo/**

## Struktur

- `index.src.html` — **DE-Master (Quelle der Wahrheit).** Hier den Inhalt bearbeiten.
- `de/ fr/ it/ en/ ru/` — generierte Sprachversionen (NICHT von Hand bearbeiten, werden überschrieben).
- `index.html` — Root-Weiterleitung auf `de/`.
- `assets/` — Bilder & Schriften (gemeinsam für alle Sprachen, relativ `../assets/`).
- `build.py` — erzeugt die Sprachordner aus `index.src.html` + Übersetzungen.

## Bearbeiten & neu bauen

1. Design/Text am DE-Master `index.src.html` ändern.
2. Für Übersetzungen: neue Texte an das Übersetzungsteam geben (Schlüsselschema wie bisher).
3. `python3 build.py` ausführen → regeneriert `de/ fr/ it/ en/ ru/` + Root-Redirect.
4. Commit + Push → GitHub Pages baut automatisch neu.

Nur den DE-Master direkt ändern? Dann `de/index.html` wird beim nächsten `build.py` überschrieben —
immer `index.src.html` pflegen.

## Sprachumschalter

DE / FR / IT / EN sichtbar. RU wird gebaut, ist aber im Umschalter versteckt (Reserve).
