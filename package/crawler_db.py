#!/usr/bin/python
#coding=UTF-8

import os
import traceback
from .date_time import *
from .app_config import *

_cfg=AppConfig()

if _cfg.dbType=='mysql':
    # print(f"_cfg.dbTyp:{_cfg.dbType}")
    from .db_handler_mysql import *
else:
    from .db_handler import *

__all__=['CrawlerDB','UniqueIdMaker']

'''
'''
global_tables={
    'dl_keys':f'''
        create table if not exists dl_keys (
            t_recid varchar(64),
            t_taskid varchar(64),
            kw1 varchar(128),
            kw2 varchar(128),
            crdt varchar(32),
            mddt varchar(32)
            )
    ''',
    'dl_tasks':'''
        create table if not exists dl_tasks (
            t_recid varchar(64),
            t_taskid varchar(64),
            t_url varchar(1024),
            t_state int default 0,
            t_keyid varchar(64),
            crdt varchar(32),
            mddt varchar(32)
            )
    ''',
    'dl_pdf_tasks':'''
        create table if not exists dl_pdf_tasks (
            t_recid varchar(64),
            t_name varchar(1024),
            t_url varchar(1024),
            t_state int default 0,
            t_taskid varchar(64),
            t_ref_recid varchar(64),
            crdt varchar(32),
            mddt varchar(32)
            )
    ''',
    'dl_pdf_files':f'''
        create table if not exists dl_pdf_files (
            t_recid varchar(64),
            t_taskid varchar(64),
            crdt varchar(32),
            mddt varchar(32),
            t_data {_cfg.type_blob}
            )
    ''',
    'dl_pdf_info':f'''
        create table if not exists dl_pdf_info (
            t_recid varchar(64),
            t_taskid varchar(64),
            contentType varchar(8),
            documentSubType varchar(8),
            doi varchar(64),
            publicationDate varchar(16),
            sourceTitle varchar(256),
            title varchar(1024),
            articleType varchar(8),
            issn varchar(64),
            isbn varchar(64)
            )
    ''',
    'dl_pdf_authors':f'''
        create table if not exists dl_pdf_authors (
            t_recid varchar(64),
            t_taskid varchar(64),
            t_order int,
            t_name varchar(1024)
            )
    '''


}

global_tables_checked=False


#---------------
#
#---------------
class CrawlerDB:

	#-------------
	#
	#-------------
    def __init__(self,code='crawler'):
        self.code=code
        self.dbtype=_cfg.dbType

    #-------------
    #
    #-------------
    def get_db_file(self,scode):
        folder=os.path.dirname(__file__)
        fpath=f'{folder}/db/{scode}.db'
        folder=os.path.dirname(fpath)
        if not os.path.exists(folder):
            os.makedirs(folder)
        return fpath

    #------------
    #
    #------------
    def init_db(self):

        global global_tables_checked

        db=None
        if self.dbtype=='mysql':
            db=DBHandler({
                'host':'localhost',
                'user':'root',
                'passwd':'stevenzhang',
                'db':'test'
                })
        else:
            filepath=self.get_db_file(self.code)
            db=DBHandler({'filepath':filepath})

        # print(f'[global_tables_checked]=({global_tables_checked})')

        if not global_tables_checked:
            ret=self.prepare_tables(db)
            if ret==False:
                db=None
            else:
                global_tables_checked=True

        return db            

    def prepare_tables(self,db):
        '''
        '''
        global global_tables

        ret=True
        tables=global_tables

        try:
            db.open()
            for name,sql in tables.items():
                db.execute(sql)
            db.close()
            ret=True
        except Exception as ex:
            print(f'[CrawlerDB][init_db][exception]:{ex}')
            traceback.print_exc()
            db.close()
            ret=False

        return ret

    #------------
    #
    #------------
    def getHandle(self):
        '''
        '''
        ret=None
        ret=self.init_db()
        return ret


class UniqueIdMaker:
    '''
    '''
    def __init__(self):
        '''
        '''
        self.key_base=DateTime.now().getTicks()
        self.rec_counter=0

    def create(self):
        '''
        '''
        rec_id=self.rec_counter
        self.rec_counter+=1
        rec_id=f'{self.key_base:016d}-{rec_id:08d}'
        return rec_id





