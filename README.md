# Abaqus-postprocessing
These Get-files can be used to extract data from .odb output files directly from the abaqus terminal. Instead of using the post-processing environment from the Abaqus/CAE, using these Get-files can be a much quicker and efficient way for extracting large sets of data for multiple load cases.
  
  Five Get-files are added here:
  - GetRF.py, collects reaction force components for a pre-defined set of nodes
  - GetRM.py, collects reaction moment components for a pre-defined set of nodes
  - GetCTF.py, collects concentrated force components for a pre-defined set of connector elements
  - GetCTM.py, collects concentrated moment components for a pre-defined set of connector elements
  - GetEigen.py, collects the Eigenvector, Eigenfrequency and Eigenvalue output values for a pre-defined set of nodes
  
