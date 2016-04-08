#!/usr/bin/env python3
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
import sqlite3



#----------------------------------------------
def nonread_sqlite(SQL, MD5_sum):
#----------------------------------------------


    db_path = os.path.dirname(os.path.abspath(__file__))
    db_path = db_path.replace("/src/db", "")
    db_path = db_path.replace("\src\db", "")

    db_path = db_path + "/tmp/" + MD5_sum + ".db"
    
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    try:
        cursor.execute(SQL)
        connection.commit()
    except:
        pass

    cursor.close()
    connection.close()
    
    del cursor
    del connection


#----------------------------------------------
def nonread_sqlite_parameterized(SQL, MD5_sum):
#----------------------------------------------

    db_path = os.path.dirname(os.path.abspath(__file__))
    db_path = db_path.replace("/src/db", "")
    db_path = db_path.replace("\src\db", "")

    db_path = db_path + "/tmp/" + MD5_sum + ".db"
    
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    try:
        cursor.execute(*SQL)
        connection.commit()
    except:
        pass

    cursor.close()
    connection.close()
    
    del cursor
    del connection




#----------------------------------------------
def read_sqlite(SQL, MD5_sum):
#----------------------------------------------


    db_path = os.path.dirname(os.path.abspath(__file__))
    db_path = db_path.replace("/src/db", "")
    db_path = db_path.replace("\src\db", "")

    db_path = db_path + "/tmp/" + MD5_sum + ".db"

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    rows = []
    try:
        for row in cursor.execute(SQL):
            rows.append(row)   

        connection.commit()
    except:
        pass


    cursor.close()
    connection.close()
    
    del cursor
    del connection
    
    return rows


#----------------------------------------------
def del_database(MD5_sum):
#----------------------------------------------


    db_path = os.path.dirname(os.path.abspath(__file__))
    db_path = db_path.replace("/src/db", "")
    db_path = db_path.replace("\src\db", "")

    db_path = db_path + "/tmp/" + MD5_sum + ".db"
    
    os.remove(db_path)