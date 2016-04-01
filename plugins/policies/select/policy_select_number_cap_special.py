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


import os.path, sys



class About():
    def run(self):

        status_dict = {}

        status_dict['active'] = True        
#        status_dict['active'] = False

        return status_dict


class Description():
    def run(self):


        DescriptionDetails = {}
        DescriptionDetails['name'] = "Select Words with at least 1 Cap, Number & Special Chars"
        
        return DescriptionDetails



class CheckWord():
    def run(self, word):

        return_flag = True
        #always return true if passed the checks
        #always return false if didn't pass checks
        
        #check if has capital letter
        if any(char.isupper() for char in word):
           pass
        else:
            # not capital letters
            return_flag = False
            
        #check if it has a digit
        if any(char.isdigit() for char in word):
            pass
        else:
            return_flag = False        

        #special characters
        special_chars = "~!@#$%^&*()_+`-={}|[]\:;'<>?,./\""
        
        special_char_flag = False
        for special_char in special_chars:
            if special_char in word:
                special_char_flag = True

        if not special_char_flag:
            return_flag = False


        return return_flag
    
    