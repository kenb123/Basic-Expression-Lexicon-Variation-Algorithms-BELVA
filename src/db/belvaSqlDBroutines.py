#!/usr/bin/python3
# -*- coding: utf-8 -*-

#--------------------------------------------------------------------------------------------------
#    pyOwaspBELVA - Contextual custom dictionary builder with character and word variations for pen-testers 
#    Copyright (C) 2016  OWASP Foundation / Kenneth F. Belva
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
# This project is named after my amazing father: 
#            Albert Joseph BELVA
#
# And, it is dedicated to him and his memory.
#
# This dedication and project is to raise awareness for 
# Lewy Body Disease / Dementia which my father lived with 
# since his mid-60s until his passing at 72.
#
# More information on Lewy Body Dementia may be found here:
# https://en.wikipedia.org/wiki/Dementia_with_Lewy_bodies
#
# Please add this dedication to every file in the project. 
# Thank you much. -Ken
#--------------------------------------------------------------------------------------------------


import sys
import os
import json
#import urlparse
#import urllib
import base64
import sqlite3

from src.db.belvaDbRoutines import nonread_sqlite as change_db
from src.db.belvaDbRoutines import nonread_sqlite_parameterized as change_db_parameterized

from src.db.belvaDbRoutines import read_sqlite



#====================================================================================
#        
#====================================================================================


#------------------------------------------------------------------------------------
def write_text_words(word, MD5_string):
#------------------------------------------------------------------------------------
    
    sqlString =  "INSERT INTO text_words (unique_text_words) VALUES ('" + word.lower() + "')"
    change_db(sqlString, MD5_string)


#------------------------------------------------------------------------------------
def count_text_words(MD5_string):
#------------------------------------------------------------------------------------
    

    sqlString = "SELECT Count(*) FROM text_words"
    sql_results = read_sqlite(sqlString, MD5_string)
    return str(sql_results).replace("(", "").replace("[", "").replace(",", "").replace("]", "").replace(")", "")


#------------------------------------------------------------------------------------
def get_all_text_words(MD5_string):
#------------------------------------------------------------------------------------
    
    sqlString = "SELECT unique_text_words FROM text_words"
    sql_results = read_sqlite(sqlString, MD5_string)
    return sql_results





#------------------------------------------------------------------------------------
def write_burp_words(word, MD5_string):
#------------------------------------------------------------------------------------
    
    sqlString =  "INSERT INTO burp_import (unique_burp_import) VALUES ('" + word.lower() + "')"
    change_db(sqlString, MD5_string)


#------------------------------------------------------------------------------------
def count_burp_words(MD5_string):
#------------------------------------------------------------------------------------
    
    sqlString = "SELECT Count(*) FROM burp_import"
    sql_results = read_sqlite(sqlString, MD5_string)
    return str(sql_results).replace("(", "").replace("[", "").replace(",", "").replace("]", "").replace(")", "")

#------------------------------------------------------------------------------------
def get_all_burp_words(MD5_string):
#------------------------------------------------------------------------------------
    
    sqlString = "SELECT unique_burp_import FROM burp_import"
    sql_results = read_sqlite(sqlString, MD5_string)
    return sql_results



#------------------------------------------------------------------------------------
def write_zap_words(word, MD5_string):
#------------------------------------------------------------------------------------
    
    sqlString =  "INSERT INTO zap_import (unique_zap_import) VALUES ('" + word.lower() + "')"
    change_db(sqlString, MD5_string)


#------------------------------------------------------------------------------------
def count_zap_words(MD5_string):
#------------------------------------------------------------------------------------
    
    sqlString = "SELECT Count(*) FROM zap_import"
    sql_results = read_sqlite(sqlString, MD5_string)
    return str(sql_results).replace("(", "").replace("[", "").replace(",", "").replace("]", "").replace(")", "")


#------------------------------------------------------------------------------------
def get_all_zap_words(MD5_string):
#------------------------------------------------------------------------------------
    
    sqlString = "SELECT unique_zap_import FROM zap_import"
    sql_results = read_sqlite(sqlString, MD5_string)
    return sql_results


#------------------------------------------------------------------------------------
def write_consolidated_list(word, MD5_string):
#------------------------------------------------------------------------------------
    
#    sqlString =  "INSERT INTO consolidated_list (unique_consolidated_list) VALUES ('" + word.lower() + "')"
#    change_db(sqlString, MD5_string)

    clean_word = str(word.lower())
    sqlString =  "INSERT INTO consolidated_list (unique_consolidated_list) VALUES (?)", [clean_word]
    change_db_parameterized(sqlString, MD5_string)



#------------------------------------------------------------------------------------
def create_consolidated_list(MD5_sum):
#------------------------------------------------------------------------------------
    

        returned_words = get_all_text_words(MD5_sum)
        for row in returned_words:
            sqlString =  "INSERT INTO consolidated_list (unique_consolidated_list) VALUES ('" + str(row[0]) + "')"
            change_db(sqlString, MD5_sum)

        returned_words = get_all_burp_words(MD5_sum)
        for row in returned_words:
            sqlString =  "INSERT INTO consolidated_list (unique_consolidated_list) VALUES ('" + str(row[0]) + "')"
            change_db(sqlString, MD5_sum)


        returned_words = get_all_zap_words(MD5_sum)
        for row in returned_words:
            sqlString =  "INSERT INTO consolidated_list (unique_consolidated_list) VALUES ('" + str(row[0]) + "')"
            change_db(sqlString, MD5_sum)

#   we need to do this manually rather than return potentially huge datasets / wordlists
    
#    db_path = os.getcwd()
#    db_path = db_path + "/tmp/" + MD5_sum + ".db"
    
#    connection = sqlite3.connect(db_path)
#    cursor = connection.cursor()

#    for row in cursor.execute('SELECT unique_text_words FROM text_words'):
#        print(row[0])
#        sqlString =  "INSERT INTO consolidated_list (unique_consolidated_list) VALUES ('" + str(row[0]) + "')"
#        change_db(sqlString, MD5_sum)

#    for row in cursor.execute('SELECT unique_burp_import FROM burp_import'):
#        print(row[0])
#        sqlString =  "INSERT INTO consolidated_list (unique_consolidated_list) VALUES ('" + str(row[0]) + "')"
#        change_db(sqlString, MD5_sum)

#    for row in cursor.execute('SELECT unique_zap_import FROM zap_import'):
#        print(row[0])
#        sqlString =  "INSERT INTO consolidated_list (unique_consolidated_list) VALUES ('" + str(row[0]) + "')"
#        change_db(sqlString, MD5_sum)


#    cursor.close()
#    connection.close()
    
#    del cursor
#    del connection



#------------------------------------------------------------------------------------
def count_consolidated_list(MD5_string):
#------------------------------------------------------------------------------------
    
    sqlString = "SELECT Count(*) FROM consolidated_list"
    sql_results = read_sqlite(sqlString, MD5_string)
    return str(sql_results).replace("(", "").replace("[", "").replace(",", "").replace("]", "").replace(")", "")


#------------------------------------------------------------------------------------
def get_all_consolidated_words(MD5_string):
#------------------------------------------------------------------------------------
    
    sqlString = "SELECT unique_consolidated_list FROM consolidated_list"
    sql_results = read_sqlite(sqlString, MD5_string)
    return sql_results



#====================================================================================
#        
#====================================================================================
