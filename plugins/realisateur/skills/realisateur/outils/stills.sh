#!/bin/sh
# Rend des images fixes de la composition aux instants donnés, les range dans <film>/stills/<lot>/ et en fait une planche.
# Usage : sh stills.sh <dossier du film> <lot> 1.0,2.5,8.2
ICI="$(cd "$(dirname "$0")" && pwd -P)"
film="$1"; lot="$2"; at="$3"
if [ -z "$film" ] || [ -z "$lot" ] || [ -z "$at" ]; then echo "Usage : sh stills.sh <dossier du film> <lot> 1.0,2.5,…" >&2; exit 2; fi
cd "$film" || { echo "Dossier introuvable : $film" >&2; exit 1; }
sh "$ICI/lancer.sh" om still . --at "$at" > /dev/null 2>&1 || { echo "om still a échoué (lancer « sh $ICI/lancer.sh om check . » pour voir pourquoi)" >&2; exit 1; }
mkdir -p "stills/$lot"
n=0
for f in index-*.png; do [ -f "$f" ] && mv "$f" "stills/$lot/" && n=$((n + 1)); done
[ "$n" -gt 0 ] || { echo "Aucune image produite" >&2; exit 1; }
sh "$ICI/lancer.sh" python "$ICI/planche.py" "stills/$lot"
