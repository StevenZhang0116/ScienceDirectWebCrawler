import htm_saver as ha
import find_count as fc
import find_pdf as fp 
import download_pdf as dd

import os
import time

# create the folder to store downloaded files
def folder_create(path):
	folder = os.path.exists(path)
	if not folder:
		print("New Folder")
		os.makedirs(path)
		print("Folder creates")
	else:
		print("Folder already exists")

# find the pdf urls from the website
def find_name_url(sample,path):
	print(f'sample_url:({sample})')
	sample_specific_url = fp.all_url_find(sample,100)

	name_list = []
	url_list = []

	for url in sample_specific_url:
		url = url.replace("\n", "")
		print(f'======')
		print(f'parse-url:({url})')

		soup = ha.get_soup(url)

		js_items = fp.find_js_data(soup, path)

		for item in js_items:
			article_name = item['title']
			pdf_url = item['pdf']['downloadLink']

			name_list.append(article_name)
			url_list.append(pdf_url)

	return name_list, url_list


if __name__ == "__main__":

	# test the time
	count = 0
	time_start = time.time();

	# general setting up
	f = open("./keywords_combination_list.csv")
	lines = f.readlines()
	general_path = "/Users/stevenzhang/Desktop/sciencedirect/download_pdf_folder"
	folder_create(general_path)

	# specific downloader
	for num in range(21, 30): 
		this_url = lines[num]
		this_title = ha.test_title(this_url)
		print(this_title)

		onto_keys = (fc.result_keyword_find(this_title))[0:3]

		the_folder_path = general_path + "/" + onto_keys[1] + "&" + onto_keys[2]
		folder_create(the_folder_path)

		total_result = int(onto_keys[0])

		count += total_result

		temp = find_name_url(this_url, the_folder_path)
		name_list, url_list = temp[0], temp[1]

		session_id = "6fb6db0833dfe04d9c2822c98fb2a9249877gxrqa"

		print(onto_keys)
		
		for i in range(total_result):
			pdf_name = name_list[i]
			pdf_url = url_list[i]

			print(f"PDF NAME: {pdf_name}")
			pdf_url = "http://www.sciencedirect.com" + pdf_url
			print(f"PDF URL: {pdf_url}")

			if pdf_url != "":
				dl = dd.PdfDownloader(session_id, save_folder= the_folder_path+"/"+pdf_name,do_debug=True) # OK
				ret = dl.download(pdf_url)

	time_end = time.time()
	print("####################")
	print("####################")
	print("####################")
	print("####################")
	print("####################")
	print("####################")
	print("####################")
	print("####################")
	print(f"total pdf download: {count}")
	print(f"total time: {time_end - time_start}")




