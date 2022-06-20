import os
import shutil
import ee
import requests
# from register import google_register
# google_register()
import geemap

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def example4():
  ee.Initialize()
  ee.Authenticate()

  def create_rect_polygon(center, width=1.0, hight=2.0):
    upper_left = [center[0]-width/2, center[1]-hight/2]
    lower_left = [center[0]-width/2, center[1]+hight/2]
    upper_right = [center[0]+width/2, center[1]-hight/2]
    lower_right = [center[0]+width/2, center[1]+hight/2]

    region =  ee.Geometry.Polygon(
            [[upper_left, lower_left, 
              upper_right, lower_right]],
              ) # proj=None, geodesic=False
    return region

  
  # ee_object = geemap.geojson_to_ee('example/train_field.json')
  # # print(type(ee_object))
  # geometry = ee_object.geometry()



  col_name = 'COPERNICUS/S2_SR'
  x = 10.96671229598333
  y = 44.65340259358304
  geometry = create_rect_polygon((x, y), width=1.0, hight=2.0)



  collection = S2_SR = ee.ImageCollection(col_name)
  S2_SR = collection.filterBounds(geometry)\
                    .filterDate('2018-01-01', '2019-01-01')

  def addNDVI(image):
    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
    return image.addBands(ndvi)
    # return image.addBands(image.expression('NDVI = (B8 - B4) / (B8 + B4)', {
    #       'B8': image.select('B8'),
    #       'B4': image.select('B4')}))

  ndvi_img = addNDVI(S2_SR.first())
  # ten_day_S2 = ndvi_col.sort('system:time_start', False).first()

  NDVIpalette = ['FFFFFF', 'CE7E45', 'DF923D',
                 'F1B555', 'FCD163', '99B718',
                 '74A901', '66A000', '529400',
                 '3E8601', '207401', '056201',
                 '004C00', '023B01', '012E01',
                 '011D01', '011301']

  url = ndvi_img.select('NDVI').getThumbUrl({
              "region": geometry, 
              #  "dimensions": '256x256',
               'dimensions': 512,
               'palette': NDVIpalette,
                'min': 0,
                'max': 1,
               "format": 'png'})
  # Print image object WITHOUT call to getInfo(); prints serialized request instructions.
  return url

  # Handle downloading the actual pixels.
  r = requests.get(url, stream=True)
  if r.status_code != 200:
    raise r.raise_for_status()

  if not os.path.exists('pics'):
      os.makedirs('pics')
  
  filename = 'pics/%05d.png' % 1
  with open(filename, 'wb') as out_file:
    shutil.copyfileobj(r.raw, out_file)
  logger.debug("saved-----")


# example4()
