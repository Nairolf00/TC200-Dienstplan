from tkinter import filedialog
import yaml

import tabula
import pandas
import numpy

import caldav
import datetime

import traceback


try:
    with open("config.yaml", 'r') as configFile:
        config = yaml.safe_load(configFile)
except:
    config = {}
    config["eigenerName"] = input("Eigener Name, exakt wie er im Dinestplan angezeigt wird: ")
    config["calDav"] = {}
    config["calDav"]["URL"]= input("CalDav URL: ")
    config["calDav"]["Username"] = input("CalDav / Mailaccount Username: ")
    config["calDav"]["Password"] = input("CalDav / Mailaccount Passwort: ")
    
    with open("config.yaml", 'w') as configFile:
        yaml.dump(config, configFile)



# Schichten die mit "frei ()"" angezeit werden
freiSchichten = ["X", "UT"]


# Timezone ist CopyPaste aus einem KalenderExport von Thunderbird
caldavTimezoneStr = 'BEGIN:VTIMEZONE\nTZID:Europe/Berlin\nX-TZINFO:Europe/Berlin[2024a]\nBEGIN:STANDARD\nTZOFFSETTO:+010000\nTZOFFSETFROM:+005328\nTZNAME:Europe/Berlin(STD)\nDTSTART:18930401T000000\nRDATE:18930401T000000\nEND:STANDARD\nBEGIN:DAYLIGHT\nTZOFFSETTO:+020000\nTZOFFSETFROM:+010000\nTZNAME:Europe/Berlin(DST)\nDTSTART:19160430T230000\nRDATE:19160430T230000\nEND:DAYLIGHT\nBEGIN:STANDARD\nTZOFFSETTO:+010000\nTZOFFSETFROM:+020000\nTZNAME:Europe/Berlin(STD)\nDTSTART:19161001T010000\nRDATE:19161001T010000\nEND:STANDARD\nBEGIN:DAYLIGHT\nTZOFFSETTO:+020000\nTZOFFSETFROM:+010000\nTZNAME:Europe/Berlin(DST)\nDTSTART:19170416T020000\nRRULE:FREQ=YEARLY;BYMONTH=4;BYDAY=3MO;UNTIL=19180415T020000\nEND:DAYLIGHT\nBEGIN:STANDARD\nTZOFFSETTO:+010000\nTZOFFSETFROM:+020000\nTZNAME:Europe/Berlin(STD)\nDTSTART:19170917T030000\nRRULE:FREQ=YEARLY;BYMONTH=9;BYDAY=3MO;UNTIL=19180916T030000\nEND:STANDARD\nBEGIN:DAYLIGHT\nTZOFFSETTO:+020000\nTZOFFSETFROM:+010000\nTZNAME:Europe/Berlin(DST)\nDTSTART:19400401T020000\nRDATE:19400401T020000\nEND:DAYLIGHT\nBEGIN:STANDARD\nTZOFFSETTO:+010000\nTZOFFSETFROM:+020000\nTZNAME:Europe/Berlin(STD)\nDTSTART:19421102T030000\nRDATE:19421102T030000\nEND:STANDARD\nBEGIN:DAYLIGHT\nTZOFFSETTO:+020000\nTZOFFSETFROM:+010000\nTZNAME:Europe/Berlin(DST)\nDTSTART:19430329T020000\nRDATE:19430329T020000\nEND:DAYLIGHT\nBEGIN:DAYLIGHT\nTZOFFSETTO:+020000\nTZOFFSETFROM:+010000\nTZNAME:Europe/Berlin(DST)\nDTSTART:19440403T020000\nRRULE:FREQ=YEARLY;BYMONTH=4;BYDAY=1MO;UNTIL=19450402T020000\nEND:DAYLIGHT\nBEGIN:DAYLIGHT\nTZOFFSETTO:+030000\nTZOFFSETFROM:+020000\nTZNAME:Europe/Berlin(DST)\nDTSTART:19450524T020000\nRDATE:19450524T020000\nEND:DAYLIGHT\nBEGIN:STANDARD\nTZOFFSETTO:+010000\nTZOFFSETFROM:+020000\nTZNAME:Europe/Berlin(STD)\nDTSTART:19431004T030000\nRRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=1MO;UNTIL=19441002T030000\nEND:STANDARD\nBEGIN:DAYLIGHT\nTZOFFSETTO:+020000\nTZOFFSETFROM:+030000\nTZNAME:Europe/Berlin(DST)\nDTSTART:19450924T030000\nRDATE:19450924T030000\nEND:DAYLIGHT\nBEGIN:STANDARD\nTZOFFSETTO:+010000\nTZOFFSETFROM:+020000\nTZNAME:Europe/Berlin(STD)\nDTSTART:19451118T030000\nRDATE:19451118T030000\nEND:STANDARD\nBEGIN:DAYLIGHT\nTZOFFSETTO:+020000\nTZOFFSETFROM:+010000\nTZNAME:Europe/Berlin(DST)\nDTSTART:19460414T020000\nRDATE:19460414T020000\nEND:DAYLIGHT\nBEGIN:DAYLIGHT\nTZOFFSETTO:+020000\nTZOFFSETFROM:+010000\nTZNAME:Europe/Berlin(DST)\nDTSTART:19470406T030000\nRDATE:19470406T030000\nEND:DAYLIGHT\nBEGIN:DAYLIGHT\nTZOFFSETTO:+030000\nTZOFFSETFROM:+020000\nTZNAME:Europe/Berlin(DST)\nDTSTART:19470511T030000\nRDATE:19470511T030000\nEND:DAYLIGHT\nBEGIN:STANDARD\nTZOFFSETTO:+010000\nTZOFFSETFROM:+020000\nTZNAME:Europe/Berlin(STD)\nDTSTART:19461007T030000\nRDATE:19461007T030000\nEND:STANDARD\nBEGIN:DAYLIGHT\nTZOFFSETTO:+020000\nTZOFFSETFROM:+030000\nTZNAME:Europe/Berlin(DST)\nDTSTART:19470629T030000\nRDATE:19470629T030000\nEND:DAYLIGHT\nBEGIN:DAYLIGHT\nTZOFFSETTO:+020000\nTZOFFSETFROM:+010000\nTZNAME:Europe/Berlin(DST)\nDTSTART:19480418T020000\nRDATE:19480418T020000\nEND:DAYLIGHT\nBEGIN:DAYLIGHT\nTZOFFSETTO:+020000\nTZOFFSETFROM:+010000\nTZNAME:Europe/Berlin(DST)\nDTSTART:19490410T020000\nRDATE:19490410T020000\nEND:DAYLIGHT\nBEGIN:STANDARD\nTZOFFSETTO:+010000\nTZOFFSETFROM:+020000\nTZNAME:Europe/Berlin(STD)\nDTSTART:19471005T030000\nRRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=1SU;UNTIL=19491002T030000\nEND:STANDARD\nBEGIN:DAYLIGHT\nTZOFFSETTO:+020000\nTZOFFSETFROM:+010000\nTZNAME:Europe/Berlin(DST)\nDTSTART:19800406T020000\nRDATE:19800406T020000\nEND:DAYLIGHT\nBEGIN:STANDARD\nTZOFFSETTO:+010000\nTZOFFSETFROM:+020000\nTZNAME:Europe/Berlin(STD)\nDTSTART:19800928T030000\nRRULE:FREQ=YEARLY;BYMONTH=9;BYDAY=-1SU;UNTIL=19950924T030000\nEND:STANDARD\nBEGIN:DAYLIGHT\nTZOFFSETTO:+020000\nTZOFFSETFROM:+010000\nTZNAME:Europe/Berlin(DST)\nDTSTART:19810329T020000\nRRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU;UNTIL=19960331T020000\nEND:DAYLIGHT\nBEGIN:STANDARD\nTZOFFSETTO:+010000\nTZOFFSETFROM:+020000\nTZNAME:Europe/Berlin(STD)\nDTSTART:19961027T030000\nRDATE:19961027T030000\nEND:STANDARD\nBEGIN:DAYLIGHT\nTZOFFSETTO:+020000\nTZOFFSETFROM:+010000\nTZNAME:(DST)\nDTSTART:19970330T020000\nRRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU\nEND:DAYLIGHT\nBEGIN:STANDARD\nTZOFFSETTO:+010000\nTZOFFSETFROM:+020000\nTZNAME:(STD)\nDTSTART:19971026T030000\nRRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU\nEND:STANDARD\nEND:VTIMEZONE'

def createAndSaveWholeDay(cal, name, starttime: datetime, endtime: datetime, comment=""):
    try:
        cal.save_event("""BEGIN:VCALENDAR
VERSION:2.0
PRODID:Flos-Python-Script
{}
BEGIN:VEVENT
UID:Skript-Dienstplaneintrag-{:02d}{:02d}{:02d}
DTSTART;VALUE=DATE;TZID=Europe/Berlin:{:04d}{:02d}{:02d}
DTEND;VALUE=DATE;TZID=Europe/Berlin:{:04d}{:02d}{:02d}
SUMMARY:{}
DESCRIPTION:{}
END:VEVENT
END:VCALENDAR
""".format(caldavTimezoneStr, starttime.year, starttime.month, starttime.day, starttime.year, starttime.month, starttime.day, endtime.year, endtime.month, endtime.day, name, comment))
    except Exception:
        print(traceback.format_exc())

def createAndSaveWithTime(cal, name, starttime: datetime, endtime: datetime, comment=""):
    try:
        cal.save_event("""BEGIN:VCALENDAR
VERSION:2.0
PRODID:Flos-Python-Script
{}
BEGIN:VEVENT
UID:Skript-Dienstplaneintrag-{:02d}{:02d}{:02d}
DTSTART;TZID=Europe/Berlin:{:04d}{:02d}{:02d}T{:02d}{:02d}00Z
DTEND;TZID=Europe/Berlin:{:04d}{:02d}{:02d}T{:02d}{:02d}00Z
SUMMARY:{}
DESCRIPTION:{}
END:VEVENT
END:VCALENDAR
""".format(caldavTimezoneStr, starttime.year, starttime.month, starttime.day, starttime.year, starttime.month, starttime.day, starttime.hour, starttime.minute, endtime.year, endtime.month, endtime.day, endtime.hour, endtime.minute, name, comment))
    except Exception:
        print(traceback.format_exc())



file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])


# Liest nur den Oberen Bereich aus (für die Erkennung welcher Monat vorliegt)
headerTableAll = tabula.read_pdf(file_path, pages="all", relative_area=True, area=[0, 0, 11.4984265311063, 68.753206772704], output_format="dataframe", multiple_tables=False)
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
contentTableAll = tabula.read_pdf(file_path, pages=0, relative_area=True, area=[14.6695715323166, 0, 100, 100], output_format="dataframe", multiple_tables=False)
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
    calendar = client.calendar(url="https://dav.mailbusiness.ionos.de/caldav/Y2FsOi8vMC8xNDc")

    # Löscht alle Termine in dem entsprechendem Monat
    events_fetched = calendar.search(start=zeitraumDatetime[0], end=zeitraumDatetime[1]+datetime.timedelta(days=1),event=True, expand=True)
    for event in events_fetched:
        event.delete()

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
            end = start + datetime.timedelta(days=y+1)
            createAndSaveWholeDay(calendar, "???", start, end, erstelltFormattestStr)
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
                end = start + datetime.timedelta(days=y+1)
                createAndSaveWholeDay(calendar, "FREI ("+str(itemDay[0])+")", start, end, erstelltFormattestStr)
                x+=y

            elif len(itemDay)==3: # frägt ab, ob die Schicht Uhrzeiten hat
                itemDay[1] = itemDay[1].split(":")
                itemDay[2] = itemDay[2].split(":")
                start = datetime.datetime(year,month,x+1,int(itemDay[1][0]), int(itemDay[1][1]))
                end = datetime.datetime(year,month,x+1,int(itemDay[2][0]), int(itemDay[2][1]))
                if end < start:
                    end += datetime.timedelta(days=1)
                print(itemDay)
                createAndSaveWithTime(calendar, itemDay[0], start, end, erstelltFormattestStr)
                
            else:
                createAndSaveWholeDay(calendar, itemDay[0], datetime.datetime(year, month, x+1), datetime.datetime(year, month, x+1), erstelltFormattestStr)
        
        x+=1