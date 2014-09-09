#!/bin/bash

#The program copies the files in the specified directory into the 
#subdirectories in students' directories in the base directory

rootDir=""
copyDir=""
roster=""
input=""

while getopts ":b:c:i:r:" opt
do
  case $opt in
    b)
      baseDir=$OPTARG
      ;;
    c)
      copyDir=$OPTARG
      ;;
    i)
      input=$OPTARG
      ;;
    r)
      roster=$OPTARG
      ;;
    \?)
      echo "Invalid arguement"
      exit 1
      ;;
    :)
      echo "Option $OPTARG missing an argument"
      exit 1
      ;;
  esac
done

while read line
do
  cp $copyDir/* $baseDir/$line
done < $roster

#running the test from the given input
cd $baseDir
while read line
do
  cd $line
  echo "Currently testing in $line"
  bash $input
  cd ..
done < $roster
