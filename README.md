# trt.Agenda

Mobile HTML/CSS/JS-Agenda mit blauem Farbverlauf und serverseitiger SQLite-Speicherung (Flask). Eine gemeinsame Agenda, fünf Beispielpunkte, frei wählbare Startzeit und individuelle Dauern, automatisch berechnete Zeitbereiche. Punkte hinzufügen, löschen und verschieben. Speichern ausdrücklich über den Button. Keine Benutzerkonten, keine personenbezogenen Daten verwenden.

## GHCR und CI

Workflow `.github/workflows/docker.yml`: Tests bei Pull Requests; nach erfolgreichem Test Build und Push bei jedem Push auf main (einschließlich Merge), außerdem manueller Start. Image `ghcr.io/jbkunama1/trt.agenda:latest` und SHA-Tags. Keine automatische Aktualisierung laufender Portainer-Container. Aktuell Build für die Architektur des ubuntu-latest-Runners, kein Multiarch-Build.

Das Image ist erst nach einem erfolgreichen Workflow verfügbar. Die Sichtbarkeit des GHCR-Pakets separat prüfen: öffentlich für anonymen Pull setzen oder GHCR-Zugang in Portainer hinterlegen. Öffentliches Repository allein garantiert keine öffentliche Paket-Sichtbarkeit.

## Portainer

Stack aus Git-Repository `https://github.com/jbkunama1/trt.Agenda`, Branch main, Compose-Pfad `docker-compose.yml` erstellen oder Datei in den Web-Editor kopieren. Es wird das fertige Image gezogen, nicht lokal gebaut.

Umgebungsvariablen im Stack: `EDIT_PASSWORD` (langer zufälliger Schlüssel, erforderlich), `FRAME_ANCESTORS` (optional, Standard `*`). Netzwerk `highfishNetwork` muss auf dem Ziel-Docker-Host existieren. Port 8288 muss frei sein.

Aufruf: `http://SERVER-IP:8288`. Bearbeiten anklicken, Schlüssel eingeben, speichern. SQLite liegt im Volume `agenda_data` unter `/data/agenda.sqlite3`; tatsächlicher Volume-Name kann den Stack-Präfix enthalten. Volume sichern und beim Entfernen des Stacks nicht löschen.

Bei Updates in Portainer das neue Image ziehen und den Stack neu bereitstellen. Die Daten bleiben im Volume.

## iFrame

```html
<iframe src="https://agenda.example.de/?embed=1" title="Agenda" style="width:100%;height:640px;border:0;border-radius:18px;" loading="lazy"></iframe>
```

Embed-Ansicht ohne Bearbeitungsbutton und Fußzeile. Aktualisierung alle 15 Sekunden. Breite responsiv, Höhe im Eltern-Dokument einstellen. Zum Bearbeiten normale URL ohne embed verwenden. Eine globale Startzeit, Dauern 1–1440 ganze Minuten, maximal 50 Punkte. Tageswechsel werden angezeigt. Keine individuellen Startzeiten pro Punkt, keine Kalendertermine oder Timer.

## Sicherheit

Inhalte sind öffentlich lesbar, sobald die URL erreichbar ist. Änderungen erfordern den Schlüssel, der nicht in der URL oder im Browser-Speicher abgelegt wird. HTTPS über Reverse Proxy verwenden. Kein echter Schlüssel im Repository. `FRAME_ANCESTORS` kann auf `'self' https://unterricht.example.de` eingeschränkt werden. Proxy darf keine widersprechenden X-Frame-Options/CSP-Header setzen, und die Elternseite muss die Agenda als Frame-Quelle erlauben. HTTPS-Seite mit HTTPS-Agenda einbetten.

## Lokal

`cp .env.example .env`, Schlüssel setzen, dann `docker compose up -d` (zieht GHCR). Für lokalen Build stattdessen `docker build -t trt-agenda .` und eigenes Compose-Override verwenden.

Ohne Docker, Linux/Python 3.12:

```bash
pip install -r requirements.txt -r requirements-dev.txt
python -m pytest -q
export EDIT_PASSWORD='dein-langer-schluessel'
export DATABASE='./data/agenda.sqlite3'
gunicorn --bind 0.0.0.0:8288 --workers 1 --threads 4 app:app
```

## Prüfstatus

Tests sind im Repository und werden in CI ausgeführt. Ein erfolgreicher Build, Docker-Start und visuelle Browser-Prüfung sind zum Zeitpunkt des initialen Uploads noch nicht bestätigt.
