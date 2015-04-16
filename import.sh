#!/bin/bash

nohup python local_import.py > import-log/import.`date +%Y-%m-%d_%H-%M-%S` 2>&1 &
exit 0
