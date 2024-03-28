import numpy as np

from layerlumos.utils_materials import load_material_RF
from layerlumos.layerlumos import stackrt0

import constants


def calculate_shielding_effectiveness(materials, thicknesses):
    num_layers = thicknesses.shape[0]
    num_wavelengths = 100

    frequencies = np.linspace(8e9, 18e9, num_wavelengths)
    n_k = np.ones((num_wavelengths, num_layers + 2), dtype=np.complex128)

    for ind_material, material in enumerate(materials):
        n_k_material = load_material_RF(material, frequencies)
        n_k[:, ind_material + 1] = n_k_material[:, 1] + 1j * n_k_material[:, 2]

    thicknesses = np.concatenate([
        [constants.THICKNESS_AIR],
        thicknesses * constants.NANO, 
        [constants.THICKNESS_AIR],
    ], axis=0)

    R_TE, T_TE, R_TM, T_TM = stackrt0(n_k, thicknesses, frequencies)

    SE_TE = -10 * np.log10(T_TE)
    SE_TM = -10 * np.log10(T_TM)
    SE = (SE_TE + SE_TM) / 2

    shielding_effectiveness = np.mean(SE)
    return shielding_effectiveness


if __name__ == '__main__':
    materials = np.array(['Ag'])
    thicknesses = np.array([20])

    shielding_effectiveness = calculate_shielding_effectiveness(materials, thicknesses)
    print(shielding_effectiveness)

    thicknesses = np.array([20, 10, 20, 10, 20, 10, 20 ,10, 20, 10, 20, 10])
    materials = np.array(['Ag', 'Al2O3', 'Al', 'Cr', 'Ni', 'Pd', 'Si3N4', 'SiO2', 'TiN', 'TiO2', 'Ti', 'W'])

    shielding_effectiveness = calculate_shielding_effectiveness(materials, thicknesses)
    print(shielding_effectiveness)
