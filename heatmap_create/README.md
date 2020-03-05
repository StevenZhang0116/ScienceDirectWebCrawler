Create Heatmap Section
====

This section of code is purposed to create heatmap based on the given keywords (different diseases and biomarkers). 

We first create URL corresponding to different keywords combinations and then get access to the "total result" information, 
which is stored in the TITLE section of the htm. Using the BeautifulSoup package, we could analyze the htm contents efficiently and directly. 

The heatmap drawing is achieved by using Matlab. The code is rather trivial and not included in the folder. 

The keywords.csv stores the original keywords. The keywords_combination_list.csv stores all generated URLs respective to different keywords combinations. The output_data.xlsx stores the final output data (about how many times each keyword combination appears in the ScienceDirect database). 

The keywords_comb.py translates each keyword combination into the particular URL in ScienceDirect form. The htm_saver.py gets access to all contents in that URL and stores its title information (<title>). The find_count.py consequentially analyzes the title and extract the "Total Result" information and stores the data in output_data.xlsx. 
 
The screenshots of the heatmap are stored in the heatmap_photos folder. 
