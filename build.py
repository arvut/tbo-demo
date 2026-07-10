#!/usr/bin/env python3
# TBO-demo multilang build: index.html (DE master) + translations .md → de/fr/it/en/ru/ + root redirect.
# Relative ../assets/ so it works both on tbo.arvut.ch (root) and GitHub Pages (/tbo-demo/ subpath).
# RU built but hidden from switcher (reserve, per Alex).
import re, os, shutil, sys, html as _html

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(ROOT, 'index.src.html')      # DE single-file master (source of truth; NOT served)
TRANS = '/Users/al/Downloads/tbo_landing_translations_EN_FR_IT_RU.md'
LANGS = ['de', 'fr', 'it', 'en', 'ru']
VISIBLE = ['de', 'fr', 'it', 'en']               # RU hidden from switcher

# ---- parse translations .md into {LANG: {sec.key: text}} ----
def parse_trans(path):
    out = {}; lang=None; sec=None
    for line in open(path, encoding='utf-8'):
        m = re.match(r'^# (EN|FR|IT|RU)\b', line)
        if m: lang=m.group(1); out.setdefault(lang, {}); continue
        ms = re.match(r'^## \[(\w+)\]', line)
        if ms: sec=ms.group(1); continue
        mk = re.match(r'^- (\w+):\s?(.*)$', line.rstrip('\n'))
        if mk and lang and sec: out[lang][f'{sec}.{mk.group(1)}'] = mk.group(2)
    return out

T = parse_trans(TRANS)   # keys: EN/FR/IT/RU

# ---- markup fragments (exact HTML in DE master) → per-lang HTML ----
# leitsatz zitat text (canon 08.07: «und nicht nur für kleine Unternehmen», verbatim per lang) — span wraps the CFO phrase
LEIT = {
 'fr': ('Un fiduciaire traditionnel est le comptable partagé des PME. Un fiduciaire du réseau Arvut est aussi leur ', 'directeur financier externe', ' — et pas seulement pour les petites entreprises.'),
 'it': ('Un fiduciario tradizionale è il contabile condiviso delle PMI. Un fiduciario della rete Arvut è anche il loro ', 'CFO esterno', ' — e non solo per le piccole imprese.'),
 'en': ('A traditional fiduciary is the shared accountant of SMEs. A fiduciary in the Arvut network is also their ', 'fractional CFO', ' — and not only for small businesses.'),
 'ru': ('Традиционная фидуциария — общий бухгалтер для малого и среднего бизнеса. Фидуциария сети Arvut — ещё и ', 'внешний финансовый директор', ', и не только для малого бизнеса.'),
}
# hero h1: "... — <span>in Echtzeit</span>"  (prefix, span-part)
H1 = {
 'fr': ("Les finances de votre entreprise — ", "en temps réel"),
 'it': ("Le finanze della vostra azienda — ", "in tempo reale"),
 'en': ("Your company's finances — ", "in real time"),
 'ru': ("Финансы вашей компании — ", "в реальном времени"),
}

def markup_map(lang):
    L = lang.upper()
    lt = LEIT[lang]; h1 = H1[lang]
    return {
      # hero h1 (span on last phrase)
      'Die Finanzen Ihres Unternehmens — <span style="color:var(--navy-2);">in Echtzeit</span>':
        f'{h1[0]}<span style="color:var(--navy-2);">{h1[1]}</span>',
      # vergleich h2 (<br>)
      'Ihre Zahlen nur einmal im Jahr?<br>Das gehört der Vergangenheit an.':
        T[L]['vergleich.h2'],
      # col1_li2 (<b>&nbsp;</b>)
      "Vollkosten pro Mitarbeitenden — ab <b style=\"color:var(--ink);\">CHF&nbsp;110'000</b> pro Jahr":
        re.sub(r"CHF 110'000", "<b style=\"color:var(--ink);\">CHF&nbsp;110'000</b>", T[L]['vergleich.col1_li2']),
      # leitsatz (span on CFO phrase)
      'Der klassische Treuhänder ist der geteilte Buchhalter der KMU. Der Treuhänder im Arvut-Netzwerk ist zusätzlich ihr <span style="color:var(--navy-2);">externer CFO</span> — und nicht nur für kleine Unternehmen.':
        f'{lt[0]}<span style="color:var(--navy-2);">{lt[1]}</span>{lt[2]}',
      # preise lead (<b>CHF 110'000</b>)
      "Eine eigene Buchhaltung ist nicht nur der Lohn. Mit Sozialabgaben und Arbeitsplatz kostet ein Buchhalter in Zürich über <b style=\"color:var(--ink);\">CHF 110'000</b> pro Jahr, ein Team mehrere Hunderttausend. Mit TBO erhalten Sie mehr — und zahlen deutlich weniger.":
        re.sub(r"CHF 110'000", "<b style=\"color:var(--ink);\">CHF 110'000</b>", T[L]['preise.lead']),
      # preise fussnote (<b>pilot</b> + <a>link</a>) — link label = cta text
      "Der genaue Preis wird nach einer kurzen Analyse festgelegt — er hängt vom Buchungsvolumen und der Anzahl Gesellschaften ab. Der Einstieg ist über eine dreimonatige Pilotphase zu <b style=\"color:var(--ink);\">CHF 1'000 pro Mandat</b> möglich (bei Fortsetzung anrechenbar). <a href=\"#kontakt\" class=\"link-u\">Offerte anfordern</a>.":
        fussnote_html(L),
      # banner h2 (<br>)
      'Konzentrieren Sie sich auf Ihr Geschäft.<br>Die Zahlen sind unsere Sache.':
        T[L]['banner.h2'],
      # team footer (<b>lead:</b> rest)
      '<b style="color:var(--ink);">Revision aus einem Haus:</b> mit TBO Revision sprechen wir die Sprache geprüfter Zahlen. Besprechungen in Zürich — persönlich oder online, auf Deutsch und Englisch.':
        team_footer_html(L),
      # footer tech desc (<br>)
      'Automatisierung und Buchhaltungsplattform.<br>Daten in der Schweiz gehostet.':
        T[L]['footer.tech_beschreibung'],
    }

def fussnote_html(L):
    t = T[L]['preise.fussnote']
    cta = T[L]['header.cta_header']
    # bold the pilot phrase
    t = re.sub(r"(CHF 1'000 [^.(]+?)( \()", r'<b style="color:var(--ink);">\1</b>\2', t, count=1)
    # strip the [Link: ...] / [Lien : ...] / [Ссылка: ...] placeholder entirely, then append the anchor
    t = re.sub(r'\s*\[[^\]]*\]\s*\.?\s*$', '', t).rstrip('. ').rstrip()
    return f'{t}. <a href="#kontakt" class="link-u">{cta}</a>.'

def team_footer_html(L):
    t = T[L]['team.footer']
    # bold the leading "Audit under one roof:" segment up to first colon
    m = re.match(r'^([^:]+:)\s*(.*)$', t)
    if m: return f'<b style="color:var(--ink);">{m.group(1)}</b> {m.group(2)}'
    return t

# ---- clean text replacements from DE source .md ----
def parse_de(path):
    out={}; sec=None
    for line in open(path, encoding='utf-8'):
        ms=re.match(r'^## \[(\w+)\]', line)
        if ms: sec=ms.group(1); continue
        mk=re.match(r'^- (\w+):\s?(.*)$', line.rstrip('\n'))
        if mk and sec: out[f'{sec}.{mk.group(1)}']=mk.group(2)
    return out
DE = parse_de('/Users/al/Downloads/tbo_landing_text_DE_SOURCE.md')

# keys handled by markup (skip in clean pass)
MARKUP_KEYS = {'hero.h1','vergleich.h2','vergleich.col1_li2','leitsatz.zitat',
 'preise.lead','preise.fussnote','banner.h2','team.footer','footer.tech_beschreibung',
 'footer.claim','footer.Marken','footer.Telefon','footer.Personennamen','meta.title','meta.meta_description'}

def build_lang(lang):
    src = open(SRC, encoding='utf-8').read()
    L = lang.upper()
    # 1) relative assets for subfolder structure
    src = src.replace('src="assets/', 'src="../assets/')
    src = src.replace("@import url('assets/", "@import url('../assets/")
    # 2) inject language switcher CSS + markup into nav
    switch_css = ('.lang-switch{display:flex;align-items:center;gap:9px;margin-left:6px;}'
      '.lang-switch a.lang{font-family:\'Manrope\',sans-serif;font-size:12px;font-weight:700;'
      'letter-spacing:.08em;text-transform:uppercase;color:var(--muted);}'
      '.lang-switch a.lang:hover{color:var(--navy-2);}'
      '.lang-switch a.lang.on{color:var(--navy);}\n</style>')
    src = src.replace('\n</style>', '\n'+switch_css, 1)
    links = ''.join(
      f'<a href="../{lc}/" class="lang{" on" if lc==lang else ""}">{lc.upper()}</a>'
      for lc in VISIBLE)
    switcher = f'<span class="lang-switch">{links}</span>'
    # place switcher right before the header CTA button
    src = src.replace('    <a href="#kontakt" class="btn" style="padding:10px 22px;font-size:.86rem;">Offerte anfordern</a>',
      f'    {switcher}\n    <a href="#kontakt" class="btn" style="padding:10px 22px;font-size:.86rem;">{T[L]["header.cta_header"] if lang!="de" else "Offerte anfordern"}</a>', 1)

    if lang == 'de':
        return finalize(src, 'de')

    # 3) markup replacements (with inline HTML)
    for de_frag, tgt in markup_map(lang).items():
        if de_frag not in src:
            print(f'  ⚠️ [{lang}] markup fragment NOT found: {de_frag[:55]}...')
        src = src.replace(de_frag, tgt)

    # 4) meta/title
    src = src.replace('TBO Treuhand — Buchhaltung und Finanzen in Echtzeit für Zürcher Unternehmen', T[L]['meta.title'])
    de_desc = DE['meta.meta_description']
    src = src.replace(de_desc, T[L]['meta.meta_description'])

    # 5) clean text replacements, longest DE first to avoid substring clobber
    items = [(k, DE[k], T[L].get(k)) for k in DE
             if k not in MARKUP_KEYS and DE[k] and T[L].get(k) and not DE[k].startswith('[')]
    items.sort(key=lambda x: len(x[1]), reverse=True)
    for k, de_t, tg in items:
        if de_t == tg: continue
        if de_t in src:
            src = src.replace(de_t, tg)
        else:
            # short nav-style: try >text< then class-context
            if f'>{de_t}<' in src: src = src.replace(f'>{de_t}<', f'>{tg}<')
            elif f'>{de_t}</a>' in src: src = src.replace(f'>{de_t}</a>', f'>{tg}</a>')
            else: print(f'  ⚠️ [{lang}] clean text not found: {k} = {de_t[:45]}')

    return finalize(src, lang)

def finalize(src, lang):
    src = re.sub(r'<html lang="de">', f'<html lang="{lang}">', src, count=1)
    return src

def teg_count(s):
    return {t: len(re.findall(f'<{t}\\b', s)) for t in ['a','section','svg','img','h1','h2','h3','form','input']}

# ---- build ----
built = {}
for lang in LANGS:
    built[lang] = build_lang(lang)

# tag parity check vs DE
base = teg_count(built['de'])
print('Tag parity (vs DE):')
for lang in LANGS:
    c = teg_count(built[lang])
    ok = c == base
    print(f'  {lang}: {"✓" if ok else "✗ "+str({k:(base[k],c[k]) for k in base if base[k]!=c[k]})}')

# write structure: <lang>/index.html + root redirect + keep assets/
for lang in LANGS:
    d = os.path.join(ROOT, lang); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(built[lang])

# root redirect index.html (works on domain root AND Pages subpath — relative de/)
redirect = ('<!doctype html><html lang="de"><head><meta charset="utf-8">'
  '<meta name="robots" content="noindex,nofollow">'
  '<link rel="canonical" href="de/"><meta http-equiv="refresh" content="0; url=de/">'
  '<script>location.replace("de/"+location.hash)</script>'
  '<title>TBO Treuhand AG</title></head>'
  '<body style="font-family:sans-serif;padding:2rem">Weiter zu <a href="de/">TBO Treuhand</a>…</body></html>')
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(redirect)

print('\n✓ Build done: de/ fr/ it/ en/ ru/ + root redirect. Assets shared at ../assets/.')
