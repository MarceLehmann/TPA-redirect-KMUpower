# Weiterleitungen der alten Domain

Dieses Repository leitet die früheren Adressen der alten Wix-Seite auf die aktuellen Seiten von Marcel Lehmann (KMUpower) um:

- Beratung, Über uns, Kontakt: https://kmupower.com
- Kurse, Workshops, Trainer: https://www.powerplatformacademy.online
- einzelne Tipp-Artikel: https://www.powerplatformtip.com

Ausgeliefert wird nur der Ordner `docs/` (GitHub Pages: Branch `main`, Ordner `/docs`). Alles andere im Repo (diese Datei,
`redirects.json`, `tools/`) wird nicht veröffentlicht.

## So funktioniert es

- GitHub Pages kann keinen HTTP-301 senden. Jede alte URL hat deshalb eine eigene kleine Seite mit sofortigem Meta-Refresh,
  `rel="canonical"` auf das Ziel und einem JavaScript-Fallback. Google wertet einen sofortigen Meta-Refresh als permanente
  Weiterleitung (Google Search Central, «Redirects and Google Search»).
- Pfade ohne eigene Seite landen in `docs/404.html`. Sie schlägt dieselbe Zuordnung per JavaScript nach (inklusive
  Präfix-Regeln, z. B. alle `/post/...`) und leitet sonst auf die Startseite von kmupower.com.
- Kein `noindex`: Google muss die alten Seiten abrufen dürfen, um die Weiterleitung zu sehen. `robots.txt` erlaubt alles,
  `sitemap.xml` listet die alten URLs.
- Auf den Seiten steht die alte Marke nicht. Die alte Domain steht nur in `CNAME`, `robots.txt` und `sitemap.xml`
  (dort technisch nötig). Das Skript prüft das bei jedem Lauf.
- Die Weiterleitungen bleiben mindestens ein Jahr stehen, länger ist unproblematisch. Die Domain muss dafür verlängert bleiben.

## Dateien

- `redirects.json`: Zuordnung alter Pfad nach neue Seite, mit Begründung je Eintrag. Einzige Quelle der Wahrheit, hier pflegen.
- `tools/build_redirects.py`: erzeugt daraus den Ordner `docs/` (Seiten, `404.html`, `robots.txt`, `sitemap.xml`, `CNAME`,
  `.nojekyll`). Nur Python 3, keine Abhängigkeiten.
- `docs/`: erzeugte Ausgabe. Nie von Hand ändern, sie wird bei jedem Lauf komplett neu geschrieben.
- `static/` (optional, noch nicht vorhanden): Dateien darin werden 1:1 nach `docs/` kopiert, z. B. eine Bestätigungsdatei
  der Search Console.

## Eintrag ändern oder ergänzen

1. `redirects.json` anpassen (Pfade ohne Domain und ohne Slash am Ende; Ziele als `kmupower:/pfad`, `academy:/pfad` oder `tip:/pfad`).
2. Im Repo-Root `python tools/build_redirects.py` ausführen. Das Skript prüft Ziel, canonical, Meta-Refresh, Schleifen,
   `noindex` und Markennamen im Seiteninhalt und bricht bei einem Fehler ab.
3. `python tools/build_redirects.py --targets` listet alle Ziel-URLs. Jede muss direkt mit 200 antworten, ohne weitere Weiterleitung.
4. `docs/` mitcommitten und auf `main` pushen. GitHub Pages veröffentlicht den Stand.

## DNS (Registrar Namecheap, Advanced DNS)

- `A Record`, Host `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` (keine weitere IP,
  insbesondere nicht `162.255.119.30`)
- `CNAME Record`, Host `www`: `marcelehmann.github.io.` (keine `URL Redirect Record` für `www` oder `@`)
- Alle Mail-Einträge (MX, SPF, weitere TXT, CNAME für Microsoft 365) unverändert lassen.
- «Enforce HTTPS» (Settings, Pages) erst einschalten, wenn das DNS stimmt und GitHub das Zertifikat ausgestellt hat.
  Der Apex leitet GitHub dann automatisch auf `www` um.
