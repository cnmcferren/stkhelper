"""

Author: W. Conor McFerren
Created: [Thu Jun 27 14:20:07 2019]

"""

__author__="W. Conor McFerren"
__email__="cnmcferren@gmail.com"

from stkhelper import application, scenario, scenarioObjects
from win32api import GetSystemMetrics
from comtypes.client import CreateObject
from comtypes.gen import STKObjects
import os

class AreaTargetTest:
    def __init__(self):
        print("Beginning test on the stkhelper.scenarioObjects.AreaTarget class...")
        self.app = application.Application(visible=False)
        self.scene = scenario.Scenario(self.app,'Test', '+24hr')
        
    #TODO Method to check parsed line
    
    def CoordList(self):
        try:
            coords = [(20,20),
                      (25,20),
                      (25,25),
                      (20,25)]
            at = scenarioObjects.AreaTarget(self.scene,name='CoordList',coordList=coords)
            print('[ ok ] scenarioObjects.AreaTarget with coordinate list.')
        except Exception as e:
            print('[ fail ] scenarioObjects.AreaTarget with coordinate list ' + \
                  'failed with exception: %s' % e)
            
    def SetElevationConstraint(self):
        try:
            coords = [(25,25),
                      (30,25),
                      (30,30),
                      (25,30)]
            at = scenarioObjects.AreaTarget(self.scene,name='ElevCon',coordList=coords)
            at.SetElevationConstraint(15)
            print('[ ok ] AreaTarget.SetElevationConstraint().')
        except Exception as e:
            print('[ fail ] AreaTarget.SetElevationConstraint() failed with ' + \
                  'exception \: %s' % e)
    
    #TODO Create methods to check GetPattens and GetTarget
    
    def GetGuardian(self):
        try:
            coords = [(25,25),
                      (30,25),
                      (30,30),
                      (25,30)]
            at = scenarioObjects.AreaTarget(self.scene,name='CoordList',coordList=coords)
            guardian = at.GetGuardian()
            if guardian == STKObjects.IAgScenario:
                print("[ ok ] AreaTarget.GetGuardian().")
            else:
                print("[ fail ] AreaTarget.GetGuardian() returns value of incorrect type")
        except Exception as e:
            print('[ fail ] AreaTarget.GetGuardian() failed with exception: %s' % e)
            
    def main(self):
        self.CoordList()
        self.SetElevationConstraint()
        self.GetGuardian()
        
        self.app.Close()
    
class SatelliteTest:
    def __init__(self):
        print("Beginning test on the stkhelper.scenarioObjects.Satellite class...")
        self.app = application.Application(visible=False)
        self.scene = scenario.Scenario(self.app,'Test','+365days')
    
    def ScenarioTime(self):
        try:
            sat = scenarioObjects.Satellite(self.scene,'Default',25544)
            os.remove('25544.tle')
            print('[ ok ] scenarioObjects.Satellite.')
        except Exception as e:
            print('[ fail ] scenarioObjects.Satellite failed with exception: %s' % e)
    
    def PresetTime(self):
        try:
            start = '10 Jan 2019 01:01:01.000 UTCG'
            stop = '11 Jan 2019 01:01:01.000 UTCG'
            sat = scenarioObjects.Satellite(self.scene,
                                            'Default',
                                            25544,
                                            StartTime=start,
                                            StopTime=stop)
            os.remove('25544.tle')
            print('[ ok ] scenarioObjects.Satellite with preset times.')
        except Exception as e:
            print('[ fail ] scenarioObjects.Satellite with presets failed with ' +
                  'exception: %s' % e)
    
    def ComputeKeplerians(self):
        try:
            timeInst = '10 Jan 2019 02:01:01.000 UTCG'
            start = '10 Jan 2019 01:01:01.000 UTCG'
            stop = '11 Jan 2019 01:01:01.000 UTCG'
        
            sat = scenarioObjects.Satellite(self.scene,
                                            'KeplTest',
                                            '+24hr',
                                            StartTime=start,
                                            StopTime=stop)
            os.remove('25544.tle')
            keplerians = sat.ComputeKeplerians(timeInst)
            for elem in keplerians:
                float(elem)
            print('[ ok ] Satellite.ComputeKeplerians()')
        except Exception as e:
            print('[ fail ] Satellite.ComputerKeplerians() failed with ' +
                  'exception: %s' % e)
    
    #TODO Add method to test ComputeDSInfo()
    def GetAccess(self):
        try:
            atList = []
            coords = [(25,25),
                      (30,25),
                      (30,30),
                      (25,30)]
            at = scenarioObjects.AreaTarget(self.scene,name='Single',coordList=coords)
            
            sat = scenarioObjects.Satellite(self.scene,'Access',25544)
            os.remove('25544.tle')
            for i in range(3):
                targ = scenarioObjects.AreaTarget(self.scene,name=str(i),coordList=coords)
                atList.append(targ)
            sat.GetAccess(at)
            sat.GetAccess(atList)
            print('[ ok ] Satellite.GetAccess()')
        except Exception as e:
            print('[ fail ] Satellite.GetAccess() failed with exception: %s' % e)
            
    def GetReference(self):
        try:
            sat = scenarioObjects.Satellite(self.scene,'Ref',25544)
            ref = sat.GetReference()
            if type(ref) == STKObjects.IAgSatellite:
                print('[ ok ] Satellite.GetReference()')
            else:
                print('[ fail ] Satellite.GetReference() returned incorrect type')
        except Exception as e:
            print('[ fail ] Satellite.GetReference() failed with exception: %s' % e)
            
    def GetGuardian(self)
        try:
            sat = scenarioObjects.Satellite(self.scene,'Guard',25544)
            ref = sat.GetGuardian()
            if type(ref) == STKObjects.IAgSatellite:
                print('[ ok ] Satellite.GetGuardian()')
            else:
                print('[ fail ] Satellite.GetGuardian()) returned incorrect type')
        except Exception as e:
            print('[ fail ] Satellite.GetGuardian() failed with exception: %s' % e)  
            
    def main(self):
        self.ScenarioTime()
        self.PresetTime()
        self.ComputeKeplerians()
        self.GetAccess()
        self.GetReference()
        self.GetGuardian()
        
        self.app.Close()
        
class CameraTest:
    def __init__(self):
        print("Beginning test on the stkhelper.scenarioObjects.Camera class...")
        self.app = application.Application(visible=False)
        self.scene = scenario.Scenario(app,'Test','+365days')
        self.sat = scenarioObjects.Satellite(scene,
                                             'Test',
                                             25544)
        coords = [(25,25),
                  (30,25),
                  (30,30),
                  (25,30)]
        self.at = scenarioObjects.AreaTarget(scene,name='Test',coordList=coords)
        
    def CreateCam(self):
        try:
            cam = scenarioObjects.Camera(self.sat,'Create',10)
            print('[ ok ] scenarioObjects.Camera')
        except Exception as e:
            print('[ fail ] scenarioObjects.Camera failed with exception: %s' % e)
            
    def GetAccess(self):
        try:
            cam = scenarioObjects.Camera(self.sat,'Access',20)
            cam.GetAccess(self.at)
            print('[ ok ] Camera.GetAccess()')
        except Exception as e:
            print('[ fail ] Camera.GetAccess() failed with exception: %s' % e)

    def GetGuardian(self):
        try:
            cam = scenarioObjects.Camera(self.sat,'Guard',30)
            guardian = cam.GetGuardian()
            if type(guardian) == STKObjects.IAgSatellite:
                print('[ ok ] Camera.GetGuardian()')
            else:
                print('[ fail ] Camera.GetGuardian() returned object of incorrect type.')
        except Exception as e:
            print('[ fail ] Camera.GetGuardian() failed with exception: %s' % e)
        
    #TODO method to test GetCamera and GetCameraGen
    def main(self):
        self.CreateCam()
        self.GetAccess()
        self.GetGuardian()
        
        self.app.Close()
        
if __name__=='__main__':
    tester = AreaTargetTest()
    tester.main()    
    
    tester = SatelliteTest()
    tester.main()
    
    tester = CameraTest()
    tester.main()
    
        