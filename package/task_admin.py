#!/usr/bin/python
#coding=UTF-8

from .keyword_searcher import *
from .keyword_builder import *
from .keyword_task_summary import *
from .keyword_remover import *
from .keyword_downloader import *
from .keyword_pdf_summary import *
from .pdf_exporter import *
from .app_config import *

__all__=['TaskAdmin']

class ParamArray:
	def __init__(self,param_array):
		self.data=param_array

	def get(self,index,default_value=None):
		ret=default_value
		if index<len(self.data):
			ret=self.data[index]
		return ret

	def find(self,pname):
		ret=None
		for sval in self.data:
			nv=sval.split('=')
			if len(nv)<2:
				continue

			name=nv[0].strip()
			if(name==pname):
				ret=nv[1].strip()
				break
		return ret


#----
#
#----
class TaskAdmin:
	'''
	'''
	def __init__(self):
		'''
		'''
		pass

	def showConfig(self,pas):
		'''
		'''
		cfg=AppConfig()
		cfg.printCommonConfig()
		cfg.printDbConfig()


	def summaryKeywords(self,pas):
		'''
		'''
		kts=KeywordTaskSummary()
		ret=kts.run()

		return ret

	def removeKeywords(self,pas):
		'''
		'''
		pas=ParamArray(pas)
		task_id=pas.get(0)

		if task_id is None:
			print(f'error:no task_id specified.')
			return False

		km=KeywordRemover(task_id)
		ret=km.run()

		return ret

	def downloadKeywords(self,pas):
		'''
		'''
		pas=ParamArray(pas)
		task_id=pas.get(0)
		max_cnt=pas.get(1)

		if task_id is None:
			print(f'error:no task_id specified.')
			return False

		kd=KeywordDownloader(task_id)
		if max_cnt is not None:
			max_cnt=int(max_cnt)
			kd.setMaxLoadCount(max_cnt)

		ret=kd.run()

		return ret

	def summaryPdf(self,pas):
		'''
		'''
		kps=KeywordPdfSummary()
		ret=kps.run()
		return ret


	def searchKeywords(self,pas):
		'''
		request keywords url to get pdf urls.
		'''
		pas=ParamArray(pas)
		task_id=pas.get(0)
		max_cnt=pas.get(1)

		if task_id is None:
			print(f'error:no task_id specified.')
			return False

		print(f'search keywords task({task_id}).')

		ks=KeywordSearcher(task_id)

		if max_cnt is not None:
			max_cnt=int(max_cnt)
			ks.setMaxLoadCount(max_cnt)

		ret=ks.run()

		print(f'search keywords done.ret({ret})')

		return ret

	def buildKeywords(self,pas):
		'''
		'''
		pas=ParamArray(pas)

		task_id=pas.get(0)
		fpath=pas.get(1)

		if (task_id is None) or (fpath is None):
			print(f'[error]:need params <task_id> <keywords file path>')
			print(f'\ttask_id({task_id})')
			print(f'\tfilepath({fpath})')
			return False

		print(f'build keywords to dl_tasks.')
		print(f'\ttask_id:({task_id})')
		print(f'\tfile path:({fpath})')

		kb=KeywordBuilder(task_id,fpath)
		ret=kb.run()

		if ret:
			print(f'build succeeded.count({kb.buildCount})')
		else:
			print(f'build Failed.')

		return ret

	def exportPdfs(self,pas):
		'''
		'''
		pas=ParamArray(pas)

		pe=PdfExporter()

		names=[
			['task','t_taskid'],
			['name','t_name']
		]

		for ns in names:
			val=pas.find(ns[0])
			if val is None:
				continue
			pe.addCondition(ns[1],val)

		if not pe.hasCondition():
			print(f'no condition given.')
			return False

		ret=pe.run()

		return ret







