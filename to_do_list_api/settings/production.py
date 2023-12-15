import os

from to_do_list_api.settings.base import *

# Initialise environment variables
DEBUG = False
ALLOWED_HOSTS = ["localhost"]
BASE_DIR = os.path.dirname(os.path.realpath(os.path.dirname(__file__) + "/.."))
CACHE_TTL = 30 #60 * 15 I set the TTL to 30 seconds to validate the data