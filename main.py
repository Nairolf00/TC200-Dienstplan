from tkinter import filedialog
import yaml

import tabula
import pandas
import numpy

import caldav
import datetime
import icalendar as iCal

import traceback

version = "0.1"

# Importiert die Einstellungen und fragt sie ab, falls die Datei nicht existiert
try:
    with open("config.yaml", 'r') as configFile:
        config = yaml.safe_load(configFile)
        configFile.close()
except FileNotFoundError:
    config = {}
    config["eigenerName"] = input("Eigener Name, exakt wie er im Dinestplan angezeigt wird: ")
    if input("Modus? iCal Datei oder WebDav (i/w): ") == "i":
        config["webDav"] = False
        config["calDav"] = {}
        config["calDav"]["URL"] = None
        config["calDav"]["Username"] = None
        config["calDav"]["Password"] = None
        config["CalendarURL"] = None
    else:
        config["webDav"] = True
        config["calDav"] = {}
        config["calDav"]["URL"]= input("CalDav URL: ")
        config["calDav"]["Username"] = input("CalDav / Mailaccount Username: ")
        config["calDav"]["Password"] = input("CalDav / Mailaccount Passwort: ")
        config["CalendarURL"] = input("URL zu dem einen spezifischen Kalender (!Alle Termine in den entsprechendne Monaten werden gelöscht!): ")
    
    with open("config.yaml", 'w') as configFile:
        yaml.dump(config, configFile)
        configFile.close()


# Schichten die mit "frei ()"" angezeit werden
freiSchichten = ["X", "UT"]

class iCalCreator:
    def getCalendar():
        # Timezone ist CopyPaste aus einem KalenderExport von Thunderbird
        cal = iCal.Calendar()
        cal.add('prodid', '-//Flos Scripte/TC 200 Dienstpläne/V'+version)
        cal.add('version', '2.0')
        return cal
       
    def getEventFullDays(name: str, starttime: datetime.datetime, endtime: datetime.datetime, comment: str = ""):
        endtime = endtime + datetime.timedelta(days=1)
        event = iCal.Event()
        event['uid'] = "Skript-Dienstplaneintrag-" + starttime.strftime("%Y-%m-%d")
        event.add('dtstart', starttime.date())
        event.add('dtend', endtime.date())
        event.add('summary', name)
        event.add('description', comment)
        return event

    def getEventWithTime(name: str, starttime: datetime.datetime, endtime: datetime.datetime, comment: str = ""):
        event = iCal.Event()
        event['uid'] = "Skript-Dienstplaneintrag-" + starttime.strftime("%Y-%m-%d")
        event.add('dtstart', starttime.astimezone(datetime.timezone.utc))
        event.add('dtend', endtime.astimezone(datetime.timezone.utc))
        event.add('summary', name)
        event.add('description', comment)
        return event

    def formatReadable(cal):
        return cal.to_ical().decode("utf-8").replace('\r\n', '\n').strip()
    

class webDavStorer:
    def __init__(self, calendar: caldav.DAVClient.calendar):
        self.cal = calendar
    
    def storeEvent(self, event: iCal.Event):
        try:
            self.cal.save_event(event)
        except Exception:
            print(traceback.format_exc())


inputPdfPath = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])


# Liest nur den Oberen Bereich aus (für die Erkennung welcher Monat vorliegt)
headerTableAll = tabula.read_pdf(inputPdfPath, pages="all", relative_area=True, area=[0, 0, 11.4984265311063, 68.753206772704], output_format="dataframe", multiple_tables=False)
headerTableFirst = headerTableAll[0]
# Gibt einmal die gesammt Tabelle aus
with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
    print(headerTableAll)

# Sucht erst nach der Postion von "Abteilung und Zeitraum" um dann in dem Feld direkt darunter den Eintrag zu finden, um welches Monat es sich handelt
erstelltRowIndex = headerTableFirst[headerTableFirst.apply(lambda row: row.astype(str).str.contains('Abteilung und Zeitraum', case=False).any(), axis=1)].index
erstelltColIndex = pandas.DataFrame(numpy.where(headerTableFirst.eq("Abteilung und Zeitraum"))[1], columns=['col_index'])
zeitraumString = str(headerTableFirst.iat[int(erstelltRowIndex[0])+1, erstelltColIndex.iat[0, 0]])
zeitraumDatetime = zeitraumString.split(" ", 1)[1].split(" - ")
zeitraumDatetime[0] = datetime.datetime.strptime(zeitraumDatetime[0], "%d.%m.%Y")
zeitraumDatetime[1] = datetime.datetime.strptime(zeitraumDatetime[1], "%d.%m.%Y")
year = zeitraumDatetime[0].year
month = zeitraumDatetime[0].month
print("Zeitraum:", zeitraumString, "=>", zeitraumDatetime, "=>", year, month)
lenMonat = (zeitraumDatetime[1]-zeitraumDatetime[0]).days+1
print("Länge des Monats:", lenMonat)

# Sucht nach dem Stand des Dienstplanes und formatiert diesen
erstelltRowIndex = headerTableFirst[headerTableFirst.apply(lambda row: row.astype(str).str.contains('erstellt am um', case=False).any(), axis=1)].index
erstelltColIndex = pandas.DataFrame(numpy.where(headerTableFirst.eq("erstellt am um"))[1], columns=['col_index'])
print(erstelltColIndex, erstelltRowIndex)
erstelltStrs = str(headerTableFirst.iat[int(erstelltRowIndex[0])+1, erstelltColIndex.iat[0, 0]]).split(" ")
erstelltDatetime = datetime.datetime.strptime(erstelltStrs[0]+" "+erstelltStrs[1], "%d.%m.%Y %H:%M")
erstelltFormattestStr = "Stand: "+erstelltDatetime.strftime("%d.%m.%Y %H:%M")
print(erstelltStrs, "=>", erstelltDatetime, "=>", erstelltFormattestStr)



# Erkennt den eigentlichen Bereich des Dienstplanes
contentTableAll = tabula.read_pdf(inputPdfPath, pages=0, relative_area=True, area=[14.6695715323166, 0, 100, 100], output_format="dataframe", multiple_tables=False)
contentTableFirst = contentTableAll[0]

# Gibt einmal die gesammt Tabelle aus
with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
    print(contentTableAll)


# Sucht die eigene Zeile
rowFlorian = contentTableFirst.loc[contentTableFirst.iloc[:, 0] == config["eigenerName"]]
print("meine Zeile:\n", rowFlorian)




with caldav.DAVClient(url=config["calDav"]["URL"], username=config["calDav"]["Username"], password=config["calDav"]["Password"]) as client:
    my_principal = client.principal()
    calendars = my_principal.calendars()
    calendar = client.calendar(url=config["CalendarURL"])

    # Löscht alle Termine in dem entsprechendem Monat
    events_fetched = calendar.search(start=zeitraumDatetime[0], end=zeitraumDatetime[1]+datetime.timedelta(days=1),event=True, expand=True)
    for event in events_fetched:
        event.delete()

    cal = iCalCreator.getCalendar()
    webDav = webDavStorer(calendar)
    
    # Iteriert durch alle Tage des Monats (eigener Zähler, da freischichten Gruppiert werden und dadurch Tage übersprungen werden)
    x=0
    while x < lenMonat:
        itemDay = rowFlorian.iat[0, x+1]
        print(itemDay)

        # Erkennt noch nicht geplante Tage, gruppiert aufeinanderfolgende und Trägt "???" ein
        if type(itemDay) != str:
            y=0
            while x+y+1 < lenMonat:
                if type(rowFlorian.iat[0, x+1+y+1]) != str:
                    y += 1
                else:
                    break
            print(str(x+1)+": itemDay ist kein String!; y=", y)
            start = datetime.datetime(year, month, x+1)
            end = start + datetime.timedelta(days=y)
            event = iCalCreator.getEventFullDays("???", start, end, erstelltFormattestStr)
            cal.add_component(event)
            webDav.storeEvent(event)
            x+=y
                
        else:
            itemDay = itemDay.split("\r")
            print(str(x+1)+":", itemDay, " -  ", end='')

            # Sortiert Freischichten aus, gruppiert aufeinanderfolgende und Trägt "frei (Name der Schicht)" ein
            # Sollten untershciedlich benannt Freischichten aufeinander Folgen wird dies falsch erkannt
            if itemDay[0] in freiSchichten:
                y=0
                while x+y+1 < lenMonat:
                    itemNextDay = rowFlorian.iat[0, x+1+y+1]
                    if type(itemNextDay) != str:
                        break
                    itemNextDay = itemNextDay.split("\r")
                    if itemNextDay[0] in freiSchichten:
                        y += 1
                    else:
                        break
                print("frei; y=", y)
                start = datetime.datetime(year, month, x+1)
                end = start + datetime.timedelta(days=y)
                event = iCalCreator.getEventFullDays("FREI ("+str(itemDay[0])+")", start, end, erstelltFormattestStr)
                cal.add_component(event)
                webDav.storeEvent(event)
                x+=y

            elif len(itemDay)==3: # frägt ab, ob die Schicht Uhrzeiten hat
                itemDay[1] = itemDay[1].split(":")
                itemDay[2] = itemDay[2].split(":")
                start = datetime.datetime(year,month,x+1,int(itemDay[1][0]), int(itemDay[1][1]))
                end = datetime.datetime(year,month,x+1,int(itemDay[2][0]), int(itemDay[2][1]))
                if end < start:
                    end += datetime.timedelta(days=1)
                print(itemDay)
                event = iCalCreator.getEventWithTime(itemDay[0], start, end, erstelltFormattestStr)
                cal.add_component(event)
                webDav.storeEvent(event)
                
            else:
                event = iCalCreator.getEventWithTime(itemDay[0], datetime.datetime(year, month, x+1), datetime.datetime(year, month, x+1), erstelltFormattestStr)
                cal.add_component(event)
                webDav.storeEvent(event)
        
        x+=1
    
    
print(iCalCreator.formatReadable(cal))
outICalPath = filedialog.asksaveasfilename(filetypes=[("iCalFiles", "*.ics")])
with open(outICalPath, 'wb') as iCalFile:
    iCalFile.write(cal.to_ical())
    iCalFile.close()