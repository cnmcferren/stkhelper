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
from stkhelper.application import Application

app = Application
scene = app.addScenario('TestScenario', '+24hr')
sat = scene.addSatellite('ISS', 25544)
```
