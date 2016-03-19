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


from src.pluginSystem.pluginDynamicMutatePolicies import dynamic_load_init as get_policy_check_mutate_names
from src.pluginSystem.pluginDynamicSelectPolicies import dynamic_load_init as get_policy_check_select_names
from src.pluginSystem.pluginDynamicSubstitutions import dynamic_load_init as get_substitution_check_names


from src.pluginSystem.pluginDynamicMutatePolicies import dynamic_load_return_mods as retrieve_policy_mutate_plugins
from src.pluginSystem.pluginDynamicSelectPolicies import dynamic_load_return_mods as retrieve_policy_select_plugins
from src.pluginSystem.pluginDynamicSubstitutions import dynamic_load_return_mods as retrieve_subsititution_plugins


from src.pluginSystem.pluginDynamicSelectPolicies import dynamic_load_test as test_policy_select_word
from src.pluginSystem.pluginDynamicMutatePolicies import dynamic_load_test as run_policy_mutate_word

from src.pluginSystem.pluginDynamicSubstitutions import dynamic_load_test as get_substitution_dictionary


#-----------------------------------
def get_policy_mutate_names():
#-----------------------------------
    
    policy_names = {}
    
    for plugin_name in retrieve_policy_mutate_plugins():
            
            temp_policy_dict = get_policy_check_mutate_names(plugin_name)
            policy_names[str(plugin_name)] = str(temp_policy_dict['name']) 

    return policy_names


#-----------------------------------
def get_policy_select_names():
#-----------------------------------
    
    policy_names = {}
    
    for plugin_name in retrieve_policy_select_plugins():
            
            temp_policy_dict = get_policy_check_select_names(plugin_name)
            policy_names[str(plugin_name)] = str(temp_policy_dict['name']) 

    return policy_names


#-----------------------------------
def test_select_policy(policy_name, word):
#-----------------------------------
    
    return test_policy_select_word(policy_name, word)


#-----------------------------------
def run_mutate_policy(policy_name, word):
#-----------------------------------
    
    return run_policy_mutate_word(policy_name, word)


#-----------------------------------
def get_substitution_names():
#-----------------------------------
    
    substitution_names = {}
    
    for plugin_name in retrieve_subsititution_plugins():
            
            temp_substitution_dict = get_substitution_check_names(plugin_name)
            substitution_names[str(plugin_name)] = str(temp_substitution_dict['name']) 

    return substitution_names


#-----------------------------------
def return_substitution_dict(substitution_plugin_name):
#-----------------------------------

    return get_substitution_dictionary(substitution_plugin_name)



#===============================================================================================================
#===============================================================================================================