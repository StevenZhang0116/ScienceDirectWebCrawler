#!/usr/bin/python
#coding=UTF-8

import os
import traceback
from .crawler_db import *
from .cr_logger import *

__all__=['PdfExporter']

class PdfExporter:
	'''
	'''
	def __init__(self):
		'''
		'''
		self.condis={}
		self.logger=Logger('PdfExporter')

	def addCondition(self,name,val):
		'''
		'''
		self.condis[name]=val
		return self

	def hasCondition(self):
		'''
		'''
		cnt=len(self.condis)
		ret=False
		if cnt>0:
			ret=True
		return ret

	def run(self):
		'''
		'''
		ret=self.export_items()
		return ret
		

	def save_pdf(self,row):
		'''
		'''
		ret=True

		recid=row['t_recid']
		fname=row['t_name']
		pdata=row['t_data']

		self.logger.info(f'Doc({fname}):size({len(pdata)}) id({recid})')

		fname=f'{fname}({recid}).pdf'
		fname=fname.replace('/','-')

		fpath=f'./pdf_files/{fname}'

		folder=os.path.dirname(fpath)

		if os.path.exists(folder)==False:
			os.makedirs(folder)

		with open(fpath,'wb') as fp:
			fp.write(pdata)

		return ret

	def is_like(self,val):
		'''
		'''
		ret=False
		if val.startswith('%') or val.endswith('%'):
			ret=True

		return ret

	def parse_where(self):
		'''
		'''
		ret=None

		for key,val in self.condis.items():

			w=''
			if self.is_like(val):
				w=f"t0.{key} like '{val}'"
			else:
				w=f"t0.{key}='{val}'"

			if ret is None:
				ret=w
			else:
				ret=f'{ret} and {w}'

		if ret is not None:
			ret=f'{ret} and t0.t_state=1'

		return ret

	def export_items(self):
		'''
		'''

		sql=f'''
select t0.t_recid,t0.t_taskid,t0.t_name,t1.t_data from dl_pdf_tasks t0
left join dl_pdf_files t1 on (t0.t_recid=t1.t_recid and t0.t_taskid=t1.t_taskid)
		'''

		where=self.parse_where()
		sql=f'{sql} where {where}'

		self.logger.debug(f'sql:[{sql}]')

		ret=self.export_with_sql(sql)

		if ret==False:
			self.logger.error(f'sql({sql})')

		return ret

	def export_with_sql(self,sql):
		'''
		'''

		ret=True

		cnt=0

		self.logger.info(f'exporting PDF.')

		db=CrawlerDB()
		dh=db.getHandle()

		try:
			ret=True
			dh.open()
			reader=dh.executeReader(sql)
			if reader is not None:
				while reader.read():
					ret=self.save_pdf(reader)
					if ret==False:
						break
					cnt+=1

				reader.close()

			dh.close()
		except Exception as ex:
			ret=False
			dh.close()
			traceback.print_exc()
			self.logger.error('[exception]:({ex})')

		self.logger.info(f'({cnt}) PDF exported.')

		return ret



