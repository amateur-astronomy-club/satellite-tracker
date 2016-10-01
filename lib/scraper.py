import math
import time
from datetime import datetime
import ephem
import os
from pathlib import Path


degrees_per_radian = 180.0 / math.pi


def setDefaultHome():
	home = ephem.Observer()
	home.lon = '0.0000'   # +E
	home.lat = '0.0000'      # +N
	home.elevation = 0 # meters
	return home
	
def setNITKHome():
	home = ephem.Observer()
	home.lon = '74.7937'   # +E
	home.lat = '13.0119'      # +N
	home.elevation = 24 # meters
	return home
	
def setCurrentHome():
	home = ephem.Observer()
	#TODO: Get current location
	return home

def printCoordintes(index,home):
	TLEfileExists = Path("./TLE/" + index + '.txt')
	if (TLEfileExists.is_file() == False):
		os.system('./GetTLE.sh '+ index)
		
	tlefile=open('./TLE/'+ index + '.txt', 'r').read()
	tlesplit=tlefile.split('\n')
	
	assert len(tlesplit) >= 3
	
	sat = ephem.readtle(index,tlesplit[1],tlesplit[2])

   	while True:
    		home.date = datetime.utcnow()
    		sat.compute(home)
    		print '\rsat: altitude %4.1f deg, azimuth %5.1f deg'% (sat.alt * degrees_per_radian,
                                                         sat.az * degrees_per_radian)
    		time.sleep(1)
    		
def convertToIndex (SateliteName):
	#TODO: Given satellite name, convert to index (use dictionary)   		
    		
def sendCoordinates(index , home):
	#Get TLE and convert to coordinates, send to arduino
	TLEfileExists = Path("./TLE/" + index + '.txt')
	if (TLEfileExists.is_file() == False):
		os.system('./GetTLE.sh '+ index)
		
	tlefile=open('./TLE/'+ index + '.txt', 'r').read()
	tlesplit=tlefile.split('\n')
	
	assert len(tlesplit) >= 3
	
	sat = ephem.readtle(index,tlesplit[1],tlesplit[2])

   	while True:
    		home.date = datetime.utcnow()
    		sat.compute(home)
    		#TODO: Convert this to sending it to arduino, maybe add arguments
    		#print '\rsat: altitude %4.1f deg, azimuth %5.1f deg'% (sat.alt * degrees_per_radian,
                                                         sat.az * degrees_per_radian)
    		time.sleep(1)
    		
home = setNITKHome()
printCoordinates('00005',home)    		
