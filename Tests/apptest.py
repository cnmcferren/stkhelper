"""

Author: W. Conor McFerren
Created: [Thu Jun 27 12:47:24 2019]

"""

__author__="W. Conor McFerren"
__email__="cnmcferren@gmail.com"

from stkhelper import application
import time
import os

class AppTest:
    def __init__(self):
        print("\nBeginning test on the stkhelper.application.Application class...")
        
    def Close(self):
        try:
            app = application.Application()
            app.Close()
            print("[ ok ] Application.Close().")
        except Exception as e:
            print("[ fail ] Application.Close() failed with exception: %s" % e)
    
    def VisibilityFalse(self):
        try:
            app = application.Application(visible=False)
            app.Close()
            print('[ ok ] Application(visible=False)')
        except Exception as e:
            print("[ fail ] Application(visible=False) failed with exception: %s" % e)
            
    def Connect(self):
        try:
            app = application.Application()
            app.Connect("CreateTLEFile * AGIServer " + os.getcwd() + "/25544.tle SSCNumber 25544")
            os.remove("24455.tle")
            app.Close()
            print("[ ok ] Application.Connect()")
        except Exception as e:
            print("[ fail ] Application.Connect() failed with exception: %s" % e)
            
    #TODO test UpdateTLEDatabase
    
    def main(self):
        self.Close()
        self.VisibilityFalse()
        self.Connect()
    
if __name__=="__main__":
    tester = AppTest()
    tester.main()
            