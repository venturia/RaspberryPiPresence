#!/bin/bash

WEBDIR=/var/www/html
ALARMDIR=/var/apache

read -p "web server file directory [$WEBDIR]" chosenwebdir

if [ ${#chosenwebdir} != 0 ]; then
  WEBDIR=$chosenwebdir
fi

# copy the web pages in the web server subdirectory "presenze"

if [ ! -d "${WEBDIR}/presenze" ]
then
   echo "creating ${WEBDIR}/presenze directory"
   mkdir -v ${WEBDIR}/presenze
   if [ ! $?=0 ]
   then
      echo "not able to create ${WEBDIR}/presenze"
      exit 1
   fi
   echo "directory ${WEBDIR}/presenze created"
fi

echo "copying php scripts"
sed 's/MOTIONCTRLPORT/'${1}'/g' webpages/presenze.php > ${WEBDIR}/presenze/presenze.php
cp -v webpages/plot_from_tmp.php ${WEBDIR}/presenze/.


# create the /var/apache directory if it does not exist and set the proper authorization

if [ ! -d ${ALARMDIR} ]
then
   echo "create ${ALARMDIR} directory"
   mkdir -v ${ALARMDIR}
   if [ ! $?=0 ]
   then
      echo "not able to create ${ALARMDIR}"
      exit 2
   fi
   echo "directory ${ALARMDIR} created"
   echo "set the proper owner, group and authorization"
   chgrp -v www-data ${ALARMDIR}
   if [ ! $?=0 ]
   then
      echo "not able to change ${ALARMDIR} group"
      exit 3
   fi
   chmod -v g+w ${ALARMDIR}
   if [ ! $?=0 ]
   then
      echo "not able to change ${ALARMDIR} authorizations"
      exit 4
   fi
   echo "directory ${ALARMDIR} is ready"
fi

