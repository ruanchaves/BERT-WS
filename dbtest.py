from database import Record, Logger

logger = Logger()
logger.add({'application' : 'testing', 'category': 'test', 'data': 'world'})