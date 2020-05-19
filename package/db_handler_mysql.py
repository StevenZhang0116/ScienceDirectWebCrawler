#!/usr/bin/python
#coding=UTF-8

import pymysql as dbapi
import pandas as pd
import traceback

import warnings
warnings.filterwarnings('ignore')

__all__=['DBHandler','DataReader']


class DataReader:
	'''
	'''
	def __init__(self,res):
		'''
		'''
		self.res=res
		self.columns=None
		self.col_index=None
		self.cur_row=None

	def build(self):
		'''
		'''
		ret=True
		res=self.res

		cols=[]
		cidx={}
		index=0

		for col in res.description:
			cname=col[0].upper()
			cols.append(cname)
			cidx[cname]=index
			index+=1

		self.columns=cols
		self.col_index=cidx

		return ret

	def __getitem__(self,index):
		'''
		'''
		ret=None
		if isinstance(index,int):
			ret=self.get_with_index(index)
		else:
			ret=self.get_with_name(index)

		return ret

	def get_with_index(self,index):
		'''
		'''
		ret=None

		row=self.cur_row
		if row is not None:
			if index>=0 and index<len(row):
				ret=row[index]

		return ret

	def get_with_name(self,name):
		'''
		'''
		ret=None
		name=name.upper()
		index=self.col_index[name]
		ret=self.get_with_index(index)

		return ret


	def read(self):
		'''
		'''
		ret=True
		res=self.res
		row=res.fetchone()

		if (row is None) or (len(row)<=0):
			ret=False
			self.cur_row=None
		else:
			ret=True
			self.cur_row=row

		return ret

	def close(self):
		'''
		do nothing.
		'''
		pass



class DBHandler:

	class ConnParams:
		def __init__(self,pas):
			self.host=pas.get('host','localhost')
			self.user=pas.get('user')
			self.passwd=pas.get('passwd')
			self.db=pas.get('db')
			self.autocommit=False
			self.error=None

		def valid(self):
			'''
			'''
			ret=True

			if self.user is None:
				self.error=f'no user.'
				ret=False

			if ret and self.db is None:
				self.error=f'no db.'

			if ret and self.passwd is None:
				self.error=f'no passwd.'

			return ret

	#-----------
	#
	#-----------
	def __init__(self,conn_params={}):
		'''
		'''
		self.conn=None
		self.cur=None

		pas=DBHandler.ConnParams(conn_params)

		if pas.valid():
			self.pas=pas
		else:
			msg=f'wrong params:{pas.error}.'
			print(f'[DBHandler][init][error]:{msg}.')
			raise Exception(msg)

	#--------------
	#
	#--------------
	def open(self):
		
		ret=True

		if self.conn is None:
			try:
				pas=self.pas
				self.conn=dbapi.connect(
					host=pas.host,
					user=pas.user,
					passwd=pas.passwd,
					db=pas.db,
					autocommit=pas.autocommit)
				
				self.cur=self.conn.cursor()

			except Exception as ex:
				# print(f'[open]:{ex} filepath:({self.filepath})')
				traceback.print_exc()
				raise ex
				ret=False

		return ret

	#--------------
	#
	#--------------
	def close(self):

		try:
			if self.cur is not None:
				self.cur=None

			if self.conn is not None:
				self.conn.close()
				self.conn=None
		except:
			self.cur=None
			self.conn=None


	#--------------
	#
	#--------------
	def begin(self):

		ret=False

		if self.conn is None:
			print(f'[begin]:no db connection.')
			return ret

		try:
			self.conn.begin()
			ret=True
		except Exception as ex:
			print(f'[begin]:{ex}')
			raise ex
			ret=False

		return ret

	#--------------
	#
	#--------------
	def commit(self):
		ret=False

		# print('commit.')

		if self.conn is None:
			print(f'[commit]:no db connection.')
			return ret

		try:
			self.conn.commit()
			ret=True
		except Exception as ex:
			print(f'[commit]:{ex}')
			raise ex
			ret=False
		
		return ret

	#--------------
	#
	#--------------
	def rollback(self):

		ret=False

		# print('rollback.')

		if self.conn is None:
			print(f'[rollback]:no db connection.')
			return ret

		try:
			self.conn.rollback()
			ret=True
		except Exception as ex:
			print(f'[rollback]:{ex}')
			ret=False

		return ret

	#----------
	#
	#----------
	def save(self,table_name,data,build_table=False,if_exists='append'):

		# print('save.')

		ret=-1

		if self.conn is None:
			print(f'[save]:no db connection.')
			return ret

		if build_table:
			drop=f'drop table if exists {table_name}'
			df=data.infer_objects()
			dts=df.dtypes
			flds=[]
			for k,v in dts.iteritems():
				dt='TEXT'
				if v==int:
					dt='INTEGER'
				elif v==float:
					dt='FLOAT'
				else:
					dt='TEXT'
				fld=f'{k} {dt}'
				flds.append(fld)

			sfld=','.join(flds)
			create=f'create table {table_name} ({sfld})'

			try:
				self.cur.execute(drop)
				self.cur.execute(create)
			except Exception as ex:
				print(f'[save]:{ex}')
				print(f'[save]:create[{create}]')
				print(f'[save]:drop[{drop}]')
				raise ex
				ret=-1

		try:
			cols=data.columns.values
			flds=','.join(cols)
			vals=','.join('?'*len(cols))

			sql=f'insert into {table_name} ({flds}) values({vals})'

			ret=0

			for index,row in data.iterrows():
				va=row.values
				res=self.cur.execute(sql,va)
				ret+=1

		except Exception as ex:
			print(f'[save]:{ex}')
			raise ex
			ret=-1

		return ret

	#--------------
	#
	#--------------
	def turn_array(self,args):
		ret=None
		if args and len(args)==1:
			if type(args[0]) is list:
				ret=args[0]
			elif type(args[0]) is tuple:
				ret=args[0]
			else:
				ret=None

		if ret is None:
			ret=list(args)
			
		return ret

	#--------------
	#
	#--------------
	def execute(self,sql,*args):

		ret=-1

		if self.conn is None:
			print(f'[execute]:no db connection.')
			return ret
		
		if args is not None:
			args=self.turn_array(args)
			sql=self.normalize_sql(sql)

		try:		
			ret=self.cur.execute(sql,args)
		except Exception as ex:
			print(f'[execute]:{ex}')
			traceback.print_exc()
			raise ex
			ret=-1

		return ret

	def executeReader(self,sql,*args):
		'''
		'''
		ret=None

		if self.conn is None:
			print(f'[executeReader]:no db connection.')
			return ret

		if args is not None:
			args=self.turn_array(args)
			sql=self.normalize_sql(sql)

		try:		
			if args is None:
				self.cur.execute(sql)
			else:
				self.cur.execute(sql,args)

			res=self.cur
			ret=DataReader(res)
			ret.build()

		except Exception as ex:
			print(f'[executeQuery][exception]:{ex}')
			print(f'[executeQuery][exception]:sql[{sql}]')
			raise ex
			ret=None

		return ret

	#---
	#
	#---
	def normalize_sql(self,sql):
		'''
		'''
		ret=sql.replace('?','%s')
		return ret

	#----------------
	#
	#----------------
	def executeQuery(self,sql,*args):

		ret=None

		if self.conn is None:
			print(f'[executeQuery]:no db connection.')
			return ret

		# print(f'[executeQuery]:args({args}) type({type(args)})')
		
		if args is not None:
			args=self.turn_array(args)
			sql=self.normalize_sql(sql)

		# print(f'[executeQuery]-1:args({args}) type({type(args)})')

		try:		
			if args is None:
				res=self.cur.execute(sql)
			else:
				res=self.cur.execute(sql,args)

			res=self.cur
			fet=res.fetchall()

			cols=[]
			for col in res.description:
				cols.append(col[0])

			df=pd.DataFrame(fet,columns=cols)

			ret=df

		except Exception as ex:
			print(f'[executeQuery][exception]:{ex}')
			print(f'[executeQuery][exception]:sql[{sql}]')
			raise ex
			ret=None

		return ret

	#----------------
	#
	#----------------
	def executeScalar(self,sql,*args):

		ret=None

		if self.conn is None:
			print(f'[executeScalar]:no db connection.')
			return ret

		if args is not None:
			args=self.turn_array(args)

		try:		
			if args is None:
				res=self.cur.execute(sql)
			else:
				res=self.cur.execute(sql,args)

			res=self.cur.fetchone()
			if res is not None and len(res)>0:
				ret=res[0]
			
		except Exception as ex:
			print(f'[executeScalar]:{ex}')
			raise ex
			ret=None

		return ret


	#--------------
	#
	#--------------
	def update(self,table_name,value_dict):
		pass

	#--------------
	#
	#--------------
	def insert(self,table_name,value_dict):

		if isinstance(value_dict,pd.Series):
			value_dict=value_dict.to_dict()

		ret=-1

		if self.conn is None:
			print(f'[insert]:no db connection.')
			return ret
		
		flds=','.join(value_dict.keys())
		vals=','.join(['%s' for _ in range(len(value_dict))])

		va=value_dict.values()
		va=list(va)

		sql=f'insert into {table_name} ({flds}) values({vals})'

		try:
			ret=self.cur.execute(sql,va)
		except Exception as ex:
			print(f'[insert]:{ex}')
			raise ex
			ret=-1

		return ret


