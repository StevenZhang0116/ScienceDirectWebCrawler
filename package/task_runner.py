#!/usr/bin/python
#coding=UTF-8

import traceback
import threading
import queue

from .cr_logger import *

__all__=['TaskRunner','TaskQueue']

#---
#
#---
class WorkState:

	def __init__(self):
		self.loadCount=0
		self.workers={}
		self.mylock=threading.RLock()

	def incrLoadCount(self,cnt=1):
		ret=0
		if cnt>0:
			if self.mylock.acquire():
				self.loadCount+=cnt
				ret=self.loadCount
				self.mylock.release()
		return ret

	def getLoadCount(self):
		ret=0
		
		if self.mylock.acquire():
			ret=self.loadCount
			self.mylock.release()

		return ret

	def get_w_cell(self,worker_id):
		
		worker_id=f'{worker_id}'
		item=self.workers.get(worker_id)
		if item is None:
			item={
				'handleCount':0
			}
			self.workers[worker_id]=item
		return item

	def incrWorkCount(self,worker_id,cnt=1):
		ret=0
		if cnt>0:
			if self.mylock.acquire():

				witem=self.get_w_cell(worker_id)
				witem['handleCount']+=cnt
				ret=witem['handleCount']
				self.mylock.release()
		return ret

	def getData(self):

		ret={}

		if self.mylock.acquire():
			ret['loadCount']=self.loadCount
			ret['workers']=self.workers
			self.mylock.release()

		return ret

#---
#
#---
class TaskRunner:
	'''
	'''
	def __init__(self,worker_count=1):
		'''
		'''
		self.__inst=InternalTaskRunner()
		self.__inst.worker_count=worker_count

	def setQueueBuilder(self,new_builder):
		'''
		'''
		self.__inst.queue_builder=new_builder
		return self

	def setTaskHandler(self,new_handler):
		'''
		'''
		self.__inst.task_handler=new_handler
		return self

	def start(self):
		'''
		'''
		ret=self.__inst.start()
		return ret

	def waitForFinish(self):
		'''
		'''
		ret=self.__inst.waitForFinish()
		return ret


#---
#
#---
class InternalTaskRunner:
	
	def __init__(self):
		'''
		'''
		self.tdc=None
		self.worker_count=1
		self.td_workers=[]
		self.task_queue=TD_Queue()
		self.c_qempty=threading.Condition()
		self.c_qready=threading.Condition()

		self.work_state=WorkState()

		self.all_tasks_loaded=False
		self.abort_ctrls=False

		self.queue_builder=None
		self.task_handler=None

		self.logger=Logger('TaskRunner')

	def getWorkState(self):
		'''
		'''
		ret=self.work_state.getData()
		return ret

	#---
	#
	#---
	def start(self):
		'''
		'''
		self.logger.info(f'[start].')

		ret=True

		if self.queue_builder is None:
			self.logger.error(f'[start][error]:no queue builder.')
			ret=False

		if ret and self.task_handler is None:
			self.logger.error(f'[start][error]:no task handler.')
			ret=False

		if ret:

			self.tdc=TD_Controller(holder=self)
			self.tdc.setDaemon(True)

			wcnt=self.worker_count
			if wcnt<=0:
				wcnt=1

			self.logger.info(f'[start]:worker count({wcnt})')

			for index in range(wcnt):
				tdw=TD_Worker(holder=self,worker_id=index)
				tdw.setDaemon(True)
				self.td_workers.append(tdw)

			self.tdc.start()
			for tdw in self.td_workers:
				tdw.start()

		self.logger.info(f'[start]:done.ret({ret})')

		return ret

	#---
	#
	#---
	def waitForFinish(self):
		'''
		'''
		ret=True
		self.logger.info(f'[waitForFinish].')
		self.wait_all_done()
		self.logger.info(f'[waitForFinish]:done.ret({ret})')
		return ret

	#---
	#
	#---
	def check_worker_done(self,timeout=0.3):
		'''
		'''
		ret=False
		try:
			
			alive=False

			for tdw in self.td_workers:
				tdw.join(timeout)
				alive=tdw.is_alive()
				if alive:
					break

			if alive==False:
				ret=True
			else:
				ret=False

		except Exception as ex:
			self.logger.error('[check_worker_done][exception]:({ex})')
			ret=False

		return ret

	def check_ctrl_done(self,timeout=0.3):
		'''
		'''
		ret=False
		try:
			self.tdc.join(timeout)
			alive=self.tdc.is_alive()
			if alive==False:
				ret=True

		except Exception as ex:
			self.logger.error('[check_ctrl_done][exception]:({ex})')
			ret=False

		return ret

	#---
	#
	#---
	def wait_all_done(self):

		self.logger.debug('[wait_all_done].')

		while True:
			ret=self.check_worker_done()
			if ret:
				self.logger.warn(f'[wait_all_done]:found all workers stopped.')
				self.abort_ctrls=True
				self.notify_queue_empty()
				self.check_ctrl_done()
				break

		self.logger.debug('[wait_all_done]:done.')


	#---
	#
	#---
	def wait_queue_empty(self):
		'''
		'''
		self.logger.debug(f'[wait_queue_empty].')

		ret=True
		if self.c_qempty.acquire():
			self.c_qempty.wait()
			self.c_qempty.release()
		else:
			self.logger.error(f'[wait_queue_empty]:acquire FAILED.')

		self.logger.debug(f'[wait_queue_empty]:done.ret({ret})')

		return ret

	#---
	#
	#---
	def wait_queue_ready(self):
		'''
		'''

		self.logger.debug(f'[wait_queue_ready].')

		ret=False

		ret=self.notify_queue_empty()
		if ret==False:
			self.logger.error(f'[wait_queue_ready]:notify empty failed.')

		if ret:
			if self.c_qready.acquire():
				self.c_qready.wait()
				self.c_qready.release()
				ret=True
			else:
				ret=False
				self.logger.error(f'[wait_queue_ready]:c_qready acquire FAILED.')

		self.logger.debug(f'[wait_queue_ready]:done.ret({ret})')

		return ret

	def is_all_tasks_loaded(self):
		'''
		'''
		ret=self.all_tasks_loaded
		return ret

	def notify_queue_empty(self):
		'''
		'''
		ret=True

		if self.c_qempty.acquire():
			self.c_qempty.notify()
			self.c_qempty.release()
			ret=True
		else:
			ret=False
			self.logger.error(f'[notify_queue_empty]:c_qempty acquire FAILED.')

		return ret


	def notify_queue_ready(self):
		'''
		'''
		ret=True
		if self.c_qready.acquire():
			self.c_qready.notifyAll()
			self.c_qready.release()
		else:
			self.logger.error('[notify_queue_ready]:FAILED.')
			ret=False

		return ret

	def check_fill_queue(self):
		'''
		'''
		ret=True

		if self.abort_ctrls:
			self.logger.warn(f'[check_fill_queue]:found abort signal,abort!')
			ret=False
		else:
			ret=self.fill_queue()
		
		return ret

	#---
	#
	#---
	def fill_queue(self):
		'''
		'''
		
		ret=True
		self.logger.debug(f'[fill_queue].')

		tq=TaskQueue(self)
		ret=self.queue_builder(tq)

		if ret is None:
			ret=True

		ret=self.notify_queue_ready()

		if self.all_tasks_loaded:
			self.logger.warn(f'[fill_queue]:all task loaded,well done!')
			ret=False

		self.logger.debug(f'[fill_queue]:done.ret({ret})')

		return ret

	#---
	#
	#---
	def pop_queue(self):
		'''
		'''
		self.logger.debug(f'[pop_queue].')

		ret=None

		if self.task_queue.count()>0:
			ret=self.task_queue.pop()

		has_data=(False if ret is None else True)
		self.logger.debug(f'[pop_queue]:done.has_data({has_data})')

		return ret

	def handle_task(self,worker,task):
		'''
		'''
		ret=True

		self.logger.debug(f'[handle_task]:task({type(task)}).')
		
		ret=self.task_handler(task)
		if ret is None:
			ret=True
		
		self.work_state.incrWorkCount(worker.wid)

		self.logger.debug(f'[handle_task]:done.ret({ret})')

		return ret

#---
#
#---
class TaskQueue:
	'''
	'''
	def __init__(self,holder):
		'''
		'''
		self.holder=holder
		self.internal=holder.task_queue

	def append(self,task):
		'''
		'''
		self.internal.push(task)

	def getCount(self):
		'''
		'''
		ret=self.internal.count()
		return ret

	def allTaskLoaded(self,flag=True):
		'''
		'''
		self.holder.all_tasks_loaded=flag
		return self


#---
#
#---
class TD_Queue:
	'''
	'''

	#---
	#
	#---	
	def __init__(self):
		self.items=queue.Queue()
		self.logger=Logger('Queue')

	#---
	#
	#---
	def push(self,item):
		'''
		'''
		self.items.put(item)

	#---
	#
	#---
	def pop(self):
		'''
		'''
		ret=None
		try:
			ret=self.items.get(timeout=0.1)
		except queue.Empty:
			# no data in queue.
			ret=None
		except Exception as ex:
			self.logger.error(f'[pop][exception]:({type(ex)})({ex})')
			ret=None
		return ret

	#---
	#
	#---
	def count(self):
		'''
		'''
		ret=self.items.qsize()
		return ret

#---
#
#---
class TD_Controller(threading.Thread):

	def __init__(self,holder):
		super().__init__()
		self.name='ctrl'
		self.holder=holder
		self.state=True
		self.logger=Logger('Controller')

	def run(self):
		'''
		'''
		self.logger.info(f'[run].')
		
		while True:
			
			if self.state==False:
				break

			holder=self.holder
			ret=True
			try:
				ret=holder.check_fill_queue()
				if ret:					
					ret=holder.wait_queue_empty()

			except Exception as ex:
				self.logger.error(f'[run][exception]:({ex})')
				traceback.print_exc()
				ret=False

			if ret==False:
				break

		self.logger.info(f'[run]:done.')

#---
#
#---
class TD_Worker(threading.Thread):

	def __init__(self,holder,worker_id):

		super().__init__()

		self.name=f'worker-{worker_id}'
		
		self.holder=holder
		self.wid=worker_id
		self.state=True
		self.logger=Logger(f'Worker({worker_id})')

	def run(self):
		'''
		'''
		self.logger.info(f'[run].')

		while True:

			if self.state==False:
				break

			ret=True
			holder=self.holder
			try:
				item=holder.pop_queue()
				if item is None:
					if holder.is_all_tasks_loaded():
						self.logger.warn(f'[run]:found all tasks loaded,exit.')
						ret=False
					else:
						ret=holder.wait_queue_ready()
				else:
					ret=holder.handle_task(self,item)
					if ret==False:
						self.logger.warn(f'[run]:handle task failed,exit!')
				
			except Exception as ex:
				self.logger.error(f'[run][exception]:({ex})')
				traceback.print_exc()
				ret=False

			if ret==False:
				break

		self.logger.info(f'[run]:done.')












