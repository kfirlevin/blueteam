import logging
import datetime
import sys,os
import inspect


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
        print(msg)
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
        print(msg)
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
        print(msg)
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
        print(msg)
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

