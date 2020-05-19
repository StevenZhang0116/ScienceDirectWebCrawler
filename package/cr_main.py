#!/usr/bin/python
#coding=UTF-8

import sys
import os

from .crawler_db import *
from .task_admin import *
from .app_config import *

__all__=['MainRoutine']

class CommandLine:
	'''
	'''
	def __init__(self):
		pass

	#----
	#
	#----
	def match(self,items=[]):
		'''
		'''
		ret=False
		if len(items)<=0:
			return ret

		if self.size()<=0:
			return ret

		ret=True
		for index in range(0,len(items)):
			src=items[index]
			dest=self.get(index)
			if src!=dest:
				ret=False
				break

		return ret

	def size(self):
		'''
		'''
		ret=len(sys.argv)
		ret-=1
		return ret

	def get(self,index):
		'''
		'''
		ret=None
		index+=1
		if index<len(sys.argv):
			ret=sys.argv[index]
		return ret

	def getParts(self,start_index):
		'''
		'''
		# print(sys.argv)
		start_index+=1
		ret=[]
		for index in range(start_index,len(sys.argv)):
			sval=sys.argv[index]
			ret.append(sval)
		return ret

#------
#
#------
class MainRoutine:
	'''
	main routine for this module.
	'''

	#---
	#
	#---
	@staticmethod
	def run():

		cfg=AppConfig()
		if cfg.doDebug:
			cfg.setDebug('debug')

		cl=CommandLine()

		if cl.match(['search','task']):
			pas=cl.getParts(2)
			job=TaskAdmin()
			job.searchKeywords(pas)

		elif cl.match(['build','task']):
			pas=cl.getParts(2)
			job=TaskAdmin()
			job.buildKeywords(pas)

		elif cl.match(['sum','task']):
			pas=cl.getParts(2)
			job=TaskAdmin()
			job.summaryKeywords(pas)

		elif cl.match(['remove','task']):
			pas=cl.getParts(2)
			job=TaskAdmin()
			job.removeKeywords(pas)

		elif cl.match(['download','task']):
			pas=cl.getParts(2)
			job=TaskAdmin()
			job.downloadKeywords(pas)

		elif cl.match(['sum','pdf']):
			pas=cl.getParts(2)
			job=TaskAdmin()
			job.summaryPdf(pas)

		elif cl.match(['exp','pdf']):
			pas=cl.getParts(2)
			job=TaskAdmin()
			job.exportPdfs(pas)

		elif cl.match(['show','config']):
			pas=cl.getParts(2)
			job=TaskAdmin()
			job.showConfig(pas)

		elif cl.match(['help']):
			MainRoutine.show_usage()

		else:
			MainRoutine.show_usage()
			exit(-1)

	#---
	#
	#---
	@staticmethod
	def show_usage():
		'''
		'''
		print(f'''

usage:
=======

# help
	show this page.

# show config 
	show config information to run.

# build task <task_id> <keywords_file_path>
	build url list for searching keywords from sciencedirect.com
	params:
		task_id - url list name.
		keywords_file_path - excel file path containing keywords pairs.

# search task <task_id> [max_load_count]
	search sciencedirect.com with urls in task and build 
		info and pdf's address.
	params:
		task_id - url list name.
		max_load_count - optional.max run count,
			if beyond,stop the process.all tasks by default.

# remove task <task_id>
	remove all task information specified by task_id.
	params:
		task_id - the task id.

# download task <task_id> [max_load_count]
	download pdf file and save into DB.
	params:
		task_id - the task id.
		max_load_count - max run count,all by default.
			if beyond,the process is stopped.

# sum task
	summary report for tasks.

# sum pdf
	summary report for pdf downloading.

# exp pdf <task=xxx|name=xxx> [...]
	export pdf file from db to hard-drive.you can input some
	conditions such as task,name ext.to search db and export.

		''')




