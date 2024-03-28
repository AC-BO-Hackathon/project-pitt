import scipy.constants as scic


NANO = scic.nano
THICKNESS_AIR = 0

WAVELENGTH_START_VISIBLE = 300 * NANO
WAVELENGTH_END_VISIBLE = 900 * NANO

MATERIALS = [
    'Ag',
    'Al2O3',
    'Al',
    'Cr',
    'Ni',
    'Pd',
    'Si3N4',
    'SiO2',
    'TiN',
    'TiO2',
    'Ti',
    'W',
]

BOUND_MATERIALS = [0, len(MATERIALS) - 0.001]
BOUND_THICKNESSES = [5, 20]
