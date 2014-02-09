#! /usr/bin/python
import sys
import os
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
#  GPIO.add_event_detect(channel,GPIO.FALLING,callback=absence_detected)
#  GPIO.add_event_detect(channel,GPIO.BOTH,callback=presence_absence_detected)
  start=datetime.datetime.now()
  timelastmail=datetime.datetime.now()
  delta=datetime.timedelta(days=1000)
  future=start+delta
  now=datetime.datetime.now()
  try:
     while (now < future):
       now=datetime.datetime.now()
       status=GPIO.input(channel)
#       print datetime.datetime.now(), status
       out_file=open("/home/pi/presence_status","w")
#       log_message=now.strftime("%Y-%m-%d %H:%M:%S") + " " + str(status)
       log_message=str(now) + " " + str(status)
       out_file.write(log_message)
       out_file.close()	
       if (status == 1 and os.path.exists("/var/apache/enabled_alarm")):
          alarm_file=open("/var/www/presenze/alarm.list","a")
          alarm_log=str(now) + " allarme"
          alarm_file.write(alarm_log)
          if(now > timelastmail + datetime.timedelta(seconds=60)):
#            mail_message="/usr/sbin/sendmail -t < /home/pi/RaspberryPiPresence/presenze_message.txt"
#            mail_message=os.path.dirname(sys.path[0])+"/message_with_snapshot.sh"
            mailok=999
            if(len(sys.argv) > 1):
              mail_message="/home/pi/RaspberryPiPresence/scripts/message_with_snapshot.sh "+sys.argv[1]
              mailok = os.system(mail_message) >> 8
            if(mailok == 0):
              alarm_file.write(" mail inviato!\n")
              timelastmail=datetime.datetime.now()
            elif(mailok < 100):
              alarm_comment=" mail inviato senza foto! [RC "+str(mailok)+"]\n" 
#              alarm_comment=" mail inviato senza foto!\n" 
              alarm_file.write(alarm_comment)
              timelastmail=datetime.datetime.now()
            else:
              alarm_comment=" invio mail fallito! [RC "+str(mailok)+"]\n" 
#              alarm_comment=" invio mail fallito!\n" 
              alarm_file.write(alarm_comment)
          else:
              alarm_comment=" mail gia' inviato il "+str(timelastmail)+"\n"
              alarm_file.write(alarm_comment)
          alarm_file.close()
          status=GPIO.input(channel)
          if(status == 0):
             continue
#       print log_message,now,future
#       time.sleep(1.)
       now=datetime.datetime.now()
       GPIO.wait_for_edge(channel,GPIO.BOTH)

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



