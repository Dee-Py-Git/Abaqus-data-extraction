## This script obtains the CTF output values from an .odb file for a defined set of elements 
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

odbFile = openOdb(path=str(PathToOdb))
# get file name and path
odbFileNameFull = odbFile.path
#split into separately name and path
odbFileName = os.path.split(odbFileNameFull)[1]

#### For each Step found in the .odb the output values are written

print ('Output is written from the following results file:    '), odbFileName
print 'Requested output:    CTF\n'

for Step in odbFile.steps.keys():
    StepName = [Step]
    print StepName[0]
    
## [-1] selects the last frame in the step 
    StepData = odbFile.steps[StepName[0]].frames[-1]
	
## This requests the output values from the step 
    ConnectorForces=StepData.fieldOutputs['CTF']
     
## This defines the set of elements and requests the output values for the set 
    ReqSet = odbFile.rootAssembly.elementSets[SetName]	
    Output = ConnectorForces.getSubset(region=ReqSet,position=WHOLE_ELEMENT)	
    OutputValues = Output.values

## This prints the output values in Global x, y and z coordinates
    print 'elem x-comp y-comp z-comp'
    for v in OutputValues:
        print '%d %6.4f %6.4f %6.4f' % (v.elementLabel, v.data[0], v.data[1], v.data[2])
