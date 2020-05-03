#    Copyright Brandon Stafford
#
#    This file is part of Pysolar.
#
#    Pysolar is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    Pysolar is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with Pysolar. If not, see <http://www.gnu.org/licenses/>.

# Disable linting as this is a work in progress
# flake8: noqa

from . import numeric as math
from .constants import standard_pressure

# single-scattering albedo used to calculate aerosol scattering transmittance;
# not used for sky or ground albedo for backscattering estimate
albedo = {}

albedo["high-frequency"] = 0.92
albedo["low-frequency"] = 0.84
standard_pressure_millibars = standard_pressure / 100
un = 0.0003  # atm*cm, from [Gueymard 2008], p. 280

E0n = {"high-frequency": 635.4,  # extra-atmospheric irradiance, 290-700 nm (UV and visible)
       "low-frequency":  709.7}  # extra-atmospheric irradiance, 700-4000 nm (short infrared)


def get_aerosol_forward_scatterance_factor(altitude_deg):
    Z = 90 - altitude_deg
    return 1 - math.e ** (-0.6931 - 1.8326 * math.cos(math.radians(Z)))


def get_aerosol_optical_depth(turbidity_beta, effective_wavelength, turbidity_alpha):
    # returns tau_a
    return turbidity_beta * effective_wavelength ** -turbidity_alpha

def get_aerosol_scattering_correction_factor(band, ma, tau_a):
    # returns F
    if band == "high-frequency":
        g0 = (3.715 + 0.368 * ma + 0.036294 * ma ** 2) / \
            (1 + 0.0009391 * ma ** 2)
        g1 = (-0.164 - 0.72567 * ma + 0.20701 * ma ** 2) / \
            (1 + 0.001901 * ma ** 2)
        g2 = (-0.052288 + 0.31902 * ma + 0.17871 * ma ** 2) / \
            (1 + 0.0069592 * ma ** 2)
        return (g0 + g1 * tau_a) / (1 + g2 * tau_a)
    else:
        h0 = (3.4352 + 0.65267 * ma + 0.00034328 * ma ** 2) / \
            (1 + 0.034388 * ma ** 1.5)
        h1 = (1.231 - 1.63853 * ma + 0.20667 * ma ** 2) / \
            (1 + 0.1451 * ma ** 1.5)
        h2 = (0.8889 - 0.55063 * ma + 0.50152 * ma ** 2) / \
            (1 + 0.14865 * ma ** 1.5)
        return (h0 + h1 * tau_a) / (1 + h2 * tau_a)


def get_aerosol_transmittance(band, ma, tau_a):
    # returns Ta
    return math.exp(-ma * tau_a)


def get_aerosol_scattering_transmittance(band, ma, tau_a):
    # returns Tas
    return math.exp(-ma * albedo[band] * tau_a)

def get_backscattered_diffuse_broadband_irradiance(band, turbidity_alpha=1.3, turbidity_beta=0.6):
    return get_backscattered_diffuse_broadband_irradiance_by_band("high-frequency", turbidity_alpha, turbidity_beta) + get_backscattered_diffuse_broadband_irradiance_by_band("low-frequency", turbidity_alpha, turbidity_beta)

def get_backscattered_diffuse_irradiance_by_band(band, Ebi, Edpi, turbidity_alpha=1.3, turbidity_beta=0.6):
    rhos = get_sky_albedo(band, turbidity_alpha, turbidity_beta)
    rhog = get_ground_albedo(band)
    Eddi = rhog * rhos * (Ebi + Edpi) / (1 - rhog * rhos)
    return Eddi


def get_beam_broadband_irradiance(altitude_deg, pressure_millibars=standard_pressure_millibars, ozone_atm_cm=0.35, nitrogen_atm_cm=0.0002, precipitable_water_cm=5.0, turbidity_alpha=1.3, turbidity_beta=0.6):
    Z = 90 - altitude_deg
    Ebn = get_broadband_direct_normal_irradiance(altitude_deg, pressure_millibars, ozone_atm_cm, nitrogen_atm_cm, precipitable_water_cm, turbidity_alpha, turbidity_beta)
    return Ebn * math.cos(math.radians(Z))

def get_beam_irradiance_by_band(band, altitude_deg, pressure_millibars=standard_pressure_millibars, ozone_atm_cm=0.35, nitrogen_atm_cm=0.0002, precipitable_water_cm=5.0, turbidity_alpha=1.3, turbidity_beta=0.6):
    Z = 90 - altitude_deg
    Ebni = get_direct_normal_irradiance_by_band(band, altitude_deg, pressure_millibars, ozone_atm_cm, nitrogen_atm_cm, precipitable_water_cm, turbidity_alpha, turbidity_beta)
    return Ebni * math.cos(math.radians(Z))

def get_diffuse_broadband_irradiance(air_mass=1.66, turbidity_alpha=1.3, turbidity_beta=0.6):
    return get_diffuse_irradiance_by_band("high-frequency", air_mass, turbidity_alpha, turbidity_beta) + get_diffuse_irradiance_by_band("low-frequency", air_mass, turbidity_alpha, turbidity_beta)


def get_diffuse_irradiance_by_band(band, air_mass=1.66, turbidity_alpha=1.3, turbidity_beta=0.6):
    Z = 90 - altitude_deg
    effective_wavelength = get_effective_aerosol_wavelength(band, turbidity_alpha)
    tau_a = get_aerosol_optical_depth(
        turbidity_beta, effective_wavelength, turbidity_alpha)
    ma = get_optical_mass_aerosol(altitude_deg)
    mo = get_optical_mass_ozone(altitude_deg)
    mR = get_optical_mass_rayleigh(altitude_deg, pressure_millibars)

    To = get_ozone_transmittance(band, mo)
    Tg = get_gas_transmittance(band, mR)
    Tn = get_nitrogen_transmittance(band, 1.66)
    Tw = get_water_vapor_transmittance(band, 1.66)
    TR = get_rayleigh_transmittance(band, mR)
    Ta = get_aerosol_transmittance(band, ma, tau_a)
    Tas = get_aerosol_scattering_transmittance(band, ma, tau_a)

    BR = get_rayleigh_extinction_forward_scattering_fraction(band, air_mass)
    Ba = get_aerosol_forward_scatterance_factor(altitude_deg)
    F = get_aerosol_scattering_correction_factor(band, ma, tau_a)

    Edpi = To * Tg * Tn * Tw * \
        (BR * (1 - TR) * Ta ** 0.25 + Ba * F * TR * (1 - Tas ** 0.25)) * \
        E0n[band]
    return Edpi


def get_broadband_direct_normal_irradiance(altitude_deg, pressure_millibars=standard_pressure_millibars, ozone_atm_cm=0.35, nitrogen_atm_cm=0.0002, precipitable_water_cm=5.0, turbidity_alpha=1.3, turbidity_beta=0.6):
    high = get_direct_normal_irradiance_by_band("high-frequency", altitude_deg, pressure_millibars,
                                           ozone_atm_cm, nitrogen_atm_cm, precipitable_water_cm, turbidity_alpha, turbidity_beta)
    low = get_direct_normal_irradiance_by_band("low-frequency", altitude_deg, pressure_millibars,
                                          ozone_atm_cm, nitrogen_atm_cm, precipitable_water_cm, turbidity_alpha, turbidity_beta)
    return high + low


def get_direct_normal_irradiance_by_band(band, altitude_deg, pressure_millibars=standard_pressure_millibars, ozone_atm_cm=0.35, nitrogen_atm_cm=0.0002, precipitable_water_cm=5.0, turbidity_alpha=1.3, turbidity_beta=0.6):
    ma = get_optical_mass_aerosol(altitude_deg)
    mo = get_optical_mass_ozone(altitude_deg)
    mR = get_optical_mass_rayleigh(altitude_deg, pressure_millibars)
    mRprime = mR * pressure_millibars / standard_pressure_millibars
    mw = get_optical_mass_water(altitude_deg)

    effective_wavelength = get_effective_aerosol_wavelength(
        band, ma, turbidity_alpha, turbidity_beta)
    tau_a = get_aerosol_optical_depth(
        turbidity_beta, effective_wavelength, turbidity_alpha)

    TR = get_rayleigh_transmittance(band, mRprime)
    Tg = get_gas_transmittance(band, mRprime)
    To = get_ozone_transmittance(band, mo, ozone_atm_cm)
    # is water_optical_mass really used for nitrogen calc?
    Tn = get_nitrogen_transmittance(band, mw, nitrogen_atm_cm)
    Tw = get_water_vapor_transmittance(band, mw, precipitable_water_cm)
    Ta = get_aerosol_transmittance(band, ma, tau_a)
    return E0n[band] * TR * Tg * To * Tn * Tw * Ta


def get_effective_aerosol_wavelength(band, ma, turbidity_alpha, turbidity_beta):
    # This function has an error somewhere. It returns negative values sometimes, but wavelength should always be positive.
    ua = math.log(1 + ma * turbidity_beta)
    if band == "high-frequency":
        a1 = turbidity_alpha  # just renaming to keep equations short
        d0 = 0.57664 - 0.024743 * a1
        d1 = (0.093942 - 0.2269 * a1 + 0.12848 * a1 ** 2) / (1 + 0.6418 * a1)
        d2 = (-0.093819 + 0.36668 * a1 - 0.12775 * a1 ** 2) / \
            (1 - 0.11651 * a1)
        d3 = a1 * (0.15232 - 0.087214 * a1 + 0.012664 * a1 ** 2) / \
            (1 - 0.90454 * a1 + 0.26167 * a1 ** 2)
        return (d0 + d1 * ua + d2 * ua ** 2) / (1 + d3 * ua ** 2)
    else:
        a2 = turbidity_alpha
        e0 = (1.183 - 0.022989 * a2 + 0.020829 * a2 ** 2) / (1 + 0.11133 * a2)
        e1 = (-0.50003 - 0.18329 * a2 + 0.23835 * a2 ** 2) / (1 + 1.6756 * a2)
        e2 = (-0.50001 + 1.1414 * a2 + 0.0083589 * a2 ** 2) / (1 + 11.168 * a2)
        e3 = (-0.70003 - 0.73587 * a2 + 0.51509 * a2 ** 2) / (1 + 4.7665 * a2)
        return (e0 + e1 * ua + e2 * ua ** 2) / (1 + e3 * ua)


def get_gas_transmittance(band, mRprime):
    if band == "high-frequency":
        return (1 + 0.95885 * mRprime + 0.012871 * mRprime ** 2) / (1 + 0.96321 * mRprime + 0.015455 * mRprime ** 2)
    else:
        return (1 + 0.27284 * mRprime - 0.00063699 * mRprime ** 2) / (1 + 0.30306 * mRprime)

def get_global_broadband_irradiance(altitude_deg, pressure_millibars=standard_pressure_millibars, ozone_atm_cm=0.35, nitrogen_atm_cm=0.0002, precipitable_water_cm=5.0, turbidity_alpha=1.3, turbidity_beta=0.6):
    Eb_high = get_beam_irradiance_by_band("high-frequency", altitude_deg, pressure_millibars, ozone_atm_cm, nitrogen_atm_cm, precipitable_water_cm, turbidity_alpha, turbidity_beta)
    Eb_low  = get_beam_irradiance_by_band("low-frequency",  altitude_deg, pressure_millibars, ozone_atm_cm, nitrogen_atm_cm, precipitable_water_cm, turbidity_alpha, turbidity_beta)

    Edp_high = get_diffuse_irradiance_by_band("high-frequency", air_mass, turbidity_alpha, turbidity_beta)
    Edp_low  = get_diffuse_irradiance_by_band("low-frequency",  air_mass, turbidity_alpha, turbidity_beta)

    Edd_high = get_backscattered_diffuse_irradiance_by_band("high-frequency", Eb_high, Edp_high, turbidity_alpha, turbidity_beta)
    Edd_low  = get_backscattered_diffuse_irradiance_by_band("low-frequency", Eb_low, Edp_low, turbidity_alpha, turbidity_beta)

    return Eb_high + Eb_low + Edp_high + Edp_low + Edd_high + Edd_low

def get_ground_albedo(band):
    # This could probably be improved with [Gueymard, 1993: Mathematically integrable parameterization of clear-sky beam and global irradiances and its use in daily irradiation applications]
    # http://www.sciencedirect.com/science/article/pii/0038092X9390059W]
    return 0.150  # mean ground albedo from [Gueymard, 2008], Table 1


def get_nitrogen_transmittance(band, mw, nitrogen_atm_cm):
    if band == "high-frequency":
        g1 = (0.17499 + 41.654 * un - 2146.4 * un ** 2) / \
            (1 + 22295.0 * un ** 2)
        g2 = un * (-1.2134 + 59.324 * un) / (1 + 8847.8 * un ** 2)
        g3 = (0.17499 + 61.658 * un + 9196.4 * un ** 2) / \
            (1 + 74109.0 * un ** 2)
        return min(1, (1 + g1 * mw + g2 * mw ** 2) / (1 + g3 * mw))
    else:
        return 1.0


# from Appendix B of [Gueymard, 2003]
def get_optical_mass_rayleigh(altitude_deg, pressure_millibars):
    Z = 90 - altitude_deg
    Z_rad = math.radians(Z)
    return (pressure_millibars / standard_pressure_millibars) / ((math.cos(Z_rad) + 0.48353 * Z_rad ** 0.095846) / (96.741 - Z_rad) ** 1.754)


def get_optical_mass_ozone(altitude_deg):  # from Appendix B of [Gueymard, 2003]
    Z = 90 - altitude_deg
    Z_rad = math.radians(Z)
    return 1 / ((math.cos(Z_rad) + 1.0651 * Z_rad ** 0.6379) / (101.8 - Z_rad) ** 2.2694)


def get_optical_mass_water(altitude_deg):  # from Appendix B of [Gueymard, 2003]
    Z = 90 - altitude_deg
    Z_rad = math.radians(Z)
    return 1 / ((math.cos(Z_rad) + 0.10648 * Z_rad ** 0.11423) / (93.781 - Z_rad) ** 1.9203)


def get_optical_mass_aerosol(altitude_deg):  # from Appendix B of [Gueymard, 2003]
    Z = 90 - altitude_deg
    Z_rad = math.radians(Z)
    return 1 / ((math.cos(Z_rad) + 0.16851 * Z_rad ** 0.18198) / (95.318 - Z_rad) ** 1.9542)


def get_ozone_transmittance(band, mo, uo):
    if band == "high-frequency":
        f1 = uo * (10.979 - 8.5421 * uo) / (1 + 2.0115 * uo + 40.189 * uo ** 2)
        f2 = uo * (-0.027589 - 0.005138 * uo) / \
            (1 - 2.4857 * uo + 13.942 * uo ** 2)
        f3 = uo * (10.995 - 5.5001 * uo) / (1 + 1.6784 * uo + 42.406 * uo ** 2)
        return (1 + f1 * mo + f2 * mo ** 2) / (1 + f3 * mo)
    else:
        return 1.0


def get_rayleigh_extinction_forward_scattering_fraction(band, mR):
    # returns BR
    if band == "high-frequency":
        return 0.5 * (0.89013 - 0.049558 * mR + 0.000045721 * mR ** 2)
    else:
        return 0.5


def get_rayleigh_transmittance(band, mRprime):
    if band == "high-frequency":
        return (1 + 1.8169 * mRprime + 0.033454 * mRprime ** 2) / (1 + 2.063 * mRprime + 0.31978 * mRprime ** 2)
    else:
        return (1 - 0.010394 * mRprime) / (1 - 0.00011042 * mRprime ** 2)


def get_sky_albedo(band, turbidity_alpha, turbidity_beta):
    if band == "high-frequency":
        a1 = turbidity_alpha  # just renaming to keep equations short
        b1 = turbidity_beta
        rhos = (0.13363 + 0.00077358 * a1 + b1 * (0.37567
                                                  + 0.22946 * a1) / (1 - 0.10832 * a1)) / (1 + b1 * (0.84057
                                                                                                     + 0.68683 * a1) / (1 - 0.08158 * a1))
    else:
        a2 = turbidity_alpha  # just renaming to keep equations short
        b2 = turbidity_beta
        rhos = (0.010191 + 0.00085547 * a2 + b2 * (0.14618
                                                   + 0.062758 * a2) / (1 - 0.19402 * a2)) / (1 + b2 * (0.58101
                                                                                                       + 0.17426 * a2) / (1 - 0.17586 * a2))
    return rhos


def get_water_vapor_transmittance(band, mw, w):
    if band == "high-frequency":
        h = get_water_vapor_transmittance_coefficients(band, w)
        return (1 + h[1] * mw) / (1 + h[2] * mw)
    else:
        c = get_water_vapor_transmittance_coefficients(band, w)
        return (1 + c[1] * mw + c[2] * mw ** 2) / (1 + c[3] * mw + c[4] * mw ** 2)


def get_water_vapor_transmittance_coefficients(band, w):
    if band == "high-frequency":
        h1 = w * (0.065445 + 0.00029901 * w) / (1 + 1.2728 * w)
        h2 = w * (0.065687 + 0.0013218 * w) / (1 + 1.2008 * w)
        return [float('NaN'), h1, h2]
    else:
        c1 = w * (19.566 - 1.6506 * w + 1.0672 * w ** 2) / \
            (1 + 5.4248 * w + 1.6005 * w ** 2)
        c2 = w * (0.50158 - 0.14732 * w + 0.047584 * w ** 2) / \
            (1 + 1.1811 * w + 1.0699 * w ** 2)
        c3 = w * (21.286 - 0.39232 * w + 1.2692 * w ** 2) / \
            (1 + 4.8318 * w + 1.412 * w ** 2)
        c4 = w * (0.70992 - 0.23155 * w + 0.096514 * w ** 2) / \
            (1 + 0.44907 * w + 0.75425 * w ** 2)
        return [float('NaN'), c1, c2, c3, c4]
