#!/bin/sh
# This script is used as postscript command for deleting data from instance and create reports in REAN Test
echo "Executing PostScript"
rm -rf  /home/ec2-user/.aws/credentials
rm -rf /tmp/cli_testdata/provider_details.json
rm -rf /tmp/cli_testdata/basic_cred.json
rm -rf /tmp/cli_testdata/urltest_jobid.txt
cd /home/ec2-user/testnow/code
allure generate /home/ec2-user/testnow/code/cli_testing/uireports
mv allure-report /home/ec2-user/testnow/code/allure-report

