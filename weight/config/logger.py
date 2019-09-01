import logging
import datetime
import sys,os
import inspect

'''
usage: 
import the logger class : import logger 
make instance of logger : log = logger.Logger()

log.LogDebug(caller,message)

caller  : where it was called from (file,function)
message : your action (api req/res, attempts db connection)

levels: 
*debug* - for dev team to log debug stuff
command : log.LogDebug("api/weight","testing stuff")
output  : [2019-09-01 02:36:48,234] caller : api/weight | level - DEBUG : testing stuff

*info* - log incoming/outgoing requests
command : log.LogInfo("api/weight","log inc data")
output  : [2019-09-01 02:36:48,234] caller : api/weight | level - INFO : log inc data

*error* - low risk error
command : log.LogError("api/weight","try parsing string to int")
output  : [2019-09-01 02:36:48,237] caller : api/weight | level - ERROR : try parsing string to int

*critical* - high risk error 
command : a.LogCritical("api weight","attempt db connection")
output  : [2019-09-01 02:36:48,237] caller : api weight | level - CRITICAL : AT /home/aweds/Desktop/develeap/task/blueteam/weight/config/logger.py attempt db connection

IMPORTANT : critical log shows dir of file that failed the action
'''


class DebugLog:
    def __init__(self,caller):
        self.logger = logging.getLogger(caller)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('[%(asctime)s] caller : %(name)s | level - %(levelname)s : %(message)s')

        self.fh = logging.FileHandler(f'../logs/DEBUG.log')
        self.fh.setLevel(logging.DEBUG)
        self.fh.setFormatter(self.formatter)

        self.sh = logging.StreamHandler(sys.stdout)
        self.sh.setLevel(logging.DEBUG)
        self.sh.setFormatter(self.formatter)

        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.sh)

    def log(self,msg):
        self.logger.debug(msg)

class InfoLog:
    def __init__(self,caller):
        self.logger = logging.getLogger(caller)
        self.logger.setLevel(logging.INFO)
        self.formatter = logging.Formatter('[%(asctime)s] caller : %(name)s | level - %(levelname)s : %(message)s')

        self.fh = logging.FileHandler(f'../logs/INFO.log')
        self.fh.setLevel(logging.INFO)
        self.fh.setFormatter(self.formatter)

        self.sh = logging.StreamHandler(sys.stdout)
        self.sh.setLevel(logging.INFO)
        self.sh.setFormatter(self.formatter)

        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.sh)

    def log(self,msg):
        self.logger.info(msg)

class ErrorLog:
    def __init__(self,caller):
        self.logger = logging.getLogger(caller)
        self.logger.setLevel(logging.ERROR)
        self.formatter = logging.Formatter('[%(asctime)s] caller : %(name)s | level - %(levelname)s : %(message)s')

        self.fh = logging.FileHandler(f'../logs/ERROR.log')
        self.fh.setLevel(logging.ERROR)
        self.fh.setFormatter(self.formatter)

        self.sh = logging.StreamHandler(sys.stderr)
        self.sh.setLevel(logging.ERROR)
        self.sh.setFormatter(self.formatter)

        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.sh)

    def log(self,msg):
        self.logger.error(msg)

class CriticlLog:
    def __init__(self,caller):
        self.logger = logging.getLogger(caller)
        self.logger.setLevel(logging.CRITICAL)
        self.formatter = logging.Formatter('[%(asctime)s] caller : %(name)s | level - %(levelname)s : AT %(pathname)-16s %(message)s')

        self.fh = logging.FileHandler(f'../logs/CRITICAL.log')
        self.fh.setLevel(logging.CRITICAL)
        self.fh.setFormatter(self.formatter)

        self.sh = logging.StreamHandler(sys.stderr)
        self.sh.setLevel(logging.CRITICAL)
        self.sh.setFormatter(self.formatter)

        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.sh)

    def log(self,msg):
        self.logger.critical(msg)


class Logger:

    def LogDebug(self,caller,msg):
        DebugLog(caller).log(msg)

    def LogInfo(self,caller,msg):
        InfoLog(caller).log(msg)

    def LogError(self,caller,msg):
        ErrorLog(caller).log(msg)
        
    def LogCritical(self,caller,msg):
        CriticlLog(caller).log(msg)

