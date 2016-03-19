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


start_application_flag = True

#==============================================================================
try:
    import PyQt4  
except ImportError:
    start_application_flag = False
    print("Please run following commands to install the GUI library:")
    print("    sudo apt-get install libqt4-dev")
    print("    sudo apt-get install python-qt4 qt4-dev-tools python-qt4-dev pyqt4-dev-tools")
    print("    sudo apt-get install python3-pyqt4")


#==============================================================================
try:
    import sqlite3  
except ImportError:
    start_application_flag = False
    print("Please run following command to install the database library: pip3 install sqlite3")


#==============================================================================
try:
    import lxml  
except ImportError:
    start_application_flag = False
    print("Please run following commands to install the xml parser library:")
    print("     sudo apt-get install -y libxml2-dev libxslt1-dev zlib1g-dev")
    print("     pip3 install lxml")

#==============================================================================
try:
    import bs4  
except ImportError:
    start_application_flag = False
    print("Please run following command to install the html parser library (bs4): pip3 install bs4")



#==============================================================================
if not start_application_flag:
    print("Please note: To run pip3 you may need to install it using the command: sudo apt-get install python3-pip")
    print("EXITING OWASP BELVA. NOT ALL MODULES WERE INSTALLED IN THE ENVIRONMENT....")
    exit()


