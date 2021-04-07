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

class Application:
    
    """
    
    Creates the application for STK
    
    """
    def __init__(self):
        self.__uiApplication = CreateObject("STK11.Application")
        self.__uiApplication.Visible = True #Make graphics visible
        self.__uiApplication.UserControl = True #Enable user control
        self.root = self.__uiApplication.Personality2
        
    """
    
    Used to run STK Connect Commands using the root
    
    Parameters:
        connectCommand(str): The Connect Command string to be executed

    Return:
        Result of the Connect Command.
    
    """
    def Connect(self,connectCommand):
        result = self.root.ExecuteCommand(connectCommand)

        return result
        
    """
    
    Closes the application
    
    """
    def Close(self):
        self.__uiApplication.Close()

class AreaTarget(ScenarioObject):
    """
    
    An area target object to be added to the scenario. Inherits from
    stkhelper.ScenarioObject.
    
    Parameters:
        guardian(stkhelper.scenario): The scenario for the area target to be
                                    placed into.
        name(str): Name of the area target.
        coordList(list): List of lat/lon pairs to draw the area target
    
    """
    def __init__(self, guardian, name=None, coordList=None, radius=None):
        #TODO Make coordList mandatory
        self.guardian = guardian
        self.name = name
        self.coordinates = coordList
        
        self.root = self.guardian.guardian.root
        
        self.centroid = Toolbox.ComputeCentroid(self.coordinates)

        self.root.BeginUpdate()
        
        if (len(self.coordinates) != 1):
            self.reference = self.root.CurrentScenario.Children.New(STKObjects.eAreaTarget,self.name)
            self.reference = self.reference.QueryInterface(STKObjects.IAgAreaTarget)
            self.reference.AreaType = STKObjects.ePattern
            patterns = self.reference.AreaTypeData
            patterns = patterns.QueryInterface(STKObjects.IAgAreaTypePatternCollection)
            for i in range(len(self.coordinates)):
                patterns.Add(self.coordinates[i][0],
                             self.coordinates[i][1])
            
            self.reference.AutoCentroid = True
        else:
            self.reference = self.root.CurrentScenario.Children.New(STKObjects.eTarget,self.name);
            self.reference = self.reference.QueryInterface(STKObjects.IAgTarget)
            self.reference.Position.AssignGeodetic(coordList[0][0],coordList[0][1],0)
        
        self.root.EndUpdate()
        
    """
    
    Computes and returns access to a given scenario object
    
    Parameters:
        scenarioObject(stkhelper.scenarioObject): Object to compute the access to.
    
    Returns:
        access(list): The list of access times
    
    """
    def GetAccess(self,scenarioObject):
        #TODO Caused error from inherited method. Fix this in scenarioobjects
        self.root.BeginUpdate()
        access = super().GetAccess(scenarioObject)
        self.root.EndUpdate()
        
        return access

class Satellite(ScenarioObject):
    
    """
    
    A satellite object to be placed into the current scenario.
    
    Parameters:
        guardian(stkhelper.scenario.Scenario): Scenario for the satellite to be
            placed into.
        name(str): Name of the satellite.
        sscNumber(str): SSC Number of the satellite to use.
        startTime(str): Start time of the satellite propogation.
        stopTime(str): Stop time of the satellite propogation.
    
    """
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
            
    """
    
    Get access to another stkhelper.scenarioObject.ScenarioObject.
    
    Parameters:
        scenarioObject(stkhelper.scenarioObject.ScenarioObject): Object to compute
            access to.
    
    Returns:
        access: List of all access over the scenario time period.
        
    """
    def GetAccess(self,scenarioObject):
        self.root.BeginUpdate()
        access = super().GetAccess(scenarioObject)
        self.root.EndUpdate()
        
        return access
    
    """
    
    Calculates the power generated by solar panels over a given time period.
    
    Parameters:
        startTime(str): Start time of the calculation.
        endTime(str): Stop time of the calculation.
        timestep(int): Time step to be used (in seconds).
        radius(float): Bounding radius used for the simulation. Should be as 
            small as possible without clipping the model.
        outputPath(str): Absolute path of the file to be saved.
    
    """
    def GetPower(self,startTime,endTime,timestep,radius,outputPath):
        command = 'VO %s SolarPanel Visualization Radius On %f' % (self.path,radius)
        self.root.ExecuteCommand(command)
        command = 'VO %s SolarPanel Compute "%s" "%s" %i Power "%s"' % \
                    (self.path,startTime,endTime,timestep,outputPath)
                    
        self.root.ExecuteCommand(command)
        
    """
    
    Sets the model of the satellite in the scenario to a provided file (.dae + .anc
    or .mdl)
    
    Parameters:
        modelFile(str): Absolute path to the model file to be used.
    
    """
    def SetModel(self,modelFile):
        command = 'VO %s Model File "%s"' % (self.path,modelFile)
        self.root.ExecuteCommand(command)
        
    """
    
    Sets the attitude of the satellite. View full list of attitudes at:
    https://help.agi.com/stk/Subsystems/connectCmds/connectCmds.htm#cmd_SetAttitudeProfile.htm
    
    Parameters:
        profile(str): Attitude profile to be used.
    
    
    """
    def SetAttitude(self,profile):
        #TODO account for offset
        command = 'SetAttitude %s Profile %s Offset 0 0 0' % (self.path,profile)
        self.root.ExecuteCommand(command)