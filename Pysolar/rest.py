from collections import defaultdict

nestable_dict = lambda: defaultdict(nestable_dict)

transmittance = nestable_dict()

transmittance["rayleigh"]["high-frequency"] = lambda m: (1 + 1.8169 * m + 0.033454 * m ** 2)/(1 + 2.063 * m + 0.31978 * m ** 2)
transmittance["rayleigh"]["low-frequency"] = lambda m: (1 - 0.010394 * m)/(1 - 0.00011042 * m ** 2)

transmittance["gas"]["high-frequency"] = lambda m: (1 + 0.95885 * m + 0.012871 * m ** 2)/(1 + 0.96321 * m + 0.015455 * m ** 2)
transmittance["gas"]["low-frequency"] = lambda m: (1 + 0.27284 * m - 0.00063699 * m ** 2)/(1 + 0.30306 * m)

transmittance["ozone"]["high-frequency"] = lambda uo, m: 1 # fake
transmittance["ozone"]["low-frequency"] = lambda uo, m: 1

transmittance["nitrogen_dioxide"]["high-frequency"] = lambda un, m: 1 # fake
transmittance["nitrogen_dioxide"]["low-frequency"] = lambda un, m: 1

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

def GetAerosolForwardScatteranceFactor(altitude_deg):
	Z = 90 - altitude_deg
	return 1 - math.e ** (-0.6931 - 1.8326 * math.cos(math.radians(Z)))

def GetAerosolScatteringCorrectionFactor(band, ma, tau_a):
	if band == "high-frequency":
		g0 = (3.715 + 0.368 * ma + 0.036294 * ma ** 2)/(1 + 0.0009391 * ma ** 2)
		g1 = (-0.164 - 0.72567 * ma + 0.20701 * ma ** 2)/(1 + 0.001901 * ma ** 2)
		g2 = (-0.052288 + 0.31902 * ma + 0.17871 * ma ** 2)/(1 + 0.0069592 * ma ** 2)
		return (g0 + g1 * tau_a)/(1 + g2 * tau_a)
	else:
		h0 = (3.4352 +  0.65267 * ma + 0.00034328 * ma ** 2)/(1 + 0.034388 * ma ** 1.5)
		h1 = (1.231 - 1.63853 * ma + 0.20667 * ma ** 2)/(1 + 0.1451 * ma ** 1.5)
		h2 = (0.8889 - 0.55063 * ma + 0.50152 * ma ** 2)/(1 + 0.14865 * ma ** 1.5)
		return (h0 + h1 * tau_a)/(1 + h2 * tau_a)

def GetRayleighExtinctionForwardScatteringFraction(air_mass, band):
	if band == "high-frequency":
		return 0.5 * (0.89013 - 0.049558 * air_mass + 0.000045721 * air_mass ** 2)
	else
		return 0.5

def GetDiffuseIrradiance():
	return GetDiffuseIrradianceByBand("high-frequency") + GetDiffuseIrradianceByBand("low-frequency")

def GetDiffuseIrradianceByBand(band, air_mass=1.66):
	Z = 90 - altitude_deg
	To =
	Tg =
	Tn =
	Tw =
	Tr =
	Ta =
	Tas =
	Br = GetRayleighExtinctionForwardScatteringFraction(air_mass, layer)
	Ba = GetAerosolForwardScatteranceFactor(altitude_deg)
	F =
	Edp = To * Tg * Tn * Tw * (Br * (1 - Tr) * Ta ** 0.25 + Ba * F * Tr * (1 - Tas ** 0.25)) * E0n[band]
	Edd = rhogi * rhosi * (Eb + Edp)/(1 - rhogi * rhosi)
	return Edp + Edd

def GetDirectNormalIrradiance(air_mass=1.66, pressure_millibars=1013.25, ozone_atm_cm=0.35, nitrogen_atm_cm=0.0002, precipitable_water_cm=5.0, turbidity_alpha=1.3, turbidity_beta=0.6):
	return GetDirectNormalIrradianceByBand("high-frequency") + GetDirectNormalIrradianceByBand("low-frequency")

def GetDirectNormalIrradianceByBand(band, air_mass=1.66, pressure_millibars=1013.25, ozone_atm_cm=0.35, nitrogen_atm_cm=0.0002, precipitable_water_cm=5.0, turbidity_alpha=1.3, turbidity_beta=0.6):

	Tr = transmittance["rayleigh"][band](optical_mass["rayleigh"](pressure_millibars, air_mass))
	Tg = transmittance["gas"][band](optical_mass["rayleigh"](pressure_millibars, air_mass))
	To = transmittance["ozone"][band](ozone_atm_cm, optical_mass["ozone"](pressure_millibars, air_mass))
	Tn = transmittance["nitrogen_dioxide"][band](nitrogen_atm_cm, optical_mass["water"](pressure_millibars, air_mass)) # is water_optical_mass really used for nitrogen calc?
	Tw = transmittance["water"][band](precipitable_water_cm, optical_mass["water"](pressure_millibars, air_mass))
	Ta = transmittance["aerosol"][band](turbidity_alpha, turbidity_beta, optical_mass["aerosol"](pressure_millibars, air_mass))
	return E0n[band] * Tr * Tg * To * Tn * Tw * Ta

def GetGlobalIrradiance(direct_normal_irradiance, altitude_deg, diffuse_irradiance):
	Z = 90 - altitude_deg
	return direct_normal_irradiance * math.cos(math.radians(Z)) + diffuse_irradiance
