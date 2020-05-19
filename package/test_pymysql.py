#!/usr/bin/python
#coding=UTF-8

import pymysql

host='localhost'
userid='admin'
passwd='interact'
cur_db='testdb'

conn=pymysql.connect(host=host,
	user=userid,passwd=passwd,db=cur_db,autocommit=False)


cur=conn.cursor()

sql='''
create table if not exists t_sales(
	t_id int primary key auto_increment not null,
	t_name varchar(32),
	t_desc text,
	t_age int
	)
'''

ret=cur.execute(sql)

print(f'create result({ret})')

conn.begin()

sql='''
insert into t_sales (t_name,t_desc,t_age)
values(%s,%s,%s)
'''

ret=cur.execute(sql,('zzh','a good teacher!3',48))

print(f'insert result({ret})')

# conn.commit()
conn.rollback()

cur.close()

conn.close()


