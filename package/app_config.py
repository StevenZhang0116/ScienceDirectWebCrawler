#!/usr/bin/python
#coding=UTF-8

__all__=['AppConfig']

#---
#
#---
class AppConfig:
	'''
	'''
	def __init__(self):
		'''
		'''
		self.data={
		
			'do_debug':False,

			'task_worker_count':3,
			'task_count_per_load':10*3,

			'session_id':''
		}

		self.db_config={
			'host':'localhost',
			'user':'root',
			'passwd':'stevenzhang',
			'db':'test'
		}

		self.db_type='mysql'

		if self.db_type=='mysql':
			self.type_blob='longblob'
		else:
			self.type_blob='blob'

	def printCommonConfig(self):
		'''
		'''
		print(f'# common config')
		print(f'#---------------')
		for k,v in self.data.items():
			print(f'# {k:>20}={v:<32}')

		print(f'#')

	#---
	#
	#---
	def printDbConfig(self):
		'''
		'''
		print(f'# db config')
		print(f'#--------------')
		print(f'# {"type":>16}=({self.db_type})')

		if self.db_config is not None:
			for k,v in self.db_config.items():
				print(f'# {k:>16}={v:<32}')

		print(f'#')
		print(f'#')

	@property
	def doDebug(self):
		'''
		'''
		ret=self.data.get('do_debug',False)
		return ret

	@property
	def curSessionId(self):
		'''
		'''
		ret=self.data.get('session_id','')
		return ret

	@property
	def dbType(self):
		'''
		'''
		ret=self.db_type
		return ret

	@property
	def dbConfig(self):
		'''
		'''
		ret=self.db_config
		return ret

	@property
	def taskWorkerCount(self):
		'''
		'''
		ret=self.data.get('task_worker_count',1)
		return ret

	@property
	def taskCountPerLoad(self):
		'''
		'''
		ret=self.data.get('task_count_per_load',0)
		if ret<=0:
			ret=self.taskWorkerCount*10
			
		return ret


