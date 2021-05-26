#!/bin/sh
# This script is used as prescript command for executing functional testcses in REAN Test
echo "Install Python Prequsites"
echo "Install Java"
sudo yum install java-1.6.0-openjdk-devel
sudo yum update
echo "======== Installing allure =========="
wget https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.10.0/allure-commandline-2.10.0.zip
unzip allure-commandline-2.10.0.zip
echo "========unzipped allure=========="
export PATH=$PATH:/home/ec2-user/testnow/code/allure-2.10.0/bin/
sudo yum update
sudo yum -y install epel-release
curl -L https://raw.github.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile
source ~/.bash_profile
sudo yum install python3 -y
pyenv install 3.7.6
pyenv local 3.7.6
cd /home/ec2-user/testnow/code/
echo "========setup virtual environment=========="
virtualenv testenv -p /usr/bin/python3.6
. testenv/bin/activate
cd cli_testing/
echo "========Rean Test CLI Env Ready to Perform=========="
pip install -r requirements.txt -t .
pip install gnureadline
pip install pytest==3.10.1
pip install pytest-allure-adaptor
pip install --upgrade pip
echo "========pip installation finish=========="
