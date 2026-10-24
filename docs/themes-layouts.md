# Themes, Layouts, Emoji, Link kopieren

Themes (13): ocean, graphite, paper, forest, sunset (unveraendert) sowie 70s, 80s, 90s, modern, cyberpunk, neon, terminal, pastell.

Layouts (4, mit jedem Theme kombinierbar, pro Agenda in SQLite gespeichert): list, columns, timeline (Breite proportional zur Dauer), tiles. Im Editor wird immer die Listenansicht gezeigt; das Layout gilt nach dem Speichern in Ansicht und View/iFrame.

Emoji: pro Punkt optional (max. 16 Zeichen), ersetzt die Nummer im Badge, wird auch im PDF/JPG-Export gezeichnet.

Link kopieren: Button Link kopiert die View-URL, Button iFrame kopiert den fertigen iframe-Code fuer die gewaehlte Agenda. Ohne HTTPS nutzt die Seite einen Fallback (execCommand).

Keine Migration noetig: Datensaetze ohne layout erhalten list. Externe Bilder (Unsplash) sind bewusst nicht enthalten, CSP bleibt 'self'.
