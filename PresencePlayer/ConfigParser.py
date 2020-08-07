import json
import pathlib

class ConfigParser:
    def __init__(self, configPath='config.json'):
        if(configPath == 'config.json'):
            configPath = str(pathlib.Path(__file__).parent.absolute()) + '/config.json'
        print(configPath)
        self.configPath = configPath
        self.parseConfig()
        
    def parseConfig(self):
        f=open(self.configPath, "r")
        if f.mode == "r":
            self.configData = json.load(f)
            