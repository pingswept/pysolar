from functools import wraps
import inspect



class NoTimeZoneInfoError(ValueError):
  def __init__(self, argname, dt, *args):
    self.argname = argname
    self.dt = dt
    super().__init__(*args)
    
  def __str__(self):
    return """datetime value '{dt}' given for arg '{argname}' \
should be made timezone-aware.
You have to specify the 'tzinfo' attribute of \
'datetime.datetime' objects.""".format(dt=self.dt, 
                                       argname=self.argname)


def check_aware_dt(*argnames):
  def checker(func):
    @wraps(func)
    def func_with_check(*args, **kwargs):
      for argname in argnames:
        # first checking if argname is a valid arg name
        full = inspect.getfullargspec(func)
        if (argname in full.args or 
            argname in full.kwonlyargs):
          # getting value given for argname
          try:
            dt = args[full.args.index(argname)]
          except (IndexError, ValueError):
            dt = kwargs[argname]
          # checking if dt is timezone-aware
          if not hasattr(dt, 'tzinfo'):
            raise ValueError(
              "Expected a 'datetime.datetime' object \
  for arg '%s', got %s instead" % (argname, dt))
          if dt.tzinfo is None:
            raise NoTimeZoneInfoError(argname, dt)
      return func(*args, **kwargs)
    return func_with_check
  return checker