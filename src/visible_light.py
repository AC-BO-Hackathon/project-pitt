import numpy as np

from layerlumos.layerlumos import stackrt0
from layerlumos.utils_spectra import convert_frequencies_to_wavelengths
from layerlumos.utils_materials import load_material, interpolate_material

import constants


def calculate_transparency(materials, thicknesses):
    TiO2_data = load_material('TiO2')
    Ag_data = load_material('Ag')

    wavelengths = np.linspace(300 * constants.NANO, 900 * constants.NANO, 100)
    frequencies = convert_frequencies_to_wavelengths(wavelengths)

    n_k_TiO2 = interpolate_material(TiO2_data, frequencies)
    n_TiO2 = n_k_TiO2[:, 0] + 1j * n_k_TiO2[:, 1]
    n_k_Ag = interpolate_material(Ag_data, frequencies)
    n_Ag = n_k_Ag[:, 0] + 1j * n_k_Ag[:, 1]

    n_air = np.ones_like(frequencies)
    d_air = constants.THICKNESS_AIR
    d_TiO2 = 20 * constants.NANO
    d_Ag = 10 * constants.NANO

    n_stack = np.vstack([n_air, n_TiO2, n_Ag, n_TiO2, n_air]).T
    d_stack = np.array([d_air, d_TiO2, d_Ag, d_TiO2, d_air])

    R_TE, T_TE, R_TM, T_TM = stackrt0(n_stack, d_stack, frequencies)

    T_avg = (T_TE + T_TM) / 2
    transparency = np.mean(T_avg)

    return transparency


if __name__ == '__main__':
    materials = None
    thicknesses = None

    transparency = calculate_transparency(materials, thicknesses)
    print(transparency)
