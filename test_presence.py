#! /usr/bin/python
import RPi.GPIO as GPIO
import time
import datetime
channel = 18
def presence_detected(channel):
  now = datetime.datetime.now()
  print "Presence detected in channel ",channel,now
def presence_absence_detected(channel):
  now = datetime.datetime.now()
  print "Presence/Absence detected in channel ",channel,now
def absence_detected(channel):
  now = datetime.datetime.now()
  print "Absence detected in channel ",channel,now
def main():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(channel,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#  GPIO.add_event_detect(channel,GPIO.RISING,callback=presence_detected)
  GPIO.add_event_detect(channel,GPIO.FALLING,callback=absence_detected)
#  GPIO.add_event_detect(channel,GPIO.BOTH,callback=presence_absence_detected)
  start=datetime.datetime.now()
  delta=datetime.timedelta(days=1)
  future=start+delta
  now=datetime.datetime.now()
  try:
     while (now < future):
        now=datetime.datetime.now()
        status=GPIO.input(channel)
        print "in the loop ",datetime.datetime.now(), status
#        log_message=now.strftime("%Y-%m-%d %H:%M:%S") + " " + str(status)
        log_message=str(now) + " " + str(status)
        time.sleep(1.)
        now=datetime.datetime.now()
#    GPIO.wait_for_edge(channel,GPIO.BOTH)

  except KeyboardInterrupt:
     print "Program interrupted"
   
  except:
     print "Program aborted"

  finally:
     GPIO.cleanup()
     print "GPIO cleanup"
 
#  print GPIO.VERSION	
  print "Program is ending: GPIO cleanup"
  GPIO.cleanup()
if __name__ == "__main__":
   main()



