### Project Aquascape minder:

A healthy aquarium with all natural aqua scape has precision controlled parameters. While the marine life can sustain some aberrations , it is best to have close control over the water body parameters. We have also made an attempt to keep all the items in the aquarium natural with minimum interference from plastic or non biological items.

Here is what our water body has now , not very diverse marine life.

|Item|Quantity|
|-----|-----|
|Serphae Tetra fish|11|
|Chinese golden algae eater|2|
|Neon Tetra fish|12|
|Green ring turtle|1|

All the enlisted are tropical life and tolerate a temperature of about 21<sup>o</sup>C to about 27<sup>o</sup>C, 6hours of LED light :4 Watts, and aeration of approximately 6 hours.

While aquarists would argue that this is not much of a task switching off / on certain accessories of the aquariums at any time during the day, automation systems allow you a chance to monitor higher parameters taking control of the drudgery of keeping a schedule clock of the aquarium. One may realize how vital this is when away from the aquarium.

> Don't you want someone to tend your pets while you are on your vacation ? Would you trust someone else's approximation of food and put the habits of your pets at stake ?

- __One__ is , it leaves the repetitive precision controlled tasks to the microprocessor (RPi in this case) and sets you free from having to keep a track of the sensitive schedule. You can leave your home WiFi ON and this would mean the system smoothly controls all electrical equipment as per the schedule. Setting the schedule is also an one time activity from either your android or your desktop.

- __Two__ is you have a remote handle / track of the electrical accessories and can even alter the schedule, force a restart on the system. Incase of emergency you can switch to manual mode and hijack control from the microprocessor. Casein - you know when to switch ON / OFF which accessory. Upon restart , the system then picks up internet local time and resumes the schedule from where it had left / crashed

> Electronic system that helps you program a schedule for your aquarium and its electrical accessories, and keep a track of the same remotely. A time keeper for all the accessories maintaining optimal ON / OFF time

### Outline of the solution



### What we are currently not doing :

1. We currently are unable to keep a track of the pH levels in the water body.
2. Nitrate / Nitrite concentration -a typical aquaponic system would need that.
3. Water turbidity and keep a measured record of the same.  - This also measures the efficiency of the filtering system.
4. Photograph of the tank that denotes the current state
5. Water temperature , this helps us schedule the water heater.


### But we intend to get these rolled out soon :

1.  Temperature probe that helps keep a track of the water temperature and schedule the heater to maintain it comfortable for the tropical marine life.
2. pH sensors - current cost restrictions are keeping us from doing this.
3. Manual mode override : There are unforeseen events when you would want to hijack control from the system , interrupt the schedule and play various accessories at times other than scheduled.
4. Settings changed on the cloud should force a restart of the services with the new setting.

### Technology stack

|Technology|Used for|Remarks|
|----|----|----|
|Raspberry Pi|Central microprocessor used for programmed controlling|RPi3B+ 2GB RAM|
|Python software on RPi|Program running on the microprocessor helps to time and control everything|RPi3B+ 2GB RAM|
|Cloud endpoints|HTTP REST cloud endpoints are the gateway for the microprocessor to store away settings and state. This is is what gets us the remoting capability|Cloud hosted HTTP services|
|Web App|Responsive web application for devices of all aspect ratios |HTMLCSS web app that works on mobile as well on desktops|
