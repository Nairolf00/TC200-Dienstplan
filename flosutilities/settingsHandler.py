import flosutilities.fancyInput as fancyInput
import configparser



configError = False
configPromtChange = False

class settingsHandler():
    def __init__(self, configStructure, configFile):
        """Legt eine Instanz an, speichert Dateinamen der Konfig-Datei und die erwartete Struktur die aktuelle Konfiguration liegt ind er Varialbel currentConfig und ist erstmals noch leer
        configStructure = {
            "SECTION1":{
                "key1": {
                    "hint": "Text, der dem Nutzer beim eingeben der Konfig angezeigt wird",
                    "type": str / bool / int,
                    "default": ""},
                "key2": {
                    "hint": "Text, der dem Nutzer beim eingeben der Konfig angezeigt wird",
                    "type": bool,
                    "default": False},
            },
            "SECTION2": {
                "key1": {
                    "hint": "Eintrag mit FancyInput multiple choise",
                    "type": int,
                    "default": 2},
                    "options": [("NEIN", "nein"), ("JEDES MAL FRAGEN", "jedes mal fragen"), ("JA", "ja")]
            }
        }

        Args:
            configStructure (dict): erwartet den Aufbau der Konfig Datei
            configFile (str): Dateiname, der Konfig-Datei
        """
        self.configFromFile = configparser.ConfigParser()
        self.configFromFile.read(configFile)
        self.configStructure = configStructure
        self.currentConfig = {}
    
    
    def checkFileIsComplete(self):
        """Überprüft ob alle Einstellungen in der SettingsDatei vorhanen sind (laut configStructure)

        Returns:
            bool: False, wenn min. 1 Element fehlt
        """
        configError = False
        for section in self.configStructure:
            if self.checkSectionIsComplete(section):
                configError = True
                break
        return configError
    
    
    def checkSectionIsComplete(self, section):
        """Überprüft ob alle Einstellungen in einer Sektion da sind (laut configStructure)

        Args:
            section (str): Die zu überprüfende Sektion

        Returns:
            bool: False, wenn min. 1 Element fehlt
        """
        configError = False
        if not section in self.configFromFile:
            configError = True
        else:
            for key in self.configStructure[section]:
                if not key in self.configFromFile[section]:
                    configError = True
                    break
        return configError
    

    def loadConfiguration(self):
        """Lädt die Einstellungen aus dem File, fehlt sie dort, wird auf den default Wert aus dem configStructure zurückgegriffen.
        Die Konfig wird sowhol zurückgegeben, als auch in der Variabel currentConfig gespeichert

        Returns:
            dict: Die gesammte Konfiguration
        """
        foundConfig = {}
        # Setzt currentConfig auf die dafault Werte
        for section in self.configStructure:
            foundConfig[section] = self.loadSection(section)
        return foundConfig
    
    
    def loadSection(self, section):
        """Lädt die Einstellungen einer bestimmten Sektion aus dem File, fehlt sie dort, wird auf den default Wert aus dem configStructure zurückgegriffen.
        Die Konfig wird sowhol zurückgegeben, als auch in der Variabel currentConfig gespeichert

        Args:
            section (str): Die zu ladende Sektion

        Returns:
            dict: Die entsprechende Sektion
        """
        foundConfig = {}
        # Setzt currentConfig auf die dafault Werte
        for key in self.configStructure[section]:
            foundConfig[key] = self.configStructure[section][key]["default"]
        
        # Frägt die Einstellungen aus dem File ab und setzt diese, falls vorhanden
        if section in self.configFromFile:
            for key in self.configStructure[section]:
                if key in self.configFromFile[section]:
                    if self.configStructure[section][key]["type"] == str:
                        valueFromFile = self.configFromFile[section][key]
                    elif self.configStructure[section][key]["type"] == bool:
                        valueFromFile = self.configFromFile[section].getboolean(key)
                    elif self.configStructure[section][key]["type"] == int:
                        valueFromFile = self.configFromFile[section].getint(key)
                    foundConfig[key] = valueFromFile
        self.currentConfig[section] = foundConfig
        return foundConfig


    def changeConfig(self, saveFile = True):
        """Frägt sämtliche Einstellungen vom Nutzer ab und setzt sie in currentConfig

        Args:
            saveFile (bool, optional): Ob die Einstellungsdatei direkt mit den neuen Einstellungen gespeichert werden soll. Defaults to True.
        """
        for section in self.configStructure:
            self.changeConfigSection(section, False)
        self.saveConfigFile()
            
            
    def changeConfigSection(self, section, saveFile = True):
        """Frägt sämtliche Einstellungen einer Sektion vom Nuter ab und setzt sie in currentConfig

        Args:
            section (str): Die abzufragnede Sektion
            saveFile (bool, optional): Ob die Einstellungsdatei direkt mit den neuen Einstellungne gespeichert werden soll. Defaults to True.

        Raises:
            Exception: Falls die Sektion nicht in der configStructure, die gegeben wurde existiert
            Exception: Falls in der configStructure ein Typ gegeben wurde, der nicht bekannt ist
        """
        if not section in self.configFromFile:
            self.configFromFile[section] = {}
        if not section in self.currentConfig:
            if not section in self.configStructure:
                raise Exception("Diese Sektion exisitiert nicht in der vorgegebenen Struktur!")
            else:
                self.currentConfig[section] = {}
        for key in self.configStructure[section]:
            if self.configStructure[section][key]["type"] == str:
                newValue = input(self.configStructure[section][key]["hint"] + ": ")
            elif self.configStructure[section][key]["type"] == bool:
                newValue = fancyInput.inputYesNo(self.configStructure[section][key]["hint"], bool(self.currentConfig[section][key]))
            elif self.configStructure[section][key]["type"] == int and "options" in self.configStructure[section][key]:
                newValue = fancyInput.inputFromSelection(self.configStructure[section][key]["hint"], self.configStructure[section][key]["options"], int(self.currentConfig[section][key]))
            elif self.configStructure[section][key]["type"] == int:
                newValue = int(input(self.configStructure[section][key]["hint"] + ": "))
            else:
                raise Exception("Der type, der Einstellung ist nicht bekannt!")
            self.currentConfig[section][key] = newValue
            self.configFromFile[section][key] = str(newValue)
        if saveFile == True:
            self.saveConfigFile()


    def saveConfigFile(self):
        """speichert die Einstellungsdatei
        """
        with open('config.ini', 'w') as configfile:
            self.configFromFile.write(configfile)