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


import multiprocessing
#from queue import Queue
#from threading import Thread

import queue
import threading


#from symbol import parameters


#-----------------------------------------------------------
def queue_cmd(function_name, parameter_datastructure_array, num_threads):
#-----------------------------------------------------------
    
    # here is the idea: the worker2 function is passed the function to call
    #    the function_name should be a wrapper function to unpack the cmd data structure

#    print("queue_cmd: " + str(function_name) + " : " + str(len(parameter_datastructure_array)))
    q = queue.Queue(maxsize=0)
    num_worker_threads = num_threads
#    num_worker_threads = 10
    for i in range(num_worker_threads):
        t = threading.Thread(target=worker, args=(q,function_name))
        t.daemon = True
        t.start()

    for parameter_datastructure in parameter_datastructure_array:
        q.put(parameter_datastructure)

    q.join()


#-----------------------------------------------------------   
def worker(q, function_name):
#-----------------------------------------------------------
    while True:
        try:
            parameter_datastructure = q.get()
            function_name(parameter_datastructure)
            q.task_done()

        except:
            pass

