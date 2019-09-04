#!/bin/python
import os
import telebot


def testresult(providers, weight):
    if providers == 0 and weight == 0:
        return "True"
    else:
        telebot.parse_files('providers.txt', 'weight.txt')
        return "False"


providers = os.system(
    'export URI=http://blue.develeap.com:8081/ && pytest ../../providers > providers.txt')
weight = os.system(
    'export URI=http://blue.develeap.com:8082/ && pytest ../../weight > weight.txt')
print(testresult(providers, weight))
