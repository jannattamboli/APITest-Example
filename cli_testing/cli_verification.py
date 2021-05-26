
"""CLI Automation Framework"""
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

import xlrd
from utils.utility import Utility
from conftest import option

instance = Utility()

excel_with_tests = option.excelname


class CliTests(Utility):
    '''
    CLI Automation framework validation
    This test suite reads testcases from excel and performs tests
    '''

    def verifyCLI(self):
        """ CLI tests execution"""
        # declare variables
        wb = xlrd.open_workbook(excel_with_tests)  # excel_with_tests excel read from testdata.properties
        sheet = wb.sheet_by_index(0)
        testcase_name = ""
        for rows in range(1, sheet.nrows):
            for cols in range(sheet.ncols):
                if sheet.cell_value(0, cols) == "TestCase":  # read TestCase names
                    testcase_name = sheet.cell_value(rows, cols)
            l_testname = str(testcase_name)

            # add run timemethods to the class with test_<testname>
            setattr(CliTests, "test_" + testcase_name, lambda l_testname: instance.validate(l_testname, excel_with_tests))

# create object of the class


executeCLI = CliTests()
executeCLI.verifyCLI()
###########################################################
