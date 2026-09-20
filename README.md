# Weiterleitungen der alten Domain

Statische Weiterleitungsseiten (GitHub Pages) fuer die frueheren Adressen der alten Wix-Seite. Jede alte URL leitet auf die
passende neue Seite von KMUpower, der Power Platform Academy oder PowerPlatformTip.

- `redirects.json`: Zuordnung alt nach neu (einzige Quelle der Wahrheit). Hier pflegen.
- `tools/build_redirects.py`: erzeugt daraus alle Seiten, `404.html`, `robots.txt`, `sitemap.xml` und `CNAME`.
  Aufruf im Repo-Root: `python tools/build_redirects.py`, danach committen und pushen.
- Jede Seite nutzt einen sofortigen Meta-Refresh mit `rel=canonical` auf das Ziel. Google wertet einen sofortigen
  Meta-Refresh als permanente Weiterleitung.
- Unbekannte Pfade landen in `404.html` und werden dort per JavaScript nach Praefix-Regeln umgeleitet.
- Die Weiterleitungen sollen mindestens ein Jahr stehen bleiben, laenger ist unproblematisch.

## DNS (bei Namecheap)

- `A` fuer `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` (keine weitere IP, insbesondere nicht `162.255.119.30`)
- `CNAME` fuer `www`: `marcelehmann.github.io.` (keine URL-Weiterleitung fuer `www`)
- Mail-Eintraege (MX, TXT, CNAME fuer Microsoft 365) nicht aendern.
