#!bin/bash

#This program goes through all the student's code and add/commits the results.txt
#file

$roster
$baseDir

while getopts ":b:r:" opts
do
  case $opts in
    b)
      baseDir=$OPTARG
      ;;
    r)
      roster=$OPTARG
      ;;
    \?)
      echo "Invalid argument"
      exit 1
      ;;
    :)
      echo "Option $OPTARG missing an argument"
      exit 1
      ;;
  esac
done

cd $baseDir

while read line
do
  echo "Committing $line"
  cd $line
  svn add results.txt
  svn commit -m "Results Uploaded"
  cd ..
done < $roster
