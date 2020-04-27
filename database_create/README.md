#MySQL database create

The find_name_url function in download_main.py file is used to extract information from the downloaded script_data-well-format.json file (prepared in download_pdf section) and store them into different list (by url). 

I eliminate some articles with meaningless name (line 21) to clean the data. 

The oper_sql_temp.py file is used to connect the local MySQL database and execute SQL language to add each elements from the lists into the table. Line 12 should be manually revised by users themselves. The second and third parameter is the user account and password that you are connect to and the fourth parameter is the name of created database. 

I execute db.commit() (line 47) after adding each data to improve the security but decrease the working efficiency. 


