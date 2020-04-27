import htm_saver as ha 
import pandas as pd 
import numpy as np 
import re
import requests

import htm_saver as ha
import find_count as fc

import json


def find_result_items(soup):

	ret=[]

	body=soup
	items=body.select('li.ResultItem')

	print(f'[find_result_items]:items-count({len(items)})')

	for item in items:

		title=item.select('a.result-list-title-link')
		if len(title)<=0:
			title=''
		else:
			title=title[0].get_text()
		# print(f'[find_result_items]:\ttitle({title})')

		href=''
		child=item.select('li.DownloadPdf')
		if len(child)>0:
			child=child[0].select('a')
			if len(child)>0:
				href=child[0].get('href')
		# print(f'[find_result_items]:\thref({href})')

		ret.append({
			'title':title,
			'pdf_url':href
			})

	sval=json.dumps(ret,indent=3)
	with open('./result_items.json','w') as fp:
		fp.write(sval)

	return ret

# store the data to htm and json; improve efficiency of accessing to the information
def find_js_data(soup, path):
	
	ret=[]
	body=soup

	pattern=re.compile(r'var INITIAL_STATE = (.*?)',re.MULTILINE|re.DOTALL)
	script=body.find('script',text=pattern)

	data=''
	if script is not None:
		data=script.text
		data=data.replace('var INITIAL_STATE = ','')
		data=data.replace(':undefined',':""')
		# data=data.replace(':null',':""')

	# print(f'script:({data})')
	if data=='':
		print(f'[FATAL]:not found script-data.')
		with open(path + '/script_data.htm','w') as fp:
			fp.write(f'{body}')
	else:

		with open(path + '/script_data.htm','w') as fp:
			fp.write(f'{body}')

		with open(path + '/script_data.json','w') as fp:
			fp.write(data)

		jobj=json.loads(data)
		# print(f'script:load ok.')
		srs=jobj['search']['searchResults']
		# print(f'srs:({srs})')
		ret=srs

		sval=json.dumps(jobj,indent=3)
		with open(path + '/script_data-well-format.json','w') as fp:
			fp.write(sval)

	return ret

# page turning
def all_url_find(basic_url,num_of_page=100):
	all_url_coll = []
	title = ha.test_title(basic_url)
	count = fc.result_keyword_find(title)[0]
	print(f"result count:({count})")

	temp = re.findall(r"\d+\.?d*",count)
	count = ""
	for i in temp:
		count += i
		
	remainder = int(count) // num_of_page
	for i in range(remainder+1):
		new_url=f'{basic_url}&show={num_of_page}&offset={str(i*num_of_page)}'
		# all_url_coll.append(basic_url+"&offset="+str(i*num_of_page))
		all_url_coll.append(new_url)
	return all_url_coll


def show100(url_lst):
	new_lines = []
	for line in url_lst:
		line += "&show=100"
		line = line.replace("\n", "")
		new_lines.append(line)
	return new_lines


if __name__ == "__main__":
	# test code

	f = open("./keywords_combination_list.csv")
	lines = f.readlines()
	newurl_lst = show100(lines)

	sample = newurl_lst[1000]
	sample='https://www.sciencedirect.com/search/advanced?qs=%20"Abdominal%20injury"%20AND%20"Biochemical"'


	print(f'sample_url:({sample})')

	sample_specific_url = all_url_find(sample,100)

	print(f'sample_specific_url:({len(sample_specific_url)})')
	for url in sample_specific_url:
		print(f'\t({url})')

	req_num=0

	for url in sample_specific_url:

		print(f'=== req:{req_num} ===')
		print(f'parse-url:({url})')
		
		page_body=ha.test_body(url)
		soup=ha.get_soup(url)
		page_body=soup.body

		# raw_name = find_rawname(page_body)
		# raw_pdf = find_pdf(page_body)

		# polished_name = generate_polished_name(raw_name)
		# polished_pdf = generate_polished_pdf(raw_name,raw_pdf)

		# print(f'len(raw_name):({len(raw_name)})')
		# print(f'len(raw_pdf):({len(raw_pdf)})')

		# print(f"len(polished_pdf):({len(polished_pdf)})")
		# print(polished_pdf)
		# print(f"len(polished_name):({len(polished_name)})")
		# print(polished_name)

		results=find_result_items(soup)

		tcnt=0
		ucnt=0
		for rit in results:
			if rit['title']!='':
				tcnt+=1
			if rit['pdf_url']!='':
				ucnt+=1

		print(f'len(result_items):({len(results)}) titles({tcnt}) pdf_urls({ucnt})')

		tcnt=0
		ucnt=0
		ocnt=0
		js_items=find_js_data(soup)
		for item in js_items:
			openAccess=item["openAccess"]
			if openAccess==True:
				ocnt+=1
			else:
				# dt_list=['idx','ind','abs','prp']
				dt_list=['idx','ind','abs']
				doctype=item['documentSubType']
				if doctype in dt_list:
					ocnt+=1
			
			pdf_url=item['pdf']['downloadLink']
			if pdf_url!='':
				ucnt+=1

			tcnt+=1

		print(f'len(js_items):({len(js_items)}) titles({tcnt}) pdf_urls({ucnt}) access({ocnt})')



		# exception consideration
		# print(js_items)
		
		if len(results)<len(js_items):
			print(f'found result_items NOT matched js_items,comparing.')
			dcnt=0
			for item in js_items:
				title=item['title']
				for res in results:
					if res['title']==title:
						title=None
						break
				if title is not None:
					dcnt+=1
					print(f'dismiss:({title})')

			line=input(f'found dismiss({dcnt}),continue(y/n)?')
			if line=='n':
				print(f'aborted!!!')
				break

		print(f"=== req fininshed. ===")

		req_num+=1


























