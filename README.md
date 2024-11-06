_(Unfortunately, the script is only commented in German, as all potential users are employees of a company in Germany.)_


__ACHTUNG DAS SCRIPT LÖSCHT ALLE TERMINE IN DEM KALENDER! (für den Monat, der eingelesen wird)__

# Verwendung
1. Das Script ist in [Python 3 (getestet mit Version 3.12.0)](https://www.python.org/downloads/release/python-3126/) geschrieben und der Teil, der das PDF auswertet benötigt [JAVA](https://www.java.com/de/) -> beides muss vorab instaliert werden
3. Unter Windows kann das Skript mit _run.bat_ ausgeführt werden, auf anderen Plattformen muss man händisch _main.py_ starten (Das funktioniert nur, wenn davor die virtuelle Python umgebung (VENV) aktiviert wurde) 
3. Bei erstmaliger Ausführung werden die gewünschten Einstellungen abgefragt. Manche Optionen bieten eine Auswahl an, die mit den Pfeiltasten selektiert werden können, mache sind Texteingaben
    - Der eigenen Name: Dieser wird verwendet, um die eigene Zeile im Dinstplan zu finden muss also genau so angegeben werden, wie er im PDF steht (vermutlich _Nachname, Vorname_), sollte das Ende abgeschnitten sein, so ist es auch hier unvollständig anzugeben
    - Soll das Hochladen mittels CalDAV aktiviert werden?: CalDAV ist ein Protokoll, mit dem Kalender bei manchen Anbietern hochgeladen werden können. Ist diese Option aktivert, müssen die entsprechenden Zugangsdaten angegeben werden, damit das Skript funktioniert.
    - Sollen die Termine als iCal gespeichert werden?: .iCal ist die standard Kalender Datei, die quasi überall importiert werden kann. Sollte selbst kein CalDAV nutzen, ist das hier die Option. (es wird jedes mal nachgefragt, wo die Datei gespeichert werden soll.)
    - Soll bei jedem Start gefragt werden, ob die Einstellungen geändert werden sollen?: Ist das deaktiviert gibt es keine Möglichkeit mehr, die Einstellungen über den Dialog zu ändern, dann müssen sie entweder händisch in config.ini angepasst werden, oder config.ini im gesammten gelöscht werden (dann werden wieder alle abgefragt) (Die Option existiert bloß, da bei mir in VSCode, der Dialog, zum PDF auswählen nicht öffnet, wenn ich davor einmal in das Terminal geklicht habe (was man bracht um auszuwählen, ob man die Einstellungen ändern möchte) wo anders sollte das Problem nicht existieren.)
    - Wenn CalDAV aktiviert ist, werden zusätlich diese Einstellungen abgefragt:
        - URL für CalDAV: Das ist die URL, die zu dem exakten Kalender führt, in dem die Termine hochgeladen werden sollen (ACHTUNG: In dem im PDF erkannten Monat werden alle Termine in dem einen Kalender gelöscht (um bei mehrmaliger Ausführung nicht die Termine doppelt zu haben))
        - Username: Bei mir ist das meine e-Mail

        - Password: Bei mir ist das das Passwort zu meinem Mail-Account (Die Einstellungne werden im Klartext gespeichert, es ist bestimmt nicht schlau hier die kompletten Zugangsdaten zu seinem Mailkonto einzugeben, aber ich habe keine bessere Option, vlt. habt ihr ja auch eigenen Zugansdaten für den Kalender)
4. Es sollte sich ein Filedialog öffnen, mit dem ihr ein PDF auswählen könnt (Das muss zuvor natürlich aus dem TC200 heruntergeladen werden)
5. Das Skript braucht durchaus paar Sekunden zum rechen und spuckt derzeit dabei noch wild Diagnose-Daten aus
6. Je nach Einstellung lädt es jetzt alle gefunden Termine hoch und öffnet am Ende noch einen Filedialog, der euch fragt, wo die erstellte iCal Datei gespeichert werden soll


# Was macht das Skript
1. Versucht die Einstellungen aus config.ini zu importieren, wenn das Settings file nicht existiert werden die gewünschten Einstellungen in der Console abgefragt. [Passwort Sicherheit](#Passwort-Sicherheit)
2. Öffnet ein PDF, wie es von TC 200 erstellt wird
3. übergibt dieses an die Tabula Library, die es in einen Dataframe verwandelt. (Man kann Seiten und Bereiche angeben, tatsächlich wird der Header und die eigentlich Dienstplan-Tabelle getrennt ausgelesen) (Alle Seiten werden einzeln eingelesen)
4. Sucht nach dem eigenen Namen in den Ergebnissen und merkt sich die ganze Zeile (wenn die Anzahl an Treffern nicht ein einziger ist, wird das Programm abgebrochen.)
5. Iteriert durch die Tage, erstellt ein iCal daraus und versucht dieses per CalDAV hochzuladen. (Beides passiert Tag für Tag => Wenn CalDAV fehlschlägt funktioniert auch das iCal nicht)
6. Versucht wenn das eingestellt ist das iCal zu speichern

## Reqirements
- Python 3.12 (andere Versionen sind ungetestet)
    - Die virtuelle Umgebung ist mit in dem Repo
- Java

## Passwort Sicherheit
Die Passwörter werden erst verschlüsselt (der Schlüssel dazu liegt in config.ini) und danach im Keyring von Windwos gespeichert.

D.h. ein potenzieller Angriff muss unter dem entsprechendem Benutzer-Konto ausgeführt werden, um überhaupt an die Passwörter zu kommen und es benötigt eine gezielten Angriff auf dieses Skript um sie dann auch zu entschlüsseln, sie werden nicht in Klartext gespeichert.

(Ich kann derzeit noch nicht ausschließen, dass sie nicht doch irgendwo in Logs der Konsole gespeichert werden, das überprüfe ich noch bei Gelegenheit)