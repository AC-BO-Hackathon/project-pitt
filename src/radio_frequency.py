import numpy as np

from layerlumos.utils_materials import load_material_RF
from layerlumos.layerlumos import stackrt0

import constants


def calculate_shielding_effectiveness(materials, thicknesses):
    frequencies = np.linspace(8e9, 18e9, 100)

    n_k_Ag = load_material_RF('Ag', frequencies)
    n_Ag = n_k_Ag[:, 1] + 1j * n_k_Ag[:, 2]

    n_air = np.ones_like(frequencies)

    d_air = constants.THICKNESS_AIR
    d_Ag = 20 * constants.NANO

    n_stack = np.vstack([n_air, n_Ag, n_air]).T
    d_stack = np.vstack([d_air, d_Ag, d_air])

    R_TE, T_TE, R_TM, T_TM = stackrt0(n_stack, d_stack, frequencies)

    SE_TE = -10 * np.log10(T_TE)
    SE_TM = -10 * np.log10(T_TM)
    SE = (SE_TE + SE_TM) / 2

    shielding_effectiveness = np.mean(SE)
    return shielding_effectiveness


if __name__ == '__main__':
    materials = None
    thicknesses = None

    shielding_effectiveness = calculate_shielding_effectiveness(materials, thicknesses)
    print(shielding_effectiveness)
