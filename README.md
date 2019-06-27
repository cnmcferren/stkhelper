# STKHelper

STKHelper is a Python package designed for making interfacing with AGI's
STK easier. 

## Installation

STKHelper is available on the Python Packaging Index and can be installed 
using pip

```bash
pip install stkhelper
```

## Usage

Interfacing STK with Python can be difficult task due to its confusing 
class system, which involves lots of type casting and several references to the
same object. To combat this, STKHelper implements a "guardian class
relationship". Every object (with the exception of the application itself) has
a guardian objects, which is the object that contains it. For example, a scenario
is the guardian of all the satellites and area targets that are contained in
the scenario. Similarly, a satellite is the guardian for all cameras that it
contains.

```python
from stkhelper import application, scenario, scenarioObjects

app = application.Application()
scene = scenario.Scenario(app,'TestScenario','+24hr')
sat = scenarioObjects.Satellite(scene,'TestSat',25544)
```

In this code snippet, an application is created. In that application, a
scenario is added and the reference to the app is passed as the guardian in the
declaration. When the satellite is created, the scenario reference is passed
at declaration as the guardian. The reference to the guardian can always be
returned with the following method on all objects:

```python
object.GetReference()
```
