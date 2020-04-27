import htm_saver as ha
import find_count as fc
import find_pdf as fp 
import download_pdf as dd
import download_main as dm

import os
import time
import pandas as pd

def collect_info(theLine):
	generalPath = "/Users/stevenzhang/Desktop/sciencedirect/download_pdf_folder"
	dm.folder_create(generalPath)

	thisTitle = ha.test_title(theLine)

	print(thisTitle)

	ontoKeys = (fc.result_keyword_find(thisTitle))[0:3]

	theFolderPath = generalPath + "/" + ontoKeys[1] + "&" + ontoKeys[2]
	dm.folder_create(theFolderPath)

	# total_result = int(ontoKeys[0])

		
	#titleList, urlList, doiList, dateList, sourceTitleList, authorsList, articleTypeList
	temp = dm.find_name_url(theLine, theFolderPath)

	#Information collection for all articles related to that keyword search
	allInformation = []

	for i in range(len(temp[0])):
		singleInformation = []
		for t in range(len(temp)):
			singleInformation.append(temp[t][i])
		singleInformation.append(ontoKeys[1])
		singleInformation.append(ontoKeys[2])
		allInformation.append(singleInformation)

	return allInformation


	







