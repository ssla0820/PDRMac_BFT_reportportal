#SubDirectory
import os,sys

if sys.version_info < (3,8):
    input(f"Python version must > 3.8\n")
    os._exit(1)


#Modules
from os.path import dirname, basename, isfile
# import glob
# modules = glob.glob(dirname(__file__)+"/*.py")
# __all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
# from . import *

from .initial import initialChrome as initial_chrome
from .initial import require_adm
from .initial import Protocol
from ._report.report import MyReport
from ._report.report import logger
from ._report.google_service import Google_sheet
from ._wrapper.page import Host,Participant