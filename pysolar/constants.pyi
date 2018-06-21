# Stubs for pysolar.constants (Python 3.6)

from typing import Dict, List, Tuple

aberration_coeffs: Dict[str,float]

def get_aberration_coeffs() -> Dict[str,float]: ...

earth_radius: float
earth_axis_inclination: float
seconds_per_day: int
standard_pressure: float
standard_temperature: float
celsius_offset: float
earth_temperature_lapse_rate: float
air_gas_constant: float
earth_gravity: float
earth_atmosphere_molar_mass: float
aberration_sin_terms: List[Tuple[float, float, float, float, float]]
nutation_coefficients: List[Tuple[float, float, float, float]]
heliocentric_longitude_coeffs: List[List[Tuple[float, float, float]]]
heliocentric_latitude_coeffs: List[List[Tuple[float, float, float]]]
sun_earth_distance_coeffs: List[List[Tuple[float, float, float]]]
