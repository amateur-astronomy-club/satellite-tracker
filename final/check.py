from pathlib2 import Path
from auromat.coordinates.spacetrack import Spacetrack

def checkTLE(index):
      TLEfileExists = Path("./TLE/" + index + '.txt')
      if (TLEfileExists.is_file() == False):
          getnewtle(index)

def getnewtle(index):
      # API credentials
      newsat = Spacetrack("asavari.limaye@gmail.com", "2016AACNITK2017")
      tledata = newsat.query(
          "class/tle_latest/NORAD_CAT_ID/%s/orderby/ORDINAL asc/limit/1/format/3le/metadata/false" % index)

      writefile = open("./TLE/" + index + '.txt', "w")
      writefile.write(tledata)
      writefile.close()
