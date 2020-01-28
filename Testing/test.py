from stkhelper import application, scenario, satellite, areatarget
import time
import platform
import socket
import os

class Test:
    def __init__(self):
        print("\n********** TEST **********\n")
        print("Hostname: " + socket.gethostname())
        print("CWD: " + os.getcwd() + "\n")
        print("Testing stkhelper on system:")
        print("\tSystem: " + platform.system())
        print("\tRelease: " + platform.release())
        print("\tVersion: " + platform.version())
        
        self.time = time.time()
        print("\nBeginning test at: " + time.time() + "\n")
        
        self.ApplicationTest()
        app = application.Application()
        scene = scenario.Scenario(app,"ScenarioObjectsTest",'+24hrs')
        
        
        
    def ApplicationTest(self):
        try:
            app = application.Application()
            print("[ OK ] stkhelper.application.Application")
            self.ApplicationTest_Close(app)
        except Exception as e:
            print("[ FAIL ] stkhelper.application.Application with error: " + e)
    
    def ApplicationTest_Close(self,app):
        try:
            app.Close()
            print("[ OK ] stkhelper.application.Application.Close()")
        except Exception as e:
            print("[ FAIL ] stkhelper.application.Application.Close() with error: " + e)
    
    def ScenarioTest(self,app):
        try:
            scene = scenario.Scenario(app,"ScenarioTest",'+24hrs')
            print("[ OK ] stkhelper.scenario.Scenario")
            self.ScenarioTest_SetTimePeriod(scene)
            self.ScenarioTest_Close()
        except Exception as e:
            print("[ FAIL ] stkhelper.scenario.Scenario with error: " + e)
            
    def ScenarioTest_SetTimePeriod(self,scene):
        try:
            scene.SetTimePeriod('27 Jan 2020 05:57:52.545',
                                '27 Jan 2020 06:08:57.185')
            print("[ OK ] stkhelper.scenario.Scenario.SetTimePeriod()")
        except Exception as e:
            print("[ FAIL ] stkhelper.scenario.Scenario.SetTimePeriod() with error: " + e)
            
    def ScenarioTest_Close(self,scene):
        try:
            scene.Close()
            print("[ OK ] stkhelper.scenario.Scenario.Close()")
        except Exception as e:
            print("[ FAIL ] stkhelper.scenario.Scenario.Close() with error: " + e)
            