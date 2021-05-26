apt-get install -y allure
allure-2.10.0/bin/allure generate /home/hcaptest/hcap-test/code/cli_testing/uireports
cd allure-report
cp /home/hcaptest/hcap-test/code/cli_testing/uireports/*testsuite.xml /home/hcaptest/hcap-test/code/allure-reportecho "Executing PostScript"
cd /home/hcaptest/hcap-test/code
apt-get install -y allure
allure-2.10.0/bin/allure generate /home/hcaptest/hcap-test/code/cli_testing/uireports
cd allure-report
cp /home/hcaptest/hcap-test/code/cli_testing/uireports/*testsuite.xml /home/hcaptest/hcap-test/code/allure-report