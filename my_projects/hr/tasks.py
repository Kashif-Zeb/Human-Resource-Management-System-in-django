from celery import shared_task
import os 
from celery.utils.log import get_task_logger
fullpath = os.path.join(os.path.dirname(__file__),"uploads")
if not os.path.exists(fullpath):
    os.makedirs(fullpath)
logger = get_task_logger(__name__)
@shared_task(ignore_result=True)
def file(data):
    print("hellllloooooooooooooooooooo")
    logger.info("hiiiiiiiiiiiiiiiiiiiiiiiiii")
    path = fullpath+"/file3.txt"
    with open(path,"w+") as f:
        print("writing the data in file")
        f.write(str(data))
        f.close()

#  celery -A my_projects worker --loglevel=info