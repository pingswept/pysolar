# Stubs for pysolar.simulate (Python 3.6)

import datetime
from typing import Iterator, List, Tuple

def datetime_range(start_datetime:datetime.datetime, end_datetime:datetime.datetime, step_minutes:float) -> Iterator[datetime.datetime]: ...
def simulate_span(latitude_deg:float, longitude_deg:float, horizon:List[float], start_datetime:datetime.datetime, end_datetime:datetime.datetime, step_minutes:float, elevation:float = ..., temperature:float = ..., pressure:float = ...) -> Iterator[Tuple[datetime.datetime, float, float, float, float]]: ...  # TODO unclear what horizon is, and never used in the code
