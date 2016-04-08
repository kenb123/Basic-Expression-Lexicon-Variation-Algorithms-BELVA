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


from src.threadQueue.aptQueue import queue_cmd

from src.belvaCommonRoutines import iterative_function
from src.belvaCommonRoutines import get_positions

#---------------------------------------------------------------------------------
def send_words_to_queue(words_array, subsitution_dictionary, policy_mutate_plugin_names, policy_select_plugin_names, output_file):
#---------------------------------------------------------------------------------

    queue_ds_array = []
    
    for word in words_array:
        
        queue_word_ds = {}
        
        queue_word_ds["word"] = str(word).strip()
        queue_word_ds["subsitution_dictionary"] = subsitution_dictionary
        queue_word_ds["policy_mutate_plugin_names"] = policy_mutate_plugin_names
        queue_word_ds["policy_select_plugin_names"] = policy_select_plugin_names
        queue_word_ds["output_file"] = output_file

        
        queue_ds_array.append(queue_word_ds)

    if queue_ds_array:
        queue_cmd(process_word, queue_ds_array, 500)



#---------------------------------------------------------------------------------
def process_word(queue_word_ds):
#---------------------------------------------------------------------------------

    word = queue_word_ds["word"]
    subsitution_dictionary = queue_word_ds["subsitution_dictionary"]
    policy_mutate_plugin_names = queue_word_ds["policy_mutate_plugin_names"]
    policy_select_plugin_names = queue_word_ds["policy_select_plugin_names"]
    output_file = queue_word_ds["output_file"]

#    print("process_word: " + str(word))
    positions_ds = get_positions(str(word).strip(), subsitution_dictionary)
    iterative_function(0, positions_ds, str(word).strip(), "", policy_mutate_plugin_names, policy_select_plugin_names, output_file)

