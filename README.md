# LR-IPM
A cost estimation application designed for Manitoba Hydro's LR/IPM jobs. The goal is to use the excel tables created by the distribution design engineers, have them specify which column contains which information, then scan a database (currently an excel file for testing purposes) for the required parts, and create a cost estimate which may then be generated into and appropriate table for submission.

To use:

1. Install kivy (min version 1.11.1), kivymd, and openpyxl.
2. Replace these packages with the corresponding packages of the same name included in the repository
3. Ensure all preinstalled python packages are up to date
4. Make sure 'Ruces_Companion_New_Format.py' 'Ruces_Comapanion_GUI.py', 'cddatabase.xlsx' and rcgui.kv are in the same folder

INSTRUCTIONS:

1. Run "Ruces_Companion_GUI.py" make sure you run in an environment where the appropriate packages have been installed
2. Click New Job
3. Click Load IPM and select one of the spreadsheats with naming convention "P#####' for ex "P30201"
4. When asked for header names enter the following, make sure they are spelled correctly as exception handling is currently incomplete. Do not use tab to switch entries, this will only add a tab space in the name entry field:
  IPM Column name: IPM
  POLE Column name: POLE
  CD# Column Name: CD#
  CONDUCTOR Column Name: CONDUCTOR
 5. Click retrieve, the screen should populate with a list of IPM numbers for ID, CD numbers for component specification and Conductor numbers for electrical conductor specification. The CD and Conductor numbers may be modified if needs be
 6.Click estimate, this should populate the screen with a list of parts and the quantity required, which may be changed as needed.
 
 Further development would have added functionality for:
 
 Reading form an SQL instead of an excel sheet
 
 Saving and loading jobs to return to later
 
 Cost estimation and entry of secondary costs
 
 
 However my time with the company came to an end and so I lost access to the information needed.
 
 From the end screen, click the options icon in the top right and click "New" to run the program again
 
 
