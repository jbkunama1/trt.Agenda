# 🗓️ trt.Agenda

![Agenda](docs/assets/banner.svg)

[![Build](https://img.shields.io/github/actions/workflow/status/jbkunama1/trt.Agenda/docker.yml?branch=main&style=for-the-badge)](https://github.com/jbkunama1/trt.Agenda/actions)
![SQLite](https://img.shields.io/badge/SQLite-persistent-003B57?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-GHCR-2496ED?style=for-the-badge)
![Agenden](https://img.shields.io/badge/Agenden-5-8b5cf6?style=for-the-badge)
![Themes](https://img.shields.io/badge/Themes-5-14b8a6?style=for-the-badge)

Mobile HTML/CSS/JS-Agenda mit Flask, SQLite und blauen bzw. frei auswählbaren Theme-Verläufen. Fünf getrennte Agenda-Plätze, je eigene Startzeit, Punkte, Dauern und in der Datenbank gespeichertes Theme. [View, Themes, Migration und Links](docs/themes-and-view.md).

## ✨ Bedienung

Agenda 1–5 auswählen → Bearbeiten → Schlüssel eingeben → Titel, Startzeit, Punkte und Theme ändern → Speichern. View ↗ öffnet reine Anzeige im neuen Tab, ohne Menü und Bearbeitung. Anzeige wird alle 15 Sekunden aktualisiert. Ocean, Graphite (eckig), Paper (hell), Forest und Sunset. Das Theme gilt geräteübergreifend für diese Agenda, nicht nur im Browser. Bis 50 Punkte je Agenda, Dauer 1–1440 ganze Minuten. Folgende Uhrzeiten werden berechnet. Keine Konten, Kalendertermine, Einzelstartzeiten oder Timer.

## 🚀 Portainer

1. Erfolgreichen test-and-docker-Lauf in Actions und GHCR-Image prüfen. GHCR-Paket trt.agenda für anonymen Pull öffentlich setzen oder Registry-Zugang hinterlegen.
2. Freien Port 8288 und vorhandenes externes Netzwerk highfishNetwork prüfen. Nur falls es fehlt und Bridge-Netzwerk gewünscht: `docker network create highfishNetwork` auf dem Docker-Host.
3. Stacks → Add stack → Repository: `https://github.com/jbkunama1/trt.Agenda`, Reference `refs/heads/main`, Compose path `docker-compose.yml`. Alternativ Datei in Web-Editor kopieren.
4. EDIT_PASSWORD als langen zufälligen Schlüssel in Stack-Variablen setzen; optional FRAME_ANCESTORS einschränken.
5. Deploy stack, dann `http://SERVER-IP:8288` öffnen.

Compose zieht `ghcr.io/jbkunama1/trt.agenda:latest`, kein lokaler Build. Aktueller Workflow ist kein Multiarch-Build; ARM-Kompatibilität nicht zugesichert.

## 🐳 Docker Compose

```bash
git clone https://github.com/jbkunama1/trt.Agenda.git
cd trt.Agenda
cp .env.example .env
joe .env
# EDIT_PASSWORD setzen!
docker network inspect highfishNetwork
docker compose pull
docker compose up -d
```

Docker Engine, Compose v2 und Git erforderlich. Bei privatem Paket zuvor `docker login ghcr.io` mit passendem Zugang. Nie Geheimnisse committen.

| Einstellung | Bedeutung |
|---|---|
| EDIT_PASSWORD | Erforderlich, Schreibschlüssel für alle fünf Agenden |
| FRAME_ANCESTORS | Erlaubte iFrame-Eltern, Standard *; z.B. 'self' https://unterricht.example.de |
| DATABASE | /data/agenda.sqlite3 |
| Port / Netzwerk | 8288:8000 / highfishNetwork |
| Volume | agenda_data; tatsächlicher Name häufig mit Stack-Präfix |

## 🖼️ iFrame

```html
<iframe src="https://agenda.example.de/static/view.html?agenda=2" title="Agenda 2" style="width:100%;height:640px;border:0;"></iframe>
```

Theme kommt aus SQLite. Ohne agenda-Parameter Agenda 1. Bestehende ?embed=1-Links bleiben nutzbar, alte theme-Parameter werden ignoriert. Höhe im Eltern-Dokument festlegen. HTTPS, FRAME_ANCESTORS und Proxy-/Eltern-CSP müssen Einbettung erlauben.

## 🔄 Updates und Datenmigration

Vor diesem Update Datenbank sichern! [Migrationsdetails und Rollback-Grenzen](docs/themes-and-view.md).

```bash
git pull
docker compose pull
docker compose up -d
```

In Portainer neues Image ziehen und Stack neu bereitstellen. Kein automatisches Update laufender Container durch den Build. Die bisherige Agenda wird verlustfrei als Agenda 1 übernommen; vier leere Plätze kommen hinzu. Neue Tabelle agendas, alte Tabelle agenda bleibt als Altbestand. Keine alte Version danach zum Bearbeiten einsetzen. Lokale Theme-Auswahl wird nicht übernommen, gewünschtes Theme einmal im Editor speichern.

## 💾 Backup

```bash
mkdir -p backups
docker compose stop agenda
docker cp trt-agenda:/data/agenda.sqlite3 ./backups/agenda.sqlite3
docker compose start agenda
```

Auch bei Kopierfehler Container wieder starten. Datierte Kopien außerhalb des Servers aufbewahren; obiger Name wird überschrieben. Restore überschreibt alle Agenden: Container stoppen, Backup mit `docker cp ./backups/agenda.sqlite3 trt-agenda:/data/agenda.sqlite3` zurückkopieren, Schreibrechte für UID 10001 sicherstellen und starten. Volume nicht löschen; `docker compose down -v` löscht persistente Daten.

## 🔐 Sicherheit / Fehlersuche

Alle Agenden öffentlich lesbar bei erreichbarer URL. Nur Schreiben ist geschützt. Keine vertraulichen Schülerdaten, keine Benutzerverwaltung, 2FA oder Login-Drosselung. Internetbetrieb mit HTTPS/Reverse Proxy und Firewall; Container läuft nicht als Root. Keine Geheimnisse im Browser-Speicher. Dokumentations-Shields laden externe Bilder.

| Problem | Prüfen |
|---|---|
| Image pull denied / not found | Actions, Paket-Sichtbarkeit und Registry-Zugang |
| Network not found / Port belegt | highfishNetwork / Port 8288 |
| Container startet nicht | EDIT_PASSWORD, `docker logs trt-agenda` |
| SQLite nicht beschreibbar | Volume-Rechte für UID 10001 |
| iFrame leer | HTTPS, FRAME_ANCESTORS, Proxy-Header, frame-src der Elternseite |
| Speichern abgewiesen | Schlüssel, Eingaben; bei Konflikt Änderungen kopieren, abbrechen und neu laden |
| Falsche Agenda | agenda-Parameter 1–5 prüfen; Standard ist 1 |

## 🧪 Entwicklung und CI

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
python -m pytest -q
export EDIT_PASSWORD='dein-langer-schluessel'
export DATABASE='./data/agenda.sqlite3'
gunicorn --bind 0.0.0.0:8288 --workers 1 --threads 4 app:app
```

Lokaler Image-Build: `docker build -t trt-agenda .`. Deployment-Compose bleibt auf GHCR. Workflow: Tests bei PRs und Push main; Image-Build/Push nach erfolgreichen Tests bei Push/Merge main oder workflow_dispatch. Tags latest und SHA, GHA-Cache. Auch Doku-Commits lösen Build aus.

API: GET /api/agendas listet Plätze; GET/PUT /api/agenda?agenda=1 liest/speichert Agenda (PUT: X-Edit-Key und JSON data/version). Theme wird validiert. GET /health ist nur HTTP-Liveness. Versionskonflikte je Agenda ergeben 409. Upload bedeutet nicht bestätigten CI-Erfolg, Live-Migration oder Browserprüfung.

## 🌐 GitHub Pages und Dateien

index.html ist eine statische Projektseite, keine SQLite-App. Aktivierung: Settings → Pages → Deploy from a branch → main → / (root). Erwartete Adresse nach Veröffentlichung: https://jbkunama1.github.io/trt.Agenda/. Live-Status nicht bestätigt; Projektseite kann noch die ursprüngliche Ein-Agenda-Vorschau zeigen.

app.py / templates / static: App; docker-compose.yml / Dockerfile: Deployment und Build; tests und .github/workflows: CI; docs/themes-and-view.md: neue Funktionen; docs/assets/banner.svg: Grafik; .env.example: Konfigurationsvorlage. Kein LICENSE vorhanden, keine Open-Source-Lizenz behauptet.
