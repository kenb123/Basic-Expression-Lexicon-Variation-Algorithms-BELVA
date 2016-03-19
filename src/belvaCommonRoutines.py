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

import hashlib
from src.pluginSystem.pluginControlSystem import test_select_policy
from src.pluginSystem.pluginControlSystem import run_policy_mutate_word

#==========================================================================
#   routines
#==========================================================================

def md5sum(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


#--------------------------------------------------------------------------
def get_positions(word, dict):
#--------------------------------------------------------------------------

    return_ds = {}

    i = 0
    for letter in word:
        i += 1 
        
        for key in dict:
            if key == letter.lower():
                return_ds[str(i)] = dict[letter.lower()]

    
    return return_ds


#--------------------------------------------------------------------------
def iterative_function(position, positions_ds, word, slice, policy_mutate_plugin_names, policy_select_plugin_names, file_location=None):
#--------------------------------------------------------------------------

    if (position + 1) <= len(word):

        value = positions_ds.get(str(position + 1), "")

        if not value:

            value = word[position:position + 1]

        for character in value:

            slice_temp = str(slice) + str(character)
            iterative_function(position + 1, positions_ds, word, slice_temp, policy_mutate_plugin_names, policy_select_plugin_names, file_location)

            if str(position +1 ) == str(len(word)):
                policy_mutate_word_function(str(slice_temp), policy_mutate_plugin_names, policy_select_plugin_names, file_location)




#--------------------------------------------------------------------------
def policy_mutate_word_function(word, policy_mutate_plugin_names, policy_select_plugin_names, file_location):
#--------------------------------------------------------------------------

    mutated_words = []
    for plugin_name in policy_mutate_plugin_names:
        mutated_words = run_policy_mutate_word(plugin_name, word)
        for mutated_word in mutated_words:
            policy_select_word_function(mutated_word, file_location, policy_select_plugin_names)




#--------------------------------------------------------------------------
def policy_select_word_function(word, file_location, policy_select_plugin_names):
#--------------------------------------------------------------------------
    
    passed_flag = True
    
    for plugin_name in policy_select_plugin_names:
        passed_flag = test_select_policy(plugin_name, word)
        
        # if we fail a test then word doesn't qualify and we leave
        if not passed_flag:
            return

    # we passed all checks so we write word...
    if file_location:
        write_outfile(word, file_location)
    else:
        print(word)




#==========================================================================
#    DB routines
#==========================================================================


def write_outfile(word, file_location=None):

    if file_location:
        outfile = file_location
    else: 
        # set for kali linux
        outfile= "/root/Desktop/output.txt"

    ofile = open(outfile, "a")
    ofile.write(word)
    ofile.write("\n")
    ofile.close()


