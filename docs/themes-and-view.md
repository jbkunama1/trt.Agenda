# Fünf Agenden mit gespeicherten Themes

Es gibt fünf feste Agenda-Plätze 1–5. Agenda 1 enthält die bisherige Agenda; 2–5 starten leer mit Titel Agenda 2 usw. Im Dropdown auswählen, Bearbeiten öffnen, Titel/Startzeit/Punkte/Theme setzen und Speichern. Platz wieder leeren: Punkte entfernen, Titel anpassen und speichern. Kein physisches Löschen, keine dynamischen IDs.

Themes Ocean, Graphite, Paper, Forest und Sunset sind unverändert verfügbar, jetzt ausschließlich im Bearbeitungsbereich. Theme wird mit der Agenda in SQLite gespeichert. View und iFrame verwenden immer das gespeicherte Theme. Keine Browser-Präferenz und kein theme-URL-Override mehr. Bisherige lokale Auswahl wird nicht migriert; nach dem Update gewünschtes Theme einmal im Editor speichern.

Beim Bearbeiten ist die Agenda-Auswahl gesperrt. Theme ist vor Speichern nur Vorschau im Editor; View bleibt auf dem gespeicherten Stand. Abbrechen lädt Datenbankstand neu. Schreibschlüssel gilt für alle fünf Agenden. Jede Agenda hat eigenen Versionskonfliktschutz.

## Links

```text
http://SERVER-IP:8288/?agenda=2
http://SERVER-IP:8288/static/view.html?agenda=2
http://SERVER-IP:8288/?embed=1&agenda=2
```

```html
<iframe src="https://agenda.example.de/static/view.html?agenda=2" title="Agenda 2" style="width:100%;height:640px;border:0;"></iframe>
```

Ohne agenda-Parameter wird Agenda 1 angezeigt. Alte Links bleiben so für Agenda 1 nutzbar. Alte theme-Parameter werden ignoriert. View zeigt nur gespeicherte Agenda, aktualisiert alle 15 Sekunden, enthält keine Toolbar, keine Theme-Auswahl und keine Fußzeile. Ungültige Agenda-ID zeigt Fehler, nicht eine andere Agenda.

## Migration und Update

Vor Update SQLite sichern. Beim ersten Datenbankzugriff entsteht Tabelle agendas mit IDs 1–5. Die alte Tabelle agenda bleibt unverändert erhalten; body und version von Agenda 1 werden übernommen, theme wird standardmäßig ocean. INSERT OR IGNORE verhindert späteres Überschreiben. Die alte Tabelle ist nur Altbestand, keine laufende Sicherung. Nach Migration keine alte App-Version zum Bearbeiten verwenden: sie schreibt in die alte Tabelle und Änderungen würden auseinanderlaufen. Rückkehr nur mit bewusstem Backup-/Restore-Plan.

Port 8288, Netzwerk highfishNetwork und Volume agenda_data bleiben gleich. Nach erfolgreichen CI-Tests/GHCR-Build neues Image ziehen und Stack aktualisieren. Migration läuft beim App-Zugriff auf dem Zielserver, nicht beim GitHub-Upload. Tests für Migration, fünf getrennte Agenden, Themes und Konflikte sind enthalten; CI-Erfolg, Live-Migration und Browserdarstellung noch nicht bestätigt. GitHub-Pages-Projektseite ist weiterhin eine statische Präsentation und wird mit dieser Änderung nicht aktualisiert.
