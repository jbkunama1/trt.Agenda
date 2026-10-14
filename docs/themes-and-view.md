# View-Seite und fünf Themes

Neben Bearbeiten stehen ein View-Link und eine Theme-Auswahl. View öffnet einen neuen Tab, damit die Editor-Seite erhalten bleibt. Die View-Seite zeigt nur Titel, Zusammenfassung, Agenda-Punkte, Uhrzeiten und Dauern. Keine Navigation, Theme-Auswahl, Bearbeitung oder Fußzeile. Nur bei Ladeproblemen erscheint eine Fehlermeldung. Aktualisierung alle 15 Sekunden; unveränderte Daten werden nicht neu gerendert. View liest die zuletzt gespeicherte Agenda; ungespeicherte Editor-Änderungen erscheinen dort nicht.

## Themes

| Name / URL-Wert | Gestaltung |
|---|---|
| Ocean / ocean | Blauer Gradient, weiche Rundungen; Standard |
| Graphite / graphite | Anthrazit und Türkis, eckige Buttons und Karten |
| Paper / paper | Weiß/Hellblau, dunkelblaue Akzente, fast eckig |
| Forest / forest | Grüner Verlauf, kleine Rundungen |
| Sunset / sunset | Violett/Orange, kräftige Akzente, größere Rundungen |

Auswahl wird pro Browser in localStorage gespeichert, nicht global in SQLite. Kein Schreibschlüssel nötig, da nur die eigene Darstellung geändert wird. Wenn Browser-Speicher blockiert ist, funktioniert die Auswahl für die aktuelle Seite weiterhin. Ein gültiger URL-Parameter theme hat Vorrang vor der Browser-Präferenz. View-Link übernimmt das gewählte Theme in die URL; so ist die Darstellung auch auf einem anderen Gerät oder im iFrame festgelegt. Ungültige Werte fallen auf gültige Browser-Präferenz oder Ocean zurück. Native Dropdown-Popups können je nach Betriebssystem unterschiedlich aussehen.

## URLs und Einbettung

```text
http://SERVER-IP:8288/static/view.html?theme=graphite
http://SERVER-IP:8288/?theme=paper
http://SERVER-IP:8288/?embed=1&theme=forest
```

```html
<iframe src="https://agenda.example.de/static/view.html?theme=sunset" title="Agenda" style="width:100%;height:640px;border:0;"></iframe>
```

Bestehende ?embed=1-Links bleiben nutzbar; auch dort sind Toolbar und Fußzeile ausgeblendet. FRAME_ANCESTORS, HTTPS und Proxy-Freigaben gelten weiterhin. View ist keine zusätzliche Zugriffssicherung: Die Agenda ist wie bisher öffentlich lesbar.

Nach erfolgreichem GHCR-Build das Image in Portainer neu ziehen und den Stack aktualisieren. Port 8288, highfishNetwork, Backend und SQLite-Schema bleiben unverändert. Keine Datenbankmigration. GitHub-Pages-Projektseite bleibt unverändert. Visuelle Browser-Prüfung und Docker-Laufzeitprüfung sind zum Zeitpunkt der Vorbereitung nicht bestätigt.
