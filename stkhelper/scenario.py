from comtypes.gen import STKObjects
from comtypes import COMError

class Scenario:
    def __init__(self, application, name, timePeriod, startTime=None):
        """
        Creates an instance of the scenario.
        Parameters:
            application (STK11 Instance): Running instance of STK 11.
            name (str): Name of the scenario to be created.
            timePeriod (str): The amount of time you want the scenario to run 
            for.
            startTime (str): The start date of the scenario.
                        Examples: "+24hr", "+365days", "+10days".
        """
        
        
        if startTime == None:
            startTime = 'Today'
        else:
            startTime = str(startTime)
        
        self.startTime = startTime
        self.stopTime = timePeriod
        
        self.guardian = application
        self.name = name.replace(' ','_')
        
        application.root.NewScenario(self.name)
        self.reference = application.root.CurrentScenario
        self.reference = self.reference.QueryInterface(STKObjects.IAgScenario)
        try:
            self.reference.SetTimePeriod(str(startTime),str(timePeriod))
        except COMError:
            raise ValueError("Time period not properly formatted")
            
    def setTimePeriod(self, startTime, stopTime):    
        """
        Sets a new time period for the scenario.
        Parameters:
            elapsedTime (str): The amound of time you want the scenario to run 
            for. Examples: "+24hr", "+365days", "+10days".
        """

        self.startTime = startTime
        self.stopTime = stopTime
        self.reference.SetTimePeriod(str(startTime),str(stopTime))
        
    def close(self):     
        """
        Closes the scenario.
        """

        self.guardian.root.CloseScenario()