#!/usr/bin/python
#coding=UTF-8

import traceback
import threading

from .task_runner import *
from .pdf_downloader import *
from .crawler_db import *
from .date_time import *
from .app_config import *

from .cr_logger import *

__all__=['KeywordDownloader']

class KeywordDownloader:
	'''
	'''
	def __init__(self,task_id):
		'''
		'''
		self.task_id=task_id
		self.max_load_cnt=0
		self.cur_load_cnt=0

		self.cfg=AppConfig()
		self.logger=Logger('Downloader')

	def setMaxLoadCount(self,new_val):
		'''
		'''
		if new_val<0:
			new_val=0

		self.max_load_cnt=new_val
		return self

	def run(self):
		'''
		'''
		ret=True

		runner=TaskRunner(self.cfg.taskWorkerCount)

		runner.setQueueBuilder(self.build_task_queue)
		runner.setTaskHandler(self.handle_task)
		ret=runner.start()
		if ret:
			ret=runner.waitForFinish()

		return ret

	def handle_task(self,task):
		'''
		'''
		ret=True

		# session_id="6fb6db0833dfe04d9c2822c98fb2a9249877gxrqa"
		session_id=self.cfg.curSessionId
		do_debug=self.cfg.doDebug

		rec_id=task['t_recid']
		url=task['t_url']

		self.logger.info(f'[handle_task]:rec_id({rec_id})')

		pdf_url="http://www.sciencedirect.com"+url

		dl=PdfDownloader(session_id,do_debug=do_debug)
		ret=dl.download(pdf_url)

		if ret:
			
			raw_data=dl.getContentData()

			db=CrawlerDB()
			dh=db.getHandle()

			try:
				dh.open()
				dh.begin()

				self.save_pdf_file(dh,rec_id,raw_data)
				self.update_state(dh,rec_id,0,1)
				
				dh.commit()
				dh.close()
				ret=True

			except Exception as ex:
				ret=False
				dh.rollback()
				dh.close()
				traceback.print_exc()
		else:
			ret=True
			self.logger.error(f'[handle_task]:download failed.')


		self.logger.info(f'[handle_task]:rec_id({rec_id}) done.ret({ret})')

		return ret

	def save_pdf_file(self,dh,rec_id,raw_data):
		'''
		'''

		task_id=self.task_id

		today=DateTime.today()
		tval=today.toDateString()

		rec={
			't_recid':rec_id,
			't_taskid':task_id,
			'crdt':tval,
			'mddt':tval,
			't_data':raw_data
		}

		dh.insert('dl_pdf_files',rec)

	def update_state(self,h,task_id,cur_state,next_state):
		'''
		'''

		self.logger.info(
			f'[update_state]:task_id({task_id}) cur({cur_state}) next({next_state})')

		sql='''
			update dl_pdf_tasks set t_state=?
			where t_recid=? and t_state=?
		'''

		acnt=-1
		acnt=h.execute(sql,next_state,task_id,cur_state)

		self.logger.info(f'[update_state]:done.task_id({task_id}) acnt({acnt}).')


	def build_task_queue(self,tq):
		'''
		'''
		ret=self.read_tasks(tq)
		if ret:
			if self.max_load_cnt>0:
				if self.cur_load_cnt>=self.max_load_cnt:
					tq.allTaskLoaded(True)

		return ret

	def read_tasks(self,tq):
		'''
		'''
		task_id=self.task_id
		self.logger.info(f'[read_tasks]:task_id({task_id}).')

		load_cnt=self.cfg.taskCountPerLoad
		max_cnt=self.max_load_cnt

		if max_cnt>0:
			load_cnt=load_cnt if load_cnt<max_cnt else max_cnt

		self.logger.info(f'[read_tasks]:task_id({task_id}) load_cnt({load_cnt}).')

		ret=True

		sql=f'''
			select * from dl_pdf_tasks
			where t_taskid=? and t_state=0
			limit 0,{load_cnt}
		'''

		db=CrawlerDB()
		h=db.getHandle()
		df=None

		try:
			h.open()
			df=h.executeQuery(sql,task_id)
			h.close()
			ret=True
		except Exception as ex:
			ret=False
			traceback.print_exc()
			h.close()

		if ret:
			for index,rec in df.iterrows():
				item={
					't_recid':rec['t_recid'],
					't_taskid':rec['t_taskid'],
					't_url':rec['t_url']
				}

				tq.append(item)
				self.cur_load_cnt+=1

		self.logger.info(f'[read_tasks]:done.ret({ret})')

		return ret




