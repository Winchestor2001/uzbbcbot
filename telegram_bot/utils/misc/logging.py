import logging
from environs import Env

env = Env()
env.read_env()

logging.basicConfig(filename=env.str('BOT_LOG_PATH'),format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    # level=logging.DEBUG,  # Можно заменить на другой уровень логгирования.
                    )
