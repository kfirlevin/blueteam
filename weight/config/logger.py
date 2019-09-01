import logging
import datetime
#logging.basicConfig(filename='test.log',filemode='w',format=f'{str(datetime.datetime.now())[:19]}')
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] user : %(name)s level : %(levelname)s : %(message)s')

handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logger.debug('often makes a very good meal of %s', 'test')