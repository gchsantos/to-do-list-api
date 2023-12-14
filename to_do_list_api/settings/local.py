import os
from to_do_list_api.settings.base import *

DEBUG = True
BASE_DIR = os.path.dirname(os.path.realpath(os.path.dirname(__file__) + "/.."))
CACHE_TTL = 60
