#!/usr/bin/env python3
"""Docteur du harnais « realisateur » : vérifie tout ce qu'il faut pour fabriquer un film, et l'installe s'il manque.

Usage (depuis n'importe quel dossier) :
    python3 -I <dossier du skill realisateur>/scripts/docteur.py              diagnostic seul
    python3 -I <dossier du skill realisateur>/scripts/docteur.py --installer  installe ce qui manque
    python3 -I <dossier du skill realisateur>/scripts/docteur.py --essai      fabrique un film de quelques secondes, de bout en bout

Ce qui s'installe, et où : uniquement dans le cache ~/.cache/realisateur (ou $REALISATEUR_CACHE),
en versions figées dont l'empreinte SHA-256 est vérifiée avant usage :
    Node.js 22.20.0 (nodejs.org), ffmpeg et ffprobe 6.1.1 autonomes (github.com/eugeneware/ffmpeg-static),
    un environnement Python pour les scripts de contrôle (numpy, Pillow, depuis PyPI),
    les instruments réels de la musique (om samples build, 55 Mo, CC0/CC-BY).
Ce qui est déjà présent sur la machine (Node 22+, ffmpeg) est utilisé tel quel. Google Chrome doit être installé :
le docteur le vérifie mais ne l'installe pas. Rien n'est publié, rien n'est modifié hors du cache.
"""
from __future__ import annotations

import gzip
import hashlib
import os
import platform
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
import zipfile
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
SKILLS = SKILL.parent
OM_DIR = SKILLS / 'huashu-motion'
VD_DIR = SKILLS / 'video-director'
OM = OM_DIR / 'bin' / 'om'
CACHE = Path(os.environ.get('REALISATEUR_CACHE') or (Path.home() / '.cache' / 'realisateur'))
BIN = CACHE / 'bin'
PYENV = CACHE / 'python'
WIN = sys.platform.startswith('win')
EXE = '.exe' if WIN else ''

NODE_VERSION = '22.20.0'
NODE = {  # plateforme -> (archive, sha256), d'après https://nodejs.org/dist/v22.20.0/SHASUMS256.txt
    'darwin-arm64': ('node-v22.20.0-darwin-arm64.tar.gz', 'cc04a76a09f79290194c0646f48fec40354d88969bec467789a5d55dd097f949'),
    'darwin-x64': ('node-v22.20.0-darwin-x64.tar.gz', '00df9c5df3e4ec6848c26b70fb47bf96492f342f4bed6b17f12d99b3a45eeecc'),
    'linux-x64': ('node-v22.20.0-linux-x64.tar.gz', 'eeaccb0378b79406f2208e8b37a62479c70595e20be6b659125eb77dd1ab2a29'),
    'linux-arm64': ('node-v22.20.0-linux-arm64.tar.gz', '4181609e03dcb9880e7e5bf956061ecc0503c77a480c6631d868cb1f65a2c7dd'),
    'win-x64': ('node-v22.20.0-win-x64.zip', 'bb819d6eb8f5bfda294bbc83a7e4ec6539da67c4233d54b0d655b9248b15e29d'),
}
FFMPEG_TAG = 'b6.1.1'
FFMPEG = {  # plateforme -> {outil: sha256 du .gz}, d'après la publication b6.1.1 de eugeneware/ffmpeg-static
    'darwin-arm64': {'ffmpeg': '8923876afa8db5585022d7860ec7e589af192f441c56793971276d450ed3bbfa',
                     'ffprobe': 'd986a8ec7b030899fe66a8a288ed809a3543338705a3ce178cfb85869c5d80be'},
    'darwin-x64': {'ffmpeg': '929b375c1182d956c51f7ac25e0b2b0411fb01f6f407aa15c9758efeb4242106',
                   'ffprobe': 'd4da574d6e2e197bd259b47d69cf262df9e312af24ad960444f6d806d3d4c186'},
    'linux-x64': {'ffmpeg': 'bfe8a8fc511530457b528c48d77b5737527b504a3797a9bc4866aeca69c2dffa',
                  'ffprobe': '25d9b6ccb05e3d9de9e04e31e2506d8dd7f9f0418981965ac6df12e8d3afd067'},
    'win-x64': {'ffmpeg': '8883a3dffbd0a16cf4ef95206ea05283f78908dbfb118f73c83f4951dcc06d77',
                'ffprobe': 'f309e6223ad89d2fe54bccd420a7709b66fd27540674e92309578ed491a43c8d'},
}
FFMPEG_NAME = {'darwin-arm64': 'darwin-arm64', 'darwin-x64': 'darwin-x64', 'linux-x64': 'linux-x64', 'win-x64': 'win32-x64'}
PY_PAQUETS = ['numpy>=1.24,<3', 'pillow>=10,<12']
ESSAI_PARTITION = """<script type="text/vnd.abc" id="om-score">
X:1
T:Essai du docteur
M:4/4
L:1/8
Q:1/4=107
K:C
V:BS inst=pizz gain=1.0
!mf! C,,2 E,,2 G,,2 A,,2 | F,,2 A,,2 C,2 D,2 | G,,2 B,,2 D,2 F,2 | C,,8 |]
V:PN inst=piano gain=0.6
!mp! [CEG]3 [CEG] z4 | z2 [FAc]2 z2 [FAc]2 | [GBd]3 [GBd] z4 | [CEGc]8 |]
V:DR inst=drums kit=acoustic gain=0.5
[C,,^F,,]2 ^F,,2 ^F,,3/^F,,/ ^F,,2 | [C,,^F,,]2 ^F,,2 ^F,,3/^F,,/ ^F,,2 | [C,,^F,,]2 ^F,,2 ^F,,3/^F,,/ ^F,,2 | [C,,^C,]2 z6 |]
</script>
"""
LANCEURS = [OM, SKILL / 'outils' / 'lancer.sh', SKILL / 'outils' / 'stills.sh', SKILL / 'outils' / 'mixage_final.sh']

problemes: list[str] = []


def ok(msg: str) -> None:
    print(f'  ✓ {msg}')


def ko(msg: str, action: str) -> None:
    print(f'  ✗ {msg}\n      → {action}')
    problemes.append(msg)


def plateforme() -> str | None:
    m = platform.machine().lower()
    arch = 'arm64' if m in ('arm64', 'aarch64') else 'x64' if m in ('x86_64', 'amd64', 'x64') else None
    if arch is None:
        return None
    if sys.platform == 'darwin':
        return f'darwin-{arch}'
    if sys.platform.startswith('linux'):
        return f'linux-{arch}'
    if WIN and arch == 'x64':
        return 'win-x64'
    return None


def chemin_outils() -> str:
    return f'{BIN}{os.pathsep}{os.environ.get("PATH", "")}'


def trouver(nom: str) -> str | None:
    return shutil.which(nom, path=chemin_outils())


def lancer(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    env = dict(os.environ, PATH=chemin_outils())
    return subprocess.run(cmd, capture_output=True, text=True, env=env, **kw)


def om(*args: str, timeout: int = 900) -> subprocess.CompletedProcess:
    return lancer(['sh', str(OM), *args], timeout=timeout)


def telecharger(url: str, dest: Path, sha256: str) -> None:
    """Télécharge url dans dest et vérifie l'empreinte ; curl d'abord (proxy et certificats du système), urllib sinon."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_name(dest.name + '.part')
    print(f'      téléchargement de {url}')
    curl = shutil.which('curl')
    try:
        if curl:
            r = subprocess.run([curl, '-fsSL', '--retry', '2', '-o', str(part), url], capture_output=True, text=True)
            if r.returncode != 0:
                raise OSError(r.stderr.strip() or f'curl a échoué ({r.returncode})')
        else:
            with urllib.request.urlopen(url, timeout=120) as rep, open(part, 'wb') as f:
                shutil.copyfileobj(rep, f)
    except Exception as e:  # réseau, proxy, certificat
        part.unlink(missing_ok=True)
        raise RuntimeError(f'téléchargement impossible ({e}). Vérifier la connexion (un proxy d\'entreprise peut bloquer), puis relancer.') from e
    h = hashlib.sha256(part.read_bytes()).hexdigest()
    if h != sha256:
        part.unlink(missing_ok=True)
        raise RuntimeError(f'empreinte inattendue pour {url} (reçu {h[:12]}…, attendu {sha256[:12]}…) : fichier refusé.')
    part.replace(dest)


# --- Vérifications ---------------------------------------------------------------------------------------------

def verifier_fichiers() -> None:
    manque = [p for p in (OM_DIR / 'moteur' / 'cli' / 'om.js', OM, VD_DIR / 'scripts' / 'qa_video.py',
                          VD_DIR / 'scripts' / 'check_timeline.py') if not p.exists()]
    if manque:
        ko('Fichiers du harnais manquants : ' + ', '.join(str(p) for p in manque),
           'Réinstaller le plugin (ou recopier les trois dossiers realisateur, huashu-motion et video-director côte à côte).')
    else:
        ok(f'Skills présents côte à côte : realisateur, huashu-motion (moteur figé), video-director ({SKILLS})')


def remettre_droits() -> None:
    if WIN:
        return
    remis = []
    for p in LANCEURS:
        if p.exists() and not os.access(p, os.X_OK):
            p.chmod(p.stat().st_mode | 0o755)
            remis.append(p.name)
    if remis:
        ok('Droits d\'exécution remis sur : ' + ', '.join(remis))


def version_node() -> tuple[str | None, int]:
    n = trouver('node')
    if not n:
        return None, 0
    r = lancer([n, '-v'])
    m = re.match(r'v(\d+)', r.stdout.strip())
    return n, int(m.group(1)) if m else 0


def verifier_node(installer: bool, plat: str | None) -> None:
    n, major = version_node()
    if n and major >= 22:
        ok(f'Node.js {major} ({n})')
        return
    quoi = f'Node.js {major} trop ancien ({n})' if n else 'Node.js absent'
    if not installer:
        ko(quoi + ' : le moteur des films en a besoin (version 22 ou plus)', 'relancer le docteur avec --installer')
        return
    if plat not in NODE:
        ko(quoi + f' et pas d\'installation automatique pour cette machine ({platform.system()} {platform.machine()})',
           'installer Node.js 22 depuis https://nodejs.org, puis relancer le docteur')
        return
    archive, sha = NODE[plat]
    dossier = CACHE / archive.replace('.tar.gz', '').replace('.zip', '')
    try:
        if not dossier.exists():
            dl = CACHE / 'telechargements' / archive
            telecharger(f'https://nodejs.org/dist/v{NODE_VERSION}/{archive}', dl, sha)
            if archive.endswith('.zip'):
                with zipfile.ZipFile(dl) as z:
                    z.extractall(CACHE)
            else:
                with tarfile.open(dl) as t:
                    t.extractall(CACHE)
            dl.unlink(missing_ok=True)
        BIN.mkdir(parents=True, exist_ok=True)
        if WIN:
            shutil.copy2(dossier / 'node.exe', BIN / 'node.exe')
        else:
            lien = BIN / 'node'
            lien.unlink(missing_ok=True)
            lien.symlink_to(dossier / 'bin' / 'node')
    except Exception as e:
        ko(f'Installation de Node.js impossible : {e}', 'réessayer sur un autre réseau, ou installer Node.js 22 depuis https://nodejs.org')
        return
    n, major = version_node()
    if n and major >= 22:
        ok(f'Node.js {major} installé dans le cache ({n})')
    else:
        ko('Node.js installé mais il ne démarre pas', 'installer Node.js 22 depuis https://nodejs.org, puis relancer le docteur')


def verifier_ffmpeg(installer: bool, plat: str | None) -> None:
    presents = {o: trouver(o) for o in ('ffmpeg', 'ffprobe')}
    if all(presents.values()):
        ok(f'ffmpeg et ffprobe ({presents["ffmpeg"]})')
        return
    if not installer:
        ko('ffmpeg ou ffprobe absent : le rendu, le son et les contrôles en ont besoin', 'relancer le docteur avec --installer')
        return
    if plat not in FFMPEG:
        ko(f'ffmpeg absent et pas d\'installation automatique pour cette machine ({platform.system()} {platform.machine()})',
           'installer ffmpeg (https://ffmpeg.org/download.html), puis relancer le docteur')
        return
    BIN.mkdir(parents=True, exist_ok=True)
    try:
        for outil, sha in FFMPEG[plat].items():
            if presents[outil] and Path(presents[outil]).parent != BIN:
                continue
            nom = f'{outil}-{FFMPEG_NAME[plat]}.gz'
            dl = CACHE / 'telechargements' / nom
            telecharger(f'https://github.com/eugeneware/ffmpeg-static/releases/download/{FFMPEG_TAG}/{nom}', dl, sha)
            cible = BIN / f'{outil}{EXE}'
            with gzip.open(dl, 'rb') as src, open(cible, 'wb') as dst:
                shutil.copyfileobj(src, dst)
            cible.chmod(0o755)
            dl.unlink(missing_ok=True)
            if sys.platform == 'darwin':
                subprocess.run(['xattr', '-d', 'com.apple.quarantine', str(cible)], capture_output=True)
    except Exception as e:
        ko(f'Installation de ffmpeg impossible : {e}', 'réessayer sur un autre réseau, ou installer ffmpeg à la main')
        return
    r = lancer([trouver('ffmpeg') or 'ffmpeg', '-hide_banner', '-version'])
    if r.returncode == 0:
        ok(f'ffmpeg et ffprobe {FFMPEG_TAG[1:]} installés dans le cache ({BIN})')
    else:
        ko('ffmpeg installé mais il ne démarre pas : ' + (r.stderr.strip()[:200] or 'raison inconnue'),
           'installer ffmpeg à la main (https://ffmpeg.org/download.html), puis relancer le docteur')


def python_env() -> Path:
    return PYENV / ('Scripts/python.exe' if WIN else 'bin/python')


def verifier_python(installer: bool) -> None:
    py = python_env()
    test = 'import numpy, PIL; print(numpy.__version__, PIL.__version__)'
    if py.exists():
        r = lancer([str(py), '-c', test])
        if r.returncode == 0:
            ok(f'Python des contrôles (numpy {r.stdout.split()[0]}, Pillow {r.stdout.split()[1]}) : {py}')
            return
    if not installer:
        ko('Environnement Python des contrôles absent (qa_video.py, planches)', 'relancer le docteur avec --installer')
        return
    try:
        if not py.exists():
            r = lancer([sys.executable, '-m', 'venv', str(PYENV)])
            if r.returncode != 0:
                raise RuntimeError('création de l\'environnement refusée : ' + r.stderr.strip()[-300:])
        r = lancer([str(py), '-m', 'pip', 'install', '--disable-pip-version-check', '-q', *PY_PAQUETS], timeout=900)
        if r.returncode != 0:
            raise RuntimeError('pip a échoué : ' + (r.stderr.strip()[-300:] or r.stdout.strip()[-300:]))
        r = lancer([str(py), '-c', test])
        if r.returncode != 0:
            raise RuntimeError(r.stderr.strip()[-300:])
        ok(f'Python des contrôles installé (numpy {r.stdout.split()[0]}, Pillow {r.stdout.split()[1]}) : {py}')
    except Exception as e:
        ko(f'Environnement Python impossible à installer : {e}',
           'vérifier la connexion à PyPI (proxy d\'entreprise ?), puis relancer le docteur avec --installer')


def verifier_moteur(installer: bool) -> None:
    n, major = version_node()
    if not (n and major >= 22):
        print('  · Chrome et instruments : vérifiés une fois Node.js en place')
        return
    r = om('doctor', timeout=120)
    sortie = (r.stdout + r.stderr).strip().splitlines()
    for ligne in sortie:
        ligne = ligne.strip()
        if ligne.startswith('✓'):
            ok('moteur : ' + ligne[1:].strip())
        elif ligne.startswith('✗') or ligne.startswith('×') or ligne.startswith('!'):
            action = 'installer Google Chrome (https://www.google.com/chrome/), puis relancer le docteur' if 'Chrome' in ligne \
                else 'relancer le docteur avec --installer'
            ko('moteur : ' + ligne[1:].strip(), action)
    r = om('samples', timeout=60)
    m = re.search(r'(\d+) instruments', r.stdout)
    if m and int(m.group(1)) > 0:
        ok(f'Instruments réels de la musique : {m.group(1)}')
        return
    if not installer:
        ko('Instruments réels de la musique pas encore installés', 'relancer le docteur avec --installer (55 Mo)')
        return
    print('      installation des instruments (om samples build, 55 Mo)…')
    r = om('samples', 'build', timeout=1800)
    r2 = om('samples', timeout=60)
    m = re.search(r'(\d+) instruments', r2.stdout)
    if m and int(m.group(1)) > 0:
        ok(f'Instruments réels installés : {m.group(1)}')
    else:
        ko('Installation des instruments impossible : ' + (r.stderr.strip()[-300:] or r.stdout.strip()[-300:]),
           'vérifier la connexion (github.com), puis relancer le docteur avec --installer ; sans eux, la musique utilise des sons de synthèse')


def essai() -> None:
    print('\nEssai réel : un film de quelques secondes, de bout en bout')
    racine = Path(tempfile.mkdtemp(prefix='realisateur-essai-'))
    projet = racine / 'essai'
    os.environ['OM_HOME'] = str(racine / 'om-home')  # l'essai n'entre pas dans l'historique musical ni dans l'expérience du moteur
    try:
        r = om('new', str(projet), timeout=120)
        if r.returncode != 0 or not (projet / 'index.html').exists():
            ko('om new a échoué : ' + (r.stderr.strip()[-300:] or r.stdout.strip()[-300:]), 'lire le message ci-dessus, corriger, relancer --essai')
            return
        ok('projet créé (om new)')
        page = projet / 'index.html'
        html = page.read_text(encoding='utf-8')
        html = html.replace('</body>', ESSAI_PARTITION + '</body>', 1) if '</body>' in html else html + ESSAI_PARTITION
        page.write_text(html, encoding='utf-8')
        r = om('sound', str(projet), timeout=600)
        if r.returncode != 0 or not (projet / 'assets' / 'sound.wav').exists():
            ko('om sound n\'a pas produit la musique : ' + (r.stderr.strip()[-400:] or r.stdout.strip()[-400:]),
               'relancer le docteur avec --installer (instruments), puis --essai')
            return
        alertes = [l.strip() for l in (r.stdout + r.stderr).splitlines() if l.strip().startswith('warning')]
        ok('musique jouée par les instruments réels (om sound)' + (f', {len(alertes)} alerte(s) : ' + ' ; '.join(alertes)[:300] if alertes else ''))
        r = om('check', str(projet), timeout=300)
        if r.returncode != 0:
            ko('om check signale des erreurs : ' + (r.stdout.strip()[-400:] or r.stderr.strip()[-400:]), 'lire le message ci-dessus')
            return
        ok('composition contrôlée (om check)')
        for tentative in (1, 2):  # une machine très chargée peut faire attendre Chrome au-delà de son délai : on réessaie une fois
            r = om('render', str(projet), timeout=900)
            films = sorted((projet / 'out').glob('*.mp4'))
            if films or 'timed out' not in (r.stdout + r.stderr):
                break
            print('      Chrome a mis trop de temps à répondre (machine chargée ?) : nouvel essai du rendu')
        if r.returncode != 0 or not films:
            ko('om render a échoué : ' + (r.stderr.strip()[-400:] or r.stdout.strip()[-400:]), 'lire le message ci-dessus')
            return
        p = lancer([trouver('ffprobe') or 'ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_type,width,height',
                    '-of', 'default=nw=1', str(films[-1])])
        duree = re.search(r'duration=([\d.]+)', p.stdout)
        flux = set(re.findall(r'codec_type=(\w+)', p.stdout))
        if not duree or float(duree.group(1)) <= 0 or 'video' not in flux:
            ko('le film rendu est illisible', 'lire la sortie de om render')
            return
        garde = CACHE / 'essai.mp4'
        CACHE.mkdir(parents=True, exist_ok=True)
        shutil.copy2(films[-1], garde)
        if 'audio' not in flux:
            ko(f'le film rendu n\'a pas de son ({garde})', 'lire la sortie de om sound et de om render')
            return
        ok(f'film rendu avec sa musique : {float(duree.group(1)):.1f} s ({garde})')
        r = lancer([str(python_env()), str(VD_DIR / 'scripts' / 'qa_video.py'), '--help'])
        if r.returncode == 0:
            ok('scripts de contrôle de video-director exécutables')
        else:
            ko('qa_video.py ne démarre pas : ' + r.stderr.strip()[-300:], 'relancer le docteur avec --installer')
    finally:
        os.environ.pop('OM_HOME', None)
        shutil.rmtree(racine, ignore_errors=True)


def main() -> int:
    installer = '--installer' in sys.argv
    plat = plateforme()
    print(f'Docteur du harnais realisateur · {platform.system()} {platform.machine()} · cache : {CACHE}')
    verifier_fichiers()
    remettre_droits()
    verifier_node(installer, plat)
    verifier_ffmpeg(installer, plat)
    verifier_python(installer)
    verifier_moteur(installer)
    if '--essai' in sys.argv and not problemes:
        essai()
    print()
    if problemes:
        print(f'Il reste {len(problemes)} point(s) à régler (détail ci-dessus, avec l\'action à faire).')
        if not installer:
            print('La plupart s\'installent seuls : relancer avec --installer.')
        return 1
    print('Tout est prêt.' + ('' if '--essai' in sys.argv else ' Pour une preuve de bout en bout : --essai.'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
