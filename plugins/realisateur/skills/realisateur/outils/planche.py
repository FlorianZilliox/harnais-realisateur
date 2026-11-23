"""Assemble des images fixes en une planche à 2 colonnes (chaque image à 960 px de large), le nom du fichier en légende.

Usage :
    sh lancer.sh python planche.py <dossier>                       écrit <dossier>/planche.png avec les PNG du dossier
    sh lancer.sh python planche.py <sortie.png> <image1> <image2>…  planche des images données
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw


def planche(sortie: Path, fichiers: list) -> None:
    w, h, cols = 960, 540, 2
    rows = (len(fichiers) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * w, rows * (h + 30)), (20, 20, 20))
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(fichiers):
        im = Image.open(f).convert('RGB').resize((w, h), Image.LANCZOS)
        x, y = (i % cols) * w, (i // cols) * (h + 30)
        sheet.paste(im, (x, y + 30))
        d.text((x + 8, y + 8), Path(f).name, fill=(230, 220, 200))
    sheet.save(sortie)
    print(sortie, sheet.size)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    premier = Path(sys.argv[1])
    if premier.is_dir():
        images = sorted(p for p in premier.glob('*.png') if p.name != 'planche.png')
        if not images:
            sys.exit(f'Aucune image PNG dans {premier}')
        planche(premier / 'planche.png', images)
    else:
        if len(sys.argv) < 3:
            sys.exit(__doc__)
        planche(premier, [Path(a) for a in sys.argv[2:]])
