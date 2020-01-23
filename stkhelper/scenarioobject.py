from win32api import GetSystemMetrics
from comtypes.client import CreateObject
from comtypes.gen import STKObjects

class ScenarioObject:
    def __init__(self, guardian, name):
        self.guardian = guardian
        self.name = name
        
    def GetAccess(self,scenarioObject):
        access = self.reference.GetAccessToObject(scenarioObject.reference)
        access.ComputeAccess()
        intervalCollection = access.ComputedAccessIntervalTimes
        
        try:
            computedIntervals = intervalCollection.ToArray(0,-1)
            self.root.EndUpdate()

            return computedIntervals
        
        except Exception:
            self.root.EndUpdate()

            return 0