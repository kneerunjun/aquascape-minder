# Aquascape-minder
A smart aquarium project to get off the responsibility of having to turn on / off aquarium accessories at the right time so as to maintain a conducive environment for the marine life therein

We start off testing the hardware and software on a aqua-scape of 2' X 1' X 8" - recalculations would then be proportionately necessary for environment of various sizes.

Driven by Raspberry Pi3B we expect to measure / control the following things :

Features of the end product :

- Water temperature control, heater schedule
- Water level / replenish schedule
- PH of the water
- Water filter schedule
- LED lightening schedule
- Marine food schedule
- Remote handle on accessories, monitoring

#### Type marine life :

| Creature            | Nos             | Sensitive to  |
| -------------       |:-------------:  | -----:|
| Neon Tetra          | 12              |       |
| Golden sucker fish  | 2               |       |
| Turtles             | 1               |       |
| Silver shark        | 5               |       |

We are training the electronics on diverse marine life. All life have different sensitivity areas. This would let us monitor the effect upon failure of the system.


#### List of sensory nodes, actuators & chipsets:


1. [Water level indicator](https://www.amazon.in/Phenovo-Sensor-Arduino-Surface-recognition/dp/B0777HZLMP/ref=sr_1_4?ie=UTF8&qid=1524232700&sr=8-4&keywords=water+level+sensor+arduino)
2. [Water temperature](https://www.amazon.in/KitsGuru-Waterproof-DS18B20-Digital-Temperature/dp/B00XTX0UQE/ref=sr_1_1?ie=UTF8&qid=1524232773&sr=8-1&keywords=water+temperature+sensor#detail_bullets_id)
3. [Water pH probe](https://www.amazon.in/Generic-Ph-Electrode-Connector-Controller/dp/B01M6ZKTTG/ref=sr_1_fkmr1_2?ie=UTF8&qid=1524232870&sr=8-2-fkmr1&keywords=water+ph+sensor+arduino)
4. [Water pH module](https://www.amazon.in/SLB-Works-Detection-arduino-Monitoring/dp/B077JRWZSH/ref=sr_1_fkmr1_3?ie=UTF8&qid=1524232870&sr=8-3-fkmr1&keywords=water+ph+sensor+arduino)
5. [4 channel relay](https://www.amazon.in/REES52-Optocoupler-Channel-Control-Arduino/dp/B01HXM1G9Q/ref=sr_1_1?ie=UTF8&qid=1524233009&sr=8-1&keywords=relay+for+arduino)
6. [Water pump](https://www.amazon.in/dp/B07CJG6SJR/ref=sr_1_14?s=industrial&ie=UTF8&qid=1524233181&sr=1-14&keywords=aquarium)
7. [ADC over I2c](https://www.amazon.in/gp/product/B01985E9CW/ref=oh_aui_search_detailpage?ie=UTF8&psc=1)
