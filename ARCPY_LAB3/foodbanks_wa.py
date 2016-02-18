# Rachel Roberts
# Arcpy Lab 3: Distilling the web into GIS datasets 
# February 18, 2016
# Discussed the lab with Will Chen. Discussed scrapping the html/website and geocoding strategies. 
# Additionally, I often referenced srcappers uploaded to the class github. They were especially useful in this lab. 
# Lastly, I refered to code in the previous labs for reference about how to convert files from shapefiles to geoJSON files.

# The following code extracts address infrmation
# for food banks/ food pantries in Washington State. The following code extracts
# information for the first 20 records. The records were listed alphabetically. 
# With the price of living in Seattle rapidly increasing, increased luxury development, 
# and an increasing wage disparity between classes, access to food, whether it be for 
# the homeless, low income, or the like will become increasingly important. Knowing the
# spatial locations for food banks and similar programs can help to inform key stakeholders
# about how to make the programs more equitable and accessible. 

# Import moduels 
import csv
import urllib2
import lxml.html
import ggeocoder
import csv
from subprocess import call
import os
os.environ["GDAL_DATA"] = "C:\\OSGeo4W\\share\\gdal"
os.environ["GDAL_DRIVER_PATH"] = "C:\\OSGeo4W\\bin\\gdalplugins"
os.environ["PROJ_LIB"] = "C:\\OSGeo4W\\share\\proj"
os.environ["PATH"] = "C:\\OSGeo4W\\bin;"+os.environ["PATH"]+";C:\\OSGeo4W\\apps\\msys\\bin;C:\\OSGeo4W\\apps\\Python27\\Scripts"

# Define getPage Function 
def get_page(url):
    html = urllib2.urlopen(url).read()
    dom = lxml.html.fromstring(html)
    dom.make_links_absolute(url)
    return dom

# Reference URLs / HTML Page. Thie section of the code extracts all relevent information from the website. 
# In this istance, the name of the food bank and the address were extracted to be geocoded, which is done
# in a later portion of rthis code.  
food = get_page("http://www.resourcehouse.org/win211/All/topics/Basic_Needs/Food/Emergency_Food/Food_Pantries/programs.aspx")
newFile = open("foodbanks_WA.csv",'wb')
foodbanks = []
#print dom

for row in food.cssselect(".agency"):
    dictionary = {}
    linkName = row.cssselect(".clearfix h2").pop()
    linkAddress = row.cssselect(".locationdetail dl dd label").pop()
    name_text = linkName.text
    address_text = linkAddress.text
    dictionary["Food Bank"] = name_text
    dictionary["Address"] = address_text
    foodbanks.append(dictionary)
# print foodbanks
# len(foodbanks)

# Slicing list because geocoder cannot work with 10+ addresses at a time. 
foodbank_1 = foodbanks[:7]
print foodbank_1

foodbank_2 = foodbanks [8:14]
print foodbank_2

foodbank_3 = foodbanks [15:]
print foodbank_3

# Geocoding Coordinates: from points to x-y coordinates. 
# The list of foodbank sites had to be sliced and processed seperately 
# because otherwise, the Geocoder reachesit query limit with google maps. 
# The following error message will occur if not run seperatly (3 seperate times):
# GeocodeError: Error: OVER_QUERY_LIMIT.

geocoder = ggeocoder.Geocoder() 
y = []
x = []
for entries in foodbank_1:
    xy = geocoder.geocode(entries["Address"])[0]
    coordinates = str(xy.coordinates)
    Y_1 = coordinates.split(",")[1][:-1].strip()
    X_1 = coordinates.split(",")[0][1:11].strip()
    #print Y_1
    #print X_1
    y.append(Y_1)
    x.append(X_1)
#print y
#print x
for entries in foodbank_2:
    xy = geocoder.geocode(entries["Address"])[0]
    coordinates = str(xy.coordinates)
    Y_2 = coordinates.split(",")[1][:-1].strip()
    X_2 = coordinates.split(",")[0][1:11].strip()
    #print Y_2
    #print X_2
    y.append(Y_2)
    x.append(X_2)
#print y
#print x
for entries in foodbank_3:
    xy = geocoder.geocode(entries["Address"])[0]
    coordinates = str(xy.coordinates)
    Y_3 = coordinates.split(",")[1][:-1].strip()
    X_3 = coordinates.split(",")[0][1:11].strip()
    #print Y_3
    #print X_3
    y.append(Y_3)
    x.append(X_3)
print y
print x

# CSV File conversion: outputs the scrapped data to a .cvs file. 
c = csv.writer(open("foodbanks_WA.csv", "wb"))
c.writerow(["Food Bank","Address","X","Y"])
field_names = ['Food Bank', 'Address', 'X', 'Y']
csvwriter = csv.DictWriter(newFile, delimiter = str(','), fieldnames = field_names)
csvwriter.writerow(dict((fn,fn,fn,fn) for fn in field_names))
for row in foodbanks:
    for row in x:
        for row in y:
            csvwriter.writerow(row)
newFile.close()

# Convert shapefile to geoJSON file. 
#import Arcpy
import sys 
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.3\\bin')
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.3\\arcpy')
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.3\\ArcToolbox\\Scripts')
import arcpy

arcpy.env.workspace = r"U:\ARCPY_LAB3\DATA\FOODBANK_SHAPEFILES\foodbanks_WA.shp"
geoJSON_output = "foodbanks_WA.geojson"
geoJSON_destination = "U:\\ARCPY_LAB3\\DATA\\GEOJSON_FILES" + geoJSON_output

# Convert files from shapefiles to geoJSON file.
call(['C:\\OSGeo4W\\bin\\ogr2ogr',
      '-f','GeoJSON','-t_srs','WGS84',
      '-s_srs','EPSG:26913',
      'U:\\ARCPY_LAB3\\DATA\\GEOJSON_FILES\\foodbanks_WA.geojson',
      'U:\\ARCPY_LAB3\\DATA\\FOODBANK_SHAPEFILES\\foodbanks_WA.geojson'])
