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


import os.path, sys



class About():
    def run(self):

        status_dict = {}

        status_dict['active'] = True        
#        status_dict['active'] = False

        return status_dict


class Description():
    def run(self):

        #Thanks to LR for reminding me to add this one as a default.... ~Ken
        DescriptionDetails = {}
        DescriptionDetails['name'] = "Generate User IDs from Firstname Lastname"        
        
        return DescriptionDetails



class MutateWord():
    def run(self, word):

        userid_array = []
        # this is just a demo more user id patters can be added:
        

        if " " in word.strip():
            first_name, last_name = word.split(" ")

            #create: firstname.lastname
            userid_array.append(str(first_name) + "." + str(last_name))

            #create: flastname
            userid_array.append(str(first_name[0:1]) + str(last_name))
        
        

        #all words must be returned in an array
        return userid_array
    
    
    