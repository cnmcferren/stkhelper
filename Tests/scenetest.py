"""

Author: W. Conor McFerren
Created: [Thu Jun 27 13:18:28 2019]

"""

__author__="W. Conor McFerren"
__email__="cnmcferren@gmail.com"

from stkhelper import application, scenario

from win32api import GetSystemMetrics
from comtypes.client import CreateObject
from comtypes.gen import STKObjects

class SceneTest:
    def __init__(self):
        print("\nBeginning test on the stkhelper.scenario.Scenario class...")
        self.app = application.Application(visible=False)
        
    def Close(self):
        try:
            scene = scenario.Scenario(self.app,'Test','+24hr')
            scene.Close()
            print("[ ok ] Scenario.Close()")
        except Exception as e:
            print("[ fail ] Scenario.Close() failed with exception: %s" % e)
            
    def SceneName(self):
        try:
            scene = scenario.Scenario(self.app,'32 adfs','+24hr')
            scene.Close()
            print("[ ok ] scenario.Scenario() with problematic names.")
        except Exception as e:
            print('[ fail ] scenario.Scenario() with problematic names ' + \
                  'failed with exception: %s' % e)
    
    def SetTimePeriod(self):
        try:
            start = '10 Jan 2019 01:01:01.000 UTCG'
            stop = '11 Jan 2019 01:01:01.000 UTCG'
            scene = scenario.Scenario(self.app,'TestTimePeriod','+365days')
            scene.SetTimePeriod(start, stop)
            scene.Close()
            print('[ ok ] Scenario.SetTimePeriod()')
        except Exception as e:
            print('[ fail ] Scenario.SetTimePeriod() failed with exception: %s' % e)
            
    def GetReference(self):
        try:
            scene = scenario.Scenario(self.app,'RefTest','+24hr')
            ref = scene.GetReference()
            scene.Close()
            if type(ref) == STKObjects.IAgScenario:
                print('[ ok ] Scenario.GetReference()')
            else:
                print('[ fail ] Scenario.GetReference() returns value of ' + \
                      'incorrect type.')
        except Exception as e:
            print('[ fail ] Scenario.GetReference() failed with exception: %s' % e)
            
    def SetTimeStandard(self):
        try:
            scene = scenario.Scenario(self.app,'SceneStandard','+24hr')
            scene.SetTimeStandard('LCLG')
            scene.Close()
            print('[ ok ] Scenario.SetTimeStandard()')
        except Exception as e:
            print('[ fail ] Scenario.SetTimeStandard() failed with exception: %s' % e)
            
    #TODO Add method to check GetGuardian()
    
    def main(self):
        self.Close()
        self.SceneName()
        self.SetTimePeriod()
        self.GetReference()
        self.SetTimeStandard()
        
        self.app.Close()
        
if __name__=='__main__':
    tester = SceneTest()
    tester.main()
            