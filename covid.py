import pandas as pd
import requests as r
from datetime import datetime

QUERY_URL = 'https://services.arcgis.com/5T5nSi527N4F7luB/arcgis/rest/services/Cases_by_country_pt_V3/FeatureServer/0/query?f=json&where=(ADM0_NAME%20%3C%3E%20%27Serbia%27)%20AND%20(ADM0_NAME%20%3C%3E%20%27Kosovo%5B1%5D%27)&returnGeometry=true&spatialRel=esriSpatialRelIntersects&maxAllowableOffset=78271&geometry=%7B%22xmin%22%3A-20037508.342788905%2C%22ymin%22%3A-20037508.342779063%2C%22xmax%22%3A20037508.342779063%2C%22ymax%22%3A20037508.342788905%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%7D%7D&geometryType=esriGeometryEnvelope&inSR=102100&outFields=*&outSR=102100&resultType=tile'

data = r.get(QUERY_URL).json()
features = data.get('features')

for feature in features:
    feature['attributes'].update({
        'longitude' :feature['geometry']['x'],
        'latitude' :feature['geometry']['y'],
    })

data = pd.DataFrame([feature['attributes'] for feature in features])
data.to_csv("covid-19_{}.csv".format(datetime.now().strftime("%Y_%m_%d")))

