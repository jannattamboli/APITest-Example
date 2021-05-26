#!/usr/bin/env python -u
"""common utils"""
# REANCloud CONFIDENTIAL
# __________________
#
#  (C) 2018 REANCloud LLC
#  All Rights Reserved.
#
# NOTICE: All information contained herein is, and remains
# the property of REANCloud LLC and its suppliers,
# if any. The intellectual and technical concepts contained
# herein are proprietary to REANCloud LLC and its suppliers
# and may be covered by U.S. and Foreign Patents,
# patents in process, and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from REANCloud LLC.

from __future__ import print_function
import unittest
import allure
from allure.constants import AttachmentType
import subprocess
import os

import configparser

from collections import Counter
import re
import fileinput
import time
import xlrd
import pytest


class Utility(unittest.TestCase):
    '''
    common util methods
    '''
    ########################################################
    # global testcase_row
    # testcase_row = 0
    # global fail_ctr
    # global fail_msg
    # global wb
    # global sheet
    # global TESTDATA
    config = configparser.ConfigParser()
    config.read('testdata.properties')
    fail_ctr = 0
    fail_msg = ""
    dir_script = "scripts/"
    wb = ""
    sheet = ""
    excel_with_tests = ""
    search_literal = r'[$<]\w+'
    min_get_seconds = .25
    calc_milli_seconds = 1000.0

    ########################################################
    def __init__(self, methodName='runTest'):
        self._testMethodName = methodName
        self._cleanups = None

    #######################################################
    def findDuplicatesList(self, in_list):
        '''
        finds duplicates in the list provided
        ARGUMENTS:
        in_list: list variable
        RETURNS:
        boolean
        '''
        counts = Counter(in_list)
        two_or_more = [item for item, count in counts.items() if count >= 2]
        print(two_or_more)
        return len(two_or_more) > 0

    ########################################################
    def findDuplicatesInColumns(self, sheet):
        '''
        finds duplicates in column of the excel. Exits pytest if duplicates found
        ARGUMENTS:
        sheet: worksheet object
        '''
        for rows in range(1, sheet.nrows):
            #check for duplicates
            col_testcase = [sheet.row(row)[0].value for row in range(sheet.nrows)] # Read in all rows
            col_test_command = [sheet.row(row)[1].value for row in range(sheet.nrows)] # Read in all rows

            if  self.findDuplicatesList(col_testcase) or self.findDuplicatesList(col_test_command):
                self.fail("TestData excel not confiured correctly. Duplicates found in testcase and command columns")
                pytest.exit("TestData excel not confiured correctly. Duplicates found in testcase and command columns")

    ########################################################
    def replaceVarCommand(self, command):
        '''
        replaces the variabes <vars> in command cell of the excel
        with the values defined in properties file
        ARGUMENTS:
        command: variable from command column
        RETURNS:
        command_with_replacedvalue: command string with replaced values
        '''
        command_with_replacedvalue = command
        list_search = re.findall(self.search_literal, command_with_replacedvalue)
        list_to_replace = [s[1:] for s in list_search]
        for index, elem in enumerate(list_to_replace):
            if  os.environ.get(elem):
                command_with_replacedvalue = command_with_replacedvalue.replace('<' + elem.upper() + '>', os.environ.get(elem))
            else:
                value_to_replace = self.findInProperties(elem.upper())
                if value_to_replace != "":
                    command_with_replacedvalue = command_with_replacedvalue.replace('<' + elem.upper() + '>', value_to_replace)
                else:
                    fail_msg = elem.upper() + " not found in export variable and properties file. Fix test data."
                    self.fail(fail_msg)
            list_search = re.findall(self.search_literal, command_with_replacedvalue)  #get updated list
            list_to_replace = [s[1:] for s in list_search]
        return command_with_replacedvalue

    ########################################################
    def findInProperties(self, key_to_find):
        '''
        finds value of the key provided in argument
        ARGUMENTS:
        key_to_find: string key from properties file
        RETURNS:
        key_value: value of th key
        '''
        key_value = ""
        for each_section in self.config.sections():
            for (each_key, each_val) in self.config.items(each_section):
                if each_key.upper() == key_to_find:
                    key_value = each_val
        return key_value

    ########################################################
    def replaceVarFile(self, file_detail):
        '''
        replaces variables in the sripts used in command column
        ARGUMENTS:
        file: file name
        '''
        file_name = "scripts/" + file_detail
        finput = fileinput.input(file_name)
        for line in finput:
            list_search = re.findall(self.search_literal, line)
            list_to_replace = [s[1:] for s in list_search]
            for index, elem in enumerate(list_to_replace):
                if  os.environ.get(elem):
                    try:
                        result = subprocess.call(['sed -i "s+<' + elem.upper() + '>+' + os.environ.get(elem) + '+g" ' + file_name + ''], shell=True)
                    except subprocess.CalledProcessError as e:
                        result = str(e.output)
                        print("output: " + result.decode('utf-8'))
                else:
                    value_to_replace = self.findInProperties(elem.upper())
                    if value_to_replace != "":
                        try:
                            result = subprocess.call(['sed -i "s+<' + elem.upper() + '>+' + value_to_replace + '+g" ' + file_name + ''], shell=True)
                        except subprocess.CalledProcessError as e:
                            result = str(e.output)
                            print("output: " + result.decode('utf-8'))
                    else:
                        fail_msg = elem.upper() + " not found in export variable and properties file. Fix test data."
                        self.fail(fail_msg)
            list_search = re.findall(self.search_literal, line)    #get updated list after changes
            list_to_replace = [s[1:] for s in list_search]
        finput.close()  #close fileinput object
########################################################
    def getRownoTestcase(self, sheet, testname):
        '''
        gets row number of the testcase
        ARGUMENTS:
        sheet: workbook sheet object
        testname: cellvalue of testnamecolumn
        RETURNS:
        row number of the testcase
        '''
        for rows in range(1, sheet.nrows):
            for cols in range(sheet.ncols):
                if sheet.cell_value(0, cols) == "TestCase" and testname == sheet.cell_value(rows, cols):
                    testcase_row = rows
        return testcase_row
########################################################
    def waitTimeout(self, proc, seconds):
        """Wait for a process to finish, or raise exception after timeout"""
        start = time.time()
        end = start + seconds
        interval = min(seconds / self.calc_milli_seconds, self.min_get_seconds)

        while True:
            result = proc.poll()
            if result is not None:
                return result
            if time.time() >= end:
                raise RuntimeError("Process timed out in " + str(seconds) + " seconds")
            time.sleep(interval)

########################################################
    @allure.step("Verify cli")    
    def validate(self, method_name, excel_with_tests):
        """ CLI testcase validation"""
        wb = xlrd.open_workbook(excel_with_tests)
        sheet = wb.sheet_by_index(0)
        testcasename = method_name._testMethodName.split("test_")[1]    #process testcase name from the runtime method
        print("started execution of " + testcasename)
        fail_ctr = 0
        fail_msg = ""
        expected_output = list()
        str_expected_output_singlerow = list()
        self.findDuplicatesInColumns(sheet)  #validate excel_with_tests excel to avoid duplicate testcases. On duplicate exit
        testcase_row = self.getRownoTestcase(sheet, testcasename)    #get rowno to read other columns for the testcase called
        list_script_files = os.listdir(self.dir_script)
        # replace environment and properties variables
        for idx, file_name in enumerate(list_script_files):
            print("replacing " + str(file_name))
            self.replaceVarFile(file_name)  #replace in any bash file used in scripts/ folder

        # get data with column name
        for cols in range(sheet.ncols):
            # read testcase command cell for the current testcase
            if sheet.cell_value(0, cols) == "Command to execute":
                testcase_command = sheet.cell_value(testcase_row, cols)
            # create list if multiple columns for expected columns are available
            if "Expected" in sheet.cell_value(0, cols):
                expected_output.append(str(sheet.cell_value(testcase_row, cols)))

        #replace variable in command with values given in properties file
        command_with_replacedvalue = self.replaceVarCommand(testcase_command)
        print("-->"+command_with_replacedvalue)
        # execute command/cli given in commands columns
        try:
            p_result = subprocess.Popen(command_with_replacedvalue, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            timeout = self.findInProperties("TIMEOUT")
            self.waitTimeout(p_result, float(timeout))   #check for timeout in seconds
            result, error = p_result.communicate()
            # capture traceback errors
            if error:
                result = error
            #check for user error, if no expected output in excels, exit with error
            empty = 0
            for idx, expected_value in enumerate(expected_output):
                if expected_value.strip():
                    if expected_value and expected_value.strip():  # checkif any of the expected column is blank
                        if str(expected_value).upper() == "BLANK" and result.decode('utf-8') == "":   #check for null output if any
                            allure.attach( 'output', "Command executed '" + command_with_replacedvalue +"'\n\nExpected value: " + expected_value + "\n\nActual: " + str(result.decode("utf-8")), type=AttachmentType.TEXT)
                            pass
                        elif str(expected_value) in str(result.decode('utf-8')):  #check expected output with command output
                            allure.attach( 'output', "Command executed '" + command_with_replacedvalue +"'\n\nExpected value: " + expected_value + "\n\nActual: " + str(result.decode("utf-8")), type=AttachmentType.TEXT)
                            pass
                        else:
                            fail_ctr += 1
                            fail_msg = fail_msg + "Command executed '" + command_with_replacedvalue +"'\n\nExpected value:" + expected_value + "\n\nActual: " + str(result.decode("utf-8"))
                else:
                    empty += 1
            # exit is tester donot specify expected result in test data excel
            if empty == len(expected_output):
                fail_ctr += 1
                fail_msg = fail_msg + "Test Failed \n \n Expected Output not set in TestData excel for the command " + command_with_replacedvalue
        except subprocess.CalledProcessError as e:
            result = str(e.output)
            print("excep " + result)
            print("output: " + result.decode('utf-8'))
            fail_ctr += 1
            fail_msg = fail_msg + "Test Failed \n \n Actual: " + result.decode('utf-8')

        #mark test failure
        if fail_ctr != 0:
            self.fail("Test Failed \n" + fail_msg)
        else:
            pass
###########################################################
