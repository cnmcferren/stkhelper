
from win32api import GetSystemMetrics
from comtypes.client import CreateObject
from comtypes.gen import STKObjects
from comtypes import COMError

import os

from toolbox import TLE_Manager, Toolbox

class AreaTarget:
    
    def __init__(self, scenario, parsedLine):
        self.__guardian = scenario
        
        root = self.__guardian.root
        
        root.BeginUpdate()
        
        self.ID = parsedLine[1]
        startLat = parsedLine[8]
        startLon = parsedLine[9]
        endLat = parsedLine[10]
        endLon = parsedLine[11]
        
        self.center =Toolbox.ComputeCenterTarget(parsedLine)

        self.__areaTarget = root.CurrentScenario.Children.New(STKObjects.eAreaTarget,self.ID)
        self.__areaTarget = self.__areaTarget.QueryInterface(STKObjects.IAgAreaTarget)
        self.__areaTarget.AreaType = STKObjects.ePattern
        self.__patterns = self.__areaTarget.AreaTypeData
        self.__patterns = self.__patterns.QueryInterface(STKObjects.IAgAreaTypePatternCollection)
        
        self.__patterns.Add(startLat,startLon)
        self.__patterns.Add(startLat,endLon)
        self.__patterns.Add(endLat,endLon)
        self.__patterns.Add(endLat,startLon)
        self.__areaTarget.AutoCentroid = True
        
        root.EndUpdate()

    def GetTarget(self):

        return self.__areaTarget

    def GetPatterns(self):

        return self.__patterns

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
        
        self.__cameraGen = self.__guardian.Children.New(20,name)
        self.__camera = __cameraGen.QueryInterface(STKObjects.IAgSensor)
        self.__camera.CommonTasks.SetPatternRectangular(fov[0],fov[1])
        
        root.EndUpdate()
       
    def GetAccess(self, areaTarget):

        root = self.__guardian.GetGuardian().root
        
        root.BeginUpdate()

        access = self.__cameraGen.GetAccessToObject(areaTarget.GetTarget())
        access.ComputeAccess()
        intervalCollection = access.ComputedAccessIntervalCollection
        try:
            computedIntervals = intervalCollection.ToArray(0,-1)
            root.BeginUpdate()

            return computedIntervals
        except:
            root.BeginUpdate()

            return 0

    def ComputeDSInfo(self, areaTarget, passArray):

        startTime = passArray[0]
        endTime = passArray[1]

        keplerians = self.ComputeKeplerians(startTime)

        return [areaTarget.ID, areaTarget.center, keplerians, (startTime, endTime)]

    def GetGuardian(self):
        return self.__guardian

class Satellite:

    def __init__(self, scenario, name, sscNumber):
        self.__guardian = scenario.GetGuardian()
        self.name = name

        root = self.__guardian.root

        TLE_Manager.GenerateTLE(self.__guardian, str(sscNumber))
        self.tle = TLE_Manager.ParseTLE(str(sscNumber) + ".tle")
        
        try:
            self.__satellite = root.CurrentScenario.Children.New(STKObjects.eSatellite, name)
        except COMError:
            raise (RuntimeError,'\nIncorrect name format or name already taken for satellite.' + 
                  ' Please do not use spaces or reuse satellite names.')
            
        try:
            root.ExecuteCommand('SetState */Satellite/' + self.name + ' TLE "' +
                                     self.tle[0] + '" "' + self.tle[1] +
                                     '" TimePeriod "' +
                                     self.__guardian.StartTime + '" "' +
                                     self.__guardian.StopTime + '"')
        except COMError:
            raise (RuntimeError, "Failure to add satellite. Check formatting of TLE.")
    
    def ComputeKeplerians(self, timeInstant):
        
        satDPSingle = self.__satellite.DataProviders.Item('Classical Elements')
        satDPSingle = satDPSingle.QueryInterface(STKObjects.IAgDataProviderGroup)
        ceicrf = satDPSingle.Group.Item('ICRF')
        ceicrf = ceicrf.QueryInterface(STKObjects.IAgDataPrvTimeVar)

        result = ceicrf.ExecSingle(timeInstant)

        time = result.DataSets.GetDataSetByName('Time').GetValues()
        sma = result.DataSets.GetDataSetByName('Semi-major Axis').GetValues()
        ecc = result.DataSets.GetDataSetByName('Eccentricity').GetValues()
        inc = result.DataSets.GetDataSetByName('Inclination').GetValues()
        raan = result.DataSets.GetDataSetByName('RAAN').GetValues()
        aop = result.DataSets.GetDataSetByName('Arg of Perigee').GetValues()
        trueAnomaly = result.DataSets.GetDataSetByName('True Anomaly').GetValues()

        arr = [time,sma,ecc,inc,raan,aop,trueAnomaly]
        
        return arr

    def GetAccess(self, areaTarget):

        root = self.__guardian.root

        root.BeginUpdate()

        access = self.__satellite.GetAccessToObject(areaTarget.GetTarget())
        access.ComputeAccess()

        intervalCollection = access.ComputedAccessIntervalTimes

        try:
            computedIntervals = intervalCollection.ToArray(0,-1)
            root.EndUpdate()

            return computedIntervals
        except Exception:
            root.EndUpdate()

            return 0

    def GetGuardian(self):
        return self.__guardian
