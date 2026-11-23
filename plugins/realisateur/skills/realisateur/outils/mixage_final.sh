#!/bin/sh
# Mixage final d'un film : l'image est copiée telle quelle ; le son reçoit un gain FIXE pour atteindre la loudness
# visée (−14 LUFS intégrés par défaut), puis un limiteur suréchantillonné (crête vraie ≤ −1 dBTP).
# Pas de normalisation dynamique (loudnorm) : elle écrase la dynamique, le temps fort cesse d'être le moment le plus
# fort, et la crête vraie passe quand même.
# Option : un vrai silence juste avant le temps fort (descente en 50 ms à <début>, retour sec à <fin>, en secondes).
#
# Usage : sh mixage_final.sh <entrée.mp4> <sortie.mp4> [<début du silence> <fin du silence>]
#         CIBLE_LUFS=-16 sh mixage_final.sh …   pour une autre loudness
# Contrôle ensuite : sh lancer.sh python ../../video-director/scripts/qa_video.py <sortie.mp4>
set -e
ICI="$(cd "$(dirname "$0")" && pwd -P)"
CACHE="${REALISATEUR_CACHE:-$HOME/.cache/realisateur}"
if [ -d "$CACHE/bin" ]; then PATH="$CACHE/bin:$PATH"; export PATH; fi
IN="$1"; OUT="$2"; DEBUT="$3"; FIN="$4"; CIBLE="${CIBLE_LUFS:--14}"
if [ -z "$IN" ] || [ -z "$OUT" ]; then echo "Usage : sh mixage_final.sh <entrée.mp4> <sortie.mp4> [<début du silence> <fin du silence>]" >&2; exit 2; fi
[ -f "$IN" ] || { echo "Fichier introuvable : $IN (lancer d'abord om render)" >&2; exit 1; }
command -v ffmpeg >/dev/null || { echo "ffmpeg manque : lancer python3 -I \"$ICI/../scripts/docteur.py\" --installer" >&2; exit 1; }
if [ -n "$DEBUT" ] && [ -n "$FIN" ]; then
  GATE="volume='if(between(t,$DEBUT,$FIN),max(0,1-(t-$DEBUT)/0.05),1)':eval=frame,"
else
  GATE=""
fi
I=$(ffmpeg -hide_banner -nostats -i "$IN" -map 0:a:0 -af "${GATE}ebur128" -f null - 2>&1 | sed -n 's/^ *I: *\(-*[0-9.]*\) LUFS.*/\1/p' | tail -1)
[ -n "$I" ] || { echo "Mesure de loudness impossible sur $IN (le film a-t-il une piste son ?)" >&2; exit 1; }
G=$(LC_ALL=C awk -v c="$CIBLE" -v i="$I" 'BEGIN { printf "%.2f", c - i }')   # LC_ALL=C : un point décimal, même sur un Mac en français
echo "loudness mesurée $I LUFS, cible $CIBLE LUFS, gain fixe appliqué $G dB"
ffmpeg -hide_banner -v error -y -i "$IN" -c:v copy \
  -af "${GATE}volume=${G}dB,aresample=192000,alimiter=limit=0.74:attack=1:release=60:level=disabled,aresample=48000" \
  -c:a aac -b:a 256k -movflags +faststart -f mp4 "$OUT.part" || { rm -f "$OUT.part"; echo "Le mixage a échoué (message de ffmpeg ci-dessus) : rien n'a été écrit." >&2; exit 1; }
mv "$OUT.part" "$OUT"
echo "écrit : $OUT"
