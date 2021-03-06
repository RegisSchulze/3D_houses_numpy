# 3D_houses_numpy
* Developer name: Régis Schulze
* 3D House Project
* Repository: 3D_houses
* Type of Challenge: Learning & Consolidation
* Duration: 2 weeks
* Deadline: 25/02/21 5:00 PM
* Deployment strategy : Github page | Powerpoint | Spyder
* Team challenge : solo

## Mission objectives
Consolidate the knowledge in Python, specifically in :

* NumPy
* Pandas
* Matplotlib

## Learning Objectives
* to be able to search and implement new librairies
* to be able to read and use shapefiles
* to be able to read and use geoTIFFs
* to be able to render a 3D plot
* to be able to present a final product

## The Mission
We are LIDAR PLANES , active in the Geospatial industy. We would like to use our data to launch a new branch in the insurrance business. So, we need you to build a solution with our data to model a house in 3D with only a home address in the area of Flanders.

#### What is LIDAR ?
LIDAR is a method to measure distance using light. The device will illuminate a target with a laser light and a sensor will measure the reflection. Differences in wavelength and return times will be used to get 3D representations of an area.

The lidardata used is from "The digitaal hoogtemodel vlaanderen" 
(https://overheid.vlaanderen.be/dhm-digitaal-hoogtemodel-vlaanderen-ii) 

This data of Flanders is segmented in 43 zones, due to the file size otherwise being to big.

The data contains two differen types of lidardata(geoTIFF files):

* Digital Surface Model (DSM) represents the earth's surface and includes all objects on it
http://www.geopunt.be/download?container=dhm-vlaanderen-ii-dsm-raster-1m&title=Digitaal%20Hoogtemodel%20Vlaanderen%20II,%20DSM,%20raster,%201m
* Digital Terrain Model (DTM) represents the bare ground surface without any objects like plants and buildings
http://www.geopunt.be/download?container=dhm-vlaanderen-ii-dtm-raster-1m&title=Digitaal%20Hoogtemodel%20Vlaanderen%20II,%20DTM,%20raster,%201m

To be able to plot a 3D house, the Canopy height model (CHM) should be calculated.
This can be done as follows:
CHM = DSM - DTM

More explenation can be found on following link:
https://www.earthdatascience.org/courses/use-data-open-source-python/data-stories/what-is-lidar-data/lidar-chm-dem-dsm/

NOTE: these files were downloaded and unzipped in directory: 'home/regis/Desktop/3D house/k01', change this to the directory where your unzipped DTM and DSM files are.

## 3D_house.py

This file prints the 3D house of a certain adress in Flanders; using the DSM and DTM data from "The digitaal hoogtemodel vlaanderen".

The rendered plots below are for the adress: Koophandelsplein 23, 9000 Gent

Google maps link:
https://www.google.com/maps/place/Koophandelsplein+23,+9000+Gent/@51.0499612,3.71851,17z/data=!4m13!1m7!3m6!1s0x47c3714480aeb4dd:0xc7db0f3c8e38c500!2sKoophandelsplein+23,+9000+Gent!3b1!8m2!3d51.0499612!4d3.7206987!3m4!1s0x47c3714480aeb4dd:0xc7db0f3c8e38c500!8m2!3d51.0499612!4d3.7206987

Steps of the code:
1. Import necessary packages: lines 1-15
2. Render plotly.io figures in browser, due to plotly not being able to plot directly in spyder: lines 17-19
3. Ask user for adress: line 21-25
4. Search for the coordinates of the floorplan of this house using the API "Basisregisters Vlaanderen": line 30-44
5. Create a polygon from these coordinates which is necessary when masking a TIFF-file: line 46-55
6. Determine in which of the 43 zones the adress can be found: lines 57-97
7. Open the DSM and DTM file of the correct zone: lines 99-117 
8. Calculate the CHM, by masking the DSM and DTM tiff files with the polygon of the house: lines 119-120
9. Create a 2D-plot of the house, with height differences portrayed by different collors, by using earthpy.plot and matplotlib.pyplot: lines 122-125


![alt text](https://github.com/RegisSchulze/3D_houses_numpy/blob/main/2d_koophandelsplein_23_gent.png?raw=true)

11. Create a 3D-plot of the house using plotly.io: lines 127-130

![alt text](https://github.com/RegisSchulze/3D_houses_numpy/blob/main/3d_koophandelsplein_23_gent.png?raw=true)

![alt text](https://github.com/RegisSchulze/3D_houses_numpy/blob/main/3d_koophandelsplein_23_2.png?raw=true)



13. Print execution time: lines 132-133


## 3D_house_extra_attributes.py
Under development


### Have fun!!!


