Satellite Tracker
======

Github Repo of the satellite tracker built by AAC NITK as part of Astro Committee for Engineer 2016 and Engineer 2017.

_**THIS IS A WORK IN PROGRESS** We are actively working on this Roadmap._

## Proposed updates for 2017

### Hardware updates

* **Step 1.** `LEAP FROGGED` Remake 2016 Version  
* **Step 2.** **[IN PROGRESS]** Create base with DC motor for tracking azimuth ( one axis )
* **Step 2.1** `NEXT STEP` Control DC motor from python server through Arduino and Motor Driver (L293D)
* **Step 3.** `DONE` Get data the from sensor on the Arduino Nano.
Notes: Magnetometer Y axis isn't working. Using X and Z axis for orientation.
* **Step 4.** `DONE` Connect Arduino Nano to python server through Bluetooh. Notes: Used Serial COM.
* **Step 5.** `NEXT STEP` Make Feedback loop controller for azimuth
* **Step 6.** `POSTPONED FOR 2018` DO same for elevation (second axis)

### Stellarium Integration
* **Step 1.** **[IN PROGRESS]** Check out interfaces for Stellarium Telescope
  Control Protocol.
* **Step 2.** Check if data canbe directly sent to the backend upon selection of
  object

### Online APIs
* Check for Web APIs that will provide satellite data directly.
