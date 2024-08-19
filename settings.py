#!/usr/bin/python3
import json

class Settings:
    # Persist settings in a gardenSettings.json file
    def __init__(self):
        self._loadSettings()

    def _loadSettings(self):
        try:
            with open("settings.json", "r") as SettingsFile:
                self._settings = json.load(SettingsFile)
        except:
            self._settings = {}

    def getPORT(self):
        return self._settings.get("PORT",80)

    def getUSER(self):
        return self._settings.get("USER","")

    def getHOST(self):
        return self._settings.get("HOST","")

    def getLOADSECONDS(self):
        return self._settings.get("LOADSECONDS",30)
