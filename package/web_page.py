#!/usr/bin/python
#coding=UTF-8

__all__=['WebPage']

class WebPage:
	'''
	'''
	def __init__(self):
		'''
		'''
		self.user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'


	@property
	def userAgent(self):
		'''
		'''
		ret=self.user_agent
		return ret

	@userAgent.setter
	def userAgent(self,new_val):
		'''
		'''
		if (new_val is None) or (new_val==""):
			return

		self.user_agent=new_val

	

