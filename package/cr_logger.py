#!/usr/bin/python
#coding=UTF-8

import traceback
import time
import threading

__all__=['Logger']

class Logger:
	'''
	'''
	def __init__(self,module_name):
		'''
		'''
		self.logger=InternalLogger(module_name,InternalLogger.log_level)

	@staticmethod
	def setLevel(level_name):
		'''
			level_name:
				info|error|warn|debug|all
		'''
		ret=InternalLogger.setLevel(level_name)
		return ret

	def always(self,msg=None):
		self.logger.print_output('ALS',msg)

	def info(self,msg=None):
		if self.logger.level<3:
			return
		self.logger.print_output('INF',msg)

	def error(self,msg):
		if self.logger.level<1:
			return
		self.logger.print_output('ERR',msg)

	def warn(self,msg):
		if self.logger.level<2:
			return
		self.logger.print_output('WRN',msg)

	def debug(self,msg=None):
		
		if self.logger.level<4:
			return

		self.logger.print_output('DBG',msg)


class InternalLogger:
	'''
	'''
	def __init__(self,module_name,level):
		'''
		'''
		self.module_name=module_name
		self.level=level

	log_level=3

	@staticmethod
	def setLevel(level_name):
		ret=True
		nval=3
		
		val=level_name.lower().strip()
		if val=='info' or val=='inf':
			nval=3
		elif val=='error' or val=='err':
			nval=1
		elif val=='warn' or val=='wrn':
			nval=2
		elif val=='debug' or val=='dbg':
			nval=4
		elif val=='all':
			nval=5
		else:
			nval=3
			ret=False

		InternalLogger.log_level=nval

		return ret


	def print_output(self,flag,msg=None):
		'''
		'''
		if msg is None:
			print()
			return

		try:

			timestamp=time.strftime('%m-%d %H:%M:%S',time.localtime())
			tname=threading.current_thread().getName()
			mname=self.module_name
			if isinstance(msg,list) or isinstance(msg,tuple):
				if len(msg)<=0:
					print()
				else:
					ident=' '*4
					print(f'[{timestamp}][{tname}][{mname}][{flag}]:')
					for ms in msg:
						if ms is None:
							print()
						else:
							print(f'{ident}{ms}')

			else:
				print(f'[{timestamp}][{tname}][{mname}][{flag}]{msg}')

		except Exception as ex:
			traceback.print_exc()
			print(f'[Logger][print_output][exception]:({ex})')


