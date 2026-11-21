#!/usr/bin/env python3
"""Genera le pagine dei dipartimenti con la cornice del mockup (barra, menu, piè di pagina).
Uso:  python3 tools/build_department.py /percorso/waqfe-nau
Legge  <waqfe-nau>/wordpress/waqfe-nau-embed.html  e  <waqfe-nau>/assets/theme-jamaat.css
e scrive dipartimenti/waqf-e-nau.html. Rilanciare dopo ogni modifica del sito Waqf-e-Nau."""
import re, sys, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
wn = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else root.parent / 'waqfe-nau')
mock = (root / 'index.html').read_text(encoding='utf-8')
embed = (wn / 'wordpress' / 'waqfe-nau-embed.html').read_text(encoding='utf-8')
theme = re.sub(r'@import url\([^)]*\);', '', (wn / 'assets' / 'theme-jamaat.css').read_text(encoding='utf-8'))

style = re.search(r'<style>(.*?)</style>', mock, re.S).group(1)
style = style.replace('url(pattern.svg)', 'url(../pattern.svg)').replace('url(img/', 'url(../img/')
body = mock.split('<body>')[1]
top_header = re.search(r'(<div class="top">.*?</header>)', body, re.S).group(1)
footer = re.search(r'(<footer.*?</footer>)', body, re.S).group(1)
for a, b in (('href="dipartimenti/', 'href="'), ):
    top_header = top_header.replace(a, b); footer = footer.replace(a, b)
top_header = top_header.replace('href="#" class="brand"', 'href="../index.html" class="brand"')

overrides = '''/* neutralizza le regole del mockup che hanno gli stessi nomi di classe (.hero .card .note) */
.wn .hero{min-height:0;display:grid;background:none;align-items:center}
.wn .card{display:block;text-decoration:none;color:inherit}
.wn .card p{margin:0 0 .6em;font-size:inherit;color:inherit}
.wn .note{text-align:start;color:inherit;font-size:inherit;border-bottom:0}
.wn{margin-bottom:60px}'''
wn_html = embed
wn_html = re.sub(r'<style>\s*@import url\([^)]*\);', '<style>', wn_html, count=1)   # un solo import di font
page = f'''<!doctype html>
<html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Waqf-e-Nau – Dipartimenti – alislam.it (bozza)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Noto+Nastaliq+Urdu:wght@400;600&family=Source+Sans+3:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>{style}
.crumbs{{max-width:980px;margin:0 auto;padding:18px 16px 0;font-size:15px;color:#6f5620}}.crumbs a{{text-decoration:none}}
</style>
</head><body>
<div class="note">Bozza di design per revisione – non è il sito pubblicato.</div>
{top_header}
<div class="crumbs"><a href="../index.html">Home</a> › <a href="index.html">Dipartimenti</a> › Waqf-e-Nau</div>
{wn_html}
<style>{theme}
{overrides}</style>
{footer}
</body></html>'''
(root / 'dipartimenti').mkdir(exist_ok=True)
(root / 'dipartimenti' / 'waqf-e-nau.html').write_text(page, encoding='utf-8')
print('scritto dipartimenti/waqf-e-nau.html', len(page), 'byte')
