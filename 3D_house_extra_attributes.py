#%%
import requests
import json
import fiona
import geopandas as gpd
import pandas as pd
import rasterio
import rasterio.mask
import matplotlib.pyplot as plt
import earthpy.plot as ep
import numpy as np


gbg =gpd.read_file('/home/regis/Desktop/3D house/k01/Gbg_20210217_Shapefile/Shapefile/Gbg.shp')

#%%

'''postal_code=input('Postcode?')
city=input('Gemeente?')
street=input('Straatnaam?')
number=input('Huisnummer?')
adres='http://loc.geopunt.be/geolocation/location?q='+street+' '+number+', '+postal_code+' '+city
#r=requests.get('http://loc.geopunt.be/geolocation/location?q=pontweg 52, 9820 Merelbeke')
r=requests.get(adres)'''
r=requests.get('http://loc.geopunt.be/geolocation/location?q=Smeyerspad 25, 2910 Essen')
jason = json.loads(r.content)
x=jason['LocationResult'][0]['BoundingBox']['LowerLeft']['X_Lambert72']
y=jason['LocationResult'][0]['BoundingBox']['LowerLeft']['Y_Lambert72']
house_IODN = jason['LocationResult'][0]['ID']




'''
#find shape file from individual file
r=requests.get('https://api.basisregisters.vlaanderen.be/v1/adresmatch', params={'postcode':2910, 'straatnaam':'Smeyerspad', 'huisnummer':24})
adres = json.loads(r.content)
objectId=adres['adresMatches'][0]['adresseerbareObjecten'][0]['detail']
r=requests.get(objectId)
gebouweenheden = json.loads(r.content)
gebouw=gebouweenheden['gebouw']['detail']
r=requests.get(gebouw)
poly = json.loads(r.content)
shapes=poly['geometriePolygoon']'''




#x2=jason['LocationResult'][0]['BoundingBox']['UpperRight']['X_Lambert72']
#y2=jason['LocationResult'][0]['BoundingBox']['UpperRight']['Y_Lambert72']

#look in one of 43 zones to find tif file for canopy height model
#get zone bounds
#iterate over numbers of file
df = pd.DataFrame(columns=['x1','y1','x2','y2','zone'])
for i in range(1,18):
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
#reset to sequential indexext
df=df.reset_index(drop=True)
#find which zone 
zone_bounds=df[(df['x1'] < x) & (df['x2'] > x) & (df['y1'] < y) & (df['y2'] > y)]
zone_number=zone_bounds.zone.iloc[0]
#%%
#get the correct tif file
#house=gbg[gbg.OIDN == house_IODN]
houses=gbg[(gbg.LBLTYPE=='hoofdgebouw')]
house=houses[(houses.bounds.minx < x)&
             (houses.bounds.miny < y)&
             (houses.bounds.maxx > x)&
             (houses.bounds.maxy > y)]

#%%    
'''with fiona.open("/home/regis/Desktop/3D house/k01/DHMVIIDSMRAS1m_k01/DHMVII_vdc_k01/DHMVII_vdc_k01.shp", "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]'''
shapes=house.geometry
shapes_normal=shapes

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
'''with rasterio.open("/home/regis/Desktop/3D house/k01/DHMVIIDSMRAS1m_k02/GeoTIFF/DHMVIIDSMRAS1m_k02.tif") as src:
    out_image_DSM, out_transform = rasterio.mask.mask(src, shapes, crop=True)
    out_meta = src.meta
    DSM=np.concatenate((DSM,out_image_DSM[0]), axis=0)
with rasterio.open("/home/regis/Desktop/3D house/k01/DHMVIIDTMRAS1m_k02/GeoTIFF/DHMVIIDTMRAS1m_k02.tif") as src:
    out_image_DTM, out_transform = rasterio.mask.mask(src, shapes, crop=True)
    out_meta = src.meta
    DTM=np.concatenate((DTM,out_image_DTM[0]), axis=0)'''
    
    
    
out_image_CHM = DSM - DTM
print(out_image_CHM.dtype)
print(out_image_CHM.max())
print(out_image_CHM.min())
print(out_image_CHM.mean())


ep.plot_bands(out_image_CHM,
              cmap='terrain')
plt.show()
#%%
from mpl_toolkits import mplot3d
x=np.linspace(shapes.bounds.iloc[0][0],shapes.bounds.iloc[0][2], out_image_CHM.size)
y=np.linspace(shapes.bounds.iloc[0][1],shapes.bounds.iloc[0][3], out_image_CHM.size)
x,y=np.meshgrid(x[:out_image_CHM.shape[1]],y[:out_image_CHM.shape[0]])
figure=plt.figure(1)
subplot3d = plt.subplot(111,projection='3d')
surface = subplot3d.plot_surface(x,y,out_image_CHM,rstride=1,cstride=1,cmap=plt.cm.coolwarm,linewidth=0.01)
plt.show()

# heres what it looks like when you run this code
# https://i.imgur.com/APJny4a.png