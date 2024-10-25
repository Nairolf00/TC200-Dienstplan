ACHTUNG DAS SCRIPT LÖSCHT ALLE TERMINE IN DEM KALENDER! (für den Monat, der eingelesen wird)

JAVA wird von Tabula benötigt.


_(Unfortunately, the script is only commented in German, as all potential users are employees of a company in Germany.)_

# Was macht das Skript
1. Versucht Einstellungen zu importieren, wenn das Settings file nicht existiert werden die gewünschten Einstellungen in der Console abgefragt. (Die Einstellung sind nicht hier in dem git, da dort Passw(rtwe in Klartext gespeichert werden
2. Öffnet ein PDF, wie es von TC 200 erstellt wird
3. übergibt dieses an die Tabula Library, die es in einen Dataframe verwandelt. (Man kann Seiten und Bereiche angeben, tatsächlich wird der Header und die eigentlich Dienstplan-Tabelle getrennt ausgelesen) (Alle Seiten werden einzeln eingelesen)
4. Sucht nach dem eigenen Namen in den Ergebnissen und merkt sich die ganze Zeile (wenn die Anzahl an Treffern nicht ein einziger ist, wird das Programm abgebrochen.
5. Iteriert durch die Tage, erstellt ein iCal daraus und versucht dieses per CalDAV hochzuladen. (Beides passiert Tag für Tag => Wenn CalDAV fehlschlägt funktioniert auch das iCal nicht
6. Versucht das iVal als Datei zu speichern
