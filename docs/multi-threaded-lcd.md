### Getting your 16X2 LCD run correctly on multi-threaded program

You would often find yourself wrestling around with the connections for an LCD and the Adafruit library [here](https://github.com/adafruit/Adafruit_Python_CharLCD). They have distilled the entire setup and personally I feel it cannot be any more easier than that. But there is always that odd spot where you find either a blank screen or screen full of just contratsting boxes. Afterall, 4 data, 2 selects, and couple of supply voltages makes it too many connections. (Just bumps up the number of possibilities you may go wrong) Either of the cases , after some efforts when you finally get the basic text display on the screen you are hoping that it would be an easy ride ahead of this.

> Mixing threads and the LCD, that is not so fast, can leave you with a LCD with alien characters on the screen. While it can excite some of you thinking it to be some message from the Decepticons :) , it really is some issue with the underlying threaded applications. Are there multiple threads accessing the LCD ?

Make a diagram to exaplain what I want to bring about  - Sequential access and multi-threaded simulteneous access

![Illustrating Tsafe LED](tsafeled.gif, "Just a illustration")
