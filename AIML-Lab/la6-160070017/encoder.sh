#!/bin/bash

if [ $# -eq 1 ]
then 
	python convert_to_mdp.py $1
else 
	python convert_to_mdp.py $1 $2
fi