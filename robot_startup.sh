#! /usr/bin/env bash

robot_arguments_file="./features/.arguments.txt"

if [ X"$PWD" != X"$KARA_HOME" ]; then
  echo "current directory is't in kara home."
  exit 127
fi

if [ ! -e $robot_arguments_file ]; then
  echo "robot arguments file not found."
  exit 126
fi

echo $KARA_HOME
echo $PWD

robot --argumentfile $robot_arguments_file $*




