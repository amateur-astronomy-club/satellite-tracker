Satellite Tracker
======

Github Repo of the satellite tracker built by AAC NITK as part of Astro Committee for Engineer 2016 and Engineer 2017.

## Proposed updates for 2017

### Hardware updates

* **Step 1.** `LEAP FROGGED` Remake 2016 Version  
* **Step 2.** `DONE` Create base with DC motor for tracking azimuth ( one axis )
* **Step 2.i.** `DONE` Control DC motor from python server through Arduino and Motor Driver (L293D)
* **Step 3.** `DONE` Get data the from sensor on the Arduino Nano.
Notes: Magnetometer Y axis isn't working. Using X and Z axis for orientation.
* **Step 4.** `DONE` Connect Arduino Nano to python server through Bluetooh. Notes: Used Serial COM.
* **Step 5.** `DONE` Make Feedback loop controller for azimuth (PID)
* **Step 6.** `POSTPONED FOR 2018` DO same for elevation (second axis)

### Stellarium Integration
* **Step 1.** `DONE` Check out interfaces for Stellarium Telescope
  Control Protocol.`[SkyPointer, Arduino-Telescope-Control]` (Can only seek, cannot track)
* **Step 2.** `BUILT GUI INSTEAD` Check if data can be directly sent to the backend upon selection of
  object

### Online APIs
* `ABANDONED IN FAVOUR OF WEB APP`Check for Web APIs that will provide satellite data directly.
