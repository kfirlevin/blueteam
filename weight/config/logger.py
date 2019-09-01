import logging
import datetime

class Logger:
    formatter = logging.Formatter('[%(asctime)s] caller : %(name)s | level - %(levelname)s : %(message)s')
    def __init__(self):
        pass

class DebugLog(Logger):
    def __init__(self,caller):
        self.logger = logging.getLogger(caller)
        self.logger.setLevel(logging.DEBUG)

        self.Debuglogger = logging.FileHandler('../logs/DEBUG.log')
        self.Debuglogger.setLevel(logging.DEBUG)

        self.formatter = Logger.formatter
        self.Debuglogger.setFormatter(self.formatter)

        self.logger.addHandler(self.Debuglogger)

    def log(self,msg):
        print(msg)
        self.logger.debug(msg)

        
a = DebugLog('some api')
a.log('test2')


#logger = logging.getLogger('spam_application')
#logger.setLevel(logging.DEBUG)#

#fh = logging.FileHandler('spam.log')
#fh.setLevel(logging.DEBUG)

#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#fh.setFormatter(formatter)

#logger.addHandler(fh)


#logger.info('creating an instance of auxiliary_module.Auxiliary')

#logger.info('created an instance of auxiliary_module.Auxiliary')
#logger.info('calling auxiliary_module.Auxiliary.do_something')
#logger.error('asdasd')
#logger.info('finished auxiliary_module.Auxiliary.do_something')
#logger.info('calling auxiliary_module.some_function()')

#logger.info('done with auxiliary_module.some_function()')