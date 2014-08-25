import importlib
_solar = importlib.import_module(".solar", __package__)
_solar.util.solar = _solar

from .solar import *

del importlib
