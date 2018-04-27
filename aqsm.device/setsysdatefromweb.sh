#!/bin/sh
# since the entire minder program is based on the system timing we need to get the system date time updated from the internet and hence the below script
sudo date -s "$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z"
