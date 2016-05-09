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


import os, base64

from src.db.belvaSqlDBroutines import write_consolidated_list

from src.parsers.belvaParseXML import parseXMLxpathSearch as parseXML
from src.parsers.belvaParseXML import parseXMLxpathSearchSingle as parseXMLsingle
from src.parsers.belvaParseXML import parseCDATA
from src.parsers.belvaParseXML import parseHTMLxpathSearch as parseHTML
from src.parsers.belvaParseXML import parseHTMLallText as parseAllHTMLtext


#--------------------------------------------------------------------------
def belvaDataImport(global_gui_status_msgs, global_gui_status_msgs_brief, global_gui_progressBar, small_filename_dict, MD5_string, remove_common_words):
#--------------------------------------------------------------------------
    

    #-------------------
#    remove_common_words = []
#    common_words_dir = os.getcwd() + "/filterDictionaries/"

    
#    for root, directories, filenames in os.walk(common_words_dir):
#        for filename in filenames:
#            full_path_w_file = os.path.join(root,filename)

#            f = open(full_path_w_file,'r')
    
#            for line in f:
#                if str(line).strip():
#                    remove_common_words.append(str(line).strip().lower())

#            f.close()
#            f = None
    #-------------------




    number_xml = sum( ".xml" in x for x in small_filename_dict.values())
    number_txt = sum( ".txt" in x for x in small_filename_dict.values())
    number_raw = sum( ".raw" in x for x in small_filename_dict.values())
    number_html = sum( ".htm" in x for x in small_filename_dict.values())


    total_files = len(small_filename_dict)

    global_gui_status_msgs.append("Total number of burp files: " + (str(number_xml)))
    global_gui_status_msgs.append("Total number of text files: " + (str(number_txt)))
    global_gui_status_msgs.append("Total number of zap files: " + (str(number_raw)))
    global_gui_status_msgs.append("Total number of HTML files: " + (str(number_html)))


    #------------------
    # process
    #------------------

######    global_gui_progressBar --> j
    global_gui_progressBar.setMinimum(0)
    global_gui_progressBar.setMaximum(int(total_files))
    global_gui_progressBar.setValue(0)



    
    # burp
    i = 0
    count = 0
    for full_path in small_filename_dict:
        if small_filename_dict[full_path] == ".xml":
            i += 1

            count = global_gui_progressBar.value() + 1
            global_gui_progressBar.setValue(count)

            global_gui_status_msgs.append("Processing burp file " + str(i) + " of " + str(number_xml))
            xmlDataImport(global_gui_status_msgs, global_gui_status_msgs_brief, full_path, MD5_string, remove_common_words)


    # text dictionaries
    i = 0
    for full_path in small_filename_dict:
        if small_filename_dict[full_path] == ".txt":
            i += 1

            count = global_gui_progressBar.value() + 1
            global_gui_progressBar.setValue(count)

            global_gui_status_msgs.append("Processing text file " + str(i) + " of " + str(number_txt))
            txtDataImport(global_gui_status_msgs, global_gui_status_msgs_brief, full_path, MD5_string, remove_common_words)


    # ZAP
    i = 0
    for full_path in small_filename_dict:
        if small_filename_dict[full_path] == ".raw":
            i += 1

            count = global_gui_progressBar.value() + 1
            global_gui_progressBar.setValue(count)

            global_gui_status_msgs.append("Processing zap file " + str(i) + " of " + str(number_raw))
            zapDataImport(global_gui_status_msgs, global_gui_status_msgs_brief, full_path, MD5_string, remove_common_words)            
            

    # html
    i = 0
    for full_path in small_filename_dict:
        if ((small_filename_dict[full_path] == ".html") or (small_filename_dict[full_path] == ".htm")):
            i += 1

            count = global_gui_progressBar.value() + 1
            global_gui_progressBar.setValue(count)

            global_gui_status_msgs.append("Processing HTML file " + str(i) + " of " + str(number_html))
            htmlDataImport(global_gui_status_msgs, global_gui_status_msgs_brief, full_path, MD5_string, remove_common_words)            
            
            
            
                
#--------------------------------------------------------------------------
def txtDataImport(global_gui_status_msgs, global_gui_status_msgs_brief, full_path_w_file, MD5_string, remove_common_words):
#--------------------------------------------------------------------------

    f = open(full_path_w_file,'r')
    
    i = 0
    for line in f:
        if str(line).strip():
            i += 1

            if not(str(line).strip() in remove_common_words):
                write_consolidated_list(str(line).strip(), MD5_string)
                global_gui_status_msgs_brief.setText("Text File word count: " + str(i))
            
            
    f.close()
    f = None

    global_gui_status_msgs.append("Total number of text file words for batch: " + str(i))
    

    
#--------------------------------------------------------------------------
def xmlDataImport(global_gui_status_msgs, global_gui_status_msgs_brief, full_path_w_file, MD5_string, remove_common_words):
#--------------------------------------------------------------------------
    

    with open(full_path_w_file) as myfile:
        data="".join(line.rstrip() for line in myfile)

    if "burpVersion=" in data:
        belvaImportBurpXML(global_gui_status_msgs, global_gui_status_msgs_brief, data, MD5_string, remove_common_words)


#--------------------------------------------------------------------------
def zapDataImport(global_gui_status_msgs, global_gui_status_msgs_brief, full_path_w_file, MD5_string, remove_common_words):
#--------------------------------------------------------------------------

    with open(full_path_w_file) as myfile:
        data="".join(line.rstrip() for line in myfile)

    all_text = parseAllHTMLtext(str(data).encode('utf-8'))
#    print(all_text)
    i = 0
    for word in all_text:
#        print(word)
        i += 1

        if not(str(word).strip() in remove_common_words):
            write_consolidated_list(word, MD5_string)
            global_gui_status_msgs_brief.setText("Zap File word count: " + str(i))

    global_gui_status_msgs.append("Total number of ZAP file words for batch: " + str(i))


#--------------------------------------------------------------------------
def htmlDataImport(global_gui_status_msgs, global_gui_status_msgs_brief, full_path_w_file, MD5_string, remove_common_words):
#--------------------------------------------------------------------------

    with open(full_path_w_file) as myfile:
        data="".join(line.rstrip() for line in myfile)

    all_text = parseAllHTMLtext(str(data).encode('utf-8'))
#    print(all_text)
    i = 0
    for word in all_text:
#        print(word)
        i += 1

        if not(str(word).strip() in remove_common_words):
            write_consolidated_list(word, MD5_string)
            global_gui_status_msgs_brief.setText("HTML File word count: " + str(i))

    global_gui_status_msgs.append("Total number of HTML file words for batch: " + str(i))




#----------------------------------------------------------------
def belvaImportBurpXML(global_gui_status_msgs, global_gui_status_msgs_brief, data, MD5_string, remove_common_words):
#----------------------------------------------------------------

    #we need to build this dynamically based on input parameters
    i = 0
    xpath = "//item"
    return_requests_items = parseXML(data, xpath)
    request_count = 0
    for specific_request in return_requests_items:
        request_count += 1

        process_request = 0
        for specific_request in return_requests_items:
            process_request += 1

            xpath = "//response"
            specific_request_encoded_data = parseXML(specific_request, xpath)

            #note there should be only one but we return an array
            for each_encoded_request in specific_request_encoded_data:
                xpath = "/response/text()"
                specific_request_encoded_data_text = parseXMLsingle(str(each_encoded_request.decode('utf-8')), xpath)
                b64msg = base64.b64decode(specific_request_encoded_data_text[0])

                all_text = parseAllHTMLtext(b64msg)

                for word in all_text:
                    i += 1

                    if not(str(word).strip() in remove_common_words):
                        write_consolidated_list(word, MD5_string)
                        global_gui_status_msgs_brief.setText("burp File word count: " + str(i))



    global_gui_status_msgs.append("Total number of burp file words for batch: " + str(i))


    