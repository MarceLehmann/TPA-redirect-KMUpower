"""Erzeugt aus redirects.json alle statischen Weiterleitungsseiten (GitHub Pages).

Aufruf im Repo-Root:  python tools/build_redirects.py
Jede alte URL bekommt eine Seite mit sofortigem Meta-Refresh (Google wertet das als permanente
Weiterleitung), rel=canonical auf das Ziel und einem JavaScript-Fallback. Unbekannte Pfade landen
in 404.html, die per JavaScript nach Praefix-Regeln weiterleitet.
"""
import io, json, os, shutil, sys, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "www.thepoweraddicts.ch"          # in CNAME gesetzt, unter dieser Adresse wurden die alten Seiten indexiert
KEEP = {".git", "tools", "redirects.json", "README.md", ".gitignore"}


def resolve(cfg, ref):
    scheme, _, path = ref.partition(":/")
    return cfg[scheme].rstrip("/") + "/" + path.lstrip("/") if scheme in ("kmupower", "academy", "tip") else ref


def label(url, cfg):
    if url.startswith(cfg["academy"]):
        return "Power Platform Academy"
    if url.startswith(cfg["tip"]):
        return "PowerPlatformTip"
    return "KMUpower"


PAGE = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<title>Weiterleitung zu {name}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="canonical" href="{target}">
<meta http-equiv="refresh" content="0; url={target}">
<script>window.location.replace({target_js});</script>
</head>
<body>
<p>Diese Seite ist umgezogen: <a href="{target}">{target}</a></p>
</body>
</html>
"""

NOT_FOUND = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<title>Weiterleitung zu KMUpower</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
<p>Diese Seite ist umgezogen. <a id="go" href="{fallback_plain}">Weiter zu KMUpower</a></p>
<script>
(function () {{
  var rules = {rules};
  var fallback = {fallback};
  var path = "";
  try {{ path = decodeURIComponent(location.pathname).toLowerCase().replace(/\\/+$/, ""); }} catch (e) {{ path = location.pathname.toLowerCase(); }}
  var target = fallback;
  for (var i = 0; i < rules.length; i++) {{
    var p = rules[i][0];
    if (path === p || path.indexOf(p + "/") === 0) {{ target = rules[i][1]; break; }}
  }}
  var link = document.getElementById("go");
  if (link) {{ link.href = target; }}
  window.location.replace(target);
}})();
</script>
</body>
</html>
"""


def main():
    cfg = json.load(io.open(os.path.join(ROOT, "redirects.json"), encoding="utf-8"))
    for name in os.listdir(ROOT):
        if name in KEEP:
            continue
        p = os.path.join(ROOT, name)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)

    def write(rel, content):
        full = os.path.join(ROOT, *rel.split("/"))
        os.makedirs(os.path.dirname(full) or ROOT, exist_ok=True)
        io.open(full, "w", encoding="utf-8", newline="\n").write(content)

    seen, urls = set(), []
    for item in cfg["redirects"]:
        src = item["from"]
        if src in seen:
            sys.exit("Doppelter Eintrag: " + src)
        seen.add(src)
        target = resolve(cfg, item["to"])
        html = PAGE.format(name=label(target, cfg), target=target, target_js=json.dumps(target))
        if src == "/":
            write("index.html", html)
        else:
            rel = src.strip("/")
            write(rel + ".html", html)          # /pfad          (GitHub Pages loest ohne Endung auf)
            write(rel + "/index.html", html)     # /pfad/
        urls.append(src)

    rules = [[r["prefix"], resolve(cfg, r["to"])] for r in cfg["fallback_rules"]]
    fb = resolve(cfg, cfg["fallback_default"])
    write("404.html", NOT_FOUND.format(rules=json.dumps(rules), fallback=json.dumps(fb), fallback_plain=fb))

    write("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: https://%s/sitemap.xml\n" % HOST)
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for src in urls:
        loc = "https://%s%s" % (HOST, urllib.parse.quote(src, safe="/-_.~") if src != "/" else "/")
        lines.append("<url><loc>%s</loc></url>" % loc)
    lines.append("</urlset>")
    write("sitemap.xml", "\n".join(lines) + "\n")
    write("CNAME", HOST + "\n")
    write(".nojekyll", "")
    print("Erzeugt: %d Weiterleitungen, 404-Auffangseite, robots.txt, sitemap.xml, CNAME (%s)" % (len(urls), HOST))


if __name__ == "__main__":
    main()
