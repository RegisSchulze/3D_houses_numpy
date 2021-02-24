#import necessary packages
import requests
import json
import fiona
import pandas as pd
import rasterio
import rasterio.mask
import matplotlib.pyplot as plt
import earthpy.plot as ep
import numpy as np
import plotly.graph_objects as go
import time
from shapely.geometry import Polygon
import geopandas as gpd
import plotly.io as pio
#added to be able to display plotly 3d graph in browser 
#as this does not plot in spyder directly
pio.renderers.default='browser'

#ask user adress
postal_code=input('Postcode?')
city=input('Gemeente?')
street=input('Straatnaam?')
number=input('Huisnummer?')

#used for calculating total runtime
start_time = time.time()


#go the vlaanderen basisregisters api under section adresmatch
r=requests.get('https://api.basisregisters.vlaanderen.be/v1/adresmatch', params={'postcode':postal_code, 'straatnaam':street, 'huisnummer':number})
jsn = json.loads(r.content)
#find link to gebouweenheden section of the vlaanderen basisregisters api based on detail
detail=jsn['adresMatches'][0]['adresseerbareObjecten'][0]['detail']
#use this link to go to the vlaanderen basisregisters api under section gebouweenheden
r=requests.get(detail)
jsn_2 = json.loads(r.content)
#find link to gebouwen section of the vlaanderen basisregisters api based on detail
detail_2=jsn_2['gebouw']['detail']
#use this link to go to the vlaanderen basisregisters api under section gebouwen
r=requests.get(detail_2)
jsn_3 = json.loads(r.content)
#get coordinates of this adress
shape=jsn_3['geometriePolygoon']['polygon']['coordinates'][0]

#create polygon from these coordinates
x_coordinates=[]
y_coordinates=[]
for i in shape:
    x_coordinates.append(i[0])
    y_coordinates.append(i[1])
polygon = Polygon(zip(x_coordinates,y_coordinates))
polygon_2 = gpd.GeoDataFrame(index=[0], geometry=[polygon])      
#polygon of given adress 
shapes=polygon_2.geometry

#determine in which of the 43 zones the adress can be found
#find details about house and especially the x and y coordinates by using geopunt
adres='http://loc.geopunt.be/geolocation/location?q='+street+' '+number+', '+postal_code+' '+city
r=requests.get(adres)
#find x and y coordinates of the house
jason = json.loads(r.content)
x_house=jason['LocationResult'][0]['BoundingBox']['LowerLeft']['X_Lambert72']
y_house=jason['LocationResult'][0]['BoundingBox']['LowerLeft']['Y_Lambert72']

#look in one of 43 zones to find tif file for canopy height model
#get zone bounds of all zones by iterating over each zone shape file
df = pd.DataFrame(columns=['x1','y1','x2','y2','zone'])
for i in range(1,43):
    if i < 10:
        file='/home/regis/Desktop/3D house/k01/DHMVIIDSMRAS1m_k0'+str(i)+'/DHMVII_vdc_k0'+str(i)+'/DHMVII_vdc_k0'+str(i)+'.shp'
        c = fiona.open(file)
        #get bound
        x1=c.bounds[0]
        y1=c.bounds[1]
        x2=c.bounds[2]
        y2=c.bounds[3]
        bound=pd.DataFrame([[x1,y1,x2,y2,i]],columns=['x1','y1','x2','y2','zone'])
        #get all bounds of all zones in a pandas df with indexes(zone=number) and columnames(x1,y1,x2,y2) fitting
        df=pd.concat([df,bound])
    else:
        file='/home/regis/Desktop/3D house/k01/DHMVIIDSMRAS1m_k'+str(i)+'/DHMVII_vdc_k'+str(i)+'/DHMVII_vdc_k'+str(i)+'.shp'
        c = fiona.open(file)
        #get bound
        x1=c.bounds[0]
        y1=c.bounds[1]
        x2=c.bounds[2]
        y2=c.bounds[3]
        bound=pd.DataFrame([[x1,y1,x2,y2,i]], columns=['x1','y1','x2','y2','zone'])
        #get all bounds of all zones in a pandas df with indexes(zone=number) and columnames(x1,y1,x2,y2) fitting
        df=pd.concat([df,bound])
#reset to sequential index
df=df.reset_index(drop=True)
#find which zone 
zone_bounds=df[(df['x1'] < x_house) & (df['x2'] > x_house) & (df['y1'] < y_house) & (df['y2'] > y_house)]
#zone of house has been found
zone_number=zone_bounds.zone.iloc[0]

#open correct Digital Surface Model(=DSM) and Digital Terrain Model(=DTM) file
if zone_number < 10:   
    with rasterio.open("/home/regis/Desktop/3D house/k01/DHMVIIDSMRAS1m_k0"+str(zone_number)+"/GeoTIFF/DHMVIIDSMRAS1m_k0"+str(zone_number)+".tif") as src:
            out_image_DSM, out_transform = rasterio.mask.mask(src, shapes, crop=True)
            #out_meta = src.meta
            DSM=out_image_DSM[0]
        
    with rasterio.open("/home/regis/Desktop/3D house/k01/DHMVIIDTMRAS1m_k0"+str(zone_number)+"/GeoTIFF/DHMVIIDTMRAS1m_k0"+str(zone_number)+".tif") as src:
            out_image_DTM, out_transform = rasterio.mask.mask(src, shapes, crop=True)
            #out_meta = src.meta
            DTM=out_image_DTM[0]
else:
    with rasterio.open("/home/regis/Desktop/3D house/k01/DHMVIIDSMRAS1m_k"+str(zone_number)+"/GeoTIFF/DHMVIIDSMRAS1m_k"+str(zone_number)+".tif") as src:
            out_image_DSM, out_transform = rasterio.mask.mask(src, shapes, crop=True)
            #out_meta = src.meta
            DSM=out_image_DSM[0]
        
    with rasterio.open("/home/regis/Desktop/3D house/k01/DHMVIIDTMRAS1m_k"+str(zone_number)+"/GeoTIFF/DHMVIIDTMRAS1m_k"+str(zone_number)+".tif") as src:
            out_image_DTM, m = rasterio.mask.mask(src, shapes, crop=True)
            #out_meta = src.meta
            DTM=out_image_DTM[0]

#calculate Canopy Height Model(=CHM) for this house
out_image_CHM = DSM - DTM

#create 2D-plot with z-axis equaling the CHM
ep.plot_bands(out_image_CHM,
              cmap='terrain')
plt.show()


#create x and y coordinates for which we have CHM value
x=np.linspace(shapes.bounds.iloc[0][0],shapes.bounds.iloc[0][2], out_image_CHM.size)
y=np.linspace(shapes.bounds.iloc[0][1],shapes.bounds.iloc[0][3], out_image_CHM.size)
z=out_image_CHM
#use plotly to plot 3d interactive figure in browser
fig = go.Figure(data=[go.Surface(z=z)])
fig.update_layout(title='Mt Bruno Elevation', autosize=True,
                  margin=dict(l=65, r=50, b=65, t=90))
fig.show()

#print runtime
print("--- %s seconds ---" % (time.time() - start_time))

