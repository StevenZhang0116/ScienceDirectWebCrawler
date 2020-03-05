Create Heatmap Section
====

This section of code is purposed to create heatmap based on the given keywords (different diseases and biomarkers). 

We first create URL corresponding to different keywords combinations and then get access to the "total result" information, 
which is stored in the TITLE section of the htm. Using the BeautifulSoup package, we could analyze the htm contents efficiently and directly. 

The heatmap drawing is achieved by using Matlab. The code is rather trivial and not included in the folder. 

The main code is find_count.py. The input file is keywords.csv. The output file (heatmap data) is keywords_combination_list.csv. The screenshots of the heatmap are stored in the heatmap_photos folder. 
