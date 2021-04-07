from win32api import GetSystemMetrics
from comtypes.client import CreateObject
import stkhelper.scenario


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
    def connect(self,connectCommand):
        result = self.root.ExecuteCommand(connectCommand)

        return result
        
    """
    
    Closes the application
    
    """
    def close(self):
        self.__uiApplication.Close()

    def addScenario(self, name, endTime, startTime=None):
        return stkhelper.scenario.Scenario(self, name, endTime, startTime)