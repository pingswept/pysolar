import importlib
_solar = importlib.import_module(".solar", __package__)
_constants = importlib.import_module(".constants", __package__)
_solar.util.solar = _solar
_solar.util.constants = _constants

from .solar import *

del importlib
