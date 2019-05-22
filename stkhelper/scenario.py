from win32api import GetSystemMetrics
from comtypes.client import CreateObject
from comtypes.gen import STKObjects
from comtypes import COMError

class Scenario:

    def __init__(self, application, name, timePeriod):
        
        
        self.__guardian = application
        self.name = name.replace(' ','_')
        
        application.root.NewScenario(self.name)
        self.__scenario = application.root.CurrentScenario
        self.__scenario = self.__scenario.QueryInterface(STKObjects.IAgScenario)
        try:
            self.__scenario.SetTimePeriod('Today',str(timePeriod))
        except COMError:
            raise ValueError, "Time period not properly formatted"

    def SetTimePeriod(self, elapsedTime):

        self.__scenario.SetTimePeriod('Today',str(elapsedTime))
        
    def GetReference(self):
        return self.__scenario

    def Close(self):

        self.__guardian.root.CloseScenario()

    def GetGuardian(self):
        return self.__guardian
