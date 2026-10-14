# Farbiger PDF- und JPG-Export

In der normalen App die Agenda 1–5 auswählen und PDF ↓ oder JPG ↓ anklicken. Export lädt ausdrücklich den zuletzt gespeicherten Datenbankstand und das gespeicherte Theme. Vor Export Änderungen einschließlich Theme speichern. Die reine View-Seite und embed=1 bleiben ohne Export-Buttons.

## Formate

- JPG: 1440 Pixel breit, variable Höhe für alle Punkte, farbiger Gradient und Karten im gespeicherten Theme, JPEG-Qualität 94 %. Lange Agenden ergeben ein langes Bild. Sehr speicherarme Geräte können bei großen Agenden an Canvas-Grenzen stoßen; dann PDF verwenden.
- PDF: A4-Hochformat, 1440 × 2036 Pixel pro gerasterter Seite (etwa 174 dpi), bei langen Agenden mehrere Seiten. Punkte werden nicht zwischen Seiten geteilt. Titel und Zusammenfassung wiederholen sich, Seitenzählung unten. Bildbasiertes PDF: Text nicht suchbar oder auswählbar; keine PDF-Barrierefreiheit zugesichert.

Titel, Nummern, Punkte, Zeiten und Dauern werden exportiert; keine Bedienfelder. Alle fünf Theme-Paletten werden übernommen, Layout für Export eigenständig gezeichnet (kein pixelgenauer Browser-Screenshot). Lange Titel werden umgebrochen. Darstellung beliebiger Emoji/Schriften hängt von installierten Systemfonts ab. Standardtext einschließlich deutscher Umlaute nutzt Browser-Fontrendering.

Dateinamen enthalten Agenda-ID und bereinigten Titel. Download erfolgt lokal im Browser ohne zusätzliche Bibliotheken/CDNs oder externe Exportdienste. Kein Bearbeitungsschlüssel nötig, da Agenden ohnehin öffentlich lesbar sind. Export erzeugt keine Datenbankänderung. Die Dateien sind statische Momentaufnahmen und können offline in einer Bildanzeige bzw. einem PDF-Reader geöffnet werden; spätere Agenda-Änderungen sind nicht enthalten. Manche mobile Browser öffnen die Datei zunächst in ihrer Vorschau statt sie direkt abzulegen.

## Update und Prüfstatus

Nach erfolgreichem GHCR-Build Image in Portainer neu ziehen und Stack aktualisieren. Keine neuen Python-Abhängigkeiten, Backend-Routen oder Datenbankmigrationen für diese Export-Erweiterung. Aktuelle Docker-Compose unverändert. Browser-Downloads, Rendering und PDF-Reader-Kompatibilität sind bei Vorbereitung noch nicht praktisch geprüft. README und Pages-Projektseite wurden in diesem Export-Commit nicht angepasst; diese Anleitung beschreibt den neuen Export.
