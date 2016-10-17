#!/bin/bash

for i in `ls -l | awk '{print $9}' | grep '20'`; do

	echo $i
 	crab -submit 500 -c $i
 	crab -submit 500 -c $i
 	crab -submit 500 -c $i
 	crab -submit 500 -c $i
 	crab -submit 500 -c $i
	#crab -kill all -c $i
    #crab -status -c $i
    #crab -get -c $i


done
