#!/bin/python
import os

def testresult(providers, weight):
    if providers == 0 and weight == 0:
        return "True"
    else:
        # send to telegram the files
        # telebot.send(provfile, weightfile)
        return "False"

providers = os.system('export URI=http://blue.develeap.com:8080/ && pytest ../providers > providers.txt')
weight = os.system('export URI=http://blue.develeap.com:8090/ && pytest ../weight > weight.txt')
testresult(providers, weight)
