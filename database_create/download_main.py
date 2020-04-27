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
	ignoredNameList = ["subject index", "index", "abstract", "abstracts", "bibliography"]

	print(f'sample_url:({sample})')
	sample_specific_url = fp.all_url_find(sample,100)

	titleList, urlList, doiList, dateList, sourceTitleList, authorsList, contentTypeList, articleTypeList = [], [], [], [], [], [], [], []

	for url in sample_specific_url:
		url = url.replace("\n", "")
		print(f'======')
		print(f'parse-url:({url})')

		soup = ha.get_soup(url)

		js_items = fp.find_js_data(soup, path)

		for item in js_items:
			if not item["title"].lower() in ignoredNameList:
				try:
					theAuthorInformation = item["authors"]
					allNames = []
					for singleAuthor in theAuthorInformation:
						allNames.append(singleAuthor["name"])
					string = " & "
					authorsList.append(string.join(allNames))
				except KeyError:
					authorsList.append("CANNOT GET ACCESS")

				try:
					urlList.append("http://www.sciencedirect.com" + item["pdf"]["downloadLink"])
				except:
					urlList.append("CANNOT GET ACCESS")

				ListCollection = [titleList, doiList, dateList, sourceTitleList, contentTypeList, articleTypeList]
				IndexCollection = ["title", "doi", "publicationDate", "sourceTitle", "contentType", "articleTypeDisplayName"]

				for i in range(len(ListCollection)):
					try:
						ListCollection[i].append(item[IndexCollection[i]])
					except:
						ListCollection[i].append("CANNOT GET ACCESS")

	return titleList, urlList, doiList, dateList, sourceTitleList, authorsList, articleTypeList

# # PDF downloader
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
	for num in range(0, 10): 
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

		session_id = "e497fe9c6679c240647bed728d5e0d1f0ba8gxrqa"

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
	print(f"total pdf download: {count}")
	print(f"total time: {time_end - time_start}")




