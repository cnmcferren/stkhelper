from scenarioobject import ScenarioObject
from toolbox import TLE_Manager

class Satellite(ScenarioObject):
    def __init__(self, guardian, name, sscNumber, startTime=None, stopTime=None):
        super().__init__(guardian,name)
        self.sscNumber = sscNumber
        
        TLE_Manager.GenerateTLE(str(sscNumber) + ".tle")
        self.tle = TLE_Manager.ParseTLE(str(sscNumber + ".tle"))        
        
        if startTime == None:
            startTime = self.guardian.reference.StartTime
        if stopTime == None:
            stopTime = self.guardian.reference.StopTime
            