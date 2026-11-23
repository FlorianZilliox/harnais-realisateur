#!/usr/bin/env python3
"""Exemple de partition écrite par programme : un jazz d'enquête à instruments réels (100 BPM, 25 mesures ≈ 60 s).

Ce que montre l'exemple (tiré d'un vrai film, textes retirés) :
- la musique s'écrit comme une partition ABC (`<script type="text/vnd.abc" id="om-score">` dans index.html), que
  `om sound` joue avec les instruments réels installés par le docteur (contrebasse en pizzicato, piano, cordes,
  trémolo, batterie aux balais) ;
- chaque mesure a un TYPE (accroche, groove, doute, arrêt, impact, temps fort, fin) qui suit le récit : la musique
  presque se tait sur le moment de doute, fait un vrai silence avant le temps fort, puis éclate en tutti ;
- les `!mark:nom!` posés sur la contrebasse tombent sur les étiquettes `scene:nom` de la timeline : c'est ce qui cale
  l'image sur la musique.

Usage : sh lancer.sh python partition-jazz.py <dossier du film ou index.html>
Pour un autre film : réécrire BARS (une ligne par mesure, avec le moment du récit en commentaire) et MARKS, garder le reste.
"""
from pathlib import Path
import re
import sys

if len(sys.argv) < 2:
    sys.exit(__doc__)
PAGE = Path(sys.argv[1])
if PAGE.is_dir():
    PAGE = PAGE / 'index.html'
if not PAGE.exists():
    sys.exit(f'Page introuvable : {PAGE}')

NAMES = ['=C', '_D', '=D', '_E', '=E', '=F', '_G', '=G', '_A', '=A', '_B', '=B']


def n(m, length=''):
    pc, octv = m % 12, m // 12 - 1
    acc, letter = NAMES[pc][0], NAMES[pc][1]
    if octv >= 5:
        s = letter.lower() + "'" * (octv - 5)
    elif octv == 4:
        s = letter
    else:
        s = letter + ',' * (4 - octv)
    return acc + s + str(length)


def ch(ms, length=''):
    return '[' + ''.join(n(m) for m in ms) + ']' + str(length)


CH = {
    'Cm':  dict(root=36, third=3, pn=[48, 51, 55, 58, 62], st=[67, 72, 75]),
    'Ab':  dict(root=44, third=4, pn=[44, 51, 55, 60], st=[68, 72, 75]),
    'Fm':  dict(root=41, third=3, pn=[41, 51, 55, 56], st=[68, 72, 77]),
    'G7':  dict(root=43, third=4, pn=[43, 53, 56, 59], st=[67, 71, 77]),
    'Bb7': dict(root=46, third=4, pn=[46, 50, 56, 60], st=[68, 74, 77]),
    'Eb':  dict(root=39, third=4, pn=[39, 46, 50, 55, 58, 65], st=[67, 70, 75, 79]),
    'Fd':  dict(root=42, third=3, pn=[42, 48, 51, 57], st=[66, 72, 75]),
    'Af':  dict(root=44, third=4, pn=[44, 51, 55, 60, 62], st=[68, 72, 74, 79]),
}

# (type, accord, nuance) pour chacune des 25 mesures ; en commentaire, le moment du récit qu'elles portent
BARS = [
    ('hookm', 'Cm', 'p'), ('hook', 'Ab', 'p'), ('hook', 'Fm', 'p'), ('hook', 'G7', 'mp'),   # 0-3   accroche : la méthode, ses étapes ; l'agent entre
    ('groovehit', 'Cm', 'mf'), ('groove', 'Ab', 'mf'),                                      # 4-5   l'agent relie les étapes
    ('groovem', 'Cm', 'mf'), ('groove', 'G7', 'mf'),                                        # 6-7   sous le capot : il travaille, la personne valide
    ('doubt', 'Cm', 'p'), ('doubt', 'Ab', 'p'),                                             # 8-9   un doute : une donnée manque
    ('groove', 'Fm', 'mf'),                                                                 # 10    la donnée arrive : la marche reprend
    ('doubt', 'G7', 'p'), ('groove', 'Fm', 'mp'),                                           # 11-12 un second doute, levé doucement
    ('stop', 'Cm', 'pp'), ('impact', 'G7', 'mf'),                                           # 13-14 presque silence (l'erreur repérée), puis un coup (l'accord donné)
    ('groove', 'Cm', 'f'),                                                                  # 15    la correction s'écrit
    ('groovehit', 'Ab', 'f'), ('groove', 'Fm', 'f'), ('groove', 'G7', 'f'),                 # 16-18 passage à l'échelle : la musique s'ouvre
    ('doubt', 'Ab', 'p'), ('groove', 'G7', 'mf'),                                           # 19-20 sa limite, dite simplement
    ('soft', 'Ab', 'mp'),                                                                   # 21    on prépare la chute
    ('pre', 'Bb7', 'mf'),                                                                   # 22    puis un vrai silence
    ('decide', 'Eb', 'ff'),                                                                 # 23    le temps fort, en tutti
    ('final', 'Eb', 'p'),                                                                   # 24    l'accord se pose, fin
]
MARKS = {0: 'm-accroche', 4: 'm-agent', 8: 'm-doute', 13: 'm-erreur', 16: 'm-echelle', 23: 'm-temps-fort'}
MOTIF = '=G3/ _A/ =G2 =D4'          # sol, la bémol, sol, ré (sol4 la♭4 sol4 ré4)


def nxt(i):
    for j in range(i + 1, len(BARS)):
        if BARS[j][1]:
            return CH[BARS[j][1]]['root']
    return 36


def walk(c, i):
    r = c['root']; third = r + c['third']; fifth = r + 7 if r + 7 <= 52 else r - 5
    a = nxt(i) + 1
    if a == fifth:
        a = nxt(i) - 1
    return ' '.join(n(m, 2) for m in (r, third, fifth, a))


def bar(i, voice):
    t, cname, dyn = BARS[i]
    c = CH.get(cname) if cname else None
    d = f'!{dyn}! '
    mk = f'!mark:{MARKS[i]}! ' if (i in MARKS and voice == 'BS') else ''
    if voice == 'BS':
        if t == 'burst':
            body = ' '.join(n(CH[k]['root'], 2) for k in ('Fm', 'Fd', 'G7', 'Ab'))
        elif t in ('doubt', 'stop'):
            body = f"{n(c['root'], 4)} {n(c['root'] + 7 if c['root'] + 7 <= 52 else c['root'] - 5, 4)}" if t == 'doubt' else 'z8'
        elif t == 'impact':
            body = 'z6 ' + n(36, 2)
        elif t == 'pre':
            body = f"{n(c['root'], 2)} {n(c['root'] + 7, 2)} z4"
        elif t == 'decide':
            body = n(c['root'], 8)
        elif t == 'final':
            body = n(c['root'], 8)
        else:
            body = walk(c, i)
    elif voice == 'PN':
        if t == 'burst':
            body = ' '.join(ch(CH[k]['pn'], 2) for k in ('Fm', 'Fd', 'G7', 'Ab'))
        elif t in ('hook', 'hookm', 'groove', 'groovem', 'groovehit', 'motifend'):
            body = f"{ch(c['pn'], 3)} {ch(c['pn'])} z4" if i % 2 == 0 else f"z2 {ch(c['pn'], 2)} z2 {ch(c['pn'], 2)}"
            if t == 'motifend':
                body = ch(c['pn'], 8)
        elif t == 'doubt':
            body = f"z4 {ch(c['pn'], 4)}"
        elif t == 'stop':
            body = 'z8'
        elif t == 'impact':
            body = 'z6 ' + ch([36, 43, 48, 51], 2)
        elif t == 'pre':
            body = f"{ch(c['pn'], 2)} z {ch(c['pn'])} z4"
        else:
            body = ch(c['pn'], 8)
    elif voice == 'MO':
        body = MOTIF if t in ('hookm', 'groovem', 'stop', 'motifend') else 'z8'
    elif voice == 'ST':
        if t in ('doubt', 'stop', 'impact'):
            body = 'z8' if t != 'impact' else 'z6 ' + ch([55, 60, 63], 2)
        elif t == 'burst':
            body = ch(CH['G7']['st'], 8)
        elif t == 'pre':
            body = 'z8'
        elif i + 1 < len(BARS) and BARS[i + 1][0] == 'pre':
            body = ch(c['st'], 6) + ' z2'
        else:
            body = ch(c['st'], 8)
    elif voice == 'TR':
        if t in ('doubt', 'stop'):
            body = ch([79, 80], 8)
        elif t == 'impact':
            body = ch([79, 80], 6) + ' z2'
        else:
            body = 'z8'
    elif voice == 'DR':
        groove = '[=C,,^F,,]2 [^C,,^F,,]2 ^F,,3/^F,,/ [^C,,^F,,]2'
        light = '^F,,2 ^F,,2 ^F,,3/^F,,/ ^F,,2'
        body = {
            'hook': light, 'hookm': light, 'groove': groove, 'groovem': groove,
            'groovehit': '[=C,,^C,]2 [^C,,^F,,]2 ^F,,3/^F,,/ [^C,,^F,,]2',
            'burst': '[=C,,=D,,]2 [=C,,=D,,]2 [=C,,=D,,]2 [=C,,=D,,]2',
            'doubt': 'z8', 'stop': 'z8', 'impact': 'z6 [=C,,^C,]2',
            'pre': '[=C,,^F,,]2 [^C,,^F,,]2 z4', 'decide': '[=C,,^C,]2 z6',
            'soft': light, 'motifend': light, 'final': 'z8',
        }[t]
    return mk + d + body


VOICES = [
    ('BS', 'inst=pizz gain=1.0'),
    ('PN', 'inst=piano gain=0.62'),
    ('MO', 'inst=piano role=melody gain=0.7'),
    ('ST', 'inst=strings gain=0.42'),
    ('TR', 'inst=trem gain=0.3'),
    ('DR', 'inst=drums kit=acoustic gain=0.5'),
]
lines = ['X:1', "T:Jazz d'enquête", 'M:4/4', 'L:1/8', 'Q:1/4=100', 'K:Cm']
for v, attrs in VOICES:
    lines.append(f'V:{v} {attrs}')
    lines.append(' | '.join(bar(i, v) for i in range(len(BARS))) + ' |]')
abc = '\n'.join(lines)

page = PAGE
s = page.read_text(encoding='utf-8')
block = f'<script type="text/vnd.abc" id="om-score">\n{abc}\n</script>'
if '<!--SCORE-->' in s:
    s = s.replace('<!--SCORE-->', block)
elif re.search(r'<script type="text/vnd\.abc" id="om-score">', s):
    s = re.sub(r'<script type="text/vnd\.abc" id="om-score">.*?</script>', lambda m: block, s, flags=re.S)
elif '</body>' in s:
    s = s.replace('</body>', block + '\n</body>', 1)
else:
    sys.exit(f'Impossible de placer la partition dans {page} : ni repère <!--SCORE-->, ni partition existante, ni </body>.')
page.write_text(s, encoding='utf-8')
if block not in page.read_text(encoding='utf-8'):
    sys.exit(f'La partition n\'a pas été écrite dans {page}.')
print(f'{len(BARS)} mesures, {len(VOICES)} voix, écrites dans {page.name}')
