#!/bin/bash
apt-get update -y && apt-get install wget gnupg pip python3.10 -y
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
apt-get update -y
apt-get install google-chrome-stable -y


