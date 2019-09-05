#!/bin/python
import telebot
import datetime
import subprocess

# czdvf


def testresult(providers, weight):
    if providers == 0 and weight == 0:
        telebot.sendMessage("Push was tested successfully - {}".format(
            datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
        return "True"
    else:
        telebot.parse_files('providers.txt', 'weight.txt')
        return "False"


providers = subprocess.Popen('./prov.sh')
weight = subprocess.Popen('./weight.sh')
print(testresult(providers, weight))
