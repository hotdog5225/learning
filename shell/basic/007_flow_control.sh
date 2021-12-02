#! /usr/bin/env bash

# if while and do in the same line, ";" needed
while (( 3>2 )); do
	echo "hello"
	break
done


name="hotdog"
case $name in 
	"hotdog" ) echo "hello $name" ;;
	*	) echo "hello other people";;
esac