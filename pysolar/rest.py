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
"""
module docstring please
"""

import math
from .constants import STANDARD_PRESSURE

# single-scattering ALBEDO used to calculate aerosol scattering transmittance;
# not used for sky or ground ALBEDO for backscattering estimate
ALBEDO = {}

ALBEDO["high-frequency"] = 0.92
ALBEDO["low-frequency"] = 0.84
STANDARD_PRESSURE_MILLIBARS = STANDARD_PRESSURE / 100
UNUM = 0.0003  # atm*cm, from [Gueymard 2008], p. 280

E0N = {"high-frequency": 635.4,  # extra-atmospheric irradiance, 290-700 nm (UV and visible)
       "low-frequency":  709.7}  # extra-atmospheric irradiance, 700-4000 nm (short infrared)


def afsf(altitude_deg):
    """
    get aerosol forward scatterance factor
    """
    zed = 90 - altitude_deg
    return 1 - math.e ** (-0.6931 - 1.8326 * math.cos(math.radians(zed)))


def aerosol_optical_depth(turbidity_beta, effective_wavelength, turbidity_alpha):
    """
    docstring please
    """
    # returns tau_a
    return turbidity_beta * effective_wavelength ** -turbidity_alpha

def ascf(band, oma, tau_a):
    """
    get aerosol scattering correction factor
    """
    # returns F
    if band == "high-frequency":
        og0 = (3.715 + 0.368 * oma + 0.036294 * oma ** 2) / \
            (1 + 0.0009391 * oma ** 2)
        og1 = (-0.164 - 0.72567 * oma + 0.20701 * oma ** 2) / \
            (1 + 0.001901 * oma ** 2)
        og2 = (-0.052288 + 0.31902 * oma + 0.17871 * oma ** 2) / \
            (1 + 0.0069592 * oma ** 2)
        return (og0 + og1 * tau_a) / (1 + og2 * tau_a)
    else:
        oh0 = (3.4352 + 0.65267 * oma + 0.00034328 * oma ** 2) / \
            (1 + 0.034388 * oma ** 1.5)
        oh1 = (1.231 - 1.63853 * oma + 0.20667 * oma ** 2) / \
            (1 + 0.1451 * oma ** 1.5)
        oh2 = (0.8889 - 0.55063 * oma + 0.50152 * oma ** 2) / \
            (1 + 0.14865 * oma ** 1.5)
        return (oh0 + oh1 * tau_a) / (1 + oh2 * tau_a)


def aerosol_transmittance(oma, tau_a):
    """
    docstring please
    """
    # returns Ta
    return math.exp(-oma * tau_a)


def astx(band, oma, tau_a):
    """
    get aerosol scattering transmittance
    """
    # returns Tas
    return math.exp(-oma * ALBEDO[band] * tau_a)

# unused arguments because of missing method
def bdbi(turbidity_alpha=1.3, turbidity_beta=0.6):
    """
    get backscattered diffuse broadband irradiance
    """
    # can't find this method so returning None
    # return backscattered_diffuse_broadband_irradiance_by_band(
    #     "high-frequency", turbidity_alpha, turbidity_beta) + \
    #     backscattered_diffuse_broadband_irradiance_by_band(
    #         "low-frequency", turbidity_alpha, turbidity_beta)
    return None

def bdibb(
        band, ebi, edpi, turbidity_alpha=1.3, turbidity_beta=0.6):
    """
    get backscattered diffuse irradiance by band
    """
    rhos = sky_albedo(band, turbidity_alpha, turbidity_beta)
    rhog = ground_albedo(band)
    eddi = rhog * rhos * (ebi + edpi) / (1 - rhog * rhos)
    return eddi

# too many arguments
def beam_broadband_irradiance(
        altitude_deg, pressure_millibars=STANDARD_PRESSURE_MILLIBARS,
        ozone_atm_cm=0.35, nitrogen_atm_cm=0.0002, precipitable_water_cm=5.0,
        turbidity_alpha=1.3, turbidity_beta=0.6):
    """
    docstring please
    """
    zed = 90 - altitude_deg
    ebn = bdni(
        altitude_deg, pressure_millibars,
        ozone_atm_cm, nitrogen_atm_cm, precipitable_water_cm,
        turbidity_alpha, turbidity_beta)
    return ebn * math.cos(math.radians(zed))

# too many arguments
def beam_irradiance_by_band(
        band, altitude_deg, pressure_millibars=STANDARD_PRESSURE_MILLIBARS,
        ozone_atm_cm=0.35, nitrogen_atm_cm=0.0002, precipitable_water_cm=5.0,
        turbidity_alpha=1.3, turbidity_beta=0.6):
        # too many parameters above. Perhaps break this down into more
        # component parts like gas, temperatuer, and turbidity
    """
    docstring please
    """
    zed = 90 - altitude_deg
    ebni = dnibb(
        band, altitude_deg, pressure_millibars,
        ozone_atm_cm, nitrogen_atm_cm, precipitable_water_cm,
        turbidity_alpha, turbidity_beta)
    return ebni * math.cos(math.radians(zed))

def diffuse_broadband_irradiance(air_mass=1.66, turbidity_alpha=1.3, turbidity_beta=0.6):
    """
    docstring please
    """
    return diffuse_irradiance_by_band(
        "high-frequency", air_mass, turbidity_alpha, turbidity_beta) + \
        diffuse_irradiance_by_band("low-frequency", air_mass, turbidity_alpha, turbidity_beta)

# too many local variables
def diffuse_irradiance_by_band(band, altitude_deg, air_mass=1.66,
                               turbidity_alpha=1.3, turbidity_beta=0.6):
    """
    docstring please
    """
     # no altitude degrees passed in parameters.
     # effects all method calls
     # unused variable zed
    zed = 90 - altitude_deg

    oma = optical_mass_aerosol(altitude_deg)
    effective_wavelength = effective_aerosol_wavelength(
        band, oma, turbidity_alpha, turbidity_beta)

    tau_a = aerosol_optical_depth(
        turbidity_beta, effective_wavelength, turbidity_alpha)

    omo = optical_mass_ozone(altitude_deg)
    # no pressure millibars.
    # so sending None
    omr = optical_mass_rayleigh(altitude_deg, None)
    # missing params ozone_atm_cm
    otx = ozone_transmittance(band, omo, None)
    gtx = gas_transmittance(band, omr)
    # missing params for nitrogen_atm_cm
    ntx = nitrogen_transmittance(band, 1.66, None)
    wvtx = water_vapor_transmittance(band, 1.66)
    rtx = rayleigh_transmittance(band, omr)
    atx = aerosol_transmittance(oma, tau_a)
    ast = astx(band, oma, tau_a)

    re1 = refsf(band, air_mass)
    af1 = afsf(altitude_deg)
    as1 = ascf(band, oma, tau_a)

    edpi = otx * gtx * ntx * wvtx * \
        (re1 * (1 - rtx) * atx ** 0.25 + af1 * as1 * rtx * (1 - ast ** 0.25)) * \
        E0N[band]
    return edpi

# too many arguments
def bdni(
        altitude_deg, pressure_millibars=STANDARD_PRESSURE_MILLIBARS,
        ozone_atm_cm=0.35, nitrogen_atm_cm=0.0002, precipitable_water_cm=5.0,
        turbidity_alpha=1.3, turbidity_beta=0.6):
    """
    get broadband direct normal irradiance
    """
    high = dnibb(
        "high-frequency", altitude_deg, pressure_millibars,
        ozone_atm_cm, nitrogen_atm_cm, precipitable_water_cm,
        turbidity_alpha, turbidity_beta)
    low = dnibb(
        "low-frequency", altitude_deg, pressure_millibars,
        ozone_atm_cm, nitrogen_atm_cm, precipitable_water_cm,
        turbidity_alpha, turbidity_beta)
    return high + low


# unused argument precipitable_water_cm besides too many
# arguments and local variables pep8 is your friend
def dnibb(
        band, altitude_deg, pressure_millibars=STANDARD_PRESSURE_MILLIBARS,
        ozone_atm_cm=0.35, nitrogen_atm_cm=0.0002, precipitable_water_cm=5.0,
        turbidity_alpha=1.3, turbidity_beta=0.6):
    """
    get direct normal irradiance by band
    """
    oma = optical_mass_aerosol(altitude_deg)
    omo = optical_mass_ozone(altitude_deg)
    omr = optical_mass_rayleigh(altitude_deg, pressure_millibars)
    omr_prime = omr * pressure_millibars / STANDARD_PRESSURE_MILLIBARS
    omw = optical_mass_water(altitude_deg)

    effective_wavelength = effective_aerosol_wavelength(
        band, oma, turbidity_alpha, turbidity_beta)
    tau_a = aerosol_optical_depth(
        turbidity_beta, effective_wavelength, turbidity_alpha)

    rtx = rayleigh_transmittance(band, omr_prime)
    gtx = gas_transmittance(band, omr_prime)
    otx = ozone_transmittance(band, omo, ozone_atm_cm)
    # is water_optical_mass really used for nitrogen calc?
    ntx = nitrogen_transmittance(band, omw, nitrogen_atm_cm)
    wvtx = water_vapor_transmittance(band, omw)
    atx = aerosol_transmittance(oma, tau_a)
    return E0N[band] * rtx * gtx * otx * ntx * wvtx * atx


def effective_aerosol_wavelength(band, oma, turbidity_alpha, turbidity_beta):
    """
    docstring please
    """
    # This function has an error somewhere.
    # It returns negative values sometimes, but wavelength should always be positive.
    ua1 = math.log(1 + oma * turbidity_beta)
    if band == "high-frequency":
        ta1 = turbidity_alpha  # just renaming to keep equations short
        ad0 = 0.57664 - 0.024743 * ta1
        ad1 = (0.093942 - 0.2269 * ta1 + 0.12848 * ta1 ** 2) / (1 + 0.6418 * ta1)
        ad2 = (-0.093819 + 0.36668 * ta1 - 0.12775 * ta1 ** 2) / \
            (1 - 0.11651 * ta1)
        ad3 = ta1 * (0.15232 - 0.087214 * ta1 + 0.012664 * ta1 ** 2) / \
            (1 - 0.90454 * ta1 + 0.26167 * ta1 ** 2)
        return (ad0 + ad1 * ua1 + ad2 * ua1 ** 2) / (1 + ad3 * ua1 ** 2)
    else:
        ta2 = turbidity_alpha
        ae0 = (1.183 - 0.022989 * ta2 + 0.020829 * ta2 ** 2) / (1 + 0.11133 * ta2)
        ae1 = (-0.50003 - 0.18329 * ta2 + 0.23835 * ta2 ** 2) / (1 + 1.6756 * ta2)
        ae2 = (-0.50001 + 1.1414 * ta2 + 0.0083589 * ta2 ** 2) / (1 + 11.168 * ta2)
        ae3 = (-0.70003 - 0.73587 * ta2 + 0.51509 * ta2 ** 2) / (1 + 4.7665 * ta2)
        return (ae0 + ae1 * ua1 + ae2 * ua1 ** 2) / (1 + ae3 * ua1)


def gas_transmittance(band, omr_prime):
    """
    docstring please
    """
    if band == "high-frequency":
        return (
            1 + 0.95885 *omr_prime + 0.012871 * omr_prime ** 2) / (
                1 + 0.96321 * omr_prime + 0.015455 * omr_prime ** 2)
    else:
        return (1 + 0.27284 * omr_prime - 0.00063699 * omr_prime ** 2) / (1 + 0.30306 * omr_prime)

# too many arguments
def global_broadband_irradiance(
        altitude_deg, pressure_millibars=STANDARD_PRESSURE_MILLIBARS,
        ozone_atm_cm=0.35, nitrogen_atm_cm=0.0002, precipitable_water_cm=5.0,
        turbidity_alpha=1.3, turbidity_beta=0.6):
    """
    docstring please
    """
    eb_high = beam_irradiance_by_band(
        "high-frequency", altitude_deg, pressure_millibars,
        ozone_atm_cm, nitrogen_atm_cm, precipitable_water_cm,
        turbidity_alpha, turbidity_beta)
    eb_low = beam_irradiance_by_band(
        "low-frequency", altitude_deg, pressure_millibars,
        ozone_atm_cm, nitrogen_atm_cm, precipitable_water_cm,
        turbidity_alpha, turbidity_beta)
    # air_mass parameter missing so sending None
    edp_high = diffuse_irradiance_by_band(
        "high-frequency", None,
        turbidity_alpha, turbidity_beta)
    edp_low = diffuse_irradiance_by_band(
        "low-frequency", None,
        turbidity_alpha, turbidity_beta)

    edd_high = bdibb(
        "high-frequency", eb_high, edp_high,
        turbidity_alpha, turbidity_beta)
    edd_low = bdibb(
        "low-frequency", eb_low, edp_low,
        turbidity_alpha, turbidity_beta)

    return eb_high + eb_low + edp_high + edp_low + edd_high + edd_low

# unused parameter band
def ground_albedo(band):
    """
    docstring please
    """
    # This could probably be improved with
    # [Gueymard, 1993: Mathematically integrable parameterization of
    # clear-sky beam and global irradiances and its use in daily irradiation applications]
    # http://www.sciencedirect.com/science/article/pii/0038092X9390059W]
    return 0.150  # mean ground ALBEDO from [Gueymard, 2008], Table 1


def nitrogen_transmittance(band, omw, nitrogen_atm_cm):
    """
    docstring please
    """
    nav = nitrogen_atm_cm
    if band == "high-frequency":
        og1 = (0.17499 + 41.654 * nav - 2146.4 * nav ** 2) / \
            (1 + 22295.0 * nav ** 2)
        og2 = nav * (-1.2134 + 59.324 * nav) / (1 + 8847.8 * nav ** 2)
        og3 = (0.17499 + 61.658 * nav + 9196.4 * nav ** 2) / \
            (1 + 74109.0 * nav ** 2)
        return min(1, (1 + og1 * omw + og2 * omw ** 2) / (1 + og3 * omw))
    else:
        return 1.0


# from Appendix B of [Gueymard, 2003]
def optical_mass_rayleigh(altitude_deg, pressure_millibars):
    """
    docstring please
    """
    zed = 90 - altitude_deg
    z_rad = math.radians(zed)
    return (
        pressure_millibars / STANDARD_PRESSURE_MILLIBARS) / (
            (math.cos(z_rad) + 0.48353 * z_rad ** 0.095846) / (96.741 - z_rad) ** 1.754)


def optical_mass_ozone(altitude_deg):  # from Appendix B of [Gueymard, 2003]
    """
    docstring please
    """
    zed = 90 - altitude_deg
    z_rad = math.radians(zed)
    return 1 / ((math.cos(z_rad) + 1.0651 * z_rad ** 0.6379) / (101.8 - z_rad) ** 2.2694)


def optical_mass_water(altitude_deg):  # from Appendix B of [Gueymard, 2003]
    """
    docstring please
    """
    zed = 90 - altitude_deg
    z_rad = math.radians(zed)
    return 1 / ((math.cos(z_rad) + 0.10648 * z_rad ** 0.11423) / (93.781 - z_rad) ** 1.9203)


def optical_mass_aerosol(altitude_deg):  # from Appendix B of [Gueymard, 2003]
    """
    docstring please
    """
    zed = 90 - altitude_deg
    z_rad = math.radians(zed)
    return 1 / ((math.cos(z_rad) + 0.16851 * z_rad ** 0.18198) / (95.318 - z_rad) ** 1.9542)


def ozone_transmittance(band, omo, ozone_atm_cm):
    """
    docstring please
    """
    oav = ozone_atm_cm
    if band == "high-frequency":
        of1 = oav * (10.979 - 8.5421 * oav) / (1 + 2.0115 * oav + 40.189 * oav ** 2)
        of2 = oav * (-0.027589 - 0.005138 * oav) / (1 - 2.4857 * oav + 13.942 * oav ** 2)
        of3 = oav * (10.995 - 5.5001 * oav) / (1 + 1.6784 * oav + 42.406 * oav ** 2)
        return (1 + of1 * omo + of2 * omo ** 2) / (1 + of3 * omo)
    else:
        return 1.0


def refsf(band, omr):
    """
    get rayleigh extinction forward scattering fraction
    """
    # returns BR
    if band == "high-frequency":
        return 0.5 * (0.89013 - 0.049558 * omr + 0.000045721 * omr ** 2)
    else:
        return 0.5


def rayleigh_transmittance(band, omr_prime):
    """
    docstring please
    """
    if band == "high-frequency":
        return (
            1 + 1.8169 * omr_prime + 0.033454 * omr_prime ** 2) / (
                1 + 2.063 * omr_prime + 0.31978 * omr_prime ** 2)
    else:
        return (1 - 0.010394 * omr_prime) / (1 - 0.00011042 * omr_prime ** 2)


def sky_albedo(band, turbidity_alpha, turbidity_beta):
    """
    docstring please
    """
    if band == "high-frequency":
        ta1 = turbidity_alpha  # just renaming to keep equations short
        tb1 = turbidity_beta
        rhos = (
            0.13363 + 0.00077358 * ta1 + tb1 * (
                0.37567 + 0.22946 * ta1) / (
                    1 - 0.10832 * ta1)) / (
                        1 + tb1 * (
                            0.84057 + 0.68683 * ta1) / (
                                1 - 0.08158 * ta1))
    else:
        ta2 = turbidity_alpha  # just renaming to keep equations short
        tb2 = turbidity_beta
        rhos = (
            0.010191 + 0.00085547 * ta2 + tb2 * (
                0.14618 + 0.062758 * ta2) / (
                    1 - 0.19402 * ta2)) / (
                        1 + tb2 * (
                            0.58101 + 0.17426 * ta2) / (
                                1 - 0.17586 * ta2))
    return rhos


def water_vapor_transmittance(band, omw):
    """
    docstring please
    """
    if band == "high-frequency":
        # missing a parameter precipitable_water_cm
        wvtc = wvtxc(band, omw)
        return (1 + wvtc[1] * omw) / (1 + wvtc[2] * omw)
    else:
        # missing a parameter precipitable_water_cm
        wvtc = wvtxc(band, omw)
        return (
            1 + wvtc[1] * omw + wvtc[2] * omw ** 2) / (
                1 + wvtc[3] * omw + wvtc[4] * omw ** 2)


def wvtxc(band, owv):
    """
    get water vapor transmittance coefficients
    """
    if band == "high-frequency":
        wvtxc1 = owv * (0.065445 + 0.00029901 * owv) / (1 + 1.2728 * owv)
        wvtxc2 = owv * (0.065687 + 0.0013218 * owv) / (1 + 1.2008 * owv)
        return [float('NaN'), wvtxc1, wvtxc2]
    else:
        wvtxc1 = owv * (19.566 - 1.6506 * owv + 1.0672 * owv ** 2) / \
            (1 + 5.4248 * owv + 1.6005 * owv ** 2)
        wvtxc2 = owv * (0.50158 - 0.14732 * owv + 0.047584 * owv ** 2) / \
            (1 + 1.1811 * owv + 1.0699 * owv ** 2)
        wvtxc3 = owv * (21.286 - 0.39232 * owv + 1.2692 * owv ** 2) / \
            (1 + 4.8318 * owv + 1.412 * owv ** 2)
        wvtxc4 = owv * (0.70992 - 0.23155 * owv + 0.096514 * owv ** 2) / \
            (1 + 0.44907 * owv + 0.75425 * owv ** 2)
        return [float('NaN'), wvtxc1, wvtxc2, wvtxc3, wvtxc4]
