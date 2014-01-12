#!/bin/bash



# some variables
# refactoring the script such that all these values are
# passed from the outside as arguments should be easy
 
#from="sender@example.com"
to=$1
subject=$2
body=$3

# Build headers
{
 
printf '%s\n' "To: $to
Subject: $subject
$body
"
} | /usr/sbin/sendmail -t -oi   # one may also use -f here to set the envelope-from

if [ $? != 0 ]; then 
  echo "Failed to send the mail message"
  exit 101
fi


