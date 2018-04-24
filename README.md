# Aquascape-minder
A smart aquarium project to get off the responsibility of having to turn on / off aquarium accessories at the right time so as to maintain a conducive environment for the marine life therein

We start off testing the hardware and software on a aqua-scape of 2' X 1' X 8" - recalculations would then be proportionately necessary for environment of various sizes.

Driven by Raspberry Pi3B we expect to measure / control the following things :

Features of the end product :

|Parameter|Description|Control & Actuation|Rule|
|----|----|----|----|
|Illumination|LED illumination helps healthy foliage growth  in the tank, and provides embellishment|LED tube , A/C controlled from a D/C switch relay|Minimum of 06 hrs ON state|
|Temperature|For marine creatures we are working with are all tropical creatures|A/C water heater controlled from D/C relay|the temperature of the water is preferred between 24oC to 27oC|
|Aeration|Air pump is used to circulate air into the water body|A/C air pump|Atleast 5hours of ON time|
|Filtration|||
|pH levels|||
|Feeder|||


- Water temperature control, heater schedule
- Water level / replenish schedule
- PH of the water
- Water filter schedule
- LED lightening schedule
- Marine food schedule
- Remote handle on accessories, monitoring

#### Type marine life :

| Creature            | Nos             | About  |
| -------------       |:-------------:  | -----:|
| Neon Tetra          | 12              |  [More](https://www.fishlore.com/Profiles-NeonTetra.htm)     |
| Golden algae eater  | 2               | [More](https://www.aquariumdomain.com/adSocial/index.php/golden-chinese-algae-eater/)      |
| Turtles             | 1               | [More](http://animal-world.com/encyclo/reptiles/turtles/RingedMapTurtle.php)      |
| Serphae Tetra       | 11              |[More](https://www.fishlore.com/Profiles-SerpaeTetra.htm)        |

We are training the electronics on diverse marine life. All life have different sensitivity areas. This would let us monitor the effect upon failure of the system.


#### List of sensory nodes, actuators & chipsets:


1. [Water level indicator](https://www.amazon.in/Phenovo-Sensor-Arduino-Surface-recognition/dp/B0777HZLMP/ref=sr_1_4?ie=UTF8&qid=1524232700&sr=8-4&keywords=water+level+sensor+arduino)
2. [Water temperature](https://www.amazon.in/KitsGuru-Waterproof-DS18B20-Digital-Temperature/dp/B00XTX0UQE/ref=sr_1_1?ie=UTF8&qid=1524232773&sr=8-1&keywords=water+temperature+sensor#detail_bullets_id)
3. [Water pH probe](https://www.amazon.in/Generic-Ph-Electrode-Connector-Controller/dp/B01M6ZKTTG/ref=sr_1_fkmr1_2?ie=UTF8&qid=1524232870&sr=8-2-fkmr1&keywords=water+ph+sensor+arduino)
4. [Water pH module](https://www.amazon.in/SLB-Works-Detection-arduino-Monitoring/dp/B077JRWZSH/ref=sr_1_fkmr1_3?ie=UTF8&qid=1524232870&sr=8-3-fkmr1&keywords=water+ph+sensor+arduino)
5. [4 channel relay](https://www.amazon.in/REES52-Optocoupler-Channel-Control-Arduino/dp/B01HXM1G9Q/ref=sr_1_1?ie=UTF8&qid=1524233009&sr=8-1&keywords=relay+for+arduino)
6. [Water pump](https://www.amazon.in/dp/B07CJG6SJR/ref=sr_1_14?s=industrial&ie=UTF8&qid=1524233181&sr=1-14&keywords=aquarium)
7. [ADC over I2c](https://www.amazon.in/gp/product/B01985E9CW/ref=oh_aui_search_detailpage?ie=UTF8&psc=1)

#### Scheduling the water filter :

Incase of the water filter we want a fine balance between the hours of operation / day and the life of the filter. Continuous operation of the filter would mean we have lesser life expectancy while short stints of operation could mean we aren't keeping water body (tank) clean enough.

Air pump cannot run in the dark time, as we want the creatures to rest and have calm water body. Filter than can substitute the air supply and keep the water body aerated incase of depletion of O2 levels. We are not expecting the filter to entirely supply the O2 but just maintain a fine balance just incase of contingency.

We also need the water filter to be `OFF` when its feeding time. We have observed that leftover fishfood is then caught in the filter if it coincides.Typical comfortable schedule would be a hour after the food is suppled the filter can be set in `ON` state.

|Time of the day|Total hours |State|Remarks|
|-----|-----|-----|----|
|00:00-06:00|06|ON|Night time is the best time to filter, and also provide backup 02 just in case|
|06:00-12:00|06|OFF|No simultaneous run for filter and air pump|
|12:00-18:00|06|OFF|Everything is put off, maybe the feeder can be started here|
|18:00-00:00|06|OFF|Again we have air-pump on here|

> Experiment done on 24-APRIL-2018: confirms that running the filter for only 6hrs in the night can actually be beneficial. It has cleanses the water considerably while supporting the water body with oxygen contents just in case of depletion.

#### Scheduling the air pump :

Air pump and the water filter work at complimentary times. We don't want the air pump and the water filter working on coincident schedules.

|Time of the day|Total hours |State|Remarks|
|-----|-----|-----|-----|
|00:00-06:00|06|OFF|No coincidence with filter|
|06:00-12:00|06|ON|This puts the water body in high 02 levels|
|12:00-18:00|06|OFF|Only the LED light working here|
|18:00-00:00|06|ON|Just after the feed we have the air pump prepping for night time|

Air pump is proposed to work total of 12 hours/ day.

#### Scheduling the LED illumination :

|Time of the day|Total hours |State|Remarks|
|-----|-----|-----|-----|
|00:00-06:00|06|OFF|No illumination required during this slot|
|06:00-08:00|02|ON|Illumination here is good for plant growth and also good for decoration|
|08:00-18:00|10|OFF|No need for illumination during the day|
|18:00-00:00|06|ON|Required illumination for evening time|

- Notice the total ON time accounts for 08 Hours

#### Complete scheduling of the devices
---
The microprocessor here acts more like a state machine, controlling the state of various devices assisting the aquarium against the time of the day. We are not illustrating the heater cycle since that is dependent on the actual water temperature and such cannot be based on timeline.

We are currently exploring the availability of thermo probe that can work well with RPi 3B+


|Device|00:00-06:00|06:00-08:00|08:00-12:00|12:00-18:00|18:00-19:00|19:00-00:00|ON HRS|
|-----|-----|-----|-----|-----|-----|----|----|
|Filter|ON|OFF|OFF|OFF|OFF|OFF|06|
|Air pump|OFF|ON|ON|OFF|OFF|ON|11|
|LED|OFF|ON|OFF|OFF|ON|ON|10|
|Feeder|OFF|OFF|OFF|OFF|ON|OFF|01|


### Domain references

1. [Aquarium temperatures](https://www.thesprucepets.com/aquarium-water-temperature-1381896)
<sub><sup>So what is the best temperature for your fish? It depends on the species, but in general, tropical fish are most healthy in the range of 75-80°F (24-27°C). Cold water fish do better in temperatures well below that, some of them enjoy water well below 70°F, which is not suitable for any tropical fish.Ultimately the best temperature will depend on the species of fish in the aquarium. Research the fish you are interested in keeping before setting up an aquarium, and only chose those that have similar needs. Use a dependable heater, thermometer, and check the water temperature regularly to ensure frequent or large temperature changes don't occur.</sup><sub>
