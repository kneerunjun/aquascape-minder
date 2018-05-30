#!/bin/sh
sudo cp ./minder.service /etc/systemd/system/minder.service
sudo systemctl enable minder.service
