# Sign-chan
My first attempt at making software based on the stack-chan project<br>
PLEASE NOTE: This is my first time using github , mistakes will be made! <br>
<br>
This is NOT based on the Stack-chan body. Because I am using the CORE2-AWS I only used a signle servo<br>
and attached it to a base plate so that it only rotates on the X-axis. <br>
If you run this code on the CORE2 , you will have to modify the code for the LED lights to the appropriate pins as well as<br>
the code for the servo for the appropriate pins. The info is in the code.<br>
<br>
<br>
Based on the following : <br>
- M5STACK CORE2-AWS ( SKU: K010-AWS ) 
- M5STACK OLED      ( SKU: U119  )
- M5STACK 180 SERVO ( SKU: A076-B )
- Lego Technic parts:<br>
Technic, Panel Plate 11 x 19 x 1, LEGO Item No: 39369<br>
Pins and brackets included in the A076B kit<br>
- Visual Studio Code with M5STACK plugins
- UiFlow Micropython firmware v. 1.10.9

Thanks to : <br>
- The M5STACK community on TWITTER ( @M5STACK )
- @mongonta555


Avatar code : <br>
 M5StackAvatar BLOCK<br>
 Based on M5StackAvatarPython : https://github.com/h-akanuma/M5StackAvatarPython <br>
 v1.0 (220801)<br>
 Copyright (c) 2022 @akita11, Released under the MIT license<br>
 NOTE : I have modified this code to correct bugs, with the help of the creator of the code. 
<br>
<br>

# WHAT DOES IT DO ? 
- Scans for Wifi Access points, lists them on the OLED and reports on their security settings on the LCD
- Reads the daily number of ads blocks and percentage of ads from PiHole and displays it on the LCD
- Checks to see if anyone mentioned Sign-Chan on twitter, and if so then displays the mention on the LCD
- Alerts you with a minions "BEE-DOO" if there is no Wifi available for it to attach to
- Looks around on the X axis
<br>


# BEFORE RUNNING
- Insert your wifi SSID / pw into the code where indicated
- Insert your PiHole IP address into the code where indicated
- I have commented out the twitter code as it relies on a custom server I have locally and not a cloud based one
<br><br>
./img : Image files for indicating services that Sign-chan is communicating with<br>
./aud : Audio files that Sign-chan uses to get your attention<br>
<br>

