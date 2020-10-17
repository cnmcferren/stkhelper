from stkhelper.scenarioobject import ScenarioObject

class Sensor(ScenarioObject):
    """
    
    A Sensor object to be place on another scenario object.
    
    Parameters:
        guardian(stkhelper.scenarioobject): Scenario object for sensor to be attached to.
        name(str): Name of the sensor.
        fov(tuple): Vertical and horizontal field of view (in degrees)
        angularRes(float): Angular resolution of sensor.
    
    """
    def __init__(self, guardian, name, fov, angularRes=None):
        super().__init__(guardian, name.replace(',','').replace(' ', '_'))
        self.path = guardian.path + "/Sensor/" + self.name
        self.root = self.guardian.root
        
        self.reference = self.guardian.reference.Children.New(20, self.name)
        
        if (angularRes == None):
            self.angularRes = 1.0
        else:
            self.angularRes = angularRes
            
        self.root.ExecuteCommand("Define %s Rectangular %s %s AngularRes %s" % (self.path, str(fov[0]), str(fov[1]), str(self.angularRes)))
        