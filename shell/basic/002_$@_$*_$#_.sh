#! /usr/bin/env bash

function test_func() {
	echo "numbs of function params: $#" # numbs of params: 4

	echo "in function, \$0 is file name:  ${0}" # in function, $0 is file name:  ./002_$@_$*_$#_.sh

	echo "get all params: $@" # get all params: p1 p2 p3 p4

	echo ">>> when in soft quote, \"\$@\" will return an array: "
	for item in "$@"; do
		echo $item
	done
	# p1
	# p2
	# p3
	# p4

	echo ">>> when in soft quote, \"\$*\" will return a string: "
	for item in "$*"; do
		echo $item
	done
}

test_func p1 "p2 p3" p4