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


import os, time, sys, sqlite3
from PyQt4 import QtGui

# converted Qt4 UI from Qt Converter & cmd; pyuic4 design.ui -o design.py
import src.gui.design

from src.db.belvaDbInitalize import belvaInitDB
from src.db.belvaDbInitalize import belvaRemoveDB

from src.db.belvaSqlDBroutines import count_text_words
from src.db.belvaSqlDBroutines import count_burp_words
from src.db.belvaSqlDBroutines import count_zap_words
from src.db.belvaSqlDBroutines import get_all_burp_words
from src.db.belvaSqlDBroutines import create_consolidated_list
from src.db.belvaSqlDBroutines import count_consolidated_list
from src.db.belvaSqlDBroutines import get_all_consolidated_words


from src.pluginSystem.pluginControlSystem import get_policy_mutate_names
from src.pluginSystem.pluginControlSystem import get_policy_select_names
from src.pluginSystem.pluginControlSystem import get_substitution_names
from src.pluginSystem.pluginControlSystem import return_substitution_dict

from src.threadQueue.aptQueueControlSystem import send_words_to_queue

from src.belvaCommonRoutines import iterative_function
from src.belvaCommonRoutines import get_positions

from src.dataImport.belvaDataImport import belvaDataImport



#--------------------------------------------------------------------------------------------------
class BELVA_AppUI(QtGui.QMainWindow, src.gui.design.Ui_MainWindow):
#--------------------------------------------------------------------------------------------------
    def __init__(self):
 
        super(self.__class__, self).__init__()
        self.setupUi(self)
        
        #UPDATE WINDOW BAR GUI VERSION NUMBER
        
        self.textBrowser_help_text.append("Follow / Contact me on Twitter: @infosecmaverick")        
        self.textBrowser_help_text.append("Help on the OWASP Project Page: http://bit.ly/1okrO1T")
#        self.textBrowser_help_text.append("    https://www.owasp.org/index.php/OWASP_Basic_Expression_%26_Lexicon_Variation_Algorithms_%28BELVA%29_Project")
        self.textBrowser_help_text.append("Topics will include:")
        self.textBrowser_help_text.append("    How to import burp xml files for org specific content")
        self.textBrowser_help_text.append("    How to import ZAP raw files for org specific content")
        self.textBrowser_help_text.append("    How to create user id combinations")
        self.textBrowser_help_text.append("    How to write a plugin")
        self.textBrowser_help_text.moveCursor(QtGui.QTextCursor.Start)       


        self.progressBar.setValue(0)

        #set the default directory to the localized importExternalSources Folder
#        current_directory = os.getcwd()
        current_directory = os.path.dirname(os.path.abspath(__file__))
        current_directory = current_directory.replace("/src/gui", "")
        current_directory = current_directory.replace("\src\gui", "")
        self.lineEdit_input_src_dir.setText(current_directory + "/importExternalSources/")

        #set the default directory to the localized outputFile Folder
        self.lineEdit_output_src_dir.setText(current_directory+ "/outputFile/output.txt")
        
        #load boxes....
        policy_names = []
        subsuitition_names = []
        
        policy_mutate_names = get_policy_mutate_names()
        policy_select_names = get_policy_select_names()

        subsuitition_names = get_substitution_names() 
                
        for policy_name in policy_mutate_names:
            self.listWidget_policies_mutate.addItem(policy_mutate_names[policy_name])

        for policy_name in policy_select_names:
            self.listWidget_policies_select.addItem(policy_select_names[policy_name])


        for subsuitition_name in subsuitition_names:
            self.listWidget_substitutions.addItem(subsuitition_names[subsuitition_name])

        self.pushButton_input_src_dir.clicked.connect(self.input_src_dir)  # When the button is pressed
        self.pushButton_output_src_dir.clicked.connect(self.output_src_dir)  # When the button is pressed
        self.pushButton_run_belva.clicked.connect(self.run_belva)  # When the button is pressed



    def form_checks(self):
        # default value should be false
        passed_checks = False
        
        # we can put error checking here
        passed_checks = True

        return passed_checks

    #=================================================
    # assuming we pass the checks, we write an API layer into UI design
    #=================================================
    def run_belva(self):
        if self.form_checks():
#        self.textBrowser_results_window.clear() # In case there are any existing elements in the list

            self.progressBar.setValue(0)
            self.textBrowser_status_msgs.clear()
            self.textBrowser_status_msgs_brief.clear()
            
            input_directory = self.lineEdit_input_src_dir.text()
            output_file = self.lineEdit_output_src_dir.text()

            global_gui_status_msgs = self.textBrowser_status_msgs
            global_gui_status_msgs_brief = self.textBrowser_status_msgs_brief
            global_gui_progressBar = self.progressBar
            
#            global_gui_status_msgs, global_gui_status_msgs_brief, global_gui_progressBar, 
            #------------------------------------
            #    This should really be passed in via parameters but need to
            #    research signals and slots for QT4... until then....
            #------------------------------------
            policy_mutate_names = []
            policy_select_names = []
            subsuitition_names = []
        
            policy_mutate_names = get_policy_mutate_names()
            policy_select_names = get_policy_select_names()
            subsuitition_names = get_substitution_names() 
            #------------------------------------


            #------------------------------------
            # Create database to normalize data and have unique words
            #------------------------------------
            MD5_string = belvaInitDB()


            #idea - have form to auto generate substitution and policy plugins...
            
            policy_mutate_descriptions_selected = []
            for policy_description_selected in self.listWidget_policies_mutate.selectedItems():
                policy_mutate_descriptions_selected.append(policy_description_selected.text())

            policy_select_descriptions_selected = []
            for policy_description_selected in self.listWidget_policies_select.selectedItems():
                policy_select_descriptions_selected.append(policy_description_selected.text())

            
            substitution_descriptions_selected = []
            for substitution_description_selected in self.listWidget_substitutions.selectedItems():
                substitution_descriptions_selected.append(substitution_description_selected.text())

            #------------------------------------
            # Translate Descriptions back into plugin names
            #------------------------------------

            policy_mutate_plugin_names = []
            for policy_description in policy_mutate_descriptions_selected:
                for policy_name in policy_mutate_names:
                    if policy_mutate_names[policy_name] == policy_description:
                        policy_mutate_plugin_names.append(policy_name)


            policy_select_plugin_names = []
            for policy_description in policy_select_descriptions_selected:
                for policy_name in policy_select_names:
                    if policy_select_names[policy_name] == policy_description:
                        policy_select_plugin_names.append(policy_name)


            substitution_plugin_names = []
            for substitution_description in substitution_descriptions_selected:
                for substitution_name in subsuitition_names:
                    if subsuitition_names[substitution_name] == substitution_description:
                        substitution_plugin_names.append(substitution_name)


            #------------------------------------
            # Get files to import / separate large from small
            #------------------------------------
            small_filename_dict = {}
            large_filename_dict = {}

            for root, directories, filenames in os.walk(input_directory):
                for filename in filenames:
                    full_path_w_file = os.path.join(root,filename)
                    filename, file_extension = os.path.splitext(full_path_w_file)
#                    small_filename_dict[full_path_w_file] = file_extension
#                    filename = os.path.basename(full_path_w_file)
                    # 10 MB
                    if ((os.path.getsize(full_path_w_file) >= 10485760) and (file_extension == '.txt')):
                        large_filename_dict[full_path_w_file] = file_extension
                    else:
                        small_filename_dict[full_path_w_file] = file_extension


            #------------------------------------
            # Get words to filter
            #------------------------------------
            remove_common_words = []
#            common_words_dir = os.getcwd() + "/filterDictionaries/"
            common_words_dir = os.path.dirname(os.path.abspath(__file__))
            common_words_dir = common_words_dir.replace("/src/gui", "")
            common_words_dir = common_words_dir.replace("\src\gui", "")
            common_words_dir = common_words_dir + "/filterDictionaries/" 
    
            for root, directories, filenames in os.walk(common_words_dir):
                for filename in filenames:
                    full_path_w_file = os.path.join(root,filename)

                    f = open(full_path_w_file,'r')
    
                    for line in f:
                        if str(line).strip():
                            remove_common_words.append(str(line).strip().lower())

                    f.close()
                    f = None
    #-------------------




            #------------------------------------
            # Import Data from Wordlists, ZAP and burp
            #------------------------------------
            self.textBrowser_status_msgs.append("Starting: reading through files...")
            self.textBrowser_status_msgs.append("Starting: removing common words...")
            self.textBrowser_status_msgs.append("Starting: creating temp word dictionary...")


            belvaDataImport(global_gui_status_msgs, global_gui_status_msgs_brief, global_gui_progressBar, small_filename_dict, MD5_string, remove_common_words)

            self.textBrowser_status_msgs_brief.clear()
            total_word_count = count_consolidated_list(MD5_string)
            self.textBrowser_status_msgs.append("Total Number of Unique Consolidated Words for small files: " + str(total_word_count))


            
            # no words found!
#            gui.belva_qt4_global_gui_vars.global_gui_window = self.textBrowser_results_window
#            gui.belva_qt4_routines_delete.run_app(nmap_text, masscan_network_text, masscan_ports_text)

            #------------------------------------
            # Set progress bar for end user info
            #------------------------------------

            self.progressBar.setMinimum(0)
            self.progressBar.setMaximum(int(total_word_count))
            self.progressBar.setValue(0)
            count = 0

            positions_ds = {}
            subsitution_dictionary = {}

            all_consolidated_words = get_all_consolidated_words(MD5_string)


            self.textBrowser_status_msgs.append("Mutating finalized temp word dictionary for small files...")
            for substitution_plugin_name in substitution_plugin_names:

                #------------------------------------
                # retrieve dictionary from substitution selected
                #------------------------------------

                subsitution_dictionary = return_substitution_dict(substitution_plugin_name)
                self.textBrowser_status_msgs.append("Using substitution plug-in: " +  substitution_plugin_name)

                #------------------------------------
                # cycle through finalized list of words
                #------------------------------------
                break_up_queue = int(total_word_count) / 20

                words_array = []
                for word in all_consolidated_words:

                    count = self.progressBar.value() + 1
                    self.progressBar.setValue(count)
                    self.textBrowser_status_msgs_brief.setText("Now processing word " + str(count) + " of " + str(total_word_count) + " : " + str(word[0]).strip())

                    if len(words_array) <= break_up_queue:
                        words_array.append(str(word[0]).strip())
                    else:
                        words_array.append(str(word[0]).strip())
                        send_words_to_queue(words_array, subsitution_dictionary, policy_mutate_plugin_names, policy_select_plugin_names, output_file)
                        words_array = []


            #------------------------------------
            #    process large files
            #------------------------------------
            self.textBrowser_status_msgs_brief.clear()
            self.textBrowser_status_msgs.append("Now processing large files...")
            for full_path in large_filename_dict:

                with open(full_path, 'r',  errors='replace') as f:
                    for i, l in enumerate(f):
                        pass
                total_word_count = i + 1

                break_up_queue = total_word_count / 20
                
                filename = os.path.basename(full_path)
                self.textBrowser_status_msgs.append("Now processing large file: " + str(filename) + " with a word count of: " + str(total_word_count))

                self.progressBar.setMinimum(0)
                self.progressBar.setMaximum(int(total_word_count))
                self.progressBar.setValue(0)
                count = 0
            
                f = open(full_path,'r',  errors='replace')
    
                words_array = []
                for line in f:

                    count = self.progressBar.value() + 1
                    self.progressBar.setValue(count)
                    self.textBrowser_status_msgs_brief.setText("Now processing up to word " + str(count) + " of " + str(total_word_count) + " : " + str(line).strip())

                    if str(line).strip():
                        if not(str(line).strip() in remove_common_words):

                            if len(words_array) <= break_up_queue:
                                words_array.append(str(line).strip())
                            else:
                                words_array.append(str(line).strip())
                                for substitution_plugin_name in substitution_plugin_names:

                                    subsitution_dictionary = return_substitution_dict(substitution_plugin_name)

                                    send_words_to_queue(words_array, subsitution_dictionary, policy_mutate_plugin_names, policy_select_plugin_names, output_file)
                                words_array = []


                f.close()
                f = None


            # total word count for output file...
            with open(output_file, 'r',  errors='replace') as f:
                for i, l in enumerate(f):
                    pass
            total_word_count = i + 1

                    

            self.textBrowser_status_msgs_brief.clear()
            self.textBrowser_status_msgs.append("Finished Mutating temp word dictionary")

            #------------------------------------
            # Clean up temporary files
            #------------------------------------
            self.textBrowser_status_msgs.append("Cleaning up temporary data....")
            belvaRemoveDB(MD5_string)
            
            self.textBrowser_status_msgs.append("Please Find the final custom dictionary here:")
            self.textBrowser_status_msgs.append(output_file)          
            self.textBrowser_status_msgs.append("Total number of words in output file: " + str(total_word_count))
            self.textBrowser_status_msgs.append("FINISHED!!!")



    def input_src_dir(self):

        directory = QtGui.QFileDialog.getExistingDirectory(self,"Pick a folder")

        self.lineEdit_input_src_dir.clear()
        self.lineEdit_input_src_dir.setText(directory)


    def output_src_dir(self):

       
        output_file =  QtGui.QFileDialog.getOpenFileName(self,"Pick Output File")

        self.lineEdit_output_src_dir.clear()
        self.lineEdit_output_src_dir.setText(output_file)


                                                                                                            

def launch_gui():
    
    app = QtGui.QApplication(sys.argv)
    form = BELVA_AppUI()
    form.show()
    app.exec_()


