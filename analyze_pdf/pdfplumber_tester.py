#!/usr/bin/python
#coding=UTF-8

import sys
import pdfplumber as ppl

def export_tables(pdf_path):
	print(f'export_tables:file({pdf_path})')
	with ppl.open(pdf_path) as pdf:
		pcnt=len(pdf.pages)
		print(f'pages:({pcnt})')

		table_settings={
		'horizontal_strategy':'text',
		'vertical_strategy':'text'
		}

		for pno in range(pcnt):
			page=pdf.pages[pno]
			tables=page.extract_tables(table_settings=table_settings)
			tcnt=len(tables)
			if tcnt<=0:
				continue

			print(f'\tpage({pno}):tables:({len(tables)})')

def main_routine():

	if len(sys.argv)<=1:
		print(f'usage:{sys.argv[0]} <pdf file path>')
		exit(1)

	pdf_path=sys.argv[1]
	export_tables(pdf_path)

if __name__=='__main__':
	main_routine()


