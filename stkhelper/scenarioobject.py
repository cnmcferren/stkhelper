from win32api import GetSystemMetrics
from comtypes.client import CreateObject
from comtypes.gen import STKObjects

class ScenarioObject:
    def __init__(self, guardian, name):
        self.guardian = guardian
        self.name = name