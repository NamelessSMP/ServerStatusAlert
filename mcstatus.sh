#!/bin/bash

screen -A -d -m -S mcstatus bash -c "source .venv/mcstatus/bin/activate && python ServerStatusAlert.py"
sleep 0.2 && screen -x mcstatus
