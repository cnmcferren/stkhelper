from win32api import GetSystemMetrics
from comtypes.client import CreateObject

class Application:
    def __init__(self):
        self.__uiApplication = CreateObject("STK11.Application")
        self.__uiApplication.Visible = True
        self.__uiApplication.UserControl = True
        
        self.root = self.__uiApplication.Personality2
