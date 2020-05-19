#!/usr/bin/python
#coding=UTF-8

import datetime as DT

__all__=['DateTime','DateRange']

#---------------
#
#---------------
class DateTime:
	def __init__(self):
		self.dval=None

	#-------------
	#
	#-------------
	@staticmethod
	def parseDate(dt_str,fmt='%Y-%m-%d'):
		dval=DT.datetime.strptime(dt_str,fmt)
		# print(f'[parseDate]:dval({dval}) type({type(dval)})')		
		ret=DateTime()
		ret.dval=dval
		return ret

	#--------------
	#
	#--------------
	@staticmethod
	def lastDayOfYear():
		today=DT.datetime.now().date()
		today=today.replace(month=12).replace(day=31)

		ret=DateTime()
		ret.dval=today
		return ret

	#--------------
	#
	#--------------
	@staticmethod
	def now():
		dval=DT.datetime.now()
		ret=DateTime()
		ret.dval=dval
		return ret

	#--------------
	#
	#--------------
	@staticmethod
	def today():
		dval=DT.datetime.today()
		dval=dval.replace(hour=0,minute=0,second=0,microsecond=0)
		# print(f'[today]:dval({dval}) type({type(dval)})')
		ret=DateTime()
		ret.dval=dval
		return ret

	#---------------
	#
	#---------------
	@staticmethod
	def getTickString():
		dval=DT.datetime.now()
		ret=dval.strftime('%Y%m%d-%H%M%S-%f')
		return ret

	#---------------
	#
	#---------------
	def getTicks(self):
		ret=self.dval.timestamp()
		ret=int(ret)
		return ret


	#-------------
	#
	#-------------
	def firstDayOfMonth(self,inplace=False):
		dval=self.dval.replace(day=1)
		if inplace:
			self.dval=dval
			return self
		else:
			ret=DateTime()
			ret.dval=dval
			return ret

	#------------
	#
	#------------
	def addDays(self,int_days,inplace=False):
		try:
			dval=self.dval+DT.timedelta(days=int_days)
			if inplace:
				self.dval=dval
				return self
			else:
				ret=DateTime()
				ret.dval=dval
				return ret
		except Exception as ex:
			print(f'[exception]:{ex}')
			print(f'dval:({self.dval}) int_days:({int_days})')
			raise ex

	#--------------
	#
	#--------------
	def addMonths(self,int_months,inplace=False):
		cm=self.dval.month
		cm+=int_months
		cm0=cm%12
		cm1=int((cm-cm0)/12)

		cm0=(1 if cm0==0 else cm0)

		dval=self.dval.replace(month=cm0)
		if cm1>0:
			yv=self.dval.year
			yv+=cm1
			dval=dval.replace(year=yv)

		if inplace:
			self.dval=dval
			return self
		else:
			ret=DateTime()
			ret.dval=dval
			return ret

	#------------
	#
	#------------
	@property
	def year(self):
		ret=self.dval.year
		return ret

	#------------
	#
	#------------
	@year.setter
	def year(self,int_val):
		print('year.setter')
		pass

	#------------
	#
	#------------
	def __repr__(self):
		ret=self.dval.strftime('%Y-%m-%d %H:%M:%S')
		return ret

	#-----------
	#
	#-----------
	def __le__(self,other):
		ret=(self.dval<=other.dval)
		return ret

	#-----------
	#
	#-----------
	def __lt__(self,other):
		ret=(self.dval<other.dval)
		return ret

	#-----------
	#
	#-----------
	def __ge__(self,other):
		ret=(self.dval>=other.dval)
		return ret

	#-----------
	#
	#-----------
	def __gt__(self,other):
		ret=(self.dval>=other.dval)
		return ret

	#-----------
	#
	#-----------
	def __eq__(self,other):
		ret=(self.dval==other.dval)
		return ret

	#------------
	#
	#------------
	def toString(self,fmt=None):
		if fmt is None:
			fmt='%Y-%m-%d'

		ret=self.dval.strftime(fmt)
		return ret

	#-------------
	#
	#-------------
	def toDateString(self):
		fmt='%Y-%m-%d'
		return self.toString(fmt)

#-----------------
#
#-----------------
class DateRange:

	#----------------
	#
	#----------------
	def __init__(self,sd,ed):
		self.startDate=sd
		self.endDate=ed

	#----------------
	#
	#----------------
	def getDays(self):

		sd=DateTime.parseDate(self.startDate)
		ed=DateTime.parseDate(self.endDate)

		ret=[]
		cd=sd

		while cd<ed:
			sval=cd.toDateString()
			ret.append(sval)
			cd=cd.addDays(1)

		return ret


if __name__=='__main__':
	dt=DateTime.parseDate('2019-01-01')
	print(dt.toString())
	sdt=dt.addDays(-30)
	print(sdt)
	print(sdt<=dt)

	print(sdt.year)
	sdt.year=2020

	print(f'lastDayOfYear:{DateTime.lastDayOfYear()}')
	




