
from win32api import GetSystemMetrics
from comtypes.client import CreateObject
from comtypes.gen import STKObjects
from comtypes import COMError

import os

from toolbox import TLE_Manager, Toolbox

class AreaTarget:
    
    def __init__(self, scenario, parsedLine):
        self.__guardian = scenario
        
        root = self.__guardian.GetGuardian().root
        
        root.BeginUpdate()
        
        self.ID = parsedLine[1]
        startLat = parsedLine[8]
        startLon = parsedLine[9]
        endLat = parsedLine[10]
        endLon = parsedLine[11]
        
        self.center =Toolbox.ComputeCenterTarget(parsedLine)

        self.areaTarget = root.CurrentScenario.Children.New(STKObjects.eAreaTarget,self.ID)
        self.areaTarget = self.areaTarget.QueryInterface(STKObjects.IAgAreaTarget)
        self.areaTarget.AreaType = STKObjects.ePattern
        self.patterns = self.areaTarget.AreaTypeData
        self.patterns = self.patterns.QueryInterface(STKObjects.IAgAreaTypePatternCollection)
        
        self.patterns.Add(startLat,startLon)
        self.patterns.Add(startLat,endLon)
        self.patterns.Add(endLat,endLon)
        self.patterns.Add(endLat,startLon)
        self.areaTarget.AutoCentroid = True
        
        root.EndUpdate()
        
    def GetGuardian(self):
        return self.__guardian
    
class Camera:
    
    def __init__(self, hostSat, name, fov):
        self.__guardian = hostSat
        
        if not ((type(fov[0]) == int or type(fov[0]) == float) and
                (type(fov[1]) == int or type(fov[1]) == float)):
            raise TypeError, "Field of View parameters of invalid type."
        
        root = self.__guardian.GetGuardian().root
        
        root.BeginUpdate()
        
        self.cameraGeneral = self.__guardian.Children.New(20,name)
        self.camera = cameraGeneral.QueryInterface(STKObjects.IAgSensor)
        self.camera.CommonTasks.SetPatternRectangular(fov[0],fov[1])
        
        root.EndUpdate()
        
    def GetGuardian(self):
        return self.__guardian

class Satellite:

    def __init__(self, scenario, name, sscNumber):
        self.__guardian = scenario.GetGuardian()
        root = self.__guardian

        TLE_Manager.GenerateTLE(self.__guardian, str(sscNumber))
        tle = TLE_Manager.ParseTLE(str(sscNumber) + ".tle")
        
        try:
            self.satellite = root.CurrentScenario.Children.New(STKObjects.eSatellite, name)
        except COMError:
            raise (RuntimeError,'\nIncorrect name format or name already taken for satellite.' + 
                  ' Please do not use spaces or reuse satellite names.')
            
        try:
            root.ExecuteCommand('SetState */Satellite/' + name + ' TLE "' +
                                     tle[0] + '" "' + tle[1] +
                                     '" TimePeriod "' +
                                     self.__guardian.StartTime + '" "' +
                                     self.__guardian.StopTime + '"')
        except COMError:
            raise (RuntimeError, "Failure to add satellite. Check formatting of TLE.")
            
    def GetGuardian(self):
        return self.__guardian
