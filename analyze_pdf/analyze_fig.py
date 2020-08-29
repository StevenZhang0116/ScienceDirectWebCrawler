#!/usr/bin/python
#coding=UTF-8

#
# URL:https://blog.csdn.net/qq_15969343/article/details/81673302
#

import fitz
import os
import time
import re
import sys

def new_img_path(path,pic_path,imgcount):
	new_name=path.replace('\\','_')+f'_img_{imgcount}.png'
	new_name=new_name.replace(':','')
	new_path=os.path.join(pic_path,new_name)
	return new_path


def pdf2pic(path,pic_path):
	'''
	'''
	t0=time.perf_counter()

	checkXO=r'/Type(?= */XObject)'
	checkIM=r'/Subtype(?= */Image)'

	doc=fitz.open(path)
	imgcount=0
	total_img_cnt=0

	# help(doc)

	lenXREF=doc._getXrefLength()

	print(f'path:({path}) pages:({len(doc)}) object:({lenXREF-1})')

	for i in range(1,lenXREF):
		text=doc._getXrefString(i)
		isXObject=re.search(checkXO,text)
		isImage=re.search(checkIM,text)

		# print(f'[{i}]:text:({text})')

		if not isXObject or not isImage:
			continue

		print(f'[{i}]:--------------')
		print(f'[{i}]:text:({text})')

		total_img_cnt+=1

		pix=fitz.Pixmap(doc,i)
		print(f'[{i}]:pix:({pix})')
		print(f'[{i}]:pix.colorspace:({pix.colorspace})')

		# help(pix)

		cs=pix.colorspace

		print(f'[{i}]:cs:name({cs.name})) value({cs.n}) pix.n({pix.n})')

		if cs.n==1: # csGRAY
			print(f'[{i}]:ignore gray image.')
		elif cs.n==2: # unknown
			print(f'[{i}]:unknown colorspace.({cs})')
		elif cs.n==3: # csRGB
			imgcount+=1
			new_path=new_img_path(path,pic_path,imgcount)
			pix.writePNG(new_path)
		elif cs.n==4: # csCMYK
			imgcount+=1
			new_path=new_img_path(path,pic_path,imgcount)
			pix0=fitz.Pixmap(fitz.csRGB,pix)
			pix0.writePNG(new_path)
			pix0=None
		else:
			print(f'[{i}]:error.unknown colorspace({cs})')

		pix=None

	t1=time.perf_counter()

	print(f'found ({total_img_cnt}) images,({imgcount}) exported.')
	print(f'done.needs ({t1-t0}) secs')

def show_fitz():
	print(f'''
###
# fitz
# file:({fitz.__file__})
# doc:({fitz.__doc__})
###
CS_GRAY=({fitz.CS_GRAY})
CS_RGB=({fitz.CS_RGB})
CS_CMYK=({fitz.CS_CMYK})
		''')


def main_routine():

	show_fitz()

	if len(sys.argv)<=1:
		print(f'usage:{sys.argv[0]} <path of pdf file>')
		return -1

	path=sys.argv[1]
	print(f'pdf file:{path}')

	pdf2pic(path,'./')



if __name__=='__main__':
	main_routine()




