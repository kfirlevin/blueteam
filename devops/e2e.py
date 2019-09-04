#!/bin/python
from datetime import datetime 
import os
os.system('export URI=http://blue.develeap.com:8080/ && pytest ../providers > errorLog.txt')
os.system('export URI=http://blue.develeap.com:8090/ && pytest ../weight > errorLog2.txt')
