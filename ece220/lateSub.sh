#!/bin/bash

#This program compares the final submission time of a homework assignment with
#a student's final commit time and calculates the amount of points that should
#be deducted from the student's score if their assignment was turned in late.
#The program assumes that the last submitted homework assignment is the most
#correct version.

submitDateTime=""
while getopts ":d:" opt; do
  case $opt in
    d)
      submitDate=$OPTARG
      ;;
    \?)
       echo "Invalid input"
       exit 1
       ;;
     :)
       echo "Option -$OPTARG requires an argument."
       exit 1
       ;;
  esac
done

#Calculate number of hours student to submit late before he/she gets 0.
maxHoursLate=50

#Getting the date and time from svn info 
#Rename some of these values, but works!
studDateTime=$(svn info | grep Date | cut -d ' ' -f 4-5)
testDate=$(date -d "$studDateTime" +"%s")
testDate2=$(date -d "$submitDate" +"%s")
diff=$(($testDate-$testDate2))

#Check to see if the difference is greater than 0. If so, calculate the 
#amount of hours before the before the student gets a score of 0.
#Compare to to the difference and write the appropriate message to the 
#pointsDeducted.txt file. If the student is fine, then no such file will 
#be created.
echo "Submission points"
echo "********************"
if [ $diff -gt 0 ]
then
  ceil=$((diff%3600))
  hoursLate=$((diff/3600)) #This truncates the remainder
  if [[ $ceil -gt 0 ]]
  then
    hoursLate=$((hoursLate+1))
  fi
  #echo "Hours late: $hoursLate"
  #echo "Max hours late: $maxHoursLate"
  if [[ $hoursLate -gt $maxHoursLate ]]
  then
    echo "Lost 100 points"
  elif [[ $hoursLate -gt 0 ]]
  then
    echo "Lost $((hoursLate*2)) points"
  fi
else
  echo "Lost 0 points"
fi
echo ""
