import os
import pandas as pd
import visidata
import requests as r
from datetime import datetime

print("What do you want to explore?")
print("1. Global Covid-19 Update Today")
print("2. Global Covid-19 Update since outbreak")
print("3. Indonesia Covid-19 Update Today by Province")
print("4. Indonesia Covid-19 Update since outbreak")

options = input("Input:")
savedata = input("Save Data [Y/N]:")
savedata = savedata.lower()

rename = False
transform = False
storage = "./saved/"
filename = ""

if options == "1":
    QUERY_URL = 'https://services.arcgis.com/5T5nSi527N4F7luB/arcgis/rest/services/Cases_by_country_pt_V3/FeatureServer/0/query?f=json&where=(ADM0_NAME%20%3C%3E%20%27Serbia%27)%20AND%20(ADM0_NAME%20%3C%3E%20%27Kosovo%5B1%5D%27)&returnGeometry=true&spatialRel=esriSpatialRelIntersects&maxAllowableOffset=78271&geometry=%7B%22xmin%22%3A-20037508.342788905%2C%22ymin%22%3A-20037508.342779063%2C%22xmax%22%3A20037508.342779063%2C%22ymax%22%3A20037508.342788905%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%7D%7D&geometryType=esriGeometryEnvelope&inSR=102100&outFields=*&outSR=102100&resultType=tile'
    transform = True
    filename = "covid-19_world_{}.csv".format(datetime.now().strftime("%Y_%m_%d"))
elif options == "2":
    QUERY_URL = 'https://services.arcgis.com/5T5nSi527N4F7luB/arcgis/rest/services/Historic_adm0_v3/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=OBJECTID%2CNewCase%2CDateOfDataEntry&orderByFields=DateOfDataEntry%20asc&resultOffset=0&resultRecordCount=2000&cacheHint=true'
    filename = "covid-19_world.csv"
elif options == "3":
    QUERY_URL = 'https://services5.arcgis.com/VS6HdKS0VfIhv8Ct/arcgis/rest/services/COVID19_Indonesia_per_Provinsi/FeatureServer/0/query?f=json&where=(Kasus_Posi%20%3C%3E%200)%20AND%20(Provinsi%20%3C%3E%20%27Indonesia%27)&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Kasus_Posi%20desc&outSR=102100&resultOffset=0&resultRecordCount=34&cacheHint=true'
    name = "indonesia"
    filename = "covid-19_ina_province_{}.csv".format(datetime.now().strftime("%Y_%m_%d"))
else:
    QUERY_URL = 'https://services5.arcgis.com/VS6HdKS0VfIhv8Ct/arcgis/rest/services/Statistik_Perkembangan_COVID19_Indonesia/FeatureServer/0/query?f=json&where=Tanggal%3Ctimestamp%20%272020-04-01%2016%3A00%3A00%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Tanggal%20asc&outSR=102100&resultOffset=0&resultRecordCount=2000&cacheHint=true'
    filename = "covid-19_ina_all.csv"
    rename = {
            "Hari_ke":"Hari ke",
            "Tanggal":"Tanggal",
            "Jumlah_Kasus_Baru_per_Hari":"Kasus Baru",
            "Jumlah_Kasus_Kumulatif":"Total Kasus",
            "Jumlah_pasien_dalam_perawatan":"Pasien Dirawat",
            "Persentase_Pasien_dalam_Perawatan":"Persentase Dirawat",
            "Jumlah_Pasien_Sembuh":"Sembuh (Total)",
            "Persentase_Pasien_Sembuh":"Persentase Sembuh",
            "Jumlah_Pasien_Meninggal":"Meninggal (Total)",
            "Persentase_Pasien_Meninggal":"Persentasi Meninggal",
            "Jumlah_Kasus_Sembuh_per_Hari":"Sembuh",
            "Jumlah_Kasus_Meninggal_per_Hari":"Meninggal",
            "Jumlah_Kasus_Dirawat_per_Hari":"Pasien Baru"
        }

data = r.get(QUERY_URL).json()
features = data.get('features')

if options == "2":
    for feature in features:
        date = datetime.fromtimestamp(feature['attributes']['DateOfDataEntry'] / 1e3)
        date = date.strftime("%Y-%m-%d")
        del feature['attributes']['DateOfDataEntry']
        del feature['attributes']['OBJECTID']
        feature['attributes'].update({"date":date})
if options == "4":
    for feature in features:
        date = datetime.fromtimestamp(feature['attributes']['Tanggal'] / 1e3)
        date = date.strftime("%Y-%m-%d")
        feature['attributes'].update({"Tanggal":date})

if transform:
    for feature in features:
        feature['attributes'].update({
            'longitude' :feature['geometry']['x'],
            'latitude' :feature['geometry']['y'],
        })

data = pd.DataFrame([feature['attributes'] for feature in features])
if rename:
    data.rename(columns=rename)


if not os.path.exists('./tmp'):
    os.makedirs('./tmp')

data.to_csv("./tmp/tmp.csv")

vd = input("View Data? [Y/N]")
vd = vd.lower()

if vd == "y":
    visidata.view_pandas(data)

if savedata == "y":
    if not os.path.exists(storage):
        os.makedirs(storage)
    data.to_csv(storage + filename)
