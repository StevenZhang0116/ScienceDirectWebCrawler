# MySQL database create

The find_name_url function in download_main.py file is used to extract information from the downloaded script_data-well-format.json file (prepared in download_pdf section) and store them into the different list (by URL). If the information is unknown or cannot get accessed to, we will just fill in "CANNNOT GET ACCESS" as a remainder. 

I eliminate some articles with meaningless names (line 21), like "subject index", "index", "abstract" to clean the data. These articles are apparently not relevant to our research. 

The oper_sql_temp.py file is used to connect the local MySQL database and execute SQL language to add each element from the lists into the table. Line 12 should be manually revised by users themselves. The second and third parameter is the user account and password that you are connected to and the fourth parameter is the name of the created database. 

I execute db.commit() (line 47) after adding each data to improve the security but decrease the working efficiency. 

The sql.txt file contains the SQL codes to check if there are duplicated data in the table. I cherish it as a good habit to create a database with well-cleaned data. Each code will take several minutes for average and should be executed consecutively and separately. 

You may find the sample db file I created in https://drive.google.com/open?id=1rhSR3rol-j7cQZzY9caSCnJY5vf2PjOn with approximately 8 millions data and 3GB large. 

You may find more information about transforming MySQL to SqLite3 in https://github.com/dumblob/mysql2sqlite. The basic idea is exporting the sql file and use MySQLWorkBench to accomplish the transformation. 


