#!/usr/bin/python
#coding=UTF-8

import traceback
from .crawler_db import *
from .cr_logger import *

__all__=['KeywordRemover']

class KeywordRemover:
	'''
	'''
	def __init__(self,task_id):
		'''
		'''
		self.task_id=task_id
		self.logger=Logger('Remover')

	def run(self):
		'''
		'''
		task_id=self.task_id

		print(f'remove task_id({task_id})')

		ret=self.process_remove()
		
		if ret:
			print(f'remove task({task_id}) succeeded.')
		else:
			print(f'remove task_id({task_id}) Failed.')

		return ret

	def process_remove(self):
		'''
		'''
		ret=True

		db=CrawlerDB()
		dh=db.getHandle()

		try:
			dh.open()
			dh.begin()

			self.remove_keys(dh)
			self.remove_task(dh)
			self.remove_pdf_task(dh)
			self.remove_pdf_files(dh)
			self.remove_pdf_info(dh)
			self.remove_pdf_authors(dh)

			dh.commit()
			dh.close()
			ret=True

		except Exception as ex:
			dh.rollback()
			dh.close()
			ret=False
			traceback.print_exc()

		return ret

	def remove_task(self,dh):
		'''
		'''
		sql='''
		delete from dl_tasks
		where t_taskid=?
		'''

		task_id=self.task_id
		dh.execute(sql,task_id)

	def remove_keys(self,dh):
		'''
		'''
		sql='''
		delete from dl_keys
		where t_taskid=?
		'''

		task_id=self.task_id
		dh.execute(sql,task_id)

	def remove_pdf_info(self,dh):
		'''
		'''
		sql='''
		delete from dl_pdf_info
		where t_taskid=?
		'''

		task_id=self.task_id
		dh.execute(sql,task_id)

	def remove_pdf_authors(self,dh):
		'''
		'''
		sql='''
		delete from dl_pdf_authors
		where t_taskid=?
		'''

		task_id=self.task_id
		dh.execute(sql,task_id)


	def remove_pdf_task(self,dh):
		'''
		'''
		sql='''
		delete from dl_pdf_tasks
		where t_taskid=?
		'''

		task_id=self.task_id
		dh.execute(sql,task_id)

	def remove_pdf_files(self,dh):
		'''
		'''
		sql='''
		delete from dl_pdf_files
		where t_taskid=?
		'''

		task_id=self.task_id
		dh.execute(sql,task_id)




