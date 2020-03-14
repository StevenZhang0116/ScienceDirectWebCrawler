import htm_saver as ha 
import pandas as pd
# This part of code is purposed to analyze the htm file saved before, find the total count information, and save to the csv file


# Analyze the components of title and find out the total result
# create list to build corresponding relationship between the count and each keyword
def result_keyword_find(title):
	# title = ha.test_result()
	sval = title.text
	sval = sval.strip()
	pos = sval.find(" ")
	count = sval[0:pos]

	cut = []
	for i in range(len(sval)):
		if sval[i] == "\"":
			cut.append(i)

	keyword1 = sval[cut[0]+1:cut[1]]
	keyword2 = sval[cut[2]+1:cut[3]]

	return [count, keyword1, keyword2]

for line in lines[0:20]:
	title = ha.test_result(line)
	print(title)
	total_list.append(result_keyword_find(title))
	print("===")

if __name__ == "__main__":
	f = open("/Users/stevenzhang/Desktop/sciencedirect/keywords_combination_list.csv")

	# all url are store in the lines list
	lines = f.readlines()

	total_list = []
	
	# store the output into the csv file
	source = "/Users/stevenzhang/Desktop/sciencedirect/heatmap_data.xlsx"
	work = pd.read_excel(source)
	for column in work.columns:
		column = column.strip()

	work = work.set_index("index")
	work.index.name = "index_name"
	
	# since the whole process of downloading is costly of time, use try & except to eliminate the potential outliers that
	# may interrupt the program processing. Dealing with these outliers afterwards. 
	for single_value in total_list:
		try: 
			work.loc[[single_value[2]], [single_value[1]]] = single_value[0]
		except KeyError:
			print(f"Error: {single_value[2]}")

		
	work.to_csv("/Users/stevenzhang/Desktop/1.csv")
