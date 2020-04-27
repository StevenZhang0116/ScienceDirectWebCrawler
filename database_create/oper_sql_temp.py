import pymysql as py
import info_coll as ic
import download_main as dm
import time

if __name__ == "__main__":
	time_start = time.time()

	f = open("./keywords_combination_list.csv")
	lines = f.readlines()

	db = py.connect("localhost", "root", "stevenzhang", "test")
	cursor = db.cursor();

	sql = """CREATE TABLE IF NOT EXISTS ArticleInformation (
	         t_ArticleName  VARCHAR(1024) NOT NULL,
	         t_Url  VARCHAR(512),
	         t_DOI VARCHAR(256),
	         t_PublishedDate VARCHAR(1024),
	         t_SourceTitle VARCHAR(1024),
	         t_Authors VARCHAR(1024),
	         t_Type VARCHAR(1024),
	         t_Keyword1 VARCHAR(256),
	         t_Keyword2 VARCHAR(256) )"""
	cursor.execute(sql)

	#some global variables
	total_missing = 0
	# unfinished_list = [3847,3892,3898,3905,3967,6203,6775,7574,14610,16961]


	for i in range(len(lines)):
		count = 0
		print(lines[i])

		 
		# temp: the information collection specifically to one url
		temp = ic.collect_info(lines[i])
		for k in range(len(temp)):
			thisPDF = temp[k]

			sql = """INSERT INTO ArticleInformation(t_ArticleName, t_Url, t_DOI, t_PublishedDate, t_SourceTitle, t_Authors, t_Type, t_Keyword1, t_Keyword2)
			Values("%s","%s","%s","%s","%s","%s","%s","%s","%s")""" %(thisPDF[0],thisPDF[1],thisPDF[2],thisPDF[3],thisPDF[4],thisPDF[5],thisPDF[6],thisPDF[7],thisPDF[8])

			try:
				cursor.execute(sql)
				db.commit()
				count += 1
			except:
				db.rollback()
				print(temp[k])
		total_missing += (len(temp)-count)

	time_end = time.time()

	print("finished")
	db.close()

	print(f"total missing: {total_missing}")
	print("======error_list=======")
	print(f"total working time: {time_end - time_start}")












