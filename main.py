import logging.config
import queue

import uvicorn
from src.api import app
from src.core.config import settings

queue_list = queue.Queue()
logging.config.dictConfig(settings.logs.get_log_config)
logger = logging.getLogger('app')
root_handler = list(logger.handlers)[0]
logger.removeHandler(root_handler)
logger.addHandler(logging.handlers.QueueHandler(queue_list))
listener = logging.handlers.QueueListener(queue_list, root_handler)
listener.start()

if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000)
