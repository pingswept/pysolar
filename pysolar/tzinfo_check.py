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
  """Returns a decorator that makes sure that
  all the arguments in 'argnames', are 'datetime.datetime' objects
  with a non-null tzinfo attribute

  Parameters
  ----------
  argnames : List[str]
    list of names from the arguments of function 'func'
    (the decorated function) that are supposed to only accept
    as values 'datetime.datetime' objects
    with a non-null tzinfo attribute

  Returns
  -------
  checker : function
    decorator that makes sure that every argument of the decorated
    function that is in 'argnames' is given only 'datetime.datetime' objects
    with non-null tzinfo attribute as values"""
  def checker(func):
    """Decorator (see above in the `Returns` section)

    Parameters
    ----------
    func : function
      decorated function
      every argument of 'func' that is in argnames
      will only accept tz-aware 'datetime' objects

    Returns
    -------
    func_with_check : function
      decorated function, basically the same function as 'func',
      with the check for tz-awareness performed before execution"""
    @wraps(func)
    def func_with_check(*args, **kwargs):
      """Decorated function ; will be, apart from the check,
      completely identical to the 'func' function
      We search for 'argnames' values in args and kwargs

      Parameters
      ----------
      args : list
        list of positional arguments that are supposedly
        passed to the 'func' function
      kwargs : dict
        dict of keyword arguments that are supposedly passed
        to the 'func' function

      Returns
      -------
      func(*args, **kwargs)
        we return the very same result that would have been returned
        by the 'func' function alone
        we just checked the values of args from argnames before"""
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
          if not hasattr(dt, 'shape'):   # don't raise Exception if dt is an array (assumed of datetime64)
            if not hasattr(dt, 'tzinfo'):
              raise ValueError(
                "Expected a 'datetime.datetime' object \
    for arg '%s', got %s instead" % (argname, dt))
            if dt.tzinfo is None:
              raise NoTimeZoneInfoError(argname, dt)
      return func(*args, **kwargs)
    return func_with_check
  return checker
