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



import importlib
import pkgutil
import sys
import os


#---------------------------------------
def get_class_name(mod_name):
#---------------------------------------

#    """Return the class name from a plugin name"""
    output = ""

    # Split on the _ and ignore the 1st word plugin
    words = mod_name.split("_")[1:]

    # Capitalise the first letter of each word and add to string
    for word in words:
        output += word.title()
    return output



#---------------------------------------
def dynamic_load_return_mods():
#---------------------------------------

#    path = os.path.join(os.getcwd(), "plugins/policies/select")
    path = os.path.join(os.path.dirname(__file__), "plugins/policies/select")
    path = path.replace("src/pluginSystem/", "")
    path = path.replace("src\pluginSystem\\", "")

    modules = pkgutil.iter_modules(path=[path])
    
#    print ""
        
    mode_names = []        
    for loader, mod_name, ispkg in modules:
        mode_names.append(mod_name)
        
    return mode_names


#---------------------------------------
def dynamic_load_init(modename):
#---------------------------------------


    getCases = True
    decision_dict = {}
    empty_array = []

    path = "plugins/policies/select/"
    path_load = str(path).replace("/", ".")

    if modename not in sys.modules:
        # Import module
        loaded_mod = importlib.import_module(path_load + modename)


    # Load class from imported module
    class_name = get_class_name(modename)
    load_class_info = getattr(loaded_mod, "About")

    # Create an instance of the class
    instance_class_info = load_class_info()
    decision_dict = instance_class_info.run()       

    #make some decisions            
    if not decision_dict['active']:
        getCases = False


    # see if plugin matches
    if getCases:        
        load_class_init = getattr(loaded_mod, "Description")
        instance_class_init = load_class_init()
        return instance_class_init.run()


    return empty_array


#---------------------------------------
def dynamic_load_test(modename, word):
#---------------------------------------


    getCases = True
    decision_dict = {}
    empty_array = []

    path = "plugins/policies/select/"
    path_load = str(path).replace("/", ".")

    if modename not in sys.modules:
        # Import module
        loaded_mod = importlib.import_module(path_load + modename)


    # Load class from imported module
    class_name = get_class_name(modename)
    load_class_info = getattr(loaded_mod, "About")

    # Create an instance of the class
    instance_class_info = load_class_info()
    decision_dict = instance_class_info.run()       

    #make some decisions            
    if not decision_dict['active']:
        getCases = False


    # see if plugin matches
    if getCases:        
        load_class_init = getattr(loaded_mod, "CheckWord")
        instance_class_init = load_class_init()
        return instance_class_init.run(word)


    return empty_array
            