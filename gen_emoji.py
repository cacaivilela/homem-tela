#!/usr/bin/env python3
"""Gera os sprites pixel-art emoji (24x24) e injeta em app.html entre /*EMOJI-START*/ e /*EMOJI-END*/.
Paleta: . vazio  Y amarelo  K buraco(apagado)  R vermelho  D vermelho-escuro  W branco
        V roxo  B azul  P rosa  G verde  O laranja  C ciano
Uso: python3 gen_emoji.py
"""
import json, re, math

N = 24
def blank(w=N, h=N): return [['.'] * w for _ in range(h)]

def disc(sp, cor='Y', cx=12, cy=12, r=11.5):
    for y in range(len(sp)):
        for x in range(len(sp[0])):
            if (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r:
                sp[y][x] = cor

def px(sp, cells, cor):
    for x, y in cells:
        if 0 <= y < len(sp) and 0 <= x < len(sp[0]): sp[y][x] = cor

def hline(sp, x0, x1, y, cor): px(sp, [(x, y) for x in range(x0, x1 + 1)], cor)

def paste(sp, patch, x0, y0):
    for r, row in enumerate(patch):
        for c, ch in enumerate(row):
            if ch != '.': sp[y0 + r][x0 + c] = ch

def s(sp): return [''.join(r) for r in sp]

# ---------- peças reutilizáveis ----------
OLHO_ARCO_L = ["..KKK.", ".K...K"]          # olho fechado de riso  ^  (6x2)
OLHO_ARCO_R = OLHO_ARCO_L
OLHO_ABERTO = ["KK", "KK", "KK"]             # 2x3
OLHO_PISCA  = ["..", "..", "KK"]             # linha fechada
CORACAO = [".##.##.", "#######", "#######", ".#####.", "..###..", "...#..."]

# boca: patches 14x7 ancorados em (5,13); fundo é preenchido com a cor do rosto
def boca_fechada(f):
    p = [[f] * 14 for _ in range(7)]
    px(p, [(0, 1), (13, 1), (1, 2), (12, 2)], 'K'); hline(p, 2, 11, 3, 'K'); return s(p)
def boca_pequena(f):
    p = [[f] * 14 for _ in range(7)]
    hline(p, 2, 11, 1, 'K'); px(p, [(1, 2), (12, 2)], 'K'); hline(p, 2, 11, 2, 'R')
    px(p, [(2, 3), (3, 3), (10, 3), (11, 3)], 'K'); hline(p, 4, 9, 3, 'R'); hline(p, 4, 9, 4, 'K'); return s(p)
def boca_grande(f):
    p = [[f] * 14 for _ in range(7)]
    hline(p, 1, 12, 0, 'K')
    px(p, [(0, 1), (13, 1)], 'K'); hline(p, 1, 12, 1, 'W')
    for y in (2, 3): px(p, [(0, y), (13, y)], 'K'); hline(p, 1, 12, y, 'R')
    px(p, [(1, 4), (12, 4)], 'K'); hline(p, 2, 11, 4, 'R')
    px(p, [(2, 5), (3, 5), (10, 5), (11, 5)], 'K'); hline(p, 4, 9, 5, 'R')
    hline(p, 4, 9, 6, 'K'); return s(p)
def boca_frown(f):
    p = [[f] * 14 for _ in range(7)]
    hline(p, 4, 9, 2, 'K'); px(p, [(2, 3), (3, 3), (10, 3), (11, 3), (1, 4), (12, 4)], 'K'); return s(p)

def frames(f): return [boca_fechada(f), boca_pequena(f), boca_grande(f)]
def crop(sp, x, y, w, h): return [''.join(sp[r][x:x + w]) for r in range(y, y + h)]
def cp(sp): return [row[:] for row in sp]

EMOJI = {}

# ---------- Rindo ----------
sp = blank(); disc(sp)
paste(sp, OLHO_ARCO_L, 4, 7); paste(sp, OLHO_ARCO_R, 14, 7)
paste(sp, boca_grande('Y'), 5, 13)
EMOJI['rindo'] = dict(nome='Rindo', fundo='Y', sprite=s(sp), boca=[5, 13], frames=frames('Y'), piscar=False)

# ---------- Apaixonado ----------
sp = blank(); disc(sp)
paste(sp, CORACAO, 3, 6); paste(sp, CORACAO, 14, 6)
for y in range(6, 12):
    for x in range(24):
        if sp[y][x] == '#': sp[y][x] = 'R'
paste(sp, boca_pequena('Y'), 5, 13)
px(sp, [(2, 12), (3, 12), (20, 12), (21, 12)], 'P')  # blush
EMOJI['apaixonado2'] = dict(nome='Apaixonado emoji', fundo='Y', sprite=s(sp), boca=[5, 13], frames=frames('Y'), piscar=False)

# ---------- Bravo (vermelho) ----------
sp = blank(); disc(sp, 'D')
px(sp, [(4, 6), (5, 6), (6, 7), (7, 7), (8, 8), (9, 8)], 'K')
px(sp, [(14, 8), (15, 8), (16, 7), (17, 7), (18, 6), (19, 6)], 'K')
paste(sp, OLHO_ABERTO, 6, 9); paste(sp, OLHO_ABERTO, 16, 9)
paste(sp, boca_frown('D'), 5, 13)
# marca de raiva (canto sup. direito, fora do disco)
px(sp, [(20, 0), (23, 0), (21, 1), (22, 1), (21, 2), (22, 2), (20, 3), (23, 3)], 'W')
EMOJI['bravo2'] = dict(nome='Furioso', fundo='D', sprite=s(sp), boca=[5, 13],
                       frames=[boca_frown('D'), boca_pequena('D'), boca_grande('D')],
                       piscar=True, olhos=[[6, 9], [16, 9]])

# ---------- Festa ---------- (24x29: 5 linhas extras no topo para o chapéu)
T = 5
sp = blank(24, 24 + T); disc(sp, 'Y', cx=12, cy=12 + T)
paste(sp, OLHO_ARCO_L, 4, 7 + T); paste(sp, OLHO_ARCO_R, 14, 7 + T)
paste(sp, boca_pequena('Y'), 5, 13 + T)
# chapéu inclinado para a esquerda, acima do rosto (encosta na borda do disco)
px(sp, [(5, 0)], 'R')
hat = [(1, 5, 5, 'V'), (2, 5, 6, 'V'), (3, 4, 6, 'W'), (4, 4, 7, 'W'), (5, 4, 8, 'V'), (6, 3, 8, 'V'), (7, 3, 9, 'W'), (8, 3, 9, 'W')]
for y, x0, x1, c in hat: hline(sp, x0, x1, y, c)
# língua-de-sogra animada (3 quadros recortados do sprite: encolhida, média, esticada)
def lingua24(sp, n):
    q = cp(sp); y = 15 + T
    if n == 0:
        px(q, [(18, y), (18, y + 1), (18, y + 2)], 'R'); px(q, [(19, y + 1)], 'W')
    elif n == 1:
        hline(q, 18, 19, y, 'R'); px(q, [(20, y)], 'W'); hline(q, 17, 18, y + 1, 'R'); hline(q, 19, 20, y + 1, 'W'); px(q, [(21, y + 1)], 'R'); hline(q, 18, 19, y + 2, 'R'); px(q, [(20, y + 2)], 'W')
    else:
        hline(q, 18, 19, y, 'R'); hline(q, 20, 21, y, 'W'); hline(q, 22, 23, y, 'R')
        hline(q, 17, 18, y + 1, 'R'); hline(q, 19, 20, y + 1, 'W'); hline(q, 21, 22, y + 1, 'R'); px(q, [(23, y + 1)], 'W')
        hline(q, 18, 19, y + 2, 'R'); hline(q, 20, 21, y + 2, 'W'); hline(q, 22, 23, y + 2, 'R')
    return crop(q, 17, y, 7, 3)
LING24 = [lingua24(sp, i) for i in range(3)]
EMOJI['festa'] = dict(nome='Festa', fundo='Y', sprite=s(sp), boca=[5, 13 + T], frames=frames('Y'), piscar=False,
                      anim=dict(x=17, y=15 + T, frames=LING24, seq=[0, 1, 2, 2, 1], ms=160),
                      confete=[[14, 1, 'B'], [17, 3, 'G'], [11, 0, 'R'], [22, 1, 'P'], [20, 4, 'B'], [23, 6, 'G'], [0, 5, 'R'], [1, 24, 'B'], [0, 21, 'G'], [21, 28, 'P'], [23, 25, 'B'], [2, 27, 'R'], [9, 2, 'P']])

# ================= estilo 16x16 (meio-termo, sem contorno) =================
def disc16(sp, cor='Y', cx=8, cy=8): disc(sp, cor, cx, cy, 7.5)
ARCO16 = [".KKK.", "K...K"]   # olho fechado de riso: arco ∩ 5x2
CORACAO16 = [".R.R.", "RRRRR", ".RRR.", "..R.."]
def b16_fechada(f):
    p = [[f] * 12 for _ in range(4)]; px(p, [(1, 1), (10, 1)], 'K'); hline(p, 2, 9, 2, 'K'); return s(p)
def b16_pequena(f):
    p = [[f] * 12 for _ in range(4)]; hline(p, 2, 9, 0, 'K'); px(p, [(1, 1), (10, 1)], 'K'); hline(p, 2, 9, 1, 'R'); hline(p, 2, 9, 2, 'K'); return s(p)
def b16_grande(f):
    p = [[f] * 12 for _ in range(4)]; hline(p, 1, 10, 0, 'K'); px(p, [(0, 1), (11, 1)], 'K'); hline(p, 1, 10, 1, 'W'); px(p, [(1, 2), (10, 2)], 'K'); hline(p, 2, 9, 2, 'R'); hline(p, 2, 9, 3, 'K'); return s(p)
def b16_frown(f):
    p = [[f] * 12 for _ in range(4)]; hline(p, 4, 7, 1, 'K'); px(p, [(3, 2), (8, 2)], 'K'); return s(p)
def frames16(f): return [b16_fechada(f), b16_pequena(f), b16_grande(f)]

# Rindo (com lágrimas)
sp = blank(16, 16); disc16(sp)
paste(sp, ARCO16, 2, 4); paste(sp, ARCO16, 9, 4)
paste(sp, b16_grande('Y'), 2, 9)
px(sp, [(1, 6), (1, 7), (14, 6), (14, 7)], 'B')
EMOJI['rindo16'] = dict(nome='Rindo 16', fundo='Y', sprite=s(sp), boca=[2, 9], frames=frames16('Y'), piscar=False)

# Apaixonado
sp = blank(16, 16); disc16(sp)
paste(sp, CORACAO16, 2, 3); paste(sp, CORACAO16, 9, 3)
paste(sp, b16_pequena('Y'), 2, 9)
EMOJI['apaixonado16'] = dict(nome='Apaixonado 16', fundo='Y', sprite=s(sp), boca=[2, 9], frames=frames16('Y'), piscar=False)

# Furioso
sp = blank(16, 16); disc16(sp, 'D')
px(sp, [(3, 3), (4, 3), (5, 4), (10, 4), (11, 3), (12, 3)], 'K')
px(sp, [(4, 6), (5, 6), (4, 7), (5, 7), (10, 6), (11, 6), (10, 7), (11, 7)], 'K')
paste(sp, b16_frown('D'), 2, 9)
px(sp, [(13, 0), (15, 0), (14, 1), (13, 2), (15, 2)], 'W')
EMOJI['bravo16'] = dict(nome='Furioso 16', fundo='D', sprite=s(sp), boca=[2, 9],
                        frames=[b16_frown('D'), b16_pequena('D'), b16_grande('D')], piscar=True, olhos=[[4, 5], [10, 5]])

# Festa (16x20, chapéu acima)
T = 4
sp = blank(16, 16 + T); disc16(sp, 'Y', 8, 8 + T)
paste(sp, ARCO16, 2, 4 + T); paste(sp, ARCO16, 9, 4 + T)
paste(sp, b16_pequena('Y'), 2, 9 + T)
px(sp, [(3, 0)], 'R'); hline(sp, 3, 3, 1, 'V'); hline(sp, 2, 4, 2, 'W'); hline(sp, 2, 4, 3, 'V'); hline(sp, 1, 5, 4, 'V')
def lingua16(sp, n):
    q = cp(sp); y = 10 + T
    if n == 0: px(q, [(12, y), (12, y + 1)], 'R')
    elif n == 1: hline(q, 12, 12, y, 'R'); px(q, [(13, y)], 'W'); hline(q, 12, 13, y + 1, 'R'); px(q, [(14, y + 1)], 'W')
    else: hline(q, 12, 13, y, 'R'); hline(q, 14, 15, y, 'W'); px(q, [(12, y + 1)], 'R'); hline(q, 13, 14, y + 1, 'W'); px(q, [(15, y + 1)], 'R')
    return crop(q, 12, y, 4, 2)
LING16 = [lingua16(sp, i) for i in range(3)]
EMOJI['festa16'] = dict(nome='Festa 16', fundo='Y', sprite=s(sp), boca=[2, 9 + T], frames=frames16('Y'), piscar=False,
                        anim=dict(x=12, y=10 + T, frames=LING16, seq=[0, 1, 2, 2, 1], ms=160),
                        confete=[[9, 0, 'B'], [12, 2, 'G'], [7, 1, 'P'], [0, 8, 'R'], [15, 6, 'B'], [0, 17, 'G'], [15, 18, 'P'], [1, 3, 'B']])

# ---------- injeta ----------
p = 'app.html'
src = open(p).read()
js = 'const EMOJI=' + json.dumps(EMOJI, ensure_ascii=False, separators=(',', ':')) + ';'
new = re.sub(r'/\*EMOJI-START\*/.*?/\*EMOJI-END\*/', '/*EMOJI-START*/' + js + '/*EMOJI-END*/', src, flags=re.S)
assert new != src or js in src, 'marcadores /*EMOJI-START*/ … /*EMOJI-END*/ não encontrados'
open(p, 'w').write(new)
for k, v in EMOJI.items():
    print(k); print('\n'.join(v['sprite'])); print()
