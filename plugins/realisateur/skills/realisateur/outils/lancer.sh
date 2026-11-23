#!/bin/sh
# Lance une commande du harnais avec les outils installés par le docteur (Node, ffmpeg, Python des contrôles).
# Usage :
#   sh lancer.sh om <arguments>                  la CLI du moteur (huashu-motion)
#   sh lancer.sh python <script.py> <arguments>  le Python des contrôles (numpy, Pillow)
#   sh lancer.sh node <script.mjs> <arguments>   Node, avec OM_MOTEUR qui pointe sur le moteur figé
#   sh lancer.sh <commande> <arguments>          toute autre commande (ffmpeg, ffprobe…), avec le bon PATH
ICI="$(cd "$(dirname "$0")" && pwd -P)"
SKILLS="$(cd "$ICI/../.." && pwd -P)"
CACHE="${REALISATEUR_CACHE:-$HOME/.cache/realisateur}"
if [ -d "$CACHE/bin" ]; then PATH="$CACHE/bin:$PATH"; export PATH; fi
OM_MOTEUR="${OM_MOTEUR:-$SKILLS/huashu-motion/moteur}"; export OM_MOTEUR
REALISATEUR_OUTILS="$ICI"; export REALISATEUR_OUTILS
cmd="$1"
if [ -z "$cmd" ]; then
  echo "usage : sh lancer.sh om|python|node|<commande> <arguments>" >&2
  exit 2
fi
shift
case "$cmd" in
  om) exec sh "$SKILLS/huashu-motion/bin/om" "$@" ;;
  python|python3)
    if [ -x "$CACHE/python/bin/python" ]; then exec "$CACHE/python/bin/python" "$@"
    elif [ -f "$CACHE/python/Scripts/python.exe" ]; then exec "$CACHE/python/Scripts/python.exe" "$@"
    else
      echo "realisateur : l'environnement Python des contrôles manque. Lancer : python3 -I \"$ICI/../scripts/docteur.py\" --installer" >&2
      exit 1
    fi ;;
  *)
    if ! command -v "$cmd" >/dev/null 2>&1; then
      echo "realisateur : « $cmd » est introuvable. Lancer : python3 -I \"$ICI/../scripts/docteur.py\" --installer" >&2
      exit 1
    fi
    exec "$cmd" "$@" ;;
esac
