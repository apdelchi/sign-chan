from m5stack import *
from m5stack_ui import *
from uiflow import *
import time
import network
import urequests as requests
import module
from servo import Servo
import random
from easyIO import * 
import _thread
import unit
import re


####
# M5StackAvatar BLOCK
# Based on M5StackAvatarPython : https://github.com/h-akanuma/M5StackAvatarPython
# v1.0 (220801)
# Copyright (c) 2022 @akita11, Released under the MIT license
####

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0)

lcd.font(lcd.FONT_DejaVu24)
M5Avatar_fw, M5Avatar_fh = lcd.fontSize()
M5Avatar_ww, M5Avatar_wh = lcd.screensize()
M5Avatar_eye_x = 90
M5Avatar_eye_y = 80
M5Avatar_eye_r = 10
M5Avatar_eye_close_x= 70
M5Avatar_eye_close_width  = 40
M5Avatar_eye_close_height = 5
M5Avatar_blink_term_ms    = 500
M5Avatar_mouth_x = 135
M5Avatar_mouth_y = 150
M5Avatar_mouth_width = 50
M5Avatar_mouth_height = 5
M5Avatar_mouth_close = True
M5Avatar_mouth_close_height = 20
M5Avatar_exclamation_x = 280
M5Avatar_exclamation_y = 20
M5Avatar_exclamation_width  = 10
M5Avatar_exclamation_height = 30
M5Avatar_exclamation_space  = 8
tm_blink = 0
st_blink = 0
tm_mouth = 0
st_mouth = 0
tm_speak = 300 # was 0 , additive ticks  
timerAvatar_period = 100
tm_blink_open = random.randint(2, 6) * 1000
tm_mouth_period = 500
M5Avatar_spaces = ' '
while lcd.textWidth(M5Avatar_spaces) < M5Avatar_ww:
  M5Avatar_spaces += ' '
htw = ""
### END AVATAR 

#_wifi_active = False
#_wifi_report = ""
###
# Create variable to hold servo_current - make sure to init. it using init_servo()
###
#servo_current = 90   # Don't forget to init_servo first or this will make for issues.
###

@timerSch.event('timerAvatar')
def ttimerAvatar():
  global tm_speak
  _blink()
  _mouth()
  tm_speak = tm_speak + timerAvatar_period
  pass


def _blink():
    global tm_blink, st_blink, tm_blink_open
    tm_blink = tm_blink + timerAvatar_period
    if st_blink == 0:
      _eye_close()
      if tm_blink >= M5Avatar_blink_term_ms:
        st_blink = 1
        tm_blink = 0
    else:
      _eye_open()
      if tm_blink >= tm_blink_open:
        tm_blink_open = random.randint(2, 6) * 1000
        st_blink = 0
        tm_blink = 0

def _eye_close():
    lcd.circle(M5Avatar_eye_x, M5Avatar_eye_y, M5Avatar_eye_r, lcd.BLACK, lcd.BLACK)
    lcd.circle(M5Avatar_ww - M5Avatar_eye_x, M5Avatar_eye_y, M5Avatar_eye_r, lcd.BLACK, lcd.BLACK)
    lcd.rect(M5Avatar_eye_close_x, M5Avatar_eye_y, M5Avatar_eye_close_width, M5Avatar_eye_close_height, lcd.WHITE, lcd.WHITE)
    lcd.rect(
        M5Avatar_ww - M5Avatar_eye_close_x - M5Avatar_eye_close_width,
        M5Avatar_eye_y, M5Avatar_eye_close_width,
        M5Avatar_eye_close_height,
        lcd.WHITE,
        lcd.WHITE
    )

def _eye_open():
    lcd.rect(M5Avatar_eye_close_x, M5Avatar_eye_y, M5Avatar_eye_close_width, M5Avatar_eye_close_height, lcd.BLACK, lcd.BLACK)
    lcd.rect(
        M5Avatar_ww - M5Avatar_eye_close_x - M5Avatar_eye_close_width,
        M5Avatar_eye_y,
        M5Avatar_eye_close_width,
        M5Avatar_eye_close_height,
        lcd.BLACK,
        lcd.BLACK
    )
    lcd.circle(M5Avatar_eye_x, M5Avatar_eye_y, M5Avatar_eye_r, lcd.WHITE, lcd.WHITE)
    lcd.circle(M5Avatar_ww - M5Avatar_eye_x, M5Avatar_eye_y, M5Avatar_eye_r, lcd.WHITE, lcd.WHITE)

def _mouth():
  global tm_mouth
  tm_mouth = tm_mouth + timerAvatar_period
  if tm_mouth >= tm_mouth_period:
    tm_mouth = 0
    lcd.rect(M5Avatar_mouth_x, M5Avatar_mouth_y, M5Avatar_mouth_width, M5Avatar_mouth_height, lcd.WHITE, lcd.WHITE)

def _lipsync():
  if M5Avatar_mouth_close:
    _lip_open()
  else:
    _lip_close()

def _lip_close():
  global M5Avatar_mouth_close
  lcd.rect(
    M5Avatar_mouth_x,
    M5Avatar_mouth_y - (M5Avatar_mouth_close_height // 2),
    M5Avatar_mouth_width,
    M5Avatar_mouth_height + M5Avatar_mouth_close_height,
    lcd.BLACK,
    lcd.BLACK
  )
  lcd.rect(M5Avatar_mouth_x, M5Avatar_mouth_y, M5Avatar_mouth_width, M5Avatar_mouth_height, lcd.WHITE, lcd.WHITE)
  M5Avatar_mouth_close = True

def _lip_open():
  global M5Avatar_mouth_close
  lcd.rect(M5Avatar_mouth_x, M5Avatar_mouth_y, M5Avatar_mouth_width, M5Avatar_mouth_height, lcd.BLACK, lcd.BLACK)
  lcd.rect(
    M5Avatar_mouth_x,
    M5Avatar_mouth_y - (M5Avatar_mouth_close_height // 2),
    M5Avatar_mouth_width,
    M5Avatar_mouth_height + M5Avatar_mouth_close_height,
    lcd.WHITE,
    lcd.WHITE
  )
  M5Avatar_mouth_close = False

def _exclamation_color(color):
  lcd.rect(M5Avatar_exclamation_x, M5Avatar_exclamation_y, M5Avatar_exclamation_width, M5Avatar_exclamation_height, color, color)
  lcd.rect(
    M5Avatar_exclamation_x,
    M5Avatar_exclamation_y + M5Avatar_exclamation_height + M5Avatar_exclamation_space,
    M5Avatar_exclamation_width,
    M5Avatar_exclamation_width,
    color,
    color
  )

def _pale_color(color):
  lcd.rect(200, 0, 5, 40, color, color)
  lcd.rect(220, 0, 5, 45, color, color)
  lcd.rect(240, 0, 5, 50, color, color)
  lcd.rect(260, 0, 5, 55, color, color)
  lcd.rect(40, 100, 5, 40, color, color)
  lcd.rect(60, 103, 5, 35, color, color)
  lcd.rect(80, 106, 5, 30, color, color)
  lcd.rect(100, 109, 5, 25, color, color)

def _wifi_signal(color):
    lcd.rect(200, 0, 5, 20, color, color)
    lcd.rect(220, 0, 5, 25, color, color)
    lcd.rect(240, 0, 5, 30, color, color)
    lcd.rect(260, 0, 5, 35, color, color)

def _wifi_signal_red(switch):
    if switch == "on":
        lcd.image(250,20,"/flash/img/wifi_red.png")
    if switch == "off":
        lcd.setwin(250,20,276,42)
        lcd.clearwin(0x000000)
    lcd.resetwin()


def _wifi_signal_green(switch):
    if switch == "on":
       lcd.image(250,20,"/flash/img/wifi_green.png")
    if switch == "off":
        lcd.setwin(250,20,276,42)
        lcd.clearwin(0x000000)
    lcd.resetwin()

def _pihole_logo(switch):
  if switch == "on":
    lcd.image(250,20,"/flash/img/logopi-3030.png")
  if switch == "off":
    lcd.setwin(250,20,280,50)
    lcd.clearwin(0x000000)
    lcd.resetwin()

def twitter_logo(switch):
  if switch == "on":
    lcd.image(250,20,"/flash/img/twitter-3030.png")
  if switch == "off":
    lcd.setwin(250,20,280,50)
    lcd.clearwin(0x000000)
    lcd.resetwin()


####
# _speak2 -- Fixes bugs in _speak
####
def _speak2(text):
  #global tm_speak
  lcd.setColor(lcd.BLACK, lcd.WHITE)
  lcd.arc((M5Avatar_eye_x + M5Avatar_mouth_x) // 2, (M5Avatar_wh - M5Avatar_fh) - 5, 25, 25, 270, 360, lcd.WHITE, lcd.WHITE)
  lcd.rect(0, (M5Avatar_wh - M5Avatar_fh) - 5, M5Avatar_ww + 5, M5Avatar_fh + 5, lcd.WHITE, lcd.WHITE)
  lcd.textClear(0, (M5Avatar_wh - M5Avatar_fh) - 1, M5Avatar_spaces, lcd.WHITE)
  lcd.print(text, 0, lcd.BOTTOM, lcd.BLACK)
  _lipsync()
  fSpeakRun = True
  wait(.2)
  # REMOVED AND REPLACED WITH WAIT() AS PART OF REMOVING TIMER/THREAD ISSUE
  #while tm_speak < 200:
  #  pass
  tm_speak = 0   
  while lcd.textWidth(text) > 0:
    text = text[1:]
    lcd.textClear(0, (M5Avatar_wh - M5Avatar_fh) - 1, M5Avatar_spaces, lcd.WHITE)
    lcd.print(text, 0, lcd.BOTTOM, lcd.BLACK)
    _lipsync()
    wait(.2)
    # REMOVED AND REPLACED WITH WAIT() AS PART OF REMOVING TIMER/THREAD ISSUE
    #while tm_speak < 200:
    #  pass
    # tm_speak = 0  
  lcd.rect(0, (M5Avatar_wh - M5Avatar_fh) - 5, M5Avatar_ww, M5Avatar_fh + 5, lcd.BLACK, lcd.BLACK)
  lcd.arc((M5Avatar_eye_x + M5Avatar_mouth_x) // 2, (M5Avatar_wh - M5Avatar_fh) - 5, 25, 25, 270, 360, lcd.BLACK, lcd.BLACK)
  _lip_close()

####   

def _init_servo():
  global servo0
  global servo1
  global servo_current
  label0 = M5Label('label0', x=0, y=0, color=0xff0000, font=FONT_MONT_14, parent=None)
  label0.set_text("INITIALIZING SERVOS - STAND BACK!")
  for x in range (1,5):
    rgb.setColorFrom(1 , 5  ,0xffff00)
    rgb.setColorFrom(6 , 10 ,0xffff00)
    wait(.5)
    rgb.setColorFrom(1 , 5  ,0x000000)
    rgb.setColorFrom(6 , 10 ,0x000000)
    wait(.5)
  ### THESE PINS ARE FOR THE CORE2-AWS PORT A (33,32), NO PORT B , PORT C = 14,13 , CORE-2 ARE DIFFERENT
  # servo1 = Servo(33,50,500,2500,180) - Pin #, Duty Cycle , ? , ? , ? ( Servo type?)
  # Also : Sign-chan only uses servo.
  #
  servo1 = Servo(33,50,500,2500,180)
  servo0 = Servo(32,50,500,2500,180)
  ###
  servo0.write_angle(90)
  label0.set_text("")
  servo_current = 90
  return servo0,servo1,servo_current


####
# _look_around : simulate looking around left to right .. looking for something 
####
def _look_around():
  global servo0
  global servo1
  global servo_current

  if servo_current >= 70:
    for x in range (servo_current,70,-1):
      servo0.write_angle(x)
      wait(0.045)
    servo_current = 70
  elif servo_current <= 70:
    for x in range (servo_current,70,+1):
      servo0.write.angle(x)
      wait(0.045)
    servo_current = 70
  wait(2)
  for x in range (servo_current,110,+1):
    servo0.write_angle(x)
    wait(0.045)
  servo_current = 110
  wait(2)
  for x in range (servo_current,90,-1):
    servo0.write_angle(x)
    wait(0.045)
  servo_current = 90
  return servo_current
####

####
# _init_wifi : Check for wifi connection to AP , connect using hard coded U/P & display settings
####
def _init_wifi():
  global _wifi_active
  global wlan
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  if not wlan.isconnected():
      _wifi_signal_red("on")
      _look_around()
      rgb.setColorFrom(1 , 5  ,0xff0000)
      rgb.setColorFrom(6 , 10 ,0xff0000)
      speaker.playWAV('res/fire2.wav')
      _speak2("               No Wifi Connected")
      _speak2("Connecting to known WiFi")
####
# NOTE
# INSERT YOUR WIFI SSID / PW HERE BEFORE RUNNING
####
      wlan.connect('my-ssid-goes-here', 'my-password-goes-here') 
      wait(8)
  if not wlan.isconnected():
        _speak2("Unable to connect to wifi")
        _wifi_signal_red("on")
        rgb.setColorFrom(1 , 5  ,0x000000)
        rgb.setColorFrom(6 , 10 ,0x000000)
        speaker.playWAV('res/fire2.wav')
        _wifi_active = False
        return
  elif wlan.isconnected():
    _wifi_signal_red("off")
    _wifi_signal_green("on")
    rgb.setColorFrom(1 , 5  ,0x00ff00)
    rgb.setColorFrom(6 , 10 ,0x00ff00)
    _speak2("            Connected to wifi")
    _wifi_signal_green("off")
    rgb.setColorFrom(1 , 5  ,0x000000)
    rgb.setColorFrom(6 , 10 ,0x000000)
    _wifi_active = True
  
def wifi_config_report():  
    rgb.setColorFrom(1 , 5 ,0x00ff00)
    rgb.setColorFrom(6 , 10 ,0x00ff00)
    wifi_text = "          IP Address :" + wlan.ifconfig()[0] + " Subnet Mask : " + wlan.ifconfig()[1] + "  Gateway : " + wlan.ifconfig()[2] + "  DNS : " + wlan.ifconfig()[3]
    _speak2(wifi_text)
    _wifi_signal(lcd.BLACK)
    rgb.setColorFrom(1 , 5 ,0x000000)
    rgb.setColorFrom(6 , 10 ,0x000000)
    _wifi_signal_green("off")


####
# _check_pihole: Pull report from PiHole using PiHole API
# NOTE : Replace 192.168.0.200 with the IP address of YOUR local Pihole!!
#
####
def _check_pihole():
  if _wifi_active:
    wait(3)
    _pihole_logo("on")
    r = requests.get('http://192.168.0.200/admin/api.php').json()
    pihole_text = "          Ads blocked today by PiHole : %s" % r['ads_blocked_today'] + "    Ad Percentage Today : %s" % r['ads_percentage_today']
    _speak2(pihole_text)
    _pihole_logo("off")
  else:
    _speak2("          ... unable to connect to PiHole")
####

def get_wifi():
  #
  # see https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/network/esp_wifi.html#_CPPv416wifi_auth_mode_t
  # for list of numbers --> security 
  #
  # Run this first , then run the functions to display the report. The call to the wifi radio makes issues with 
  # threading, which is used to display the report on the OLED and LCD at the same time. 
  # Init variables / globals
  #
    global wlan
    global message
    global wifi_report
    message =[""]
    ap_count =0
    no_sec = 0 
    wep = 0
    wpa_psk = 0
    wpa2_psk = 0
    wpa_wpa2_psk =0
    wpa_enterprise = 0 
    wpa3_psk = 0
    wpa2_wpa3_psk =0
    wapi_psk =0
    owe =0
    auth_max =0
    weird = 0 
    ####
    wifilist = wlan.scan()
    for i in wifilist:
        # get list of access points
        message.append(i[0].decode())
        #
        # For each access point determine their security 
        #
        ap_count +=1
        if i[4] == 0:
            no_sec +=1
        elif i[4] == 1:
            wep +=1
        elif i[4] ==2:
            wpa_psk += 1
        elif i[4] == 3:
            wpa2_psk += 1
        elif i[4] == 4:
            wpa_wpa2_psk +=1
        elif i[4] == 5:
            wpa_enterprise+=1
        elif i[4] == 6:
            wpa3_psk +=1
        elif i[4] == 7:
            wpa2_wpa3_psk +=1
        elif i[4] == 8:
            wapi_psk +=1
        elif i[4] == 9:
            owe +=1
        elif i[4] ==10:
            auth_max +=1
        else:
            weird +=1
        #
        # Generate strings for display
        #
        wifi_report = "               Found " + str(ap_count) + " access points, " + str(no_sec) + " with no security, "\
                                         + str(wep) + " with WEP, " + str(wpa_psk) + " with WPA-PSK, " + str(wpa2_psk) \
                                         + " with WPA2-PSK, " + str(wpa_wpa2_psk) + " with WPA/WPA2-PSK and "\
                                         +str(wpa_enterprise)+" with WPA Enterprise, " + str(wpa3_psk) + " WPA3-PSK, "\
                                         +str(wpa2_wpa3_psk) + " with WPA2-WPA3-PS1, " + str(wapi_psk) + " WAPI-PSK, "\
                                         +str(owe) + " OWE " + str(auth_max) + " Auth Max, "\
                                         + str(weird) + " weird one(s) you should look at"

def wifi_oled():
    global message
    oled_1.fill(0x000000)
    oled_1.show()
    y=0
    for x in range (0,len(message)):
        oled_1.text(message[x],0,y,0xffffff)
        oled_1.show()
        y += 11
        if y==66 : 
            for a in range (0,11):
                oled_1.scroll(0,-1)
                oled_1.show()
            y=55
    for w in range (0,51):
        oled_1.scroll(0,-1)
        oled_1.show()

    init_oled()


def scroll_up(oled_text):
    y=0
    oled_1.fill(0x000000)
    oled_1.show()
    for x in range (0,len(oled_text)):
        oled_1.text(oled_text[x],0,y,0xffffff)
        oled_1.show()
        wait(1)
        y += 11
        if y==66 : 
            for a in range (0,11):
                oled_1.scroll(0,-1)
                oled_1.show()
            y=55
    for w in range (0,51):
        oled_1.scroll(0,-1)
        oled_1.show()  

def wifi_lcd():
    global wifi_report
    _wifi_signal_green("on")
    _speak2(wifi_report)
    _wifi_signal_green("off")

def init_oled():
  oled_1 = unit.get(unit.OLED, unit.PORTC)
  oled_1.poweron()
  oled_1.fill(0x000000)
  oled_1.text('Sign-Chan v5!',5,25)
  oled_1.show()
  
def doit():
    b = _thread.start_new_thread(wifi_oled,())
    c = _thread.start_new_thread(wifi_lcd,())
    wait(120)

####
# NOTE 
# THIS IS BASED ON CUSTOM CODE RUNNING ON MY LOCAL WEB SERVER. 
# IT DOES NOT USE CLOUD SERVICES
# YOU MAY WANT TO COMMENT/REMOVE THIS CODE
####
#def gettwit():
#  global htw
#  twitter_logo("on")
#  t = requests.get('http://192.168.0.200/signchan.html')
#  tw = re.search('^(.+?):',t.text).group(1)
#  fm = re.search(':(.+?):',t.text).group(1)
#  me = re.search('.+:.+:(.+)',t.text).group(1)
#  if tw == htw :
#    _speak2("                 No new mentions")
#    twitter_logo("off")
#    # _speak2("                 No new mentions"+tw+"::"+htw)
#    return
#  _speak2("        Twitter Mention from " + fm )
#  y=0
#  oled_1.fill(0x000000)
#  for q in range (0,len(me),16):
#    line = me[q:q+16]
#    oled_1.text(line,0,y,0xffffff)
#    oled_1.show()
#    y+=11
#    if y==66 : 
#            for a in range (0,11):
#                oled_1.scroll(0,-1)
#                oled_1.show()
#            y=55
#  wait (5)
#  init_oled()
#  htw = tw
#  twitter_logo("off")

    
#
# Start timer to make avatar face active while idle 
#

timerSch.setTimer('timerAvatar', timerAvatar_period, 0x00)
timerSch.run('timerAvatar', timerAvatar_period, 0x00)
tm_blink_open = random.randint(2, 6) * 1000

####

init_oled()
_init_servo()
wait(3)
_look_around()
wait(3)
_init_wifi()
wait(3)

while True:
# gettwit()
#  wait(3)
  get_wifi()
  doit()
  wait(3)
  _check_pihole()
  wait(3)
  _look_around()
  _speak2("             I'm the only me as far as I can see .....")



