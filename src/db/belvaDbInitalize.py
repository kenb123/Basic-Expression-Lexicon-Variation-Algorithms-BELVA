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


import os
import datetime

from src.belvaCommonRoutines import md5sum

from src.db.belvaDbRoutines import nonread_sqlite as create_db
from src.db.belvaDbRoutines import read_sqlite
from src.db.belvaDbRoutines import del_database

 

#--------------------------------------------------------------------------
def belvaInitDB():
#--------------------------------------------------------------------------
    
    
    #-----------------------------------------
    # create database
    #-----------------------------------------
    date_time = str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
    MD5_sum = md5sum(str(date_time) + str(os.urandom(10)))

    database_name = MD5_sum + ".db"

    #-----------------------------------------
    # create tables in database
    #-----------------------------------------

    # primary table with URLs
    sqlString = "CREATE TABLE text_words (unique_text_words UNIQUE)"
    create_db(sqlString, MD5_sum)

    # we create table to hold the raw query string GET & POST data of our urls 
    sqlString = "CREATE TABLE burp_import (unique_burp_import UNIQUE)"
    create_db(sqlString, MD5_sum)

    # we create table to hold the tokenized query string GET & POST data of our urls 
    sqlString = "CREATE TABLE zap_import (unique_zap_import UNIQUE)"
    create_db(sqlString, MD5_sum)

    sqlString = "CREATE TABLE consolidated_list (unique_consolidated_list UNIQUE)"
    create_db(sqlString, MD5_sum)

    sqlString = "CREATE TABLE generated_words (unique_generated_words UNIQUE)"
    create_db(sqlString, MD5_sum)


    return MD5_sum

#    future?
#    we create table to hold the combinations generated frompURLsDictionary
#    sqlString = "CREATE TABLE pURLsTestQueries (pURLsTestQueries_key INTEGER PRIMARY KEY, pURLs_key INTEGER, pURLsTestQueries_mode TEXT, pURLsTestQueries_queries TEXT, pURLsTestQueries_spidered TEXT, pURLsTestQueries_checked TEXT)"
#    create_db(sqlString)


#--------------------------------------------------------------------------
def belvaRemoveDB(MD5_sum):
#--------------------------------------------------------------------------

    del_database(MD5_sum)


