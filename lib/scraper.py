import math
import time
from datetime import datetime
import ephem
import os
from pathlib import Path

#use this as reference for all paths henceforth.
#ensure we use absolute paths with reference to project home directory everywhere
# So that no errors are thrown when we run a script as say python ./lib/scraper.py from tracker home directory
project_home = Path("../")
#edit at all places


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

def printCoordinates(index,home):
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
	print ('todo');

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
                #                                         sat.az * degrees_per_radian)
    		time.sleep(1)
            
if __name__ == '__main__':
    home = setNITKHome()
    printCoordinates('00005',home)
