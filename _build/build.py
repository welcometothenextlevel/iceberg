#!/usr/bin/env python3
"""Generates docs/ for the Iceberg Sàrl site. Run: python3 _build/build.py"""
import json, pathlib, html
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs"
V = "8"                                  # bump to bust the CSS/JS cache
BASE = "https://welcometothenextlevel.github.io/iceberg/"
NOINDEX = True                           # flip to False once live on iceberg-sarl.ch

TEL, TEL_D = "+41216261111", "021 626 11 11"
URG, URG_D = "+41797261111", "079 726 11 11"
WA = "41797261111"                       # TODO-CONFIRM: is WhatsApp active on this mobile?
MAIL = "info@iceberg-sarl.ch"
IG = "https://www.instagram.com/iceberg.sarl/"
MAPS = "https://www.google.com/maps/search/?api=1&query=Chemin+du+Bois-de-Vaux+1%2C+1007+Lausanne"

I = {
 "phone": '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2.2 2A17 17 0 0 1 3 5.200 2 2 0 0 1 5 3Z"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "doc": '<path d="M7 3h7l5 5v13H7zM14 3v5h5M10 13h6M10 17h4"/>',
 "pin": '<path d="M12 21s7-6.200 7-11.500A7 7 0 0 0 5 9.500C5 14.800 12 21 12 21Z"/><circle cx="12" cy="9.500" r="2.500"/>',
 "mail": '<path d="M3 6h18v12H3zM3 7l9 7 9-7"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.500 2"/>',
 "close": '<path d="M6 6l12 12M18 6 6 18"/>',
 "left": '<path d="M15 5l-7 7 7 7"/>', "right": '<path d="m9 5 7 7-7 7"/>',
 "menu": '<path d="M4 8h16M4 16h16"/>', "play": '<path d="M8 5.500v13l11-6.500z" fill="currentColor"/>',
 "layers": '<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M4 16V6a2 2 0 0 1 2-2h10"/>',
 "snow": '<path d="M12 2v20M3.300 7l17.400 10M20.700 7 3.300 17M12 6 9.500 4M12 6l2.500-2M12 18l-2.500 2M12 18l2.500 2"/>',
 "check": '<path d="m5 12.500 4.500 4.500L19 7.500"/>',
 "ig": '<rect x="3.500" y="3.500" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17" cy="7" r=".8" fill="currentColor"/>',
}
def ic(n): return f'<svg class="ic" viewBox="0 0 24 24" aria-hidden="true">{I[n]}</svg>'
WAI = '<svg class="ic wa-ic" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" stroke="none" d="M12 2a10 10 0 0 0-8.600 15L2 22l5.200-1.400A10 10 0 1 0 12 2Zm0 18.200a8.200 8.200 0 0 1-4.200-1.200l-.3-.2-3.100.8.800-3-.2-.3A8.200 8.200 0 1 1 12 20.200Zm4.500-6.100c-.2-.1-1.500-.7-1.700-.8-.2-.1-.4-.1-.6.100l-.8 1c-.1.200-.3.200-.5.100a6.700 6.700 0 0 1-3.300-2.900c-.3-.4.300-.4.700-1.300.1-.2 0-.3 0-.5l-.8-1.800c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.5.100-.7.300-.3.300-.9.900-.9 2.200s.9 2.500 1.100 2.700c.1.200 1.800 2.800 4.400 3.900 1.600.7 2.300.700 3.100.6.500-.1 1.500-.6 1.700-1.200.2-.6.2-1.100.2-1.200-.1-.2-.3-.2-.6-.4Z"/></svg>'
def img(n, alt, w, h, cls="", lazy=True, extra=""):
    return f'<img src="assets/img/{n}.webp" alt="{html.escape(alt)}" width="{w}" height="{h}"{" loading=lazy" if lazy else ""} decoding="async"{f" class={chr(34)}{cls}{chr(34)}" if cls else ""} {extra}>'
from urllib.parse import quote
def wa(t): return f"https://wa.me/{WA}?text={quote(t)}"

NAV = [("climatisation.html","Climatisation"),("caves-a-vin.html","Caves à vin"),("froid-commercial.html","Froid commercial"),("locaux-informatiques.html","Locaux informatiques"),("depannage.html","Dépannage"),("index.html#realisations","Réalisations")]

def page(fn, title, desc, body, cls="", crumbs=None):
    ld = [{"@context":"https://schema.org","@type":"HVACBusiness","@id":BASE+"#entreprise","name":"Iceberg Sàrl","url":BASE,"telephone":TEL,"email":MAIL,
      "image":BASE+"assets/img/og.jpg","logo":BASE+"assets/img/logo.svg",
      "address":{"@type":"PostalAddress","streetAddress":"Chemin du Bois-de-Vaux 1","postalCode":"1007","addressLocality":"Lausanne","addressRegion":"VD","addressCountry":"CH"},
      "areaServed":["Lausanne","Suisse romande","Arc lémanique"],"sameAs":[IG],
      "openingHoursSpecification":[
        {"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday"],"opens":"07:30","closes":"12:00"},
        {"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday"],"opens":"13:30","closes":"18:00"},
        {"@type":"OpeningHoursSpecification","dayOfWeek":"Friday","opens":"07:30","closes":"12:00"},
        {"@type":"OpeningHoursSpecification","dayOfWeek":"Friday","opens":"13:30","closes":"16:30"}],
      "contactPoint":{"@type":"ContactPoint","telephone":URG,"contactType":"Dépannage 24h/24, 7j/7","availableLanguage":"fr"}}]
    if crumbs:
        ld.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Accueil","item":BASE},{"@type":"ListItem","position":2,"name":crumbs,"item":BASE+fn.replace(".html","")}]})
    nav = "".join(f'<a href="{u}"{" aria-current=page" if u==fn else ""}>{t}</a>' for u,t in NAV)
    hero = fn=="index.html"
    doc = f'''<!doctype html>
<html lang="fr-CH" class="no-js">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title><meta name="description" content="{html.escape(desc)}">
{'<meta name="robots" content="noindex">' if NOINDEX else ''}
<link rel="canonical" href="{BASE}{'' if hero else fn.replace('.html','')}">
<meta property="og:type" content="website"><meta property="og:locale" content="fr_CH"><meta property="og:title" content="{title}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:image" content="{BASE}assets/img/og.jpg"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0b2a66"><link rel="icon" href="assets/img/mark.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/albert.woff2" as="font" type="font/woff2" crossorigin>
{'<link rel="preload" as="image" href="assets/img/iceberg-m.webp" media="(max-width:800px)"><link rel="preload" as="image" href="assets/img/iceberg.webp" media="(min-width:801px)">' if hero else ''}
<script>document.documentElement.className='js'</script>
<link rel="stylesheet" href="assets/site.css?v={V}">
<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>
</head>
<body class="{cls}">
<a class="skip" href="#contenu">Aller au contenu</a>
<header class="top" id="top">
 <div class="top-in">
  <a class="brand" href="index.html" aria-label="Iceberg Sàrl, accueil"><img class="lg-w" src="assets/img/logo-white-nav.svg" alt="" width="740" height="238"><img class="lg-c" src="assets/img/logo-nav.svg" alt="Iceberg Sàrl" width="740" height="238"></a>
  <nav class="nav" aria-label="Navigation principale">{nav}</nav>
  <div class="top-cta">
   <a class="tel" href="tel:{TEL}">{ic('phone')}<span><b>{TEL_D}</b><i data-status>Dépannage 24h/24</i></span></a>
   <a class="btn btn-c" href="{'#devis' if hero else 'index.html#devis'}" data-devis>Demander un devis</a>
   <button class="burger" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="menu">{ic('menu')}</button>
  </div>
 </div>
</header>
<div class="menu" id="menu" inert><div class="menu-top"><img src="assets/img/logo-white-nav.svg" alt="Iceberg Sàrl" width="740" height="238"><button class="menu-x" aria-label="Fermer le menu">{ic('close')}</button></div><nav>{nav}<a href="index.html#contact">Contact</a></nav><div class="menu-cta"><a class="btn btn-w" href="tel:{TEL}">{ic('phone')}{TEL_D}</a><a class="btn btn-g" href="{wa('Bonjour Iceberg, ')}" target="_blank" rel="noopener">{WAI}WhatsApp</a></div></div>
<main id="contenu">{body}</main>
<footer class="foot">
 <div class="wrap foot-in">
  <div><img src="assets/img/logo-white.svg" alt="Iceberg Sàrl, Coolers and Heaters Solutions" width="740" height="324" loading="lazy"><p>Climatisation, chambres froides et caves à vin sur mesure. Lausanne, Suisse romande et arc lémanique.</p><a class="foot-ig" href="{IG}" target="_blank" rel="noopener" aria-label="Instagram @iceberg.sarl">{ic('ig')}@iceberg.sarl</a></div>
  <div><h2>Nous appeler</h2><p><a href="tel:{TEL}">{TEL_D}</a><br>Dépannage 24h/24, 7j/7<br><a href="tel:{URG}">{URG_D}</a><br><a href="mailto:{MAIL}">{MAIL}</a></p></div>
  <div><h2>Horaires</h2><p>Lundi à jeudi<br>07h30 – 12h00, 13h30 – 18h00<br>Vendredi<br>07h30 – 12h00, 13h30 – 16h30</p></div>
  <div><h2>Services</h2><p>{"<br>".join(f'<a href="{u}">{t}</a>' for u,t in NAV[:5])}</p></div>
 </div>
 <div class="wrap foot-b"><span>© <span data-year>2026</span> Iceberg Sàrl, Chemin du Bois-de-Vaux 1, 1007 Lausanne</span><a href="confidentialite.html">Protection des données</a></div>
</footer>
<div class="bar" aria-label="Contact rapide"><a href="tel:{TEL}" class="bar-c">{ic('phone')}<span>Appeler</span></a><a href="{wa('Bonjour Iceberg, ')}" class="bar-w" target="_blank" rel="noopener">{WAI}<span>WhatsApp</span></a><a href="{'#devis' if hero else 'index.html#devis'}" class="bar-d" data-devis>{ic('doc')}<span>Devis</span></a></div>
<div class="side"><a href="tel:{URG}" class="side-u">{ic('snow')}<span>Panne ? <b>{URG_D}</b></span></a></div>
<div class="wa" id="wa">
 <div class="wa-box" role="dialog" aria-label="Écrire à Iceberg sur WhatsApp" inert>
  <div class="wa-h"><img src="assets/img/mark.svg" alt="" width="42" height="42"><div><b>Iceberg Sàrl</b><span data-status>Dépannage 24h/24</span></div><button aria-label="Fermer">{ic('close')}</button></div>
  <div class="wa-b"><p>Bonjour. De quoi avez-vous besoin ?</p>
   <a target="_blank" rel="noopener" href="{wa('Bonjour Iceberg, j’ai une panne à signaler : ')}">J’ai une panne</a>
   <a target="_blank" rel="noopener" href="{wa('Bonjour Iceberg, je souhaite un devis pour une climatisation. Lieu : ')}">Devis climatisation</a>
   <a target="_blank" rel="noopener" href="{wa('Bonjour Iceberg, j’ai un projet de cave à vin sur mesure. Lieu : ')}">Projet de cave à vin</a>
   <a target="_blank" rel="noopener" href="{wa('Bonjour Iceberg, je souhaite un devis pour une chambre froide. Lieu : ')}">Chambre froide ou congélation</a>
   <a target="_blank" rel="noopener" href="{wa('Bonjour Iceberg, ')}">Autre question</a></div>
 </div>
 <button class="wa-fab" aria-label="Ouvrir WhatsApp" aria-expanded="false">{WAI}</button>
</div>
<script src="assets/vendor/gsap.min.js" defer></script><script src="assets/vendor/ScrollTrigger.min.js" defer></script><script src="assets/site.js?v={V}" defer></script>
</body></html>'''
    (OUT/fn).write_text(doc, encoding="utf-8")

# ---------------------------------------------------------------- shared blocks
BRANDS = ["daikin","mitsubishi","panasonic","fujitsu","toshiba","hitachi","lg","samsung","haier","aermec","airwell","danfoss","siemens","sanyo","delonghi","whirlpool"]
from PIL import Image
def brands():
    o=""
    for b in BRANDS:
        w,h=Image.open(OUT/f"assets/img/m-{b}.webp").size
        o+=f'<li><img src="assets/img/m-{b}.webp" alt="{b.capitalize() if b!="lg" else "LG"}" width="{w}" height="{h}" loading="lazy"></li>'
    return f'<section class="brands"><div class="wrap"><h2>Nous vendons, installons et réparons les grandes marques.</h2><ul>{o}</ul></div></section>'

def urgent():
    return f'''<section class="urg"><div class="wrap urg-in">
 <div class="urg-t" data-r><h2>Une panne de froid n’attend pas lundi.</h2><p>Chambre froide qui remonte, climatisation à l’arrêt, salle serveurs qui chauffe : un technicien Iceberg vous répond 24 heures sur 24, 7 jours sur 7.</p>
 <a class="urg-n" href="tel:{URG}"><span>Dépannage 24h/24</span><b>{URG_D}</b></a>
 <div class="row"><a class="btn btn-w" href="tel:{URG}">{ic('phone')}Appeler maintenant</a><a class="btn btn-g" href="{wa('Bonjour Iceberg, j’ai une panne à signaler : ')}" target="_blank" rel="noopener">{WAI}Envoyer une photo</a></div></div>
 <div class="urg-v" data-drive>{img('van-17','Le véhicule Iceberg Sàrl, vu de l’arrière',720,533)}{img('van-5','Le véhicule Iceberg Sàrl et sa nouvelle identité',720,533)}</div>
</div></section>'''

def form(default=""):
    def chips(name, opts, req=True):
        return "".join(f'<label class="chip"><input type="radio" name="{name}" value="{o}"{" required" if req and i==0 else ""}{" checked" if o==default else ""}><span>{o}</span></label>' for i,o in enumerate(opts))
    return f'''<section class="devis" id="devis"><div class="wrap devis-in">
 <div class="devis-l" data-r><h2>Votre devis, en une minute.</h2><p>Quatre réponses nous suffisent pour vous rappeler avec les bonnes questions. Chaque devis est personnalisé selon les exigences thermiques du lieu.</p>
  <ul class="ticks"><li>{ic('check')}Réponse directe d’un frigoriste</li><li>{ic('check')}Vente, installation, réparation et SAV</li><li>{ic('check')}Lausanne, Suisse romande et arc lémanique</li></ul>
  <a class="bigtel" href="tel:{TEL}">{ic('phone')}<span>Plus simple de vive voix ?<b>{TEL_D}</b></span></a></div>
 <form class="wiz" id="wiz" novalidate>
  <div class="wiz-p" aria-hidden="true"><i></i></div>
  <fieldset class="st on"><legend>Quel est votre besoin ?</legend><div class="chips">{chips('Besoin',['Climatisation','Pompe à chaleur','Cave à vin','Chambre froide','Congélation','Local informatique','Réparation','Entretien'])}</div></fieldset>
  <fieldset class="st"><legend>Pour quel type de lieu ?</legend><div class="chips">{chips('Lieu',['Villa ou appartement','Bureaux','Restaurant ou hôtel','Commerce','Industrie','Autre'])}</div></fieldset>
  <fieldset class="st"><legend>Où et pour quand ?</legend><label class="f">Localité ou NPA<input name="Localité" autocomplete="postal-code" required placeholder="1007 Lausanne"></label><div class="chips">{chips('Délai',['Urgent','Ce mois-ci','Dans les 3 mois','Je me renseigne'])}</div></fieldset>
  <fieldset class="st"><legend>Comment vous joindre ?</legend><div class="two"><label class="f">Nom<input name="Nom" autocomplete="name" required></label><label class="f">Téléphone<input name="Téléphone" type="tel" inputmode="tel" autocomplete="tel" required></label></div><label class="f">Précisions (facultatif)<textarea name="Précisions" rows="3" placeholder="Surface, nombre de pièces, marque de l’appareil…"></textarea></label>
   <div class="send"><button type="button" class="btn btn-g" data-send="wa">{WAI}Envoyer sur WhatsApp</button><button type="button" class="btn btn-i" data-send="mail">{ic('mail')}Envoyer par e-mail</button></div><p class="fine">Votre message s’ouvre prêt à envoyer. Rien n’est enregistré sur ce site.</p></fieldset>
  <p class="err" role="alert" hidden></p>
  <div class="wiz-n"><button type="button" class="back" hidden>{ic('left')}Retour</button><button type="button" class="btn btn-c next">Continuer{ic('arrow')}</button></div>
 </form>
</div></section>'''

def faq(items):
    return '<section class="faq"><div class="wrap faq-in"><h2 data-r>Questions fréquentes</h2><div>'+"".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in items)+'</div></div></section>'

def contact():
    return f'''<section class="contact" id="contact"><div class="wrap contact-in"><div data-r><h2>Passez nous voir à Bois-de-Vaux.</h2>
 <dl><div><dt>{ic('pin')}Adresse</dt><dd>Chemin du Bois-de-Vaux 1<br>1007 Lausanne<br><a class="lnk" href="{MAPS}" target="_blank" rel="noopener">Itinéraire{ic('arrow')}</a></dd></div>
 <div><dt>{ic('phone')}Téléphone</dt><dd><a href="tel:{TEL}">{TEL_D}</a><br><a href="mailto:{MAIL}">{MAIL}</a></dd></div>
 <div><dt>{ic('clock')}Horaires</dt><dd>Lun – jeu 07h30 – 12h00, 13h30 – 18h00<br>Vendredi 07h30 – 12h00, 13h30 – 16h30<br><strong data-status></strong></dd></div></dl></div>
 <div class="map"><iframe title="Iceberg Sàrl sur la carte" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=Chemin+du+Bois-de-Vaux+1,+1007+Lausanne&z=15&hl=fr&output=embed"></iframe></div></div></section>'''

# ---------------------------------------------------------------- home
STOPS = [
 ("+23","Confort","Climatisation et pompe à chaleur","Split, multisplit ou mobile : un appareil réversible rafraîchit l’été et chauffe l’hiver. Filtres à charbon actif, antibactériens, lampes UV ou ionisation rendent l’air plus sain.","climatisation.html","salon","Salon au bord de l’eau équipé d’une climatisation murale","Climatisation"),
 ("+20","Locaux informatiques","Serveurs, bureaux, téléphonie","Freecooling et froid mécanique combinés, close control : vos machines restent à température constante, avec une consommation réduite.","locaux-informatiques.html","serveurs","Baies de serveurs dans un local informatique","Local informatique"),
 ("+12","Cave à vin","Caves et carnotzets sur mesure","Une température stable, une hygrométrie maîtrisée et un agencement pensé autour de vos bouteilles.","caves-a-vin.html","cave-22_5","Cave à vin sur mesure réalisée par Iceberg Sàrl","Cave à vin"),
 ("+3","Chambre froide","Froid commercial","Restaurants, traiteurs, commerces : chambres froides, garde-mangers et frigos professionnels, de la conception à l’entretien.","froid-commercial.html","cuisine","Cuisine professionnelle en inox","Chambre froide"),
 ("−20","Congélation","Froid négatif","Chambres de congélation et meubles négatifs, installés, entretenus et dépannés jour et nuit.","froid-commercial.html","congelation","Armoires de congélation professionnelles","Congélation"),
]
POSTS = [
 dict(id="De-K2QBMTwr", kind="reel", src="reel-cave", date="26 octobre 2026", cap="L’art du froid au service du sur-mesure. Une cave à vin où esthétique, précision et performance frigorifique se rencontrent. Une belle réalisation qui reflète notre savoir-faire et notre passion pour le froid commercial. Film : @thefresh.ch", poster="cave-13_2", t="Le film de la cave sur mesure", cls="t-big"),
 dict(id="DZIAv4Tsl1Q", kind="reel", src="reel-van", date="3 juin 2026", cap="Notre image évolue, notre engagement reste le même. Iceberg prend la route avec une nouvelle identité.", poster="van-1", t="Nouvelle identité, nouveau véhicule", cls="t-tall"),
 dict(id="BzX37SVoMIy", kind="p", imgs=[f"ig-clim-{i}" for i in range(1,11)], date="1 juillet 2019", cap="Climatisation, réalisations, projet clim, froid et chaud, pompe à chaleur. Coolers and heaters solutions. Installations, dépannage, vente.", cls="t-clim", cover=1, t="Climatisation d’un logement"),
 dict(id="CEg_3xNgMVJ", kind="p", imgs=["ig-cave-2020"], date="30 août 2020", cap="Cave à vin sur mesure.", cls="t-cave", t="Cave à vin voûtée"),
 dict(id="CElkHErAuE1", kind="p", imgs=["ig-mobile-1","ig-mobile-2"], date="1 septembre 2020", cap="Climatiseur mobile, unité intérieure et unité extérieure. Crissier.", t="Climatiseur mobile", cls="t-mob", cover=1),
]
def insta():
    t=""
    for i,p in enumerate(POSTS):
        if p["kind"]=="reel":
            m=f'<video muted loop playsinline preload="none" poster="assets/img/{p["poster"]}.webp" data-src="assets/video/{p["src"]}.mp4" aria-hidden="true"></video><span class="t-k">{ic("play")}</span>'
        else:
            m=img(p["imgs"][p.get("cover",0)],p["cap"],1080,1080)+(f'<span class="t-k">{ic("layers")}<b>{len(p["imgs"])}</b></span>' if len(p["imgs"])>1 else "")
        t+=f'<button class="tile {p["cls"]}" data-post="{i}" aria-label="Voir la publication du {p["date"]}">{m}<span class="t-c">{p["t"]}</span></button>'
    return f'''<section class="insta" id="realisations"><div class="wrap">
 <div class="insta-h"><div data-r><h2>Nos chantiers, en images.</h2><p>Tout ce que nous publions sur Instagram, réuni ici.</p></div>
  <div class="stories" aria-label="Stories à la une"><a href="https://www.instagram.com/stories/highlights/17981025742292296/" target="_blank" rel="noopener"><i><span class="s-cgn">CGN</span></i>Entretien CGN</a><a href="https://www.instagram.com/stories/highlights/17874466897409947/" target="_blank" rel="noopener"><i><span class="s-leo">Leonardo</span></i>Leonardo</a><a href="{IG}" target="_blank" rel="noopener"><i><span>{ic('ig')}</span></i>@iceberg.sarl</a></div></div>
 <div class="tiles">{t}</div></div></section>
<dialog class="lb" aria-label="Publication Instagram"><div class="lb-in"><div class="lb-m"></div><button class="lb-n lb-prev" aria-label="Image précédente">{ic('left')}</button><button class="lb-n lb-next" aria-label="Image suivante">{ic('right')}</button><div class="lb-t"><div class="lb-dots"></div><p class="lb-cap"></p><p class="lb-d"></p><div class="row"><a class="btn btn-c" href="#devis" data-devis data-lbclose>Un projet similaire ?</a><a class="lnk lb-l" target="_blank" rel="noopener">Voir sur Instagram{ic('arrow')}</a></div></div></div><button class="lb-x" aria-label="Fermer">{ic('close')}</button></dialog>
<script type="application/json" id="posts">{json.dumps([{k:v for k,v in p.items() if k!='cls'} for p in POSTS],ensure_ascii=False)}</script>'''

def home():
    stops="".join(f'<figure class="th-bg{" on" if i==0 else ""}" data-i="{i}">{img(s[5],s[6],1800,1200,lazy=i>0)}</figure>' for i,s in enumerate(STOPS))
    cards="".join(f'<article class="th-card{" on" if i==0 else ""}" data-i="{i}"{"" if i==0 else " inert"}><h3>{s[2]}</h3><p>{s[3]}</p><div class="row"><a class="btn btn-c" href="#devis" data-devis data-besoin="{s[7]}">Demander un devis</a><a class="lnk lnk-w" href="{s[4]}">En savoir plus{ic("arrow")}</a></div></article>' for i,s in enumerate(STOPS))
    marks="".join(f'<button data-i="{i}" style="--p:{i*25}%"{" class=on" if i==0 else ""}><b>{s[0]}°</b><span>{s[1]}</span></button>' for i,s in enumerate(STOPS))
    return f'''
<section class="dive" aria-label="Iceberg Sàrl"><div class="dive-st">
 <div class="dive-img"><picture><source media="(max-width:800px)" srcset="assets/img/iceberg-m.webp"><img src="assets/img/iceberg.webp" alt="Un iceberg vu au-dessus et au-dessous de la surface de l’eau" width="2200" height="2261" fetchpriority="high"></picture></div>
 <div class="dive-sh"></div><canvas class="dive-c" aria-hidden="true"></canvas>
 <div class="dive-a wrap"><h1>Le froid juste, au&nbsp;degré&nbsp;près.</h1><p>Climatisation, chambres froides et caves à vin sur mesure. Vente, installation, réparation et dépannage 24h/24 à Lausanne et dans toute la Suisse romande.</p>
  <div class="row"><a class="btn btn-c" href="#devis" data-devis>Demander un devis</a><a class="btn btn-o" href="tel:{TEL}">{ic('phone')}{TEL_D}</a></div></div>
 <div class="dive-b wrap"><h2>Vous sentez le confort.<br>Nous nous occupons de&nbsp;tout&nbsp;le&nbsp;reste.</h2>
  <ul><li><b>Calculer</b><span>Le besoin thermique réel du lieu, avant de parler d’appareil.</span></li><li><b>Installer</b><span>Des machines des meilleures marques, posées proprement.</span></li><li><b>Réparer</b><span>Un diagnostic d’expert, sur tout type d’installation.</span></li><li><b>Veiller</b><span>Un technicien joignable 24h/24, 7 jours sur 7.</span></li></ul></div>
 <div class="dive-d" aria-hidden="true"><span>Surface</span><i><em></em></i><span>Technique</span></div>
</div></section>

<section class="th" id="services" aria-labelledby="th-h"><div class="th-bgs">{stops}</div><div class="th-tint"></div><div class="th-frost"></div>
 <div class="wrap th-in"><h2 id="th-h">À quelle température commence votre projet&nbsp;?</h2>
  <div class="th-mid"><div class="th-num" aria-hidden="true"><span id="thn">+23</span><sup>°C</sup></div><div class="th-cards">{cards}</div></div>
  <div class="th-sl"><div class="th-tr"><div class="th-marks">{marks}</div><input type="range" id="thr" min="0" max="100" step="0.5" value="0" aria-label="Choisir une température" aria-valuetext="+23 °C, Confort"><i class="th-fill"></i><i class="th-k"><svg viewBox="0 0 24 24"><path d="m9 7-5 5 5 5M15 7l5 5-5 5"/></svg></i></div></div>
 </div></section>

<section class="cave"><div class="cave-st"><div class="wrap cave-in">
 <div class="cave-t"><h2>L’art du froid au service du sur&#8209;mesure.</h2><p>Une cave où esthétique, précision et performance frigorifique se rencontrent. Nous dimensionnons le froid, l’intégrons à l’agencement et le rendons discret, pour que l’on ne voie que les bouteilles.</p>
  <dl class="cave-d"><div><dd><span data-count="12">12</span> °C</dd><dt>la température stable, été comme hiver</dt></div><div><dd><span data-count="70">70</span> %</dd><dt>d’humidité, pour ménager les bouchons</dt></div></dl>
  <div class="row"><a class="btn btn-c" href="#devis" data-devis data-besoin="Cave à vin">Imaginer ma cave</a><a class="lnk lnk-w" href="caves-a-vin.html">Découvrir les caves{ic('arrow')}</a></div><p class="cred">Réalisation Iceberg, film @thefresh.ch</p></div>
 <div class="cave-g"><div class="cg cg-1">{img('cave-9_2','Allée centrale d’une cave à vin sur mesure',900,1600)}{img('cave-15','Verres et bouteilles suspendus dans une cave à vin',900,1600)}{img('cave-4_3','Bouteilles en étagères',900,1600)}</div><div class="cg cg-2"><button class="cave-v" data-post="0" aria-label="Voir le film de la cave"><video muted loop playsinline preload="none" poster="assets/img/cave-13_2.webp" data-src="assets/video/cave.mp4" aria-hidden="true"></video><span>{ic('play')}Voir le film</span></button>{img('cave-21','Bouteilles rangées sur des étagères en bois éclairées',900,1600)}</div><div class="cg cg-3">{img('cave-5_3','Bouteilles alignées dans une cave éclairée',900,1600)}{img('cave-11','Étagères inclinées et lumière intégrée',900,1600)}{img('cave-22_5','Angle d’une cave à vin éclairée',900,1600)}</div></div>
</div></div></section>

<section class="ref"><div class="wrap ref-in"><div class="ref-m" data-par>{img('vapeur','Bateau Belle Époque sur le lac Léman (photo d’illustration)',1800,1199)}</div><div class="ref-t" data-r><h2>Ils nous confient leur froid.</h2><p>Du lac à la cuisine, les installations changent, l’exigence reste. La CGN et le restaurant Leonardo figurent parmi les références que nous partageons sur Instagram.</p>
 <ul><li><a href="https://www.instagram.com/stories/highlights/17981025742292296/" target="_blank" rel="noopener"><b>CGN</b><span>Entretien</span>{ic('arrow')}</a></li><li><a href="https://www.instagram.com/stories/highlights/17874466897409947/" target="_blank" rel="noopener"><b>Leonardo</b><span>Restaurant, pizzeria</span>{ic('arrow')}</a></li></ul></div></div></section>

<section class="free"><div class="wrap free-in"><div data-r><h2>Jusqu’à 70&nbsp;% d’électricité en moins.</h2><p>Pour refroidir bureaux, locaux informatiques et centrales de téléphonie, nous combinons le freecooling, qui utilise l’air frais extérieur, et un froid mécanique de dernière génération.</p><a class="lnk" href="locaux-informatiques.html">Comment ça marche{ic('arrow')}</a></div>
 <div class="free-g" role="img" aria-label="Consommation électrique : climatiseur conventionnel 100, freecooling et froid mécanique jusqu’à 30"><div><span>Climatiseur conventionnel</span><i style="--w:100%"><b>100</b></i></div><div class="lo"><span>Freecooling + froid mécanique</span><i style="--w:30%"><b>30</b></i></div><p>Consommation électrique, base 100. Économie maximale annoncée par rapport à un climatiseur conventionnel.</p></div></div></section>

{insta()}
{urgent()}
<section class="about"><div class="wrap about-in"><div class="about-m">{img('cave-19_2','Un frigoriste Iceberg entretient l’unité de froid d’une cave à vin',900,1600)}</div><div class="about-t" data-r><h2>Célibataire, en couple, ou frigoriste.</h2><p>C’est écrit sur nos t-shirts, et la bonne case est cochée. Iceberg est une entreprise lausannoise où l’on parle directement à ceux qui posent, règlent et réparent.</p><p>Vente d’appareils des meilleures marques, installation soignée, réparation et service après-vente : une seule équipe suit votre installation de l’étude à l’entretien.</p><a class="btn btn-i" href="tel:{TEL}">{ic('phone')}Parler à un frigoriste</a></div></div></section>
{brands()}
{form()}
{faq([("Une climatisation peut-elle aussi chauffer ?","Oui. Les climatiseurs actuels sont réversibles : ce sont des pompes à chaleur qui chauffent en hiver et rafraîchissent en été."),("Intervenez-vous sur une installation que vous n’avez pas posée ?","Oui. Nous diagnostiquons et réparons tout type d’installation, y compris la vôtre."),("Que faire si ma chambre froide tombe en panne la nuit ?",f'Appelez le <a href="tel:{URG}">{URG_D}</a>. Le dépannage fonctionne 24h/24, 7 jours sur 7. Gardez les portes fermées en attendant notre appel.'),("Peut-on avoir une climatisation sans unité extérieure fixe ?","Nous proposons des climatiseurs mobiles et des modèles mobiles déconnectables, utiles en location ou lorsque la façade ne permet pas d’installation. Nous vérifions avec vous la solution adaptée."),("Dans quelle région travaillez-vous ?","Notre siège est à Lausanne et nous intervenons en Suisse romande et sur l’arc lémanique."),("Comment obtenir un devis ?","Par téléphone, par WhatsApp ou avec le formulaire ci-dessus. Le devis est personnalisé, en tenant compte des exigences thermiques du lieu.")])}
{contact()}'''

def service(fn, title, desc, h1, lead, hero, halt, blocks, steps, qs, besoin, gallery=None):
    bl="".join(f'<article data-r><h3>{a}</h3><p>{b}</p></article>' for a,b in blocks)
    st="".join(f'<li data-r><b>{a}</b><span>{b}</span></li>' for a,b in steps)
    gal=f'<section class="sg"><div class="wrap"><h2 data-r>{gallery[0]}</h2><div class="sg-g">'+"".join(f'<figure>{img(n,a,w,h)}</figure>' for n,a,w,h in gallery[1])+'</div></div></section>' if gallery else ""
    body=f'''<section class="sh sh-{fn.split(chr(46))[0]}"><div class="sh-m">{img(hero,halt,1800,1200,lazy=False,extra='fetchpriority="high"')}</div><div class="wrap sh-t"><nav class="bc" aria-label="Fil d’Ariane"><a href="index.html">Accueil</a> / <span>{title.split(" | ")[0].split(" à Lausanne")[0]}</span></nav><h1>{h1}</h1><p>{lead}</p><div class="row"><a class="btn btn-c" href="#devis" data-devis>Demander un devis</a><a class="btn btn-o" href="tel:{URG if 'depannage' in fn else TEL}">{ic('phone')}{URG_D if 'depannage' in fn else TEL_D}</a></div></div></section>
<section class="sb"><div class="wrap"><div class="sb-g">{bl}</div></div></section>{gal}
<section class="ss"><div class="wrap ss-in"><h2 data-r>Comment cela se passe</h2><ol>{st}</ol></div></section>
{urgent() if 'depannage' not in fn else brands()}{form(besoin)}{faq(qs)}{contact()}'''
    page(fn,title,desc,body,"svc",title.split(" | ")[0])

OUT.mkdir(exist_ok=True)
page("index.html","Iceberg Sàrl | Climatisation, chambres froides et caves à vin à Lausanne","Frigoriste à Lausanne : climatisation, pompe à chaleur, chambre froide, congélation et cave à vin sur mesure. Vente, installation, réparation, dépannage 24h/24.",home(),"home")
STEPS=[("Échange","Vous décrivez le lieu et le besoin, par téléphone, WhatsApp ou formulaire."),("Étude","Nous tenons compte des exigences thermiques du lieu et proposons l’appareil adapté."),("Devis","Vous recevez un devis personnalisé."),("Installation et suivi","La même équipe pose, met en service, entretient et répare.")]
service("climatisation.html","Climatisation et pompe à chaleur à Lausanne | Iceberg Sàrl","Climatiseur split, multisplit, mobile ou réversible à Lausanne et en Suisse romande. Vente, installation, entretien et réparation par Iceberg Sàrl.","Fraîche l’été, chaude l’hiver.","Les climatiseurs actuels sont réversibles. Une seule installation rafraîchit, chauffe et filtre l’air de votre logement ou de vos bureaux.","salon","Salon au bord de l’eau équipé d’une climatisation murale",
 [("Split et multisplit","Une unité extérieure, une ou plusieurs unités intérieures, murales ou en console, pour régler chaque pièce."),("Réversible, pompe à chaleur","Le même appareil chauffe en hiver et rafraîchit en été."),("Mobile et mobile déconnectable","Une solution pour les locataires, les bureaux ou un besoin temporaire."),("Un air plus propre","Filtres à charbon actif, filtres antibactériens, lampes UV et ionisation."),("Réparation et SAV","Nous savons diagnostiquer tout type d’installation, y compris celles que nous n’avons pas posées."),("Les meilleures marques","Daikin, Mitsubishi, Panasonic, Fujitsu, Toshiba, Hitachi, LG, Samsung et d’autres.")],STEPS,
 [("Faut-il une autorisation pour poser une unité extérieure ?","Les règles dépendent de la commune et, en copropriété, du règlement de l’immeuble. Il faut vérifier ce point avant la pose ; parlez-nous-en dès le premier contact."),("Quelle différence entre climatisation et pompe à chaleur ?","Un climatiseur réversible est une pompe à chaleur air-air : il déplace la chaleur vers l’extérieur l’été, vers l’intérieur l’hiver."),("Installez-vous dans des bureaux ?","Oui, en logement, bureaux, commerces et locaux techniques.")],"Climatisation",
 ("Une installation, de la terrasse au salon",[("ig-clim-1","Deux unités extérieures installées sur une terrasse",1080,1076),("ig-clim-10","Unité murale Daikin posée au-dessus d’une porte",1080,1076),("ig-clim-2","Unités extérieures et goulotte assortie à la façade",1080,1076),("ig-clim-6","Unité murale dans une chambre",1080,1076),("ig-mobile-2","Unité extérieure Iceberg sur gravier",1080,1080),("ig-mobile-1","Climatiseur mobile Iceberg dans un bureau",1080,1079)]))
service("caves-a-vin.html","Caves à vin sur mesure à Lausanne | Iceberg Sàrl","Cave à vin et carnotzet sur mesure à Lausanne et en Suisse romande : climatisation de cave, température et humidité stables, intégration soignée.","Vos bouteilles méritent mieux qu’un sous&#8209;sol.","Nous concevons le froid de votre cave ou de votre carnotzet et l’intégrons à l’agencement, en toute discrétion.","cave-9_2","Cave à vin sur mesure réalisée par Iceberg Sàrl",
 [("Température stable","Une cave se tient autour de 12 °C. Ce sont les variations qui abîment le vin, pas le froid."),("Humidité maîtrisée","Autour de 70 %, pour préserver les bouchons et les étiquettes."),("Intégration discrète","L’unité se fond dans l’agencement : on voit le bois, la lumière et les bouteilles."),("Carnotzets","Un lieu où l’on garde, mais aussi où l’on reçoit."),("Restaurants et hôtels","Des caves visibles en salle, qui deviennent un élément du décor."),("Entretien et dépannage","Nous suivons l’installation et répondons 24h/24.")],STEPS,
 [("Peut-on transformer une pièce existante ?","Souvent oui. L’isolation, le volume et l’évacuation de la chaleur sont les trois points que nous étudions en premier."),("La cave sera-t-elle bruyante ?","Le bruit dépend du matériel et de l’emplacement du groupe. C’est un critère que nous traitons dès l’étude."),("Faites-vous aussi l’entretien de caves existantes ?","Oui, y compris celles que nous n’avons pas réalisées.")],"Cave à vin",
 ("Deux caves, un même soin",[("cave-13_2","Verres suspendus et bouteilles mises en valeur",900,1600),("cave-22_5","Cave à vin avec étagères rétroéclairées",900,1600),("cave-4_3","Bouteilles rangées en étagères",900,1600),("ig-cave-2020","Cave à vin voûtée derrière une verrière",1060,982),("cave-11","Étagères inclinées éclairées",900,1600),("cave-15","Verres à vin suspendus",900,1600)]))
service("froid-commercial.html","Froid commercial et chambres froides à Lausanne | Iceberg Sàrl","Chambre froide, chambre de congélation, garde-manger et frigos professionnels à Lausanne et en Suisse romande. Installation, entretien, dépannage 24h/24.","La chaîne du froid, sans maillon faible.","Chambres froides, congélation et frigos professionnels pour restaurants, hôtels, commerces et industrie.","cuisine","Cuisine professionnelle en inox",
 [("Chambres froides","Conçues selon vos volumes, vos produits et le rythme de vos livraisons."),("Chambres de congélation","Le froid négatif, dimensionné pour tenir même quand la porte s’ouvre souvent."),("Garde-mangers","Une pièce fraîche sur mesure, en cuisine professionnelle ou à domicile."),("Frigos professionnels","Entretien, réparation et installation de vos meubles et points de froid."),("Entretien","Un suivi régulier limite les pannes et la consommation."),("Dépannage 24h/24","Parce qu’un stock n’attend pas les heures de bureau.")],STEPS,
 [("Ma chambre froide remonte en température, que faire ?",f'Gardez la porte fermée et appelez le <a href="tel:{URG}">{URG_D}</a>, jour et nuit.'),("Réparez-vous toutes les marques ?","Nous diagnostiquons tout type d’installation."),("Proposez-vous un entretien régulier ?","Oui. Parlez-nous de vos équipements et nous vous ferons une offre adaptée.")],"Chambre froide",
 ("Du frais au grand froid",[("affinage","Meules de fromage en cave d’affinage (photo d’illustration)",1800,1202),("congelation","Armoires de congélation (photo d’illustration)",1800,1200),("van-10","La nouvelle identité Iceberg sur son véhicule",720,1280)]))
service("locaux-informatiques.html","Climatisation de locaux informatiques à Lausanne | Iceberg Sàrl","Refroidissement de salles serveurs, bureaux et centrales de téléphonie : freecooling et froid mécanique, jusqu’à 70 % d’électricité en moins.","Vos serveurs au frais, votre facture aussi.","Refroidissement de locaux informatiques, bureaux et centrales de téléphonie mobile et fixe, en Suisse romande.","serveurs","Baies de serveurs dans un local informatique",
 [("Freecooling","Quand l’air extérieur est assez frais, il refroidit le local presque sans compresseur."),("Froid mécanique","Dès qu’il fait trop chaud dehors, la machine prend le relais automatiquement."),("Close control","Une régulation précise de la température, pensée pour des équipements sensibles."),("Jusqu’à 70 % d’économie","D’énergie électrique, par rapport à un climatiseur conventionnel."),("Téléphonie","Centrales mobiles et fixes, locaux techniques, bureaux."),("Urgence 24h/24","Une salle serveurs qui chauffe se traite tout de suite.")],STEPS,
 [("Le freecooling fonctionne-t-il en Suisse romande ?","Oui. Notre climat offre de nombreuses heures fraîches dans l’année, ce qui en fait une région favorable. Le gain réel dépend du local."),("Peut-on garder notre installation actuelle ?","Nous commençons par un diagnostic. Si elle peut être réparée ou optimisée, nous vous le disons."),("Intervenez-vous la nuit ?",f'Oui, au <a href="tel:{URG}">{URG_D}</a>.')],"Local informatique")
service("depannage.html","Dépannage climatisation et froid 24h/24 à Lausanne | Iceberg Sàrl","Dépannage frigorifique 24h/24 et 7j/7 à Lausanne et en Suisse romande : climatisation, chambre froide, congélateur, cave à vin, salle serveurs.","En panne&nbsp;? Appelez, on vous répond.","Dépannage 24 heures sur 24, 7 jours sur 7 : climatisation, chambre froide, congélation, cave à vin et salle serveurs.","van-1","Véhicule Iceberg Sàrl avec le numéro 021 626 11 11",
 [("Diagnostic","Experts en diagnostic, nous trouvons la solution pour remettre en marche tout type d’installation."),("Réparation","Climatiseurs, pompes à chaleur, groupes de froid et meubles frigorifiques."),("Toutes marques","Y compris une installation que nous n’avons pas posée.")],
 [("Appelez",f'<a href="tel:{URG}">{URG_D}</a>, jour et nuit.'),("Décrivez","Le lieu, l’appareil, ce qui s’affiche. Une photo par WhatsApp fait gagner du temps."),("Gardez le froid","Portes fermées, ouvertures limitées."),("Nous intervenons","Diagnostic et remise en service, dans les meilleurs délais.")],
 [("Le numéro fonctionne-t-il le dimanche ?","Oui, 24 heures sur 24 et 7 jours sur 7."),("Puis-je envoyer une photo de la panne ?","Oui, par WhatsApp : plaque signalétique et code d’erreur nous aident beaucoup."),("Réparez-vous les frigos professionnels ?","Oui, nous entretenons, réparons et installons vos frigos professionnels.")],"Réparation")
page("confidentialite.html","Protection des données | Iceberg Sàrl","Protection des données du site Iceberg Sàrl.",f'''<section class="txt"><div class="wrap"><h1>Protection des données</h1><p>Responsable : Iceberg Sàrl, Chemin du Bois-de-Vaux 1, 1007 Lausanne, <a href="mailto:{MAIL}">{MAIL}</a>.</p><h2>Formulaire</h2><p>Le formulaire de devis n’enregistre rien sur ce site. Il prépare un message que vous envoyez vous-même par WhatsApp ou par e-mail.</p><h2>Services tiers</h2><p>La carte de la page d’accueil provient de Google Maps, qui peut recevoir votre adresse IP lors de son affichage. Les liens WhatsApp et Instagram ouvrent les services de Meta.</p><h2>Cookies</h2><p>Ce site ne dépose pas de cookies de mesure d’audience.</p><h2>Vos droits</h2><p>Vous pouvez demander l’accès, la rectification ou la suppression de vos données en nous écrivant.</p></div></section>''',"svc plain")
page("404.html","Page introuvable | Iceberg Sàrl","Cette page n’existe pas.",f'''<section class="txt"><div class="wrap"><h1>Cette page a fondu.</h1><p>Le lien n’existe plus. Revenez à l’accueil ou appelez-nous.</p><div class="row"><a class="btn btn-c" href="{BASE}">Retour à l’accueil</a><a class="btn btn-i" href="tel:{TEL}">{TEL_D}</a></div></div></section>''',"svc plain")
# 404 is served from any depth
p=OUT/"404.html"; p.write_text(p.read_text().replace("<head>",f'<head><base href="{BASE}">',1))
(OUT/"robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")
(OUT/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{BASE}{u}</loc></url>" for u in ["","climatisation","caves-a-vin","froid-commercial","locaux-informatiques","depannage"])+"</urlset>")
(OUT/".nojekyll").write_text("")
print("built")
