"""

Application class that creates an instance of the STK11 application.


"""

from win32api import GetSystemMetrics
from comtypes.client import CreateObject

__author__ = "W. Conor McFerren"
__maintainer__ = "W. Conor McFerren"
__email__ = "cnmcferren@gmail.com"

class Application:

    """

    Application that holds the STK11 application.

    """

    def __init__(self):
        self.__uiApplication = CreateObject("STK11.Application")
        self.__uiApplication.Visible = True
        self.__uiApplication.UserControl = True
        
        self.root = self.__uiApplication.Personality2
        
    def Connect(self, connectCommand):
        self.root.ExecuteCommand(connectCommand)

    """

    Closes the application.

    """

    def Close(self):

        self.__uiApplication.Quit()
