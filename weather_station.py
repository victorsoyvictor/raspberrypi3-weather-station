#!/usr/bin/python3
import mpl_mod as MPL3115A2 #written by me
import Adafruit_DHT as DHT #written by community
import http.client
import urllib.request
import urllib.parse
import json
import time

api_url = "http://api.carriots.com/streams"
device = "pi@victorsoyvictor.victorsoyvictor"
api_key = "6f2edce47c0092869e50d0ab88be331ef6d8ed062da04cf3ac15e41df8b66f65"

#parameter - body 
timestamp = int(time.time())

#GPIO 23 will be used and DHT22 is the sensor that we use
humidity, temperature = DHT.read_retry(DHT.DHT22, 23)
pressure, altitude, temperatureC_MPL, temperatureF_MPL = MPL3115A2.getValues()

#params for uploading into Carriots. DHT and MPL suffix are my sensors
params = {
    "protocol": "v2",
    "checksum": "",
    "device": device,
    "at": "now",
    "data": dict(
		temp_DHT  = '{0:0.2f}*C'.format(temperature),
		hum_DHT   = '{0:0.2f}%'.format(humidity),
		tempC_MPL = '{0:0.2f}*C'.format(temperatureC_MPL),
		tempF_MPL = '{0:0.2f}*F'.format(temperatureF_MPL),
		alt_MPL   = '{0:0.2f} m'.format(altitude),
		press_MPL = '{0:0.2f} kPa'.format(pressure))}

binary_data = json.dumps(params).encode('ascii')

#Header
header = {"User-Agent": "raspberrycarriots",
              "Content-Type": "application/json",
              "carriots.apikey" : api_key}

#Request
req = urllib.request.Request(api_url,binary_data,header)
f = urllib.request.urlopen(req)

#Print response
#print(f.read().decode('utf-8'))

#print pretty way
data=json.loads(f.read().decode('utf-8'))
print(json.dumps(data,indent=4,sort_keys=True))
