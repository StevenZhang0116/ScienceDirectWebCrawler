# Use Python to investigate the ScienceDirect database

This folder of codes is crafted by Zihan Zhang for his lab internship at [McDevitt Research Group](https://dental.nyu.edu/faculty/biomaterials/mcdevitt-research-group.html), NYU College of Dentistry. 
The purpose is to get access to information from [ScienceDirect](https://www.sciencedirect.com/) database in using a web crawler. The codes are primary python-based and a few Matlab and SQL involved. 

The heatmap_create section is used to generate a visual presentation of the total found results of different keywords combinations. 
The download_pdf section is used to download all pdfs relevant to this keyword combinations and store them into different folders. 
The database_create section is used to extract important information related to each article, including related keywords, DOI, authors, published date, etc., and store them into the MySQL database. 

Notice that the codes in each folder are more or less similar to each other. That is for readers' convenience to treat them as separate projects for future reference. 

I also post the interim presentation of the data extraction team to better my program's role, functionalities, and effects for the entire project. The final well-organized program can be found at [here](https://github.com/StevenZhang0116/crawler_release). 
