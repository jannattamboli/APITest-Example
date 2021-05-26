#!/bin/sh
echo "Install Python Prequsites"
apt-get update -y
apt-get install -y wget
dpkg -l | grep wget
apt-get install -y unzip
wget https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.10.0/allure-commandline-2.10.0.zip
unzip allure-commandline-2.10.0.zip
export PATH=$PATH:/home/seluser/hcap-test/code/allure-2.10.0/bin/
cd cli_testing/
apt-get update
export DEBIAN_FRONTEND=noninteractive
apt install  -y software-properties-common
apt install -y python-software-properties
add-apt-repository ppa:deadsnakes/ppa
apt update -y
apt install -y python3.6
apt-get install -y python3-pip
pip3 uninstall -y enum
pip3 uninstall -y enum34
pip3 install virtualenv
virtualenv -p python3.6 testenv
source testenv/bin/activate
pip3 uninstall -y enum
pip3 uninstall -y enum34
pip3 install pytest>=3.3.0
pip3 install requests>=2.18.4
pip3 install unittest2>=1.1.0
pip3 install awscli
pip3 install xlrd==1.2.0
pip3 install pytest-excel==1.2.2
pip3 install gnureadline
pip3 install  pytest-allure-adaptor
pip3 install --no-cache-dir reanplatform-cli --index-url https://preetika.ravkhande:AKCp5bC1xwUZbw2GcQJ1rpbt2Qq1GQ1SapokpTg9i8bfBPvgoxxW5V7v2UWrguXgF9QrzfSfU@artifactory.prod.platform.reancloud.com/artifactory/api/pypi/virtual-qa-pypi/simple
echo "Rean Test CLI Automation"
pip3 list |  grep reanplatform-cli
export PLATFORM_BASE_URL=https://hcap.hcapekstest.itsreaning.com/;
export USERNAME="jannat";
export PASSWORD="Jannat@123";
export GIT_USER=pravkhande;
export GIT_PASS=Pikatika@123;
export ADMIN_USER=admin;
export ADMIN_PASS=admin;
export USER_TO_SEARCH=shruti;
export PEM_FILE_PATH_NAME=/tmp/jannat-govcloud.pem;
export TEST_URL=http://www.google.com;
export SECURITY_TEST_URL=http://help.websiteos.com/;
export CROSS_BROWSER_TEST_URL=https://hcap.hcapekstest.itsreaning.com/;
export CHROME_BROWSER1=83;
export CHROME_BROWSER2=81;
export FIREFOX_BROWSER=76;
export PLATFORM_IP=10.64.7.41;
export PAGE_TIME_OUT=20;
export USER_ID=2;
