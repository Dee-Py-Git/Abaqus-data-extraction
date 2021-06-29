## This script obtains the Eigenvector, Eigenfrequency and Eigenvalue output values from an .odb file for a defined set of nodes 
## This file is updated from a previous version to smoothly provide input to the analysis tool of Leichtwork which they will use to perform flutter analysis for AP3
## The Eigenvectors are formed from U and UR outputs 
## written by Daniel Jansen		June 12th 2021
## Version v4

from odbAccess import *
from abaqusConstants import *
from odbMaterial import *
from odbSection import *
import tkFileDialog
import numpy as np

mode = 0

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

outputFileName = odbFileName[:-4] + '_' + SetName
outputFile = open("%s_eigenvectors.txt" % outputFileName, "w")
outputFile.write('Output is written from the following results file:    ')
outputFile.write('%s\n' % (odbFileName))
outputFile.write('Requested output:    COORD, U, UR\n\n')

for Step in odbFile.steps.keys():
   StepName = [Step]
	
## This creates a loop to obtain the requested output for each frame in the step 
   for x in odbFile.steps[StepName[0]].frames:
   
## This requests the output values from the step 
		Coordinates=x.fieldOutputs['COORD']
		Translations=x.fieldOutputs['U']
		Rotations=x.fieldOutputs['UR']
		
## This defines the set of nodes and requests the output values for the set 
		ReqSet = odbFile.rootAssembly.nodeSets[SetName]	
		Output1 = Coordinates.getSubset(region=ReqSet)	
		Output2 = Translations.getSubset(region=ReqSet)	
		Output3 = Rotations.getSubset(region=ReqSet)
		OutputValues1 = Output1.values
		OutputValues2 = Output2.values
		OutputValues3 = Output3.values	
		
## This prints the frame description, which in this case is the mode number, eigenvalue and eigenfrequency
		eigenmode = odbFile.steps[StepName[0]].frames[mode].description
		
		outputFile.write('\n%s\n' % (eigenmode))		
		mode = mode + 1		
		
## This prints the (undeformed!) coordinates in Global x, y and z coordinates		
		outputFile.write('node X-coord Y-coord Z-coord U_x U_y U_z UR_x UR_y UR_z\n')	
		
		
## This collects the output values in three matrices matrix. The Numpy library is used here to create 'arrays', which work a bit different then 'lists'.

## First the coordinates		
		Bini = np.array([0,0,0,0])
		for u in OutputValues1:
			A = (u.nodeLabel, u.data[0], u.data[1], u.data[2])
			Bini = np.vstack([Bini, A])
		
		B = Bini[1:,:]

## Then the translations			
		Dini = np.array([0,0,0])
		for v in OutputValues2:
			C = (v.data[0], v.data[1], v.data[2])
			Dini = np.vstack([Dini, C])
			
		D = Dini[1:,:]	
		
## Then the rotations		
		Fini = np.array([0,0,0])
		for w in OutputValues3:
			E = (w.data[0], w.data[1], w.data[2])
			Fini = np.vstack([Fini, E])
		
		F = Fini[1:,:]		

## This collects the output values in a single matrix
		G = np.hstack((B,D,F))
		
##		for row in G:
		fmt = '%d', '%1.2f', '%1.2f', '%1.2f', '%.4E', '%.4E', '%.4E', '%.4E', '%.4E', '%.4E'
		np.savetxt(outputFile, G, fmt=fmt)
		
			
outputFile.close()