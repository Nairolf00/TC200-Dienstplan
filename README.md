_(Unfortunately, the script is only commented in German, as all potential users are employees of a company in Germany.)_


ACHTUNG DAS SCRIPT LÖSCHT ALLE TERMINE IN DEM KALENDER! (für den Monat, der eingelesen wird)

# Requirments
PYTHON für das eigentliche Skript
JAVA für tabula

# Was macht das Skript
1. Versucht die Einstellungen aus config.ini zu importieren, wenn das Settings file nicht existiert werden die gewünschten Einstellungen in der Console abgefragt. (ACHTUNG, die Einstellungen werden im Klartext gespeichert, das Eingeben des Email-Passwortes ist auf eigenen Gefahr)
2. Öffnet ein PDF, wie es von TC 200 erstellt wird
3. übergibt dieses an die Tabula Library, die es in einen Dataframe verwandelt. (Man kann Seiten und Bereiche angeben, tatsächlich wird der Header und die eigentlich Dienstplan-Tabelle getrennt ausgelesen) (Alle Seiten werden einzeln eingelesen)
4. Sucht nach dem eigenen Namen in den Ergebnissen und merkt sich die ganze Zeile (wenn die Anzahl an Treffern nicht ein einziger ist, wird das Programm abgebrochen.)
5. Iteriert durch die Tage, erstellt ein iCal daraus und versucht dieses per CalDAV hochzuladen. (Beides passiert Tag für Tag => Wenn CalDAV fehlschlägt funktioniert auch das iCal nicht)
6. Versucht dwenn das Eingestellt ist das iCal zu speichern
