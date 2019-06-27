"""

Author: W. Conor McFerren
Created: [Thu Jun 27 17:46:04 2019]

"""

__author__="W. Conor McFerren"
__email__="cnmcferren@gmail.com"

import apptest, scenetest, sceneobjtest

if __name__=='__main__':
    appTest = apptest.AppTest()
    appTest.main()
    
    sceneTest = scenetest.SceneTest()
    sceneTest.main()
    
    atTest = sceneobjtest.AreaTargetTest()
    atTest.main()
    
    satTest = sceneobjtest.SatelliteTest()
    satTest.main()
    
    camTest = sceneobjtest.CameraTest()
    camTest.main()