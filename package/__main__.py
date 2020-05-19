#!/usr/bin/python
#coding=UTF-8

# import sys
import traceback

try:
	from .cr_main import MainRoutine
except Exception as ex:
	print(f'[{__package__}]:can not load MainRoutine,should run <python -m crawler>.')
	traceback.print_exc()
	exit(1)

MainRoutine.run()

