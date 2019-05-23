
from win32api import GetSystemMetrics
from comtypes.client import CreateObject
from comtypes.gen import STKObjects
from comtypes import COMErrorpi

from toolbox import TLE_Manager, Toolbox

__author__ = "W. Conor McFerren"
__maintainer__ = "W. Conor McFerren"
__email__ = "cnmcferren@gmail.com"

"""

Area target class that holds the reference for area targets
to be added to the scenario.

"""

class AreaTarget:
   
    """

    Creates an AreaTarget object.

    Parameters:
        scenario (STKObjects.IAgScenario): Scenario for the area target
                                        to be placed in.
        parsedLine (list): Line parsed from the Target List.

    """

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

    """

    Returns the reference to the area target object.

    Returns:
        self.__areaTarget: The reference to the area target objects.

    """

    def GetTarget(self):

        return self.__areaTarget

    """

    Returns the patterns for the area target objects.

    Returns:
        self.__patterns: The reference to the patterns

    """

    def GetPatterns(self):

        return self.__patterns

    """

    Returns the guardian of the class (the scenario).

    Returns:
        self.__guardian: The scenario the area target is in.

    """

    def GetGuardian(self):

        return self.__guardian

"""

The camera that can be added to a satellite object.

"""

class Camera:

    """

    Creation of the camera.

    Parameters:
        hostSat (STKObjects.eSatellite): The satellite that the camera is to be attached to.
        name (str): A new and unique name of the camera.
        fov (list): A list containing the field of view width and height.

    """

    def __init__(self, hostSat, name, fov):
        self.__guardian = hostSat
        
        if not ((type(fov[0]) == int or type(fov[0]) == float) and
                (type(fov[1]) == int or type(fov[1]) == float)):
            raise TypeError, "Field of View parameters of invalid type."
        
        root = self.__guardian.GetGuardian().GetGuardian().root
        
        root.BeginUpdate()
        
        self.__cameraGen = self.__guardian.GetReference().Children.New(20,name)
        self.__camera = self.__cameraGen.QueryInterface(STKObjects.IAgSensor)
        self.__camera.CommonTasks.SetPatternRectangular(fov[0],fov[1])
        
        root.EndUpdate()
    
    """

    Computes the access to an area target with the camera during the time
    interval of the scenario. 

    Parameters:
        areaTarget (STKObjects.IAgAreaTarget): The area target that access
                                            is to be computed to.

    Returns:
        comptuedIntervals: An array containing the start and end time of
                        all passes within the scenario's time interval.

    """

    def GetAccess(self, areaTarget):

        root = self.__guardian.GetGuardian().GetGuardian().root
        
        root.BeginUpdate()

        access = self.__cameraGen.GetAccessToObject(areaTarget.GetTarget())
        access.ComputeAccess()
        intervalCollection = access.ComputedAccessIntervalTimes
        try:
            computedIntervals = intervalCollection.ToArray(0,-1)
            root.EndUpdate()

            return computedIntervals
        except:
            root.EndUpdate()

            return 0
    
    """

    Returns the reference to the camera.

    Returns: 
        self.__camera: Returns the camera of type STKObjects.IAgSensor.

    """

    def GetCamera(self):
        return self.__camera
    
    """

    Returns the general camera.

    Returns:
        self.__cameraGen: The camera but of a general type.

    """

    def GetCameraGen(self):
        return self.__cameraGen
    
    """

    Returns the guardian of the camera.

    Returns
        self.__guardian: The satellite that is the guardian of the camera.

    """

    def GetGuardian(self):
        return self.__guardian

"""

The satellite that is to be placed into a scenario.

"""

class Satellite:

    """

    Creates a satellite to be added to the scenario
    
    Parameters:
        scenario (STKObjects.IAgScenario): The scenario that the satellite will be placed in.
        name (str): The unique name of the satellite.
        sscNumber (str or int): The SSC Number of the satellite to model the orbit of.

    """

    def __init__(self, scenario, name, sscNumber):
        self.__guardian = scenario
        self.name = name

        root = self.__guardian.GetGuardian().root

        TLE_Manager.GenerateTLE(self.__guardian.GetGuardian().root, str(sscNumber))
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
                                     self.__guardian.GetReference().StartTime + '" "' +
                                     self.__guardian.GetReference().StopTime + '"')
        except COMError:
            raise (RuntimeError, "Failure to add satellite. Check formatting of TLE.")
    
    """

    Computes the Keplerian parameters for the satellite at a time instant.

    Parameters:
        timeInstant (str): The time instant for the Keplerians to be computed
                        in the format that STK provides.

    """

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

    """

    Computes access to the area target provided over the time interval of the scenario.

    Parameters:
        areaTarget (AreaTarget): The area target to compute access to.

    Returns:
        computedIntervals (list): The time intervals of the access times.

    """

    def GetAccess(self, areaTarget):

        root = self.__guardian.GetGuardian().root

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
    
    """

    Computes the information for the dynamic simulations.

    Parameters:
        areaTarget (AreaTarget): The area target that is going to be used 
                            in the dynamic simulations.
        passArray (list): The list that contains the start and end time
                        for a pass over the given area target.

    Returns:
        List in the following format:
            [areaTarget.ID, areaTarget.center, keplerians, (startTime, endTime)]

    """

    def ComputeDSInfo(self, areaTarget, passArray):

        startTime = passArray[0]
        endTime = passArray[1]

        keplerians = self.ComputeKeplerians(startTime)

        return [areaTarget.ID, areaTarget.center, keplerians, (startTime, endTime)]


        keplerians = self.ComputeKeplerians(startTime)

        return [areaTarget.ID, areaTarget.center, keplerians, (startTime, endTime)]

    """

    Get reference to the satellite.

    Returns:
        self.__satellite: Returns the reference to the STKObjects.eSatellite.

    """

    def GetReference(self):
        
        return self.__satellite
    
    """

    Returns the guardian of the satellite object (the scenario).

    Returns:
        self.__guardian: The scenario that the satellite is in.

    """

    def GetGuardian(self):
        return self.__guardian
