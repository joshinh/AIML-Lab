#!/bin/bash

if [ $# -eq 2 ]
then 
	python decode_path.py $1 $2
else 
	python decode_path.py $1 $2 $3
fi