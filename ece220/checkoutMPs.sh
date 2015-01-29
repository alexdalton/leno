#!bin/bash

#This program checks out the correct MP from the students directory
#in subversion

$roster
$date
$baseDir
$mp

while getopts ":b:d:m:r:" opts
do
  case $opts in
    b)
      baseDir=$OPTARG
      ;;
    d)
       date=$OPTARG
       ;;
    m)
      mp=$OPTARG
      ;;
    r)
      roster=$OPTARG
      ;;
    \?)
      echo "Invalid Argument"
      exit 1
      ;;
    :)
      echo "Option $OPTARG missing an argment"
      exit 1
      ;;
  esac
done

mkdir $baseDir/$mp
cd $baseDir/$mp

while read line
do
  mkdir $line
  cd $line
  echo "Checking out $line"
  svn co -r {"$date"} https://subversion.ews.illinois.edu/svn/sp15-ece220/$line/$mp .
  cd ..
done < $roster
