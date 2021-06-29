## This script obtains the CTM output values from an .odb file for a defined set of elements 
## written by Daniel Jansen		July 10th 2017
## Version 1.0

from odbAccess import *
from abaqusConstants import *
from odbMaterial import *
from odbSection import *
import tkFileDialog

########################## Input for this file ##############################

SetName = input('Enter the set name in capitals and as a string: ') ##Example: 'SET-HT_IFS'
PathToOdb = tkFileDialog.askopenfilename()

#############################################################################

odb = openOdb(path=str(PathToOdb))

#### For each Step found in the .odb the output values are written
 
print 'CTM output values'
for Step in odb.steps.keys():    
    StepName = [Step]
    print StepName[0]
    
## [-1] selects the last frame in the step 
    StepData = odb.steps[StepName[0]].frames[-1]
	
## This requests the output values from the step 
    ConnectorMoments=StepData.fieldOutputs['CTM']
     
## This defines the set of elements and requests the output values for the set 
    ReqSet = odb.rootAssembly.elementSets[SetName]	
    Output = ConnectorMoments.getSubset(region=ReqSet,position=WHOLE_ELEMENT)	
    OutputValues = Output.values

## This prints the output values in Global x, y and z coordinates
    print 'elem x-comp y-comp z-comp'
    for v in OutputValues:
        print '%d %6.4f %6.4f %6.4f' % (v.elementLabel, v.data[0], v.data[1], v.data[2])
