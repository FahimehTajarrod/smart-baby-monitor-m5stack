from m5stack import *
from m5ui import *
from uiflow import *
import wifiCfg
from hardware import sdcard
import imu
from flow import ezdata
import json

import os
import time
import unit
remoteInit()

setScreenColor(0x222222)
env3_0 = unit.get(unit.ENV3, unit.PORTA)
pir_0 = unit.get(unit.PIR, unit.PORTC)
rgb_0 = unit.get(unit.RGB, unit.PORTC)
angle_0 = unit.get(unit.ANGLE, unit.PORTB)




slider_value = None
CurrentMode = None
Temperature = None
telemetry = None
LastAngle = None
Motion = None
Humidity = None
IMU = None
ErrorDetails = None
LastSyncTime = None
Volume = None
TelemetryMap = None
MotionFlag = None
ErrorMap = None
hardware_component = None
JsonStr = None
error_code = None
FileName = None

imu0 = imu.IMU()
wifiCfg.autoConnect(lcdShow=False)

lbl_status = M5TextBox(35, 33, "STATUS: SAFE", lcd.FONT_Default, 0x0efa25, rotate=0)
circle_status = M5Circle(18, 38, 7, 0x11ec09, 0x35f510)
lbl_mode = M5TextBox(177, 33, "GOOD MORNING", lcd.FONT_Default, 0x1ded0c, rotate=0)
rectangle0 = M5Rect(8, 58, 146, 15, 0x0f3fa5, 0x0157b1)
rectangle8 = M5Rect(8, 74, 146, 41, 0x222222, 0x0157b1)
label3 = M5TextBox(10, 62, "TEMPERATURE / HUMIDITY", lcd.FONT_DefaultSmall, 0xFFFFFF, rotate=0)
lbl_temp = M5TextBox(15, 81, "22.4 *C", lcd.FONT_DefaultSmall, 0xFFFFFF, rotate=0)
lbl_humidity = M5TextBox(15, 95, "HUMIDITY: --%", lcd.FONT_Default, 0xFFFFFF, rotate=0)
rectangle1 = M5Rect(160, 59, 150, 15, 0xda0101, 0xd60808)
rectangle9 = M5Rect(160, 75, 150, 41, 0x222222, 0xd60808)
label6 = M5TextBox(179, 63, "MOTION DETECTION", lcd.FONT_DefaultSmall, 0xFFFFFF, rotate=0)
lbl_motion = M5TextBox(177, 88, "NONE", lcd.FONT_DejaVu18, 0xFFFFFF, rotate=0)
lbl_sd = M5TextBox(11, 154, "SD:", lcd.FONT_DefaultSmall, 0xFFFFFF, rotate=0)
rectangle2 = M5Rect(8, 120, 304, 22, 0x222222, 0x8bfd00)
lbl_wifi = M5TextBox(11, 172, "WiFi:", lcd.FONT_DefaultSmall, 0xFFFFFF, rotate=0)
lbl_imu_tilt = M5TextBox(16, 126, "TILT ANGLE: 0.0*", lcd.FONT_Default, 0x8bfd00, rotate=0)
lbl_sync = M5TextBox(11, 192, "Last sync: --:--", lcd.FONT_DefaultSmall, 0xFFFFFF, rotate=0)
lbl_imu_status = M5TextBox(164, 126, "DEVICE: STABLE", lcd.FONT_Default, 0x8bfd00, rotate=0)
rectangle5 = M5Rect(5, 218, 95, 20, 0x58b317, 0xFFFFFF)
label15 = M5TextBox(16, 223, "Good Morning", lcd.FONT_DefaultSmall, 0xffffff, rotate=0)
rectangle6 = M5Rect(113, 218, 95, 20, 0x1010bb, 0xFFFFFF)
label16 = M5TextBox(130, 223, "Good Night", lcd.FONT_DefaultSmall, 0xFFFFFF, rotate=0)
rectangle7 = M5Rect(222, 218, 95, 20, 0xc82fc0, 0xFFFFFF)
title0 = M5Title(title="Baby Monitor", x=3, fgcolor=0xFFFFFF, bgcolor=0x0000FF)
label17 = M5TextBox(247, 223, "Standby", lcd.FONT_DefaultSmall, 0xFFFFFF, rotate=0)


# Describe this function...
def EZsync():
  global slider_value, CurrentMode, Temperature, telemetry, LastAngle, Motion, Humidity, IMU, ErrorDetails, LastSyncTime, Volume, TelemetryMap, MotionFlag, ErrorMap, hardware_component, JsonStr, error_code, FileName
  try :
    ezdata.setData('umG2xyGmimghToGaFieFIiWRGGsWiLd8', 'IMU-Status', IMU)
    ezdata.setData('umG2xyGmimghToGaFieFIiWRGGsWiLd8', 'Temperature', (env3_0.temperature))
    ezdata.setData('umG2xyGmimghToGaFieFIiWRGGsWiLd8', 'Humidity', (env3_0.humidity))
    ezdata.setData('umG2xyGmimghToGaFieFIiWRGGsWiLd8', 'Motion', Motion)
    ezdata.setData('umG2xyGmimghToGaFieFIiWRGGsWiLd8', 'Mode', CurrentMode)
    LastSyncTime = time.ticks_ms()
    lbl_sync.setText(str((str('Last sync: ') + str(LastSyncTime))))
    pass
  except:
    lbl_sync.setText('Last sync: ERR')
    hardware_component = 'EzData'
    error_code = 503
    LogError()

# Describe this function...
def Morning():
  global slider_value, CurrentMode, Temperature, telemetry, LastAngle, Motion, Humidity, IMU, ErrorDetails, LastSyncTime, Volume, TelemetryMap, MotionFlag, ErrorMap, hardware_component, JsonStr, error_code, FileName
  lbl_mode.setText('GOOD MORNING')
  lbl_mode.setColor(0xffff33)
  ENV()
  Motion2()
  DiviceStatus()

# Describe this function...
def ENV():
  global slider_value, CurrentMode, Temperature, telemetry, LastAngle, Motion, Humidity, IMU, ErrorDetails, LastSyncTime, Volume, TelemetryMap, MotionFlag, ErrorMap, hardware_component, JsonStr, error_code, FileName
  Temperature = env3_0.temperature
  Humidity = env3_0.humidity
  lbl_temp.setText(str((str((env3_0.temperature)) + str(' *C'))))
  lbl_humidity.setText(str((str('HUMIDITY: ') + str(((str((env3_0.humidity)) + str(' %')))))))
  if Temperature > 36 or Humidity > 50:
    rgb_0.setColorFrom(1, 3, 0xff6600)
    circle_status.setBgColor(0xff6600)
    circle_status.setBorderColor(0xff6600)
    lbl_status.setColor(0xff6600)
    lbl_status.setText('STATUS: WARNING!!')
    IMU = 'Warning'
    EZsync()
  else:
    Safe()

# Describe this function...
def Night():
  global slider_value, CurrentMode, Temperature, telemetry, LastAngle, Motion, Humidity, IMU, ErrorDetails, LastSyncTime, Volume, TelemetryMap, MotionFlag, ErrorMap, hardware_component, JsonStr, error_code, FileName
  lbl_mode.setText('GOOD NIGHT')
  lbl_mode.setColor(0x33ccff)
  lullaby()
  ENV()
  Motion2()
  DiviceStatus()

# Describe this function...
def LogTelemetry():
  global slider_value, CurrentMode, Temperature, telemetry, LastAngle, Motion, Humidity, IMU, ErrorDetails, LastSyncTime, Volume, TelemetryMap, MotionFlag, ErrorMap, hardware_component, JsonStr, error_code, FileName
  telemetry = {'ambient_temperature_c':Temperature,'relative_humidity_pct':Humidity,'motion_detected':MotionFlag,'sound_level_db':0,'crying_detected':'false','imu_tilt_deg':(imu0.acceleration[0])}
  TelemetryMap = {'timestamp':(time.ticks_ms()),'device_id':'M5_BABY_MONITOR_01','current_mode':CurrentMode,'telemetry':telemetry}
  JsonStr = json.dumps(TelemetryMap)
  try :
    FileName = (str('/sd/JSON/telemetry_') + str(((str((time.ticks_ms())) + str('.json')))))
    with open('/sd/' + str(FileName), 'w+') as fs:
      fs.write(str(JsonStr))
    pass
  except:
    lbl_sd.setText('SD: ERR')
    hardware_component = 'SD Card'
    error_code = 502
    LogError()

# Describe this function...
def WiFiInit():
  global slider_value, CurrentMode, Temperature, telemetry, LastAngle, Motion, Humidity, IMU, ErrorDetails, LastSyncTime, Volume, TelemetryMap, MotionFlag, ErrorMap, hardware_component, JsonStr, error_code, FileName
  wifiCfg.doConnect('prhtac', 'v2kCW4j5SrNRzf6B')
  if wifiCfg.wlan_sta.isconnected():
    lbl_wifi.setText('WiFi :OK')
  else:
    lbl_wifi.setText('WiFi: ERR')
    hardware_component = 'WiFi'
    error_code = 501
    LogError()

# Describe this function...
def lullaby():
  global slider_value, CurrentMode, Temperature, telemetry, LastAngle, Motion, Humidity, IMU, ErrorDetails, LastSyncTime, Volume, TelemetryMap, MotionFlag, ErrorMap, hardware_component, JsonStr, error_code, FileName
  speaker.setVolume(Volume)
  rgb.setColorAll(0x0000ff)
  speaker.sing(196, 1)
  rgb.setColorAll(0x0032ff)
  speaker.sing(196, 1)
  rgb.setColorAll(0x0064ff)
  speaker.sing(247, 2)
  rgb.setColorAll(0x3200ff)
  speaker.sing(196, 2)
  rgb.setColorAll(0x6400ff)
  speaker.sing(523, 2)
  rgb.setColorAll(0x9600c8)
  speaker.sing(247, 4)
  rgb.setColorAll(0x0000ff)
  speaker.sing(196, 1)
  rgb.setColorAll(0x0032ff)
  speaker.sing(196, 1)
  rgb.setColorAll(0x0064ff)
  speaker.sing(247, 2)
  rgb.setColorAll(0x3200ff)
  speaker.sing(196, 2)
  rgb.setColorAll(0x6400ff)
  speaker.sing(587, 2)
  rgb.setColorAll(0x9600c8)
  speaker.sing(523, 4)
  rgb.setColorAll(0x000000)

# Describe this function...
def Motion2():
  global slider_value, CurrentMode, Temperature, telemetry, LastAngle, Motion, Humidity, IMU, ErrorDetails, LastSyncTime, Volume, TelemetryMap, MotionFlag, ErrorMap, hardware_component, JsonStr, error_code, FileName
  if (pir_0.state) == 1:
    MotionFlag = True
  else:
    MotionFlag = False
  if MotionFlag == True:
    lbl_motion.setText('MOTION!')
    rgb_0.setColorFrom(1, 3, 0xff0000)
    circle_status.setBorderColor(0xff0000)
    circle_status.setBgColor(0xff0000)
    lbl_status.setColor(0xff0000)
    lbl_status.setText('STATUS: ALERT!')
    speaker.tone(1800, 500)
    Motion = 'Motion'
    IMU = 'Alert'
    EZsync()
  else:
    Safe()

# Describe this function...
def Initialization():
  global slider_value, CurrentMode, Temperature, telemetry, LastAngle, Motion, Humidity, IMU, ErrorDetails, LastSyncTime, Volume, TelemetryMap, MotionFlag, ErrorMap, hardware_component, JsonStr, error_code, FileName
  LastAngle = angle_0.read()
  LastSyncTime = 0
  CurrentMode = 'Morning'
  Motion = 'None'
  IMU = 'Safe'
  Humidity = '%'
  Temperature = '*C'
  MotionFlag = False
  Volume = 5

# Describe this function...
def SDInit():
  global slider_value, CurrentMode, Temperature, telemetry, LastAngle, Motion, Humidity, IMU, ErrorDetails, LastSyncTime, Volume, TelemetryMap, MotionFlag, ErrorMap, hardware_component, JsonStr, error_code, FileName
  sdcard.SDCard(20000000)
  try :
    if os.stat('/sd//sd')[0] == 0x4000:
      if os.stat('/sd//sd/LOGS')[0] == 0x4000:
        lbl_sd.setText('SD: OK')
      else:
        os.mkdir('/sd//sd/LOGS')
        os.mkdir('/sd//sd/JSON')
    else:
      os.mkdir('/sd//sd')
      os.mkdir('/sd//sd/LOGS')
      os.mkdir('/sd//sd/JSON')
    pass
  except:
    hardware_component = 'SD Card'
    error_code = 502
    LogError()

# Describe this function...
def DiviceStatus():
  global slider_value, CurrentMode, Temperature, telemetry, LastAngle, Motion, Humidity, IMU, ErrorDetails, LastSyncTime, Volume, TelemetryMap, MotionFlag, ErrorMap, hardware_component, JsonStr, error_code, FileName
  if (imu0.acceleration[2]) < 0.5:
    lbl_imu_status.setText('DEVICE: !! FALLEN !!')
    rgb_0.setColorFrom(1, 3, 0xff0000)
    circle_status.setBorderColor(0xff0000)
    circle_status.setBgColor(0xff0000)
    lbl_status.setColor(0xff0000)
    lbl_status.setText('STATUS: ALERT!')
    speaker.tone(1800, 500)
    IMU = 'Alert'
    EZsync()
  else:
    Safe()
  lbl_imu_tilt.setText(str((str('TILT ANGLE: ') + str((imu0.acceleration[0])))))

# Describe this function...
def LogError():
  global slider_value, CurrentMode, Temperature, telemetry, LastAngle, Motion, Humidity, IMU, ErrorDetails, LastSyncTime, Volume, TelemetryMap, MotionFlag, ErrorMap, hardware_component, JsonStr, error_code, FileName
  ErrorDetails = {'error_code':error_code,'message':((str(hardware_component) + str(' failed.'))),'retry_attempt':1}
  ErrorMap = {'timestamp':(time.ticks_ms()),'error_id':'M5_BABY_MONITOR_01_ERROR','severity':'Warning','hardware_component':hardware_component,'error_details':ErrorDetails}
  JsonStr = json.dumps(ErrorMap)
  try :
    FileName = (str('/sd/LOGS/error_') + str(((str((time.ticks_ms())) + str('.json')))))
    with open('/sd/' + str(FileName), 'w+') as fs:
      fs.write(str(JsonStr))
    pass
  except:
    lbl_sd.setText('SD: ERR')
    hardware_component = 'SD Card'
    error_code = 502

# Describe this function...
def Safe():
  global slider_value, CurrentMode, Temperature, telemetry, LastAngle, Motion, Humidity, IMU, ErrorDetails, LastSyncTime, Volume, TelemetryMap, MotionFlag, ErrorMap, hardware_component, JsonStr, error_code, FileName
  rgb_0.setColorFrom(1, 3, 0x33cc00)
  circle_status.setBgColor(0x33cc00)
  circle_status.setBorderColor(0x33cc00)
  lbl_status.setColor(0x33cc00)
  lbl_status.setText('STATUS: SAFE')
  lbl_motion.setText('NONE')
  lbl_imu_status.setText('DEVICE: STABLE')
  Motion = 'None'
  IMU = 'Safe'

# Describe this function...
def Standby():
  global slider_value, CurrentMode, Temperature, telemetry, LastAngle, Motion, Humidity, IMU, ErrorDetails, LastSyncTime, Volume, TelemetryMap, MotionFlag, ErrorMap, hardware_component, JsonStr, error_code, FileName
  lbl_mode.setText('STANDBY')
  rgb_0.setColorFrom(1, 3, 0x000000)
  lbl_mode.setColor(0x666666)
  circle_status.hide()
  lbl_temp.hide()
  lbl_humidity.hide()
  lbl_status.hide()
  lbl_imu_tilt.hide()
  lbl_imu_status.hide()
  lbl_sync.hide()
  lbl_wifi.hide()
  lbl_sd.hide()
  lbl_motion.hide()


def buttonA_wasPressed():
  global CurrentMode, Temperature, telemetry, LastAngle, Motion, Humidity, IMU, ErrorDetails, LastSyncTime, Volume, TelemetryMap, MotionFlag, ErrorMap, slider_value, hardware_component, JsonStr, error_code, FileName
  CurrentMode = 'Morning'
  lbl_mode.setText('GOOD  MORNING')
  lbl_mode.setColor(0x009900)
  circle_status.show()
  lbl_status.show()
  pass
btnA.wasPressed(buttonA_wasPressed)

def buttonB_wasPressed():
  global CurrentMode, Temperature, telemetry, LastAngle, Motion, Humidity, IMU, ErrorDetails, LastSyncTime, Volume, TelemetryMap, MotionFlag, ErrorMap, slider_value, hardware_component, JsonStr, error_code, FileName
  CurrentMode = 'Night'
  lbl_mode.setText('GOOD NIGHT')
  lbl_mode.setColor(0x3333ff)
  circle_status.show()
  lbl_status.show()
  pass
btnB.wasPressed(buttonB_wasPressed)

def buttonC_wasPressed():
  global CurrentMode, Temperature, telemetry, LastAngle, Motion, Humidity, IMU, ErrorDetails, LastSyncTime, Volume, TelemetryMap, MotionFlag, ErrorMap, slider_value, hardware_component, JsonStr, error_code, FileName
  CurrentMode = 'Standby'
  Standby()
  pass
btnC.wasPressed(buttonC_wasPressed)









def label_r_motion_callback():
  global CurrentMode, Temperature, telemetry, LastAngle, Motion, Humidity, IMU, ErrorDetails, LastSyncTime, Volume, TelemetryMap, MotionFlag, ErrorMap, slider_value, hardware_component, JsonStr, error_code, FileName, env3_0, pir_0, rgb_0, angle_0, DiviceStatus, ENV, EZsync, Initialization, LogError, LogTelemetry, lullaby, Morning, Motion, Night, Safe, SDInit, Standby, WiFiInit 
  return Motion
def label_r_temp_callback():
  global CurrentMode, Temperature, telemetry, LastAngle, Motion, Humidity, IMU, ErrorDetails, LastSyncTime, Volume, TelemetryMap, MotionFlag, ErrorMap, slider_value, hardware_component, JsonStr, error_code, FileName, env3_0, pir_0, rgb_0, angle_0, DiviceStatus, ENV, EZsync, Initialization, LogError, LogTelemetry, lullaby, Morning, Motion, Night, Safe, SDInit, Standby, WiFiInit 
  return Temperature
def label_r_hummidity_callback():
  global CurrentMode, Temperature, telemetry, LastAngle, Motion, Humidity, IMU, ErrorDetails, LastSyncTime, Volume, TelemetryMap, MotionFlag, ErrorMap, slider_value, hardware_component, JsonStr, error_code, FileName, env3_0, pir_0, rgb_0, angle_0, DiviceStatus, ENV, EZsync, Initialization, LogError, LogTelemetry, lullaby, Morning, Motion, Night, Safe, SDInit, Standby, WiFiInit 
  return Humidity
def label_r_status_callback():
  global CurrentMode, Temperature, telemetry, LastAngle, Motion, Humidity, IMU, ErrorDetails, LastSyncTime, Volume, TelemetryMap, MotionFlag, ErrorMap, slider_value, hardware_component, JsonStr, error_code, FileName, env3_0, pir_0, rgb_0, angle_0, DiviceStatus, ENV, EZsync, Initialization, LogError, LogTelemetry, lullaby, Morning, Motion, Night, Safe, SDInit, Standby, WiFiInit 
  return IMU
def label_r_mode_callback():
  global CurrentMode, Temperature, telemetry, LastAngle, Motion, Humidity, IMU, ErrorDetails, LastSyncTime, Volume, TelemetryMap, MotionFlag, ErrorMap, slider_value, hardware_component, JsonStr, error_code, FileName, env3_0, pir_0, rgb_0, angle_0, DiviceStatus, ENV, EZsync, Initialization, LogError, LogTelemetry, lullaby, Morning, Motion, Night, Safe, SDInit, Standby, WiFiInit 
  return CurrentMode
def label_r_imu_callback():
  global CurrentMode, Temperature, telemetry, LastAngle, Motion, Humidity, IMU, ErrorDetails, LastSyncTime, Volume, TelemetryMap, MotionFlag, ErrorMap, slider_value, hardware_component, JsonStr, error_code, FileName, env3_0, pir_0, rgb_0, angle_0, DiviceStatus, ENV, EZsync, Initialization, LogError, LogTelemetry, lullaby, Morning, Motion, Night, Safe, SDInit, Standby, WiFiInit 
  return imu0.acceleration[0]
def label_r_sync_callback():
  global CurrentMode, Temperature, telemetry, LastAngle, Motion, Humidity, IMU, ErrorDetails, LastSyncTime, Volume, TelemetryMap, MotionFlag, ErrorMap, slider_value, hardware_component, JsonStr, error_code, FileName, env3_0, pir_0, rgb_0, angle_0, DiviceStatus, ENV, EZsync, Initialization, LogError, LogTelemetry, lullaby, Morning, Motion, Night, Safe, SDInit, Standby, WiFiInit 
  return LastSyncTime
def button_r_btn_morning_callback():
  global CurrentMode, Temperature, telemetry, LastAngle, Motion, Humidity, IMU, ErrorDetails, LastSyncTime, Volume, TelemetryMap, MotionFlag, ErrorMap, slider_value, hardware_component, JsonStr, error_code, FileName, env3_0, pir_0, rgb_0, angle_0, DiviceStatus, ENV, EZsync, Initialization, LogError, LogTelemetry, lullaby, Morning, Motion, Night, Safe, SDInit, Standby, WiFiInit 
  CurrentMode = 'Morning'
  lbl_mode.setText('GOOD  MORNING')
  lbl_mode.setColor(0x009900)
  circle_status.show()
  lbl_status.show()

def button_r_btn_night_callback():
  global CurrentMode, Temperature, telemetry, LastAngle, Motion, Humidity, IMU, ErrorDetails, LastSyncTime, Volume, TelemetryMap, MotionFlag, ErrorMap, slider_value, hardware_component, JsonStr, error_code, FileName, env3_0, pir_0, rgb_0, angle_0, DiviceStatus, ENV, EZsync, Initialization, LogError, LogTelemetry, lullaby, Morning, Motion, Night, Safe, SDInit, Standby, WiFiInit 
  CurrentMode = 'Night'
  lbl_mode.setText('GOOD NIGHT')
  lbl_mode.setColor(0x3333ff)
  circle_status.show()
  lbl_status.show()

def button_r_btn_standby_callback():
  global CurrentMode, Temperature, telemetry, LastAngle, Motion, Humidity, IMU, ErrorDetails, LastSyncTime, Volume, TelemetryMap, MotionFlag, ErrorMap, slider_value, hardware_component, JsonStr, error_code, FileName, env3_0, pir_0, rgb_0, angle_0, DiviceStatus, ENV, EZsync, Initialization, LogError, LogTelemetry, lullaby, Morning, Motion, Night, Safe, SDInit, Standby, WiFiInit 
  CurrentMode = 'Standby'
  Standby()

def slider_r_volume_callback(slider_value):
  global CurrentMode, Temperature, telemetry, LastAngle, Motion, Humidity, IMU, ErrorDetails, LastSyncTime, Volume, TelemetryMap, MotionFlag, ErrorMap, hardware_component, JsonStr, error_code, FileName, env3_0, pir_0, rgb_0, angle_0, DiviceStatus, ENV, EZsync, Initialization, LogError, LogTelemetry, lullaby, Morning, Motion, Night, Safe, SDInit, Standby, WiFiInit 
  Volume = slider_value

WiFiInit()
SDInit()
Initialization()
Safe()
EZsync()
while True:
  if (angle_0.read()) != LastAngle:
    Volume = ((angle_0.read()) / 1024) * 20
    LastAngle = angle_0.read()
  speaker.setVolume(Volume)
  if (time.ticks_ms()) - LastSyncTime > 30000:
    EZsync()
    LogTelemetry()
    LastSyncTime = time.ticks_ms()
  if CurrentMode == 'Standby':
    Standby()
  else:
    if CurrentMode == 'Night':
      Night()
    else:
      if CurrentMode == 'Morning':
        Morning()
  wait_ms(500)
  wait_ms(2)
