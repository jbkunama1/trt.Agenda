# Agenda-View automatisch in den iFrame einpassen

Die reine View-Seite erkennt ab diesem Stand die Einbettung in einen iFrame und passt die Agenda proportional an dessen verfügbare Breite und Höhe an. Erst kompakteres Layout, dann bei Bedarf Skalierung. Inhalte werden nicht durch bloßes Verstecken einer Scrollleiste abgeschnitten. Bei Größenänderung, geladenen Fonts und aktualisierten Agenda-Punkten wird neu gemessen. Keine Kommunikation oder DOM-Zugriffe auf die Elternseite nötig.

Die vorhandene URL bleibt verwendbar:

```text
http://192.168.178.21:8288/static/view.html?agenda=1
```

Optional explizit:

```html
<iframe src="http://192.168.178.21:8288/static/view.html?agenda=1&fit=1" title="Agenda" style="display:block;width:100%;height:420px;border:0;"></iframe>
```

fit=1 erzwingt Einpassung auch ohne iFrame. fit=0 deaktiviert Einpassung und erlaubt wieder normales Scrollen. Ohne Parameter automatisch nur im iFrame aktiv. Gilt für alle fünf Agenden und gespeicherten Themes. Editor, PDF-/JPG-Export und Datenbank unverändert; alte ?embed=1-Ansicht erhält diesen Fit-Modus nicht, dafür die reine /static/view.html verwenden.

Die Höhe des äußeren iFrames wird weiterhin von der einbettenden Seite bestimmt; diese Erweiterung vergrößert sie nicht. Bei sehr kleinen Rahmen oder vielen Punkten kann Text sehr klein werden. Für bessere Lesbarkeit größeren Rahmen wählen oder fit=0 mit Scrollen verwenden. Umgebende Seite kann unabhängig vom iFrame weiter scrollen. HTTPS-/CSP-/FRAME_ANCESTORS-Regeln gelten unverändert.

Nach erfolgreichem GHCR-Build neues Image in Portainer ziehen und Stack aktualisieren, dann View neu laden. Lokale URL konnte bei Vorbereitung nicht extern abgerufen werden. Praktische Browser-/iFrame-Prüfung und CI-Erfolg sind noch nicht bestätigt.
