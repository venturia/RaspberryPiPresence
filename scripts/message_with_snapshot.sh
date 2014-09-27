#!/bin/bash



# some variables
# refactoring the script such that all these values are
# passed from the outside as arguments should be easy
 
#from="sender@example.com"
to=$1
subject="[${HOSTNAME}] Rilevata presenza"
boundary="ZZ_/afg6432dfgkl.94531q"
body="Rilevata presenza"
declare -a attachments
attachments=( "/tmp/motion/lastsnap.jpg" )

# check if motion is running: if not return !=0

pgrep -u motion motion
if [ $? != 0 ]; then 
  echo "motion is not running!"
  # send the text-only message
  $(dirname "$(readlink -f "$0")")/message_without_snapshot.sh "$to" "$subject" "$body"
  if [ $? != 0 ]; then 
    echo "Failed to send the text-only message"
    exit 101
  fi
  exit 1
fi

# wait for two seconds

sleep 2

# take the snapshot: if fail return !=0

wget -q -O /dev/null http://localhost:8182/0/action/snapshot
if [ $? != 0 ]; then 
  echo "Failed to take a snapshot"
  #send the text-only message
  $(dirname "$(readlink -f "$0")")/message_without_snapshot.sh "$to" "$subject" "$body"
  if [ $? != 0 ]; then 
    echo "Failed to send the text-only message"
    exit 102
  fi
  exit 2
fi

# sleep 5 seconds before checking for the file to be sure it is done

sleep 5

# check that the snapshot exists and that it is not too old , otherwise return !=0

if [ ! `find /tmp/motion/lastsnap.jpg -mmin -1` ]; then
  echo "snapshot file not found"
  #send the text-only message
  $(dirname "$(readlink -f "$0")")/message_without_snapshot.sh "$to" "$subject" "$body"
  if [ $? != 0 ]; then 
    echo "Failed to send the text-only message"
    exit 103
  fi
  exit 3
fi  

# Build headers
{
 
printf '%s\n' "To: $to
Subject: $subject
Mime-Version: 1.0
Content-Type: multipart/mixed; boundary=\"$boundary\"

--${boundary}
Content-Type: text/plain; charset=\"US-ASCII\"
Content-Transfer-Encoding: 7bit
Content-Disposition: inline

$body
"
 
# now loop over the attachments, guess the type
# and produce the corresponding part, encoded base64
for file in "${attachments[@]}"; do
 
  [ ! -f "$file" ] && echo "Warning: attachment $file not found, skipping" >&2 && continue
 
  mimetype="image/jpeg"
 
  printf '%s\n' "--${boundary}
Content-Type: $mimetype
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename=\"$file\"
"
 
  base64 "$file"
  echo
done
 
# print last boundary with closing --
printf '%s\n' "--${boundary}--"
 
} | /usr/sbin/sendmail -t -oi   # one may also use -f here to set the envelope-from

if [ $? != 0 ]; then 
  echo "Failed to send the mail message"
  exit 101
fi

exit 0
