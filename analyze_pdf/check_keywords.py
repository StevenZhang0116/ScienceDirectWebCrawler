import json
import os
import sys
import pymysql as py
import pandas as pd
import time


path = "./demo_1/jsons/"
jsons = os.listdir(path)

keywords = []
with open("./demo_1/keywords.txt") as f:
	for line in f:
		keywords.append(list(line.strip("\n").split(",")))

included = []

print(len(jsons))

for i in range(0, len(jsons)):
	# print(path + jsons[i])

	with open(path + jsons[i], "r") as load_f:
		load_dict = json.load(load_f)
		temp = ""
		for k in load_dict["Pages"]:
			temp += str(k.values())

		for theKey in keywords:
			if theKey[0] in temp:
				included.append(jsons[i][0:-5])
				break

print(len(included))

db = py.connect("localhost", "root", "stevenzhang", "test")
df = pd.DataFrame(columns = ['t_ArticleName', 't_Url', 't_DOI', 't_PublishedDate', 't_SourceTitle', 't_Authors', 't_Type', 't_Keyword1', 't_Keyword2', 't_ID'])

for i in range(len(included)):
	sqlcmd = "select * from allData2 where t_Url like '%" + included[i] + "%'"
	theData = pd.read_sql(sqlcmd, db)
	df.loc[i] = theData.values.tolist()[0]
	print(i)

df.to_csv("./demo_1/demo1.csv")










