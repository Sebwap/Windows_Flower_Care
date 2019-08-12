# Windows_Flower_Care
A simple python example to read values from Xiaomi Flower Care device from a Windows 10 PC.

It use bleak as library to communicate with Bluetooth LE driver.

Many thanks to:

https://github.com/vrachieru/xiaomi-flower-care-api/ for doc about Xiaomi GATT protocol

https://github.com/hbldh/bleak for wonderfull work on Bleak !

Feel free to make a better code of this, it was just made in a few hours just to see if it was possible under Windows 10.

Sample result below:
Name: Flower care
Firmware version: 3.2.1
Battery level: 98 %
Seconds since boot: 1357390
===== Real Time =====
Temperature: 18.2 °C
Light: 362  lux
Moisture: 37 %
Fertility: 326 µS/cm
===== Hystoric measures =====
14 value(s) stored
Date:2019-08-12 20:42:51 +0200 > Temp:18.7°C Moist 37% Light 68 mmol (1022 Lux) Fert 319 µS/cm
Date:2019-08-12 19:42:51 +0200 > Temp:19.9°C Moist 37% Light 171 mmol (2559 Lux) Fert 309 µS/cm
Date:2019-08-12 18:42:51 +0200 > Temp:20.4°C Moist 38% Light 257 mmol (3860 Lux) Fert 306 µS/cm
Date:2019-08-12 17:42:51 +0200 > Temp:21.1°C Moist 37% Light 505 mmol (7579 Lux) Fert 301 µS/cm
Date:2019-08-12 16:42:51 +0200 > Temp:19.9°C Moist 37% Light 259 mmol (3880 Lux) Fert 307 µS/cm
Date:2019-08-12 15:42:51 +0200 > Temp:21.3°C Moist 37% Light 609 mmol (9136 Lux) Fert 297 µS/cm
Date:2019-08-12 14:42:51 +0200 > Temp:23.6°C Moist 38% Light 826 mmol (12393 Lux) Fert 283 µS/cm
Date:2019-08-12 13:42:51 +0200 > Temp:18.6°C Moist 37% Light 470 mmol (7047 Lux) Fert 306 µS/cm
Date:2019-08-12 12:42:51 +0200 > Temp:21.1°C Moist 38% Light 510 mmol (7647 Lux) Fert 292 µS/cm
Date:2019-08-12 11:42:51 +0200 > Temp:20.3°C Moist 37% Light 543 mmol (8145 Lux) Fert 294 µS/cm
Date:2019-08-12 10:42:51 +0200 > Temp:17.9°C Moist 36% Light 261 mmol (3908 Lux) Fert 307 µS/cm
Date:2019-08-12 09:42:51 +0200 > Temp:16.7°C Moist 36% Light 167 mmol (2498 Lux) Fert 315 µS/cm
Date:2019-08-12 08:42:51 +0200 > Temp:15.9°C Moist 36% Light 108 mmol (1620 Lux) Fert 320 µS/cm
Date:2019-08-12 07:42:51 +0200 > Temp:15.5°C Moist 36% Light 33 mmol (493 Lux) Fert 324 µS/cm

Unfortunately, sometimes, the result is only
bleak.exc.BleakError: Device with address XX:XX:XX:XX:XX:XX was not found.
I don't know why the device seem to be invisible sometimes.
