#!/bin/sh
sudo cp ./minder.service /etc/systemd/system/minder.service
sudo cp ./minder.gov.service /etc/systemd/system/minder.gov.service
sudo systemctl enable minder.service
sudo systemctl enable minder.gov.service
