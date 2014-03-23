from collections import defaultdict

nestable_dict = lambda: defaultdict(nestable_dict)

transmittance = nestable_dict()

transmittance["rayleigh"]["high-frequency"] = lambda m: (1 + 1.8169 * m + 0.033454 * m)/(1 + 2.063 * m + 0.31978 * m ** 2)
transmittance["rayleigh"]["low-frequency"] = lambda m: (1 - 0.010394 * m)/(1 - 0.00011042 * m ** 2)

transmittance["gas"]["high-frequency"] = lambda x: 1 # fake
transmittance["gas"]["low-frequency"] = lambda x: 1 # fake

transmittance["ozone"]["high-frequency"] = lambda o, m: 1 # fake
transmittance["ozone"]["low-frequency"] = lambda o, m: 1

transmittance["nitrogen_dioxide"]["high-frequency"] = lambda n, m: 1 # fake
transmittance["nitrogen_dioxide"]["low-frequency"] = lambda n, m: 1

transmittance["water"]["high-frequency"] = lambda w, m: 1 # fake
transmittance["water"]["low-frequency"] = lambda w, m: 1 # fake

transmittance["aerosol"]["high-frequency"] = lambda a, b, m: 1 # fake
transmittance["aerosol"]["low-frequency"] = lambda a, b, m: 1 # fake

optical_mass = {}

optical_mass["rayleigh"] = lambda p, m: m
optical_mass["ozone"] = lambda p, m: m
optical_mass["water"] = lambda p, m: m
optical_mass["aerosol"] = lambda p, m: m


E0n = {"high-frequency": 635.4, # extra-atmospheric irradiance, 290-700 nm (UV and visible)
       "low-frequency":  709.7} # extra-atmospheric irradiance, 700-4000 nm (short infrared)

def GetGlobalIrradiance(direct_normal_irradiance, altitude_deg, diffuse_irradiance):
	return direct_normal_irradiance * math.cos(math.radians(90 - altitude_deg)) + diffuse_irradiance

def GetDirectNormalIrradianceByBand(band, air_mass=1.66, pressure_millibars=1013.25, ozone_atm_cm=0.35, nitrogen_atm_cm=0.0002, precipitable_water_cm=5.0, turbidity_alpha=1.3, turbidity_beta=0.6):

	Tr = transmittance["rayleigh"][band](optical_mass["rayleigh"](pressure_millibars, air_mass))
	Tg = transmittance["gas"][band](optical_mass["rayleigh"](pressure_millibars, air_mass))
	To = transmittance["ozone"][band](ozone_atm_cm, optical_mass["ozone"](pressure_millibars, air_mass))
	Tn = transmittance["nitrogen_dioxide"][band](nitrogen_atm_cm, optical_mass["water"](pressure_millibars, air_mass)) # is water_optical_mass really used for nitrogen calc?
	Tw = transmittance["water"][band](precipitable_water_cm, optical_mass["water"](pressure_millibars, air_mass))
	Ta = transmittance["aerosol"][band](turbidity_alpha, turbidity_beta, optical_mass["aerosol"](pressure_millibars, air_mass))
	return E0n[band] * Tr * Tg * To * Tn * Tw * Ta

def GetDirectNormalIrradiance(air_mass=1.66, pressure_millibars=1013.25, ozone_atm_cm=0.35, nitrogen_atm_cm=0.0002, precipitable_water_cm=5.0, turbidity_alpha=1.3, turbidity_beta=0.6):
	return GetDirectNormalIrradianceByBand("high-frequency") + GetDirectNormalIrradianceByBand("low-frequency")
