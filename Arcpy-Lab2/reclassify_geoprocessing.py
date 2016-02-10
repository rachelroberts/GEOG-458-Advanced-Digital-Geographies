# Rachel Roberts
# Arcpy Lab 2: Geoprocessing Tools and Services
# February 10, 2016
# Worked with Will Chan. Primarily discussed the use of cursors and nested loops under the context of reclassifying values and looping through various fields in the table. 

#Import Arcpy

import sys 
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.3\\bin')
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.3\\arcpy')
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.3\\ArcToolbox\\Scripts')
import arcpy
import os 
from arcpy import env 
         
# Set environment tool settings 
input_layer = arcpy.GetParameterAsText(0)   # input layer/ featureclass / shapefile.
reclass_table = arcpy.GetParameterAsText(1) # table that contains reclass values.
reclass_field = arcpy.GetParameterAsText(2) # field the reclass will be based off of.
new_field = arcpy.GetParameterAsText(3)     # name of the new field that will be populated with reclass values.
no_data = arcpy.GetParameterAsText(4)       # the value specified if a feature in the input file cannot be reclassified.\
output_layer = arcpy.GetParameterAsText(5)  # output file resulting from tool 

# Create field to populate with reclassify values. 
arcpy.AddField_management (input_layer, new_field)
    
# Reclassify values in the input_field based on values in the reclass_table. 
update_cursor = arcpy.da.UpdateCursor (input_layer, [reclass_field, new_field]) #updates the field created with the reclass values.

for update_row in update_cursor: #loops through the reclass_field and updates the new_field based on the parameters set in the reclass_table (see line below).
    with arcpy.da.SearchCursor (reclass_table, ["lowerbound", "upperbound", "value"]) as cursor: #loops through the reclass_table to assign the appropriate values.
		for row in cursor: 
			lowerbound = row[0] 
			upperbound = row[1]
			value = row[2]
			if (update_row[0] >= lowerbound and update_row[0] <= upperbound): # assigned reclass values to rows.
				update_row[1] = value 
				break #stops the loop if the parameters specified above are fullfilled. 
			else: 
				update_row[1] = no_data #value used if none of the values in the input_layer can be reclassified. 
    
    update_cursor.updateRow(update_row)
            
del update_row     
del update_cursor

# Create new feature class with classification field. 
arcpy.CopyFeatures_management (input_layer, output_layer)
