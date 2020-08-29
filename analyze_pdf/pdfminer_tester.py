#!/usr/bin/python
#coding=UTF-8

#
# URL:https://www.jb51.net/article/170798.htm
# needs:
# pip install pdfminer3k
#
# URL:http://www.elecfans.com/d/826517.html
# 模块自带命令行工具，很酷
# pdf2txt.py 1.pdf 
# 上面的命令行居然可以直接执行，如何寻找的呢？
#
# URL:https://www.cnblogs.com/jamespei/p/5339769.html
# 这个文档描述了如何分析LTFigure对象。
#


import sys
import json
import os

import matplotlib.pyplot as plt

from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfdevice import TagExtractor
from pdfminer.converter import PDFPageAggregator

# from pdfminer.converter import PDFPageAggregator,XMLConverter,HTMLConverter,TextConverter
from pdfminer.layout import *

# from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.image import ImageWriter

from binascii import b2a_hex

class pdf_file_parser:
	'''
	'''
	def __init__(self):
		'''
		'''
		self.objs=[]
		self.obj_counter=0
		self.pdf_path=None

	def parse_pdf(self,pdf_path):
		'''
		'''
		self.pdf_path=pdf_path
		fp=open(pdf_path,'rb')
		parser=PDFParser(fp)

		doc=PDFDocument(parser)

		if not doc.is_extractable:
			print(f'[error]:pdf not allowed extract.')
			return False

		mgr=PDFResourceManager()
		laparams=LAParams()

		device=PDFPageAggregator(mgr,laparams=laparams)
		interpreter=PDFPageInterpreter(mgr,device)

		pages=PDFPage.create_pages(doc)

		# print(f'pages:({pages})')

		pnum=0
		for page in pages:
			pnum+=1
			interpreter.process_page(page)
			layout=device.get_result()

			(l,t,w,h)=self.calc_bbox(layout.bbox)

			xobj={
				'pagenum':pnum,
				'xtype':self.get_type(layout),
				'bbox':{
					'left':l,
					'top':t,
					'width':w,
					'height':h
				},
				'uniqueid':f'{self.incr_obj_counter()}',
				'desc':f'{layout}',
				'children':[]
			}

			self.parse_lt_objs(layout,xobj)
			self.objs.append(xobj)


		# print(f'pdf summary:')
		# print(f'{self.objs}')

		self.save2json(self.objs)

		print('=== done.===')

	def calc_bbox(self,bbox):
		(x0,y0,x1,y1)=bbox
		width=x1-x0
		height=y1-y0
		return (x0,y0,width,height)

	def save2json(self,objs):
		[folder,fname]=os.path.split(self.pdf_path)
		print(f'folder({folder}) fname({fname})')
		ss=json.dumps(objs,indent=4)
		with open(f'./pdfm-{fname}.json','w') as fp:
			fp.write(ss)

	def incr_obj_counter(self):
		ret=self.obj_counter
		self.obj_counter+=1
		return ret

	def parse_lt_objs(self,lt_objs,xobj):
		'''
		'''
		for x in lt_objs:
			ctype=self.get_type(x)
			(l,t,w,h)=self.calc_bbox(x.bbox)
			cobj={
				'xtype':ctype,
				'bbox':{
					'left':l,
					'top':t,
					'width':w,
					'height':h
				},
				'uniqueid':f'{self.incr_obj_counter()}',
				'desc':f'{x}'
			}

			if isinstance(x,LTFigure):
				cobj['children']=[]
				self.parse_lt_objs(x,cobj)

			xobj['children'].append(cobj)

		return

	def get_type(self,x):
		cls=type(x)
		# sval=f'{type(x)}'
		sval=cls.__name__
		pos=sval.rfind('.')
		if pos>=0:
			sval=sval[pos+1:]
		return sval


	def save_image(self,lt_image):
		'''
		'''
		ret=False

		print(f'[save_image]:lt_image({lt_image})')

		if lt_image.stream:
			file_stream=lt_image.stream.get_rawdata()
			if file_stream:
				file_ext=self.determine_image_type(file_stream[0:4])
				if file_ext:
					file_name=f'pdfminer_{self.num_page}-{lt_image.name}{file_ext}'
					ret=self.write_file(file_name,file_stream,flags='wb')
				else:
					print(f'[save_image][error]:no file ext.')
			else:
				print(f'[save_image][error]:no raw data.')

		else:
			print(f'[save_image][error]:no image stream.')

		
		print(f'[save_image]:done.ret({ret}).')

		return ret

	def determine_image_type(self,stream_first_4_bytes):
		'''
		'''
		file_type=None

		bytes_as_hex=b2a_hex(stream_first_4_bytes)
		bytes_as_hex=bytes_as_hex.decode()

		# print(f'bytes_as_hex:({type(bytes_as_hex)})({bytes_as_hex})')
		if bytes_as_hex.startswith('ffd8'):
			file_type='.jpeg'
		elif bytes_as_hex=='89504e47':
			file_type='.png'
		elif bytes_as_hex=='47494638':
			file_type='.gif'
		elif bytes_as_hex.startswith('424d'):
			file_type='.bmp'
		else:
			print(f'[error]:can not determine image type({bytes_as_hex})')
			file_type='.png'

		return file_type

	def write_file(self,filename,filedata,flags='w'):
		'''
		'''
		ret=True
		file_path=f'./dump_imgs/{filename}'
		try:
			fp=open(file_path,flags)
			fp.write(filedata)
			fp.close()
		except Exception as ex:
			print(f'[exception][write_file]:filename({filename}) ({ex})')
			ret=False

		return ret

	def draw_page(self,pageno):
		page=self.objs[pageno]
		fig=plt.figure()
		ax=fig.add_subplot(111)
		ax.set_xlim(0,800)
		ax.set_ylim(0,800)
		self.color_list=['r','g','b','y']
		self.draw_obj(ax,page)
		plt.show()

	def draw_obj(self,ax,obj):

		# xtype=obj['xtype']
		# if xtype=='LTLine':
		# 	return

		chs=obj.get('children')
		if chs is not None:
			for cobj in chs:
				self.draw_obj(ax,cobj)
			return

		color=self.color_list.pop(0)
		self.color_list.append(color)

		bbox=obj['bbox']
		# print(f'[draw_obj]:bbox({bbox}) color({color})')

		rect=plt.Rectangle((bbox['left'],bbox['top']),
			bbox['width'],bbox['height'],color=color)

		# rect=plt.Rectangle((0.1,0.1),0.5,0.3,color=color)
		ax.add_patch(rect)


if __name__=='__main__':

	if len(sys.argv)<=1:
		print(f'usage:{sys.argv[0]} <pdf file path>')
		exit(1)

	fpath=sys.argv[1]

	pno=-1
	if len(sys.argv)>=3:
		pno=sys.argv[2]
		pno=int(pno)

	pobj=pdf_file_parser()	
	pobj.parse_pdf(fpath)

	if pno>=0:
		pobj.draw_page(pno)









