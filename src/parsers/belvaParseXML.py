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


import lxml.html
from lxml import etree

from bs4 import BeautifulSoup


#---------------------------------------------------------------------------------
# parse XML and return value asked (designed for errors via stdout)
def parseXMLxpathSearch(xml_source, xpathString):
#---------------------------------------------------------------------------------

    return_values = []

    try:
        root = etree.XML(xml_source)

        data_points = root.xpath(xpathString)
    
        for data in data_points:
            return_values.append(etree.tostring(data))
            data.clear()

    except:
        pass

    return return_values

#---------------------------------------------------------------------------------
# parse XML and return value asked (designed for errors via stdout)
def parseXMLxpathSearchSingle(xml_source, xpathString):
#---------------------------------------------------------------------------------

    return_values = []

    try:
        root = etree.XML(xml_source)

        data_points = root.xpath(xpathString)
    
        for data in data_points:
            return_values.append(data)
            data.clear()

    except:
        pass

    return return_values



#---------------------------------------------------------------------------------
# parse HTML and return value asked
def parseXMLxpathSearchAttribute(xml_source, xpathString):
#---------------------------------------------------------------------------------


    return_values = []

    try:
        root = etree.XML(xml_source)

        data_points = root.xpath(xpathString)
    
        for data in data_points:
            return_values.append(data)
            data.clear()
    except:
        pass

    return return_values




#---------------------------------------------------------------------------------
# parse HTML and return value asked
def parseHTMLxpathSearch(http_source, xpathString):
#---------------------------------------------------------------------------------

    return_values = []


    http_source= str(http_source).replace('\x00','')
    try:
        html = lxml.html.fromstring(http_source)

        for data in html.xpath(xpathString):
            return_values.append(etree.tostring(data.content))
            data.clear()

    except:
        pass

    return return_values



#---------------------------------------------------------------------------------
# parse HTML and return value asked
def parseHTMLallText(http_source):
#---------------------------------------------------------------------------------

    return_values = []

#    print(http_source)
    # if it's not an html page we return
    try:
        if (not (("<html>" in http_source.decode('utf-8').lower())
            or ("<html " in http_source.decode('utf-8').lower()))
            
            or ("'<html>" in http_source.decode('utf-8').lower())
            or ('"<html>' in http_source.decode('utf-8').lower())):
            
            return return_values
    except:        
        return return_values

    # if we cant find the start of the file
    # or if there is a decode error we want to skip
    try:
        pure_html = http_source[http_source.decode('utf-8').find("<html"):]

        #----------------
        # Get Meta items
        #----------------
        meta_description_array = []    
        try:
            html = lxml.html.fromstring(pure_html)

            for data in html.xpath("//meta[@name='description']/@content"):
                meta_description_array = data.split(" ")
                data.clear()

        except:
            pass


        meta_keywords_array = []
        try:
            html = lxml.html.fromstring(pure_html)

            for data in html.xpath("//meta[@name='keywords']/@content"):
                meta_keywords_array = data.split(",")
                data.clear()

        except:
            pass


        #----------------
        # Beautiful soup text
        #----------------
        soup = BeautifulSoup(pure_html, "lxml")


        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        text = soup.findAll(text=True, recursive=True)

        temp_return_values = []
        temp_return_values = meta_description_array + meta_keywords_array + text

        really_temp_array = []
        final_temp_array = []

        for text_string in temp_return_values:
            #we actually have a string to deal with
            if str(text_string.strip()):
                # this is to prevent a beautiful soup warning: not an http string for a . (which is a file)
                if not ("http://" in text_string[0:8] or "https://"in text_string[0:8] or "." == str(text_string)):
                
                    # check to make sure we don't have HTML / scripts in our text"
                    if not (bool(BeautifulSoup(text_string, "html.parser").find())):

                        # kind of a repeat of the first one but we don't want URLs or other HTML in our data
                        if not ("http://" in text_string or "https://"in text_string or "<!["in text_string):
                            really_temp_array = text_string.split(" ")

                            for really_temp in really_temp_array:
                                temp_string = ''.join([i for i in really_temp if i.isalpha()])
                                # non-alpha characters end up as spaces so we remove them....
                                if not (str(temp_string).strip() == ""):
                                # we also case all strings as lower case!!!
                                    final_temp_array.append(temp_string.lower())

        # remove duplicates
        return_values = list(set(final_temp_array))

        return return_values

    except:
        return return_values



#---------------------------------------------------------------------------------
#    error suppression
#---------------------------------------------------------------------------------
def noerr(ctx, str):
    pass


#---------------------------------------------------------------------------------
# parse HTML and return value asked
def parseCDATA(xml_source, xpathString):
#---------------------------------------------------------------------------------

    return_values = []

    print(xml_source)
    root = etree.fromstring(xml_source)
    for log in root.xpath(xpathString):
        return_values.append(str(log.text))

    return return_values




