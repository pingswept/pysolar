#!/usr/bin/python

coeff_list = [
		('ArgumentOfLatitudeOfMoon', (93.27191, 483202.017538, -0.0036825, 327270.0)),
		('LongitudeOfAscendingNode', (125.04452, -1934.136261, 0.0020708, 450000.0)),
		('MeanElongationOfMoon', (297.85036, 445267.111480, -0.0019142, 189474.0)),
		('MeanAnomalyOfMoon', (134.96298, 477198.867398, 0.0086972, 56250.0)),
		('MeanAnomalyOfSun', (357.52772, 35999.050340, -0.0001603, -300000.0))
	]

def buildPolyFit((a, b, c, d)):
	return (lambda x: a + b * x + c * x ** 2 + (x ** 3) / d)

def buildPolyDict():
	return dict([(name, buildPolyFit(coeffs)) for (name, coeffs) in coeff_list])
