import os

from to_do_list_api.settings.base import *

# Initialise environment variables
DEBUG = False
ALLOWED_HOSTS = ["localhost"]
BASE_DIR = os.path.dirname(os.path.realpath(os.path.dirname(__file__) + "/.."))
CACHE_TTL = 60 * 15