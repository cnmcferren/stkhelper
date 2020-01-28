"""

Application class that creates an instance of the STK11 Application

"""

from win32api import GetSystemMetrics
from comtypes.client import CreateObject


class Application:
    def __init__(self):
    
        #TODO Add __uiApplication to UML Diagram
        self.__uiApplication = CreateObject("STK11.Application")
        self.__uiApplication.Visible = True #Make graphics visible
        self.__uiApplication.UserControl = True #Enable user control
        self.root = self.__uiApplication.Personality2
        
    def Connect(self,connectCommand):
        self.root.ExecuteCommand(connectCommand)
        
    def Close(self):
        self.__uiApplication.Close()
