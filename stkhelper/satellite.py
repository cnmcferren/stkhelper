from stkhelper.scenarioobject import ScenarioObject
from stkhelper.toolbox import TLE_Manager

from comtypes import COMError
from comtypes.gen import STKObjects

class Satellite(ScenarioObject):
    def __init__(self, guardian, name, sscNumber, startTime=None, stopTime=None):
        super().__init__(guardian,name)
        self.sscNumber = sscNumber
        self.name = name
        self.path = "*/Satellite/" + name
    
        self.root = guardian.guardian.root    
        TLE_Manager.GenerateTLE(self.root, str(sscNumber))
        self.tle = TLE_Manager.ParseTLE(str(sscNumber) + ".tle") 
        
        if startTime == None:
            startTime = self.guardian.reference.StartTime
        if stopTime == None:
            stopTime = self.guardian.reference.StopTime
            
        self.reference = self.root.CurrentScenario.Children.New(STKObjects.eSatellite, name)

        command = 'SetState */Satellite/' + self.name + ' TLE "' + \
                self.tle[0] + '" "' + self.tle[1] + \
                '" TimePeriod "' + \
                startTime + '" "' + \
                stopTime + '"'
        try:                                 
            self.root.ExecuteCommand(command)
        except COMError:
            raise RuntimeError("Failure to add satellite. Check formatting of TLE.")
            
    def GetAccess(self,scenarioObject):
        self.root.BeginUpdate()
        access = super().GetAccess(scenarioObject)
        self.root.EndUpdate()
        
        return access
    
    def GetPower(self,startTime,endTime,timestep,radius,outputPath):
        command = 'VO %s SolarPanel Visualization Radius On %f' % (self.path,radius)
        self.root.ExecuteCommand(command)
        command = 'VO %s SolarPanel Compute "%s" "%s" %i Power "%s"' % \
                    (self.path,startTime,endTime,timestep,outputPath)
                    
        self.root.ExecuteCommand(command)
        
    def SetModel(self,modelFile):
        command = 'VO %s Model File "%s"' % (self.path,modelFile)
        self.root.ExecuteCommand(command)
        
    def SetAttitude(self,profile):
        #TODO account for offset
        command = 'SetAttitude %s Profile %s Offset 0 0 0' % (self.path,profile)
        self.root.ExecuteCommand(command)